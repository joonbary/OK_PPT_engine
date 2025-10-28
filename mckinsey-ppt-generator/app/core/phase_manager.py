"""Phase Manager: orchestrates phased operations and stores interim results.

Implements LLM-based analysis for extracting core message and key topics.
Other phases remain lightweight or delegate to agents/services.
"""

from __future__ import annotations

from typing import Dict, Any
from time import perf_counter

from app.core.state_manager import StateManager, PhaseName, PhaseStatus
from app.services.workflow_orchestrator import WorkflowOrchestrator
from app.models.workflow_models import GenerationRequest


class PhaseManager:
    def __init__(self) -> None:
        self.state = StateManager()

    async def run_analyze(self, project_id: str, document: str, language: str = "ko") -> Dict[str, Any]:
        await self.state.set_status(project_id, PhaseName.ANALYZE, PhaseStatus.RUNNING)
        t0 = perf_counter()
        try:
            # LLM-based analysis via StrategistAgent
            from app.agents.strategist_agent import StrategistAgent
            agent = StrategistAgent()
            try:
                agent.language = (language or 'ko').lower()
            except Exception:
                pass

            # Structured LLM analysis (avoid fragile free-form JSON)
            lang = (language or 'ko').lower()
            lang_inst = '紐⑤뱺 ?묐떟???쒓뎅?대줈 ?묒꽦.' if lang.startswith('ko') else 'Respond in the specified language.'
            prompt = (
                f"{lang_inst}\n"
                f"?ㅼ쓬 鍮꾩쫰?덉뒪 臾몄꽌瑜?遺꾩꽍?섏뿬 ?듭떖 ?붿냼瑜?JSON?쇰줈 異붿텧?섏꽭??\n\n"
                f"臾몄꽌:\n{document}\n\n"
                f"諛섑솚 ?뺤떇(?꾨뱶紐?怨좎젙, 遺덊븘?뷀븳 ?ㅻ챸 湲덉?):\n"
                "{\n"
                "  \"key_message\": string,\n"
                "  \"data_points\": [string],\n"
                "  \"target_audience\": string,\n"
                "  \"purpose\": string,\n"
                "  \"context\": string,\n"
                "  \"industry\": string\n"
                "}"
            )
            obj = await agent._generate_structured(
                prompt=prompt,
                response_format={
                    "key_message": "",
                    "data_points": [],
                    "target_audience": "",
                    "purpose": "",
                    "context": "",
                    "industry": "",
                },
                max_tokens=1200,
                use_cache=False,
            )
            # Normalize
            dp_list = obj.get('data_points') or []
            if isinstance(dp_list, str):
                dp_list = [x.strip() for x in dp_list.split('\n') if x.strip()]
            if not isinstance(dp_list, list):
                dp_list = []
            analysis = {
                "key_message": (obj.get('key_message') or '').strip(),
                "data_points": dp_list,
                "target_audience": (obj.get('target_audience') or '').strip(),
                "purpose": (obj.get('purpose') or '').strip(),
                "context": (obj.get('context') or '').strip(),
                "industry": (obj.get('industry') or '').strip(),
            }
            # Re-prompt essential fields if empty
            if not analysis["key_message"]:
                try:
                    lang_inst_safe = 'Respond in Korean.' if (language or 'ko').lower().startswith('ko') else 'Respond in the specified language.'
                    prompt_summary = (
                        f"{lang_inst_safe}\nProvide a one-sentence core message for the document. Plain text only.\n\nDocument:\n{document}"
                    )
                    summary = await agent.llm_client.generate(prompt_summary, max_tokens=120, temperature=0.3)
                    analysis["key_message"] = (summary or '').strip()
                except Exception:
                    pass
            if not analysis["data_points"]:
                try:
                    lang_inst_safe = 'Respond in Korean.' if (language or 'ko').lower().startswith('ko') else 'Respond in the specified language.'
                    prompt_points = (
                        f"{lang_inst_safe}\nList 3-5 key data points as a JSON array of strings.\n\nDocument:\n{document}\n\nFormat:\n[\"point1\",\"point2\"]"
                    )
                    pts_raw = await agent.llm_client.generate(prompt_points, max_tokens=200, temperature=0.3)
                    if "[" in pts_raw and "]" in pts_raw:
                        s = pts_raw.find("["); e = pts_raw.rfind("]");
                        import json as _json
                        pts = _json.loads(pts_raw[s:e+1])
                        if isinstance(pts, list):
                            analysis["data_points"] = [str(x).strip() for x in pts if str(x).strip()][:5]
                except Exception:
                    pass

            # LLM topic extraction (no non-LLM fallback)
            try:
                lang_inst = '紐⑤뱺 ?묐떟???쒓뎅?대줈 ?묒꽦.' if (language or 'ko').lower().startswith('ko') else 'Respond in the specified language.'
                prompt = (
                    f"{lang_inst}\n"
                    f"?ㅼ쓬 臾몄꽌?먯꽌 媛??以묒슂???좏뵿 5~8媛쒕? ?쒓?/?곷Ц ?쇳빀 洹몃?濡?異붿텧??JSON 諛곗뿴留?諛섑솚?섏꽭??\n"
                    f"?붽뎄?ы빆:\n- 以묐났/?숈쓽?대뒗 ?섎굹濡??⑹튂湲?n- ?섎? ?⑥쐞(?? '?붿????꾪솚')??寃고빀?대줈 ?좎?\n- ?쇰컲 ?묒냽??議곗궗???쒖쇅\n\n臾몄꽌:\n{document}\n\n?뺤떇:\n[\"?좏뵿1\", \"?좏뵿2\", ...]"
                )
                lang_clean = (language or 'ko').lower()
                lang_inst2 = '紐⑤뱺 ?묐떟???쒓뎅?대줈 ?묒꽦.' if lang_clean.startswith('ko') else 'Respond in the specified language.'
                prompt2 = (
                    f"{lang_inst2}\n"
                    f"?ㅼ쓬 臾몄꽌?먯꽌 媛??以묒슂???좏뵿 5~8媛쒕? ?쒓?/?곷Ц ?쇳빀 洹몃?濡?異붿텧??JSON 諛곗뿴留?諛섑솚?섏꽭??\n"
                    f"?붽뎄?ы빆:\n- 以묐났/?숈쓽?대뒗 ?섎굹濡??⑹튂湲?n- ?섎? ?⑥쐞(?? '?붿????꾪솚')??寃고빀?대줈 ?좎?\n- ?쇰컲 ?묒냽??議곗궗???쒖쇅\n\n臾몄꽌:\n{document}\n\n?뺤떇:\n[\"?좏뵿1\", \"?좏뵿2\", ...]"
                )
                topics_raw = await agent.llm_client.generate(prompt2)
                if "[" in topics_raw and "]" in topics_raw:
                    s = topics_raw.find("[")
                    e = topics_raw.rfind("]")
                    topics_json = topics_raw[s:e+1]
                else:
                    topics_json = "[]"
                import json as _json
                key_topics = _json.loads(topics_json)
                key_topics = [str(t).strip() for t in key_topics if str(t).strip()]
                key_topics = key_topics[:10]
            except Exception:
                key_topics = []

            core_message = analysis.get('key_message') or analysis.get('core_message') or ''
            data_points = analysis.get('data_points') or []
            if data_points and all(isinstance(dp, str) for dp in data_points):
                data_points = [{"type": "Insight", "value": dp, "context": ""} for dp in data_points[:20]]

            res = {
                "core_message": core_message,
                "key_message": core_message,
                "data_points": data_points,
                "key_topics": key_topics,
                "target_audience": analysis.get('target_audience') or "C-Level",
                "tone": analysis.get('tone') or "LLM 湲곕컲 遺꾩꽍",
                "processed_content": (document or '')[:2000],
            }
            await self.state.set_status(
                project_id,
                PhaseName.ANALYZE,
                PhaseStatus.COMPLETED,
                result=res,
                meta={"elapsed": perf_counter() - t0, "language": language},
            )
            return res
        except Exception as e:
            await self.state.set_status(project_id, PhaseName.ANALYZE, PhaseStatus.FAILED, result={"error": str(e)})
            raise

    async def run_structure(self, project_id: str, document: str, num_slides: int = 10, language: str = "ko") -> Dict[str, Any]:
        await self.state.set_status(project_id, PhaseName.STRUCTURE, PhaseStatus.RUNNING)
        t0 = perf_counter()
        try:
            from app.agents.strategist_agent import StrategistAgent
            agent = StrategistAgent()
            res = await agent.process(input_data={"document": document, "num_slides": num_slides}, context={"language": language})
            out = {
                "mece_segments": res.get("mece_segments"),
                "slide_outline": res.get("slide_outline") or res.get("outline"),
            }
            await self.state.set_status(
                project_id, PhaseName.STRUCTURE, PhaseStatus.COMPLETED, result=out, meta={"elapsed": perf_counter() - t0}
            )
            return out
        except Exception as e:
            await self.state.set_status(project_id, PhaseName.STRUCTURE, PhaseStatus.FAILED, result={"error": str(e)})
            raise

    async def run_content(self, project_id: str, document: str, num_slides: int = 10, language: str = "ko") -> Dict[str, Any]:
        await self.state.set_status(project_id, PhaseName.CONTENT, PhaseStatus.RUNNING)
        t0 = perf_counter()
        try:
            plan = {"language": language, "num_slides": num_slides, "summary": document[:400]}
            await self.state.set_status(
                project_id, PhaseName.CONTENT, PhaseStatus.COMPLETED, result=plan, meta={"elapsed": perf_counter() - t0}
            )
            return plan
        except Exception as e:
            await self.state.set_status(project_id, PhaseName.CONTENT, PhaseStatus.FAILED, result={"error": str(e)})
            raise

    async def run_design(self, project_id: str) -> Dict[str, Any]:
        await self.state.set_status(project_id, PhaseName.DESIGN, PhaseStatus.RUNNING)
        t0 = perf_counter()
        try:
            result = {"template_rules": "applied", "style": "mckinsey"}
            await self.state.set_status(
                project_id, PhaseName.DESIGN, PhaseStatus.COMPLETED, result=result, meta={"elapsed": perf_counter() - t0}
            )
            return result
        except Exception as e:
            await self.state.set_status(project_id, PhaseName.DESIGN, PhaseStatus.FAILED, result={"error": str(e)})
            raise

    async def run_review(self, project_id: str) -> Dict[str, Any]:
        await self.state.set_status(project_id, PhaseName.REVIEW, PhaseStatus.RUNNING)
        t0 = perf_counter()
        try:
            result = {"quality": {"score": 0.0, "passed": False}}
            await self.state.set_status(
                project_id, PhaseName.REVIEW, PhaseStatus.COMPLETED, result=result, meta={"elapsed": perf_counter() - t0}
            )
            return result
        except Exception as e:
            await self.state.set_status(project_id, PhaseName.REVIEW, PhaseStatus.FAILED, result={"error": str(e)})
            raise

    async def export(self, project_id: str, document: str, num_slides: int = 10, language: str = "ko") -> Dict[str, Any]:
        try:
            orch = WorkflowOrchestrator(language=language)
        except TypeError:
            orch = WorkflowOrchestrator()
        req = GenerationRequest(document=document, num_slides=num_slides)
        result = await orch.execute(req, job_id=project_id)
        return {
            "success": getattr(result, "success", False),
            "pptx_path": getattr(result, "pptx_path", None),
            "quality_score": getattr(result, "quality_score", 0.0),
        }


