# -*- coding: utf-8 -*-
"""
?꾨왂 援ъ“ ?ㅺ퀎 ?먯씠?꾪듃
MECE ?먯튃怨??쇰씪誘몃뱶 援ъ“瑜??쒖슜?섏뿬 PPT ?꾩썐?쇱씤???앹꽦?⑸땲??
"""

from typing import Dict, List, Any
from app.agents.base_agent_v2 import BaseAgentV2
from app.db.models import AgentType
from app.agents.frameworks import MECEFrameworkLibrary
import json
import re
from loguru import logger


class StrategistAgent(BaseAgentV2):
    """
    McKinsey 而⑥꽕?댄듃 ?섏????꾨왂 ?먯씠?꾪듃
    
    二쇱슂 湲곕뒫:
    - 鍮꾩쫰?덉뒪 臾몄꽌 遺꾩꽍
    - MECE ?꾨젅?꾩썙???좏깮
    - ?쇰씪誘몃뱶 援ъ“ ?앹꽦
    - ?щ씪?대뱶 ?꾩썐?쇱씤 ?ㅺ퀎
    """
    
    def __init__(self):
        super().__init__(
            name="Strategist Agent",
            agent_type=AgentType.STRATEGIST,
            model="gpt-4-0613"
        )
        self.framework_library = MECEFrameworkLibrary()
        # Lazy-init ContentGenerator to avoid import-time failures during analyze phase
        self.content_generator = None
        self.metrics = {}

    def _ensure_content_generator(self):
        if self.content_generator is None:
            try:
                from app.services.content_generator import ContentGenerator
                logger.info("StrategistAgent: Instantiating ContentGenerator...")
                self.content_generator = ContentGenerator()
            except Exception as e:
                logger.warning(f"ContentGenerator initialization failed: {e}")
    
    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        ?꾨왂 遺꾩꽍 硫붿씤 ?뚯씠?꾨씪??        
        Args:
            input_data: {
                'document': str,  # 鍮꾩쫰?덉뒪 臾몄꽌
                'num_slides': int  # 紐⑺몴 ?щ씪?대뱶 ??(湲곕낯 15)
            }
            context: {
                'job_id': str,  # ?묒뾽 ID (吏꾪뻾瑜?異붿쟻??
            }
        
        Returns:
            {
                'analysis': Dict,      # 臾몄꽌 遺꾩꽍 寃곌낵
                'framework': Dict,     # ?좏깮??MECE ?꾨젅?꾩썙??                'pyramid': Dict,       # ?쇰씪誘몃뱶 援ъ“
                'outline': List[Dict]  # ?щ씪?대뱶 ?꾩썐?쇱씤
            }
        """
        logger.info(f"Starting strategist processing for job {context.get('job_id')}")
        
        try:
            # 而⑦뀓?ㅽ듃 ?몄뼱 ????꾨＼?꾪듃 吏??솕???ъ슜)
            try:
                self.language = (context.get('language') or 'ko').lower()
            except Exception:
                self.language = 'ko'
            # Step 1: 臾몄꽌 遺꾩꽍
            logger.info("Step 1: Analyzing document")
            analysis = await self._analyze_document(input_data['document'])
            logger.info(f"Document analysis complete: {analysis.get('key_message', 'N/A')}")
            
            # Step 2: MECE ?꾨젅?꾩썙???좏깮
            logger.info("Step 2: Selecting MECE framework")
            framework = self._select_framework(analysis)
            logger.info(f"Selected framework: {framework['framework_name']}")
            
            # Step 3: Create pyramid structure
            logger.info("Step 3: Creating pyramid structure")
            pyramid = await self._create_pyramid_structure(analysis, framework)
            logger.info(f"Pyramid structure created with {len(pyramid.get('supporting_arguments', []))} arguments")
            
            # Step 4: Create slide outline
            logger.info("Step 4: Creating slide outline")
            num_slides = input_data.get('num_slides', 15)
            outline = await self._create_slide_outline(pyramid, framework, num_slides)
            logger.info(f"Created outline with {len(outline)} slides")

            # Step 5: MECE decomposition and slide mapping
            mece_framework = self._pick_mece_framework(analysis)
            try:
                mece_segments = await self._decompose_by_mece(input_data['document'], mece_framework, analysis)
            except Exception as e:
                logger.warning(f"MECE decomposition failed: {e}; using heuristic split")
                mece_segments = self._heuristic_mece_split(input_data['document'], mece_framework)
            slide_outline = self._map_segments_to_slides(mece_segments, num_slides)
            
            self.metrics['slides_created'] = len(outline)
            self.metrics['framework_used'] = framework['framework_name']
            
            return {
                'analysis': analysis,
                'framework': framework,
                'pyramid': pyramid,
                'outline': outline,
                'mece_segments': mece_segments,
                'slide_outline': slide_outline,
            }
            
        except Exception as e:
            logger.error(f"Strategist processing failed: {e}")
            raise
    
    async def _analyze_document(self, document: str) -> Dict:
        lang = (getattr(self, 'language', 'ko') or 'ko').lower()
        lang_inst = '모든 답변은 한국어로 작성.' if lang.startswith('ko') else 'Respond in the specified language.'
        prompt = (
            f"{lang_inst}\n"
            "다음 비즈니스 문서를 분석하여 핵심 요소를 JSON으로 추출하세요.\n\n"
            f"문서:\n{document}\n\n"
            "반환 형식(JSON):\n{\n"
            "  \"key_message\": \"핵심 메시지(한 문장 요약)\",\n"
            "  \"data_points\": [\"주요 데이터 포인트 1\", \"주요 데이터 포인트 2\"],\n"
            "  \"target_audience\": \"대상 독자\",\n"
            "  \"purpose\": \"의도\",\n"
            "  \"context\": \"맥락\",\n"
            "  \"industry\": \"업종\"\n"
            "}\n\nJSON만 반환하세요."
        )
        response = await self.llm_client.generate(prompt)
        def _extract_json_block(text: str) -> str:
            if not text:
                return ""
            t = text.strip()
            if "```json" in t:
                s = t.find("```json") + 7
                e = t.find("```", s)
                if e > s:
                    return t[s:e].strip()
            first = t.find("{"); last = t.rfind("}")
            if first != -1 and last != -1 and last > first:
                return t[first:last+1].strip()
            return t
        try:
            raw = response if isinstance(response, str) else json.dumps(response, ensure_ascii=False)
            json_str = _extract_json_block(raw)
            analysis = json.loads(json_str)
            return analysis
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}. Response(head): {raw[:200] if isinstance(raw,str) else str(raw)[:200]}")
            raise RuntimeError(f"Document analysis failed - LLM response parsing error: {e}")

    def _select_framework(self, analysis: Dict) -> Dict:
        context = (analysis.get('context') or '').lower()
        purpose = (analysis.get('purpose') or '').lower()
        key = 'CUSTOM'
        if any(k in context for k in ['market', 'go-to-market', 'launch', 'entry']):
            key = '3C'
        if any(k in context for k in ['swot']):
            key = 'SWOT'
        if any(k in context for k in ['matrix', 'bcg']):
            key = 'BCG'
        framework = self.framework_library.get_framework(key)
        logger.info(f"Selected framework: {framework.get('name', key)}")
        return framework

    def _pick_mece_framework(self, analysis: Dict) -> str:
        try:
            ctx = (analysis.get('context') or '').lower()
            if 'swot' in ctx:
                return 'SWOT'
            return '3C'
        except Exception:
            return '3C'

    async def _decompose_by_mece(self, document: str, framework: str, analysis: Dict) -> List[Dict[str, Any]]:
        mece_prompts = {
            '3C': (
                "?ㅼ쓬 臾몄꽌瑜?3C ?꾨젅?꾩썙??Company, Competitors, Customers)濡?遺꾩꽍?섏뿬\n"
                "媛??곸뿭???대떦?섎뒗 ?댁슜???꾩쟾??遺꾨━?섏뿬 異붿텧?섏꽭??\n\n臾몄꽌:\n{document}\n\n"
                "JSON ?뺤떇?쇰줈 諛섑솚:\n{\n  \"Company\": \"湲곗뾽 ?먯껜??????댁슜\",\n  \"Competitors\": \"寃쎌웳 ?섍꼍\",\n  \"Customers\": \"怨좉컼/?쒖옣\"\n}\n"
                "以묒슂: 媛??곸뿭? ?곹샇 諛고??곸씠?댁빞 ??"
            ),
            'SWOT': (
                "?ㅼ쓬 臾몄꽌瑜?SWOT 遺꾩꽍?쇰줈 遺꾨쪟?섏뿬 JSON?쇰줈 諛섑솚:\n"
                "{document}\n\n{\n  \"Strengths\": \"媛뺤젏\",\n  \"Weaknesses\": \"?쎌젏\",\n  \"Opportunities\": \"湲고쉶\",\n  \"Threats\": \"?꾪삊\"\n}"
            ),
        }
        lang = (getattr(self, 'language', 'ko') or 'ko').lower()
        lang_inst = '紐⑤뱺 ?묐떟? ?쒓뎅?대줈 ?묒꽦.' if lang.startswith('ko') else 'Respond in the specified language.'
        prompt = (lang_inst + "\n" + mece_prompts.get(framework, mece_prompts['3C']).format(document=document))
        try:
            resp = await self.llm_client.generate(prompt)
            if "```json" in resp:
                s = resp.find("```json") + 7
                e = resp.find("```", s)
                resp = resp[s:e].strip()
            obj = json.loads(resp)
        except Exception as e:
            logger.warning(f"LLM MECE parsing failed: {e}")
            obj = {}
        segs = []
        for k, v in (obj.items() if isinstance(obj, dict) else []):
            segs.append({"category": k, "content": v})
        if not segs:
            segs = self._heuristic_mece_split(document, framework)
        return segs

    def _heuristic_mece_split(self, document: str, framework: str) -> List[Dict[str, Any]]:
        parts = re.split(r"\n\s*\n+", document)
        buckets = {"Company": [], "Competitors": [], "Customers": []}
        for p in parts:
            pl = p.lower()
            if any(w in pl for w in ["competitor","competition","rival","vs"]):
                buckets["Competitors"].append(p)
            elif any(w in pl for w in ["customer","market","demand","trend"]):
                buckets["Customers"].append(p)
            else:
                buckets["Company"].append(p)
        return [{"category": k, "content": "\n".join(v)} for k, v in buckets.items() if v]

    def _map_segments_to_slides(self, mece_segments: List[Dict[str, Any]], num_slides: int) -> List[Dict[str, Any]]:
        outline: List[Dict[str, Any]] = []
        outline.append({"slide_number": 1, "type": "Title", "content_focus": "?꾩껜 二쇱젣", "mece_segment": None})
        outline.append({"slide_number": 2, "type": "Executive Summary", "content_focus": "?꾩껜 ?붿빟", "mece_segment": "ALL"})
        content_slots = max(0, num_slides - 3)
        segments: List[Dict[str, Any]] = []
        if not mece_segments:
            segments = [{"category": "Analysis", "content": ""}]
        else:
            segments = mece_segments
        idx = 0
        for slot in range(content_slots):
            seg = segments[idx % len(segments)]
            outline.append({
                "slide_number": 3 + slot,
                "type": self._determine_slide_type(seg.get("category", "")),
                "content_focus": seg.get("category", "Segment"),
                "mece_segment": seg.get("content", ""),
                "instructions": f"???щ씪?대뱶??{seg.get('category','')} ?댁슜留??ㅻ（?몄슂.",
            })
            idx += 1
        outline.append({
            "slide_number": max(3, num_slides),
            "type": "Recommendations",
            "content_focus": "醫낇빀 ?쒖뼵",
            "mece_segment": "ALL",
        })
        return outline
    
    async def _create_pyramid_structure(self, analysis: Dict, framework: Dict) -> Dict:
        prompt = f"""?ㅼ쓬 鍮꾩쫰?덉뒪 遺꾩꽍??諛뷀깢?쇰줈 ?쇰씪誘몃뱶 援ъ“瑜??앹꽦?섏꽭??\n\n?듭떖 硫붿떆吏: {analysis['key_message']}\n?꾨젅?꾩썙?? {framework['framework_name']} - {framework['description']}\n移댄뀒怨좊━: {', '.join(framework['categories'])}\n二쇱슂 ?곗씠?? {', '.join(analysis.get('data_points', [])[:5])}\n\n?쇰씪誘몃뱶 援ъ“瑜??ㅼ쓬 JSON ?뺤떇?쇰줈 ?앹꽦?섏꽭??\n{{\n  "top_message": "?듭떖 硫붿떆吏 (So What??紐낇솗???≪뀡 吏?μ쟻 臾몄옣)",\n  "supporting_arguments": [\n    {{\n      "argument": "二쇱슂 二쇱옣 1 (?꾨젅?꾩썙??移댄뀒怨좊━? ?곌껐)",\n      "category": "{framework['categories'][0]}",\n      "evidence": [\n        "吏吏 洹쇨굅 1 (援ъ껜???섏튂 ?ы븿)",\n        "吏吏 洹쇨굅 2",\n        "吏吏 洹쇨굅 3"\n      ]\n    }},\n    ... (珥?{len(framework['categories'])}媛쒖쓽 二쇱옣)\n  ]\n}}\n\n?붽뎄?ы빆:\n1. 媛?移댄뀒怨좊━蹂꾨줈 1媛쒖쓽 二쇱슂 二쇱옣 ?앹꽦\n2. 媛?二쇱옣? 紐낇솗??So What ?ы븿\n3. 吏吏 洹쇨굅???뺣웾???섏튂 ?ы븿\n4. MECE ?먯튃 以??(?곹샇 諛고??곸씠硫??꾩껜瑜??ш큵)\n\nJSON留?諛섑솚?섏꽭??"""
        # Override prompt with ASCII-only safe version to avoid encoding issues
        cats = [str(c) for c in framework.get('categories', [])]
        fw_name = framework.get('framework_name') or framework.get('name') or 'CUSTOM'
        fw_desc = framework.get('description', '')
        first_cat = cats[0] if cats else 'Category'
        dp_src = analysis.get('data_points') or []
        dps = [str(x) for x in (dp_src if isinstance(dp_src, list) else [dp_src])][:5]
        prompt = (
            "Build a pyramid structure as JSON.\n\n"
            f"Top message: {analysis.get('key_message','')}\n"
            f"Framework: {fw_name} - {fw_desc}\n"
            f"Categories: {', '.join(cats)}\n"
            f"Key points: {', '.join(dps)}\n\n"
            "Return JSON only in the format:\n{\n"
            "  \"top_message\": \"So-What oriented single sentence\",\n"
            "  \"supporting_arguments\": [\n"
            "    {\n"
            "      \"argument\": \"Main claim 1\",\n"
            f"      \"category\": \"{first_cat}\",\n"
            "      \"evidence\": [\"evidence 1\", \"evidence 2\"]\n"
            "    }\n"
            "  ]\n}\n"
        )

        response = await self.llm_client.generate(prompt)
        
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            pyramid = json.loads(response)
            
            covered_categories = {arg['category'] for arg in pyramid['supporting_arguments']}
            expected_categories = set(framework['categories'])
            
            if covered_categories != expected_categories:
                logger.warning(f"Missing categories: {expected_categories - covered_categories}")
            
            return pyramid
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Failed to parse pyramid structure: {e}. Response: {response[:200] if response else 'Empty'}")
            raise RuntimeError(f"Pyramid structure generation failed: {e}")
    
    async def _create_slide_outline(self, pyramid: Dict, framework: Dict, num_slides: int) -> List[Dict]:
        prompt = f"""?ㅼ쓬 ?쇰씪誘몃뱶 援ъ“瑜?諛뷀깢?쇰줈 {num_slides}?μ쓽 ?щ씪?대뱶 ?꾩썐?쇱씤???앹꽦?섏꽭??\n\n?듭떖 硫붿떆吏: {pyramid['top_message']}\n二쇱슂 二쇱옣: {len(pyramid['supporting_arguments'])}媛? ?꾨젅?꾩썙?? {framework['framework_name']}\n\n?щ씪?대뱶 援ъ“ (SCR):\n1. Title Slide (1??\n2. Executive Summary (1??\n3-4. Situation (?곹솴) - 2??n5-6. Complication (臾몄젣) - 2??n7-{num_slides-3}. Resolution (?닿껐梨? - {num_slides-8}??(?꾨젅?꾩썙??移댄뀒怨좊━蹂?\n{num_slides-2}-{num_slides-1}. Recommendation (沅뚭퀬) - 2??n{num_slides}. Next Steps (?ㅼ쓬 ?④퀎) - 1??n\n?ㅼ쓬 JSON 諛곗뿴濡?諛섑솚?섏꽭??\n[\n  {{\n    "slide_number": 1,\n    "slide_type": "title",\n    "title": "?꾨젅?좏뀒?댁뀡 ?쒕ぉ",\n    "headline": "{pyramid['top_message']}",\n    "content_type": "text",\n    "key_points": [],\n    "data_requirements": [],\n    "layout_suggestion": "title_slide",\n    "category": "intro"\n  }},\n  {{\n    "slide_number": 2,\n    "slide_type": "executive_summary",\n    "title": "Executive Summary",\n    "headline": "?듭떖 硫붿떆吏 (?뺣웾?붾맂 So What)",\n    "content_type": "text",\n    "key_points": ["?듭떖 洹쇨굅 1", "?듭떖 洹쇨굅 2", "?듭떖 洹쇨굅 3"],\n    "data_requirements": ["二쇱슂 ?섏튂 1", "二쇱슂 ?섏튂 2"],\n    "layout_suggestion": "dual_header",\n    "category": "summary"\n  }},\n  ... ({num_slides}媛??щ씪?대뱶)\n]\n\n?붽뎄?ы빆:\n1. 媛??щ씪?대뱶??紐낇솗??So What ?ㅻ뱶?쇱씤\n2. ?꾨젅?꾩썙??移댄뀒怨좊━ 洹좊벑 遺꾨같\n3. ?곗씠???쒓컖?붽? ?꾩슂???щ씪?대뱶??content_type? 'chart'濡?n4. ?덉씠?꾩썐? 'title_slide', 'dual_header', 'three_column', 'matrix', 'waterfall' 以??좏깮\n\nJSON 諛곗뿴留?諛섑솚?섏꽭??"""
        # Override prompt with ASCII-only outline request to avoid encoding issues
        prompt = (
            f"Create a {num_slides}-slide outline as a JSON array, based on the pyramid.\n\n"
            f"Top message: {pyramid.get('top_message','')}\n"
            f"Supporting arguments: {len(pyramid.get('supporting_arguments', []))}\n\n"
            "Return JSON array only. Example element:\n[\n  {\n    \"slide_number\": 1,\n    \"slide_type\": \"title\",\n    \"title\": \"Title\",\n    \"headline\": \"...\",\n    \"content_type\": \"text\",\n    \"key_points\": [],\n    \"data_requirements\": [],\n    \"layout_suggestion\": \"title_slide\",\n    \"category\": \"intro\"\n  }\n]\n"
        )

        response = await self.llm_client.generate(prompt)
        
        def _extract_json_array(text: str) -> str:
            if not text:
                return ""
            t = text.strip()
            if "```json" in t:
                s = t.find("```json") + 7
                e = t.find("```", s)
                if e > s:
                    return t[s:e].strip()
            first = t.find("[")
            last = t.rfind("]")
            if first != -1 and last != -1 and last > first:
                return t[first:last+1].strip()
            return t

        try:
            json_str = _extract_json_array(response)
            outline = json.loads(json_str)
            # Heuristic enrichment: content_type/layout_type if missing
            enriched = []
            for s in outline:
                title = (s.get('title') or '').lower()
                ctype = s.get('content_type')
                if not ctype:
                    if any(k in title for k in ['comparison','鍮꾧탳','pros/cons']):
                        ctype = 'comparison'
                    elif any(k in title for k in ['matrix','留ㅽ듃由?뒪','2x2','3x3']):
                        ctype = 'matrix'
                    elif any(k in title for k in ['chart','李⑦듃','data','遺꾩꽍','roi']):
                        ctype = 'data_visualization'
                    elif s.get('slide_number', 1) == 1 or any(k in title for k in ['summary','?붿빟','executive']):
                        ctype = 'summary'
                    else:
                        ctype = 'text'
                    s['content_type'] = ctype
                ltype = s.get('layout_type') or s.get('layout_suggestion')
                if not ltype:
                    if s.get('slide_number', 1) == 1 or ctype == 'summary':
                        ltype = 'title_slide'
                    elif ctype == 'comparison':
                        ltype = 'three_column'
                    elif ctype == 'matrix':
                        ltype = 'matrix'
                    elif ctype == 'data_visualization':
                        ltype = 'split_text_chart'
                    else:
                        ltype = 'title_and_content'
                    s['layout_type'] = ltype
                enriched.append(s)
            outline = enriched
            
            if len(outline) != num_slides:
                logger.warning(f"Expected {num_slides} slides, got {len(outline)}")
            
            for i, slide in enumerate(outline, 1):
                slide['slide_number'] = i
            
            return outline
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse slide outline: {e}; head={response[:200] if response else 'Empty'}")
            raise RuntimeError(f"Slide outline generation failed: {e}")
    
    def _determine_slide_type(self, category: str) -> str:
        cat_lower = category.lower()
        if any(k in cat_lower for k in ['company', 'strengths', 'weaknesses']):
            return "Internal Analysis"
        if any(k in cat_lower for k in ['competitors', 'threats']):
            return "Competitive Landscape"
        if any(k in cat_lower for k in ['customers', 'opportunities']):
            return "Market Analysis"
        return "Strategic Analysis"



