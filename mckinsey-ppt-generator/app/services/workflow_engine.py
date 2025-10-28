# -*- coding: utf-8 -*-
"""
            # Structure preview (layout heuristic)
            try:
                outline = strategy_result.get('outline', []) or []
                preview = []
                for i, item in enumerate(outline, 1):
                    title = (item.get('title') or '').strip() if isinstance(item, dict) else str(item)
                    t = title.lower()
                    layout = 'title_and_content'
                    if i == 1 or ('summary' in t) or ('¿ä¾à' in t):
                        layout = 'title_slide'
                    elif ('comparison' in t) or ('ºñ±³' in t) or ('3c' in t) or ('three' in t):
                        layout = 'three_column'
                    elif ('matrix' in t) or ('¸ÅÆ®¸¯½º' in t) or ('2x2' in t) or ('3x3' in t):
                        layout = 'matrix'
                    elif ('roi' in t) or ('data' in t) or ('ºÐ¼®' in t) or ('chart' in t) or ('Â÷Æ®' in t):
                        layout = 'split_text_chart'
                    preview.append({'slide': i, 'title': title, 'layout': layout})
                await self._update_progress(job_id, 'structure_design', 60)
                try:
                    rc = RedisClient()
                    await rc.update_ppt_status(job_id, {
                        'current_stage': 'structure_design',
                        'progress': 60,
                        'structure_preview': preview[:12],
                    })
                except Exception:
                    pass
                logger.info(f"Structure preview (first 5): {preview[:5]}")
            except Exception as e:
                logger.warning(f"Structure preview failed: {e}")
?í¬?ë¡???ì§
5ê°??ì´?í¸ë¥?ì¡°ì¨?ì¬ PPTë¥??ì±?ë ë©ì¸ ?ì´?ë¼??"""

from typing import Dict, List, Optional
from app.agents.strategist_agent import StrategistAgent
from app.agents.data_analyst_agent import DataAnalystAgent
from app.agents.storyteller_agent import StorytellerAgent
from app.agents.design_agent import DesignAgent
from app.agents.quality_review_agent import QualityReviewAgent
from app.core.redis_client import RedisClient
from app.services.pptx_generator import PptxGeneratorService # Added
import asyncio
import json
from datetime import datetime
from loguru import logger


class WorkflowEngine:
    """
    ë©???ì´?í¸ ?í¬?ë¡???ì§
    
    ?ì´?ë¼??
    1. Document Analysis (Strategist)
    2. Data Extraction (DataAnalyst)
    3. Story Construction (Storyteller)
    4. Design Application (Designer)
    5. Quality Review (QualityReview)
    6. Iteration (?ì§ ë¯¸ë¬ ??ê°ì )
    """
    
    def __init__(self):
        # ?ì´?í¸ ì´ê¸°??        self.strategist = StrategistAgent()
        self.analyst = DataAnalystAgent()
        self.storyteller = StorytellerAgent()
        self.designer = DesignAgent()
        self.reviewer = QualityReviewAgent()
        self.pptx_generator = PptxGeneratorService() # Added

        # ?ì´?ë¼???¨ê³
        self.stages = [
            "document_analysis",
            "data_extraction",
            "story_construction",
            "design_application",
            "quality_review",
            "iteration"
        ]
        
        # ?ì§ ê¸°ì?
        self.quality_threshold = 0.85
        self.max_iterations = 3
    
    async def execute(self, input_data: Dict) -> Dict:
        """
        ?ì²´ ?í¬?ë¡???¤í
        
        Args:
            input_data: {
                'job_id': str,           # ?ì ID (ì§íë¥?ì¶ì )
                'document': str,         # ë¹ì¦?ì¤ ë¬¸ì
                'num_slides': int,       # ëª©í ?¬ë¼?´ë ??(ê¸°ë³¸ 15)
                'style': str,            # ?¤í???(ê¸°ë³¸ 'mckinsey')
                'target_audience': str   # ?ê²?ì²?¤
            }
        
        Returns:
            {
                'job_id': str,
                'status': str,              # 'completed' or 'failed'
                'ppt_data': Dict,           # ?ì±??PPT ?°ì´??                'quality_score': float,
                'iterations': int,
                'processing_time': float,
                'metadata': Dict
            }
        """
        job_id = input_data.get('job_id', 'unknown')
        start_time = datetime.now()
        
        logger.info(f"Starting workflow execution for job {job_id}")
        
        try:
            # ì»¨í?¤í¸ ì´ê¸°??            context = {
                'job_id': job_id,
                'input': input_data,
                'start_time': start_time.isoformat(),
                'iteration': 0
            }
            
            # ë©ì¸ ?ì´?ë¼???¤í
            result = await self._execute_pipeline(context)
            
            # ë°ë³µ ê°ì  ë£¨í
            iteration = 0
            while iteration < self.max_iterations:
                quality_score = result.get('quality_review', {}).get('quality_scores', {}).get('total_score', 0)
                
                if quality_score >= self.quality_threshold:
                    logger.info(f"Quality threshold met: {quality_score:.3f} >= {self.quality_threshold}")
                    break
                
                logger.warning(f"Quality below threshold: {quality_score:.3f} < {self.quality_threshold}. Iteration {iteration + 1}")
                
                # ê°ì  ?¤í
                result = await self._improve_pipeline(result, context)
                iteration += 1
                context['iteration'] = iteration
            
            # ìµì¢ ê²°ê³¼ ?ì±
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            final_result = {
                'job_id': job_id,
                'status': 'completed',
                'generated_pptx_path': result.get('generated_pptx_path', ''), # Key name matches what ppt_service expects
                'quality_score': result.get('quality_review', {}).get('quality_scores', {}).get('total_score', 0),
                'iterations': iteration,
                'processing_time': processing_time,
                'metadata': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'num_slides': len(result.get('design_application', {}).get('styled_slides', [])), # Still use styled_slides for count
                    'quality_passed': result.get('quality_review', {}).get('passed', False)
                }
            }
            
            logger.info(f"Workflow completed for job {job_id}. Quality: {final_result['quality_score']:.3f}")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Workflow execution failed for job {job_id}: {e}")
            return {
                'job_id': job_id,
                'status': 'failed',
                'error': str(e),
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
    
    async def _execute_pipeline(self, context: Dict) -> Dict:
        """
        ë©ì¸ ?ì´?ë¼???¤í
        
        ?ì:
        1. Strategist: ë¬¸ì ë¶ì + êµ¬ì¡° ?¤ê³
        2. DataAnalyst: ?°ì´??ì¶ì¶ + ?¸ì¬?´í¸
        3. Storyteller: ?¤í ë¦¬ë¼??êµ¬ì±
        4. Designer: ?ì???ì©
        5. QualityReview: ?ì§ ê²ì¦?        """
        input_data = context['input']
        job_id = context['job_id']
        
        result = {}
        
        # Stage 1: Document Analysis (Strategist)
        logger.info("Stage 1/5: Document Analysis (Strategist)")
        await self._update_progress(job_id, 'document_analysis', 20)
        
        strategy_result = await self.strategist.process(
            input_data={
                'document': input_data['document'],
                'num_slides': input_data.get('num_slides', 15)
            },
            context=context
        )
        result['document_analysis'] = strategy_result

        # Stage 1.5: Structure preview (from outline)
        try:
            outline = strategy_result.get('outline', []) or []
            preview = []
            for i, item in enumerate(outline, 1):
                title = (item.get('title') or '').strip() if isinstance(item, dict) else str(item)
                t = title.lower()
                layout = 'title_and_content'
                if i == 1 or ('summary' in t) or ('¿ä¾à' in t):
                    layout = 'title_slide'
                elif ('comparison' in t) or ('ºñ±³' in t) or ('3c' in t) or ('three' in t):
                    layout = 'three_column'
                elif ('matrix' in t) or ('¸ÅÆ®¸¯½º' in t) or ('2x2' in t) or ('3x3' in t):
                    layout = 'matrix'
                elif ('roi' in t) or ('data' in t) or ('ºÐ¼®' in t) or ('chart' in t) or ('Â÷Æ®' in t):
                    layout = 'split_text_chart'
                preview.append({'slide': i, 'title': title, 'layout': layout})
            await self._update_progress(job_id, 'structure_design', 60)
            rc = RedisClient()
            await rc.update_ppt_status(job_id, {
                'current_stage': 'structure_design',
                'progress': 60,
                'structure_preview': preview[:12],
            })
            logger.info(f"Structure preview (first 5): {preview[:5]}")
        except Exception as e:
            logger.warning(f"Structure preview failed: {e}")
        
        # Stage 2: Data Extraction (DataAnalyst)
        logger.info("Stage 2/5: Data Extraction (DataAnalyst)")
        await self._update_progress(job_id, 'data_extraction', 40)
        
        data_result = await self.analyst.process(
            input_data={
                'document': input_data['document'],
                'outline': strategy_result['outline'],
                'pyramid': strategy_result['pyramid']
            },
            context=context
        )
        result['data_extraction'] = data_result
        
        # Stage 3: Story Construction (Storyteller)
        logger.info("Stage 3/5: Story Construction (Storyteller)")
        await self._update_progress(job_id, 'story_construction', 60)
        
        story_result = await self.storyteller.process(
            input_data={
                'outline': strategy_result['outline'],
                'pyramid': strategy_result['pyramid'],
                'insights': data_result['insights']
            },
            context=context
        )
        result['story_construction'] = story_result
        
        # Stage 4: Design Application (Designer)
        logger.info("Stage 4/5: Design Application (Designer)")
        await self._update_progress(job_id, 'design_application', 80)

        # Persist structure preview for UI continuity if available
        try:
            if 'outline' in strategy_result:
                outline = strategy_result.get('outline', []) or []
                preview = []
                for i, item in enumerate(outline, 1):
                    title = (item.get('title') or '').strip() if isinstance(item, dict) else str(item)
                    t = title.lower()
                    layout = 'title_and_content'
                    if i == 1 or ('summary' in t) or ('¿ä¾à' in t):
                        layout = 'title_slide'
                    elif ('comparison' in t) or ('ºñ±³' in t) or ('3c' in t) or ('three' in t):
                        layout = 'three_column'
                    elif ('matrix' in t) or ('¸ÅÆ®¸¯½º' in t) or ('2x2' in t) or ('3x3' in t):
                        layout = 'matrix'
                    elif ('roi' in t) or ('data' in t) or ('ºÐ¼®' in t) or ('chart' in t) or ('Â÷Æ®' in t):
                        layout = 'split_text_chart'
                    preview.append({'slide': i, 'title': title, 'layout': layout})
                rc = RedisClient()
                await rc.update_ppt_status(job_id, {
                    'current_stage': 'design_application',
                    'progress': 80,
                    'structure_preview': preview[:12],
                })
        except Exception:
            pass
        
        design_result = await self.designer.process(
            input_data={
                'outline': strategy_result['outline'],
                'chart_specs': data_result['chart_specs'],
                'insights': data_result['insights']
            },
            context=context
        )
        result['design_application'] = design_result

        # PPTX ?ì¼ ?ì±
        logger.info("Generating PPTX file from styled slides")
        pptx_filename = f"generated_presentation_{job_id}.pptx"
        pptx_file_path = self.pptx_generator.generate_pptx(
            styled_slides=design_result['styled_slides'],
            output_filename=pptx_filename
        )
        result['generated_pptx_path'] = pptx_file_path # Store path in result
        
        # Fix #4: McKinsey ?ì§ ê²ì¦?ë°??ë ?ì 
        logger.info("? McKinsey ?ì§ ê²ì¦?ë°??ë ?ì  ?ì...")
        try:
            from pptx import Presentation
            from app.services.quality_service import QualityService
            
            # PPTX ?ì¼ ë¡ë
            prs = Presentation(pptx_file_path)
            
            # ?ì§ ê²ì¦?ë°??ë ê°ì 
            quality_service = QualityService()
            quality_result = await quality_service.validate_and_improve_presentation(
                prs, 
                auto_fix=True,
                target_quality=0.85
            )
            
            # ê°ì ???ë ? í?´ì ???            prs.save(pptx_file_path)
            
            # ?ì§ ê²°ê³¼ ë¡ê¹
            logger.info(f"??McKinsey ?ì§ ê²ì¦??ë£: ?ì {quality_result['final_quality_score']:.3f}")
            logger.info(f"? ?ì§ ê°ì : {quality_result['total_iterations']}??ë°ë³µ, {quality_result['total_issues_resolved']}ê°??´ì ?´ê²°")
            
            # ê²°ê³¼???ì§ ?ë³´ ì¶ê?
            result['mckinsey_quality'] = quality_result
            
        except Exception as e:
            logger.error(f"??McKinsey ?ì§ ê²ì¦??¤í¨: {e}")
            # ?ë¬ê° ë°ì?´ë ?ì²´ ?ë¡?¸ì¤??ê³ì ì§í

        # Stage 5: Quality Review (QualityReview)
        logger.info("Stage 5/5: Quality Review (QualityReview)")
        await self._update_progress(job_id, 'quality_review', 95)

        # Persist structure preview during quality_review
        try:
            if 'outline' in strategy_result:
                outline = strategy_result.get('outline', []) or []
                preview = []
                for i, item in enumerate(outline, 1):
                    title = (item.get('title') or '').strip() if isinstance(item, dict) else str(item)
                    t = title.lower()
                    layout = 'title_and_content'
                    if i == 1 or ('summary' in t) or ('¿ä¾à' in t):
                        layout = 'title_slide'
                    elif ('comparison' in t) or ('ºñ±³' in t) or ('3c' in t) or ('three' in t):
                        layout = 'three_column'
                    elif ('matrix' in t) or ('¸ÅÆ®¸¯½º' in t) or ('2x2' in t) or ('3x3' in t):
                        layout = 'matrix'
                    elif ('roi' in t) or ('data' in t) or ('ºÐ¼®' in t) or ('chart' in t) or ('Â÷Æ®' in t):
                        layout = 'split_text_chart'
                    preview.append({'slide': i, 'title': title, 'layout': layout})
                rc = RedisClient()
                await rc.update_ppt_status(job_id, {
                    'current_stage': 'quality_review',
                    'progress': 95,
                    'structure_preview': preview[:12],
                })
                logger.info("Structure preview persisted at quality_review")
        except Exception:
            pass

        quality_result = await self.reviewer.process(
            input_data={
                'pptx_file_path': pptx_file_path, # Pass PPTX path
                'insights': data_result['insights'],
                'pyramid': strategy_result['pyramid']
            },
            context=context
        )
        result['quality_review'] = quality_result
        
        await self._update_progress(job_id, 'completed', 100)
        
        return result
    
    async def _improve_pipeline(self, previous_result: Dict, context: Dict) -> Dict:
        """
        ?ì§ ê°ì  ë°ë³µ ë£¨í
        
        ê°ì  ?ëµ:
        1. ê°ì  ?ì ë¶ì
        2. ?´ë¹ ?ì´?í¸ ?¬ì¤??        3. ?ì ?¨ê³ ?¬ì¤??        """
        improvements = previous_result.get('quality_review', {}).get('improvements', [])
        
        logger.info(f"Applying {len(improvements)} improvements")
        
        # ê°???°ì ?ì ?ì? ê°ì  ??ª© ?ë³
        high_priority = [imp for imp in improvements if imp.get('priority') == 'high']
        
        if not high_priority:
            logger.warning("No high priority improvements found")
            return previous_result
        
        # ê°ì  ì¹´íê³ ë¦¬ë³?ì²ë¦¬
        categories_to_improve = {imp['category'] for imp in high_priority}
        
        # ?ì???¨ê³ë§??¬ì¤??        result = previous_result.copy()
        
        if 'clarity' in categories_to_improve or 'insight' in categories_to_improve:
            # DataAnalyst ?¬ì¤??            logger.info("Re-running DataAnalyst for improved insights")
            data_result = await self.analyst.process(
                input_data={
                    'document': context['input']['document'],
                    'outline': result['document_analysis']['outline'],
                    'pyramid': result['document_analysis']['pyramid']
                },
                context=context
            )
            result['data_extraction'] = data_result
        
        if 'actionability' in categories_to_improve:
            # Storyteller ?¬ì¤??            logger.info("Re-running Storyteller for improved actionability")
            story_result = await self.storyteller.process(
                input_data={
                    'outline': result['document_analysis']['outline'],
                    'pyramid': result['document_analysis']['pyramid'],
                    'insights': result['data_extraction']['insights']
                },
                context=context
            )
            result['story_construction'] = story_result
        
        # ?ì???¬ì ??        design_result = await self.designer.process(
            input_data={
                'outline': result['document_analysis']['outline'],
                'chart_specs': result['data_extraction']['chart_specs'],
                'insights': result['data_extraction']['insights']
            },
            context=context
        )
        result['design_application'] = design_result

        # PPTX ?ì¼ ?ì± (ê°ì  ë£¨í ??
        logger.info("Generating PPTX file for iteration from styled slides")
        pptx_filename = f"generated_presentation_{context['job_id']}_iter{context['iteration']}.pptx" # Use job_id and iteration for unique name
        pptx_file_path = self.pptx_generator.generate_pptx(
            styled_slides=design_result['styled_slides'],
            output_filename=pptx_filename
        )
        result['generated_pptx_path'] = pptx_file_path # Store path in result
        
        # Fix #4: McKinsey ?ì§ ê²ì¦?(ê°ì  ë£¨í ??
        logger.info(f"? ë°ë³µ {context['iteration']}: McKinsey ?ì§ ê²ì¦??ì...")
        try:
            from pptx import Presentation
            from app.services.quality_service import QualityService
            
            # PPTX ?ì¼ ë¡ë
            prs = Presentation(pptx_file_path)
            
            # ?ì§ ê²ì¦?ë°??ë ê°ì 
            quality_service = QualityService()
            quality_result = await quality_service.validate_and_improve_presentation(
                prs, 
                auto_fix=True,
                target_quality=0.85
            )
            
            # ê°ì ???ë ? í?´ì ???            prs.save(pptx_file_path)
            
            # ?ì§ ê²°ê³¼ ë¡ê¹
            logger.info(f"??ë°ë³µ {context['iteration']} ?ì§ ê²ì¦? ?ì {quality_result['final_quality_score']:.3f}")
            
            # ê²°ê³¼???ì§ ?ë³´ ì¶ê?
            result['mckinsey_quality'] = quality_result
            
        except Exception as e:
            logger.error(f"??ë°ë³µ {context['iteration']} ?ì§ ê²ì¦??¤í¨: {e}")

        # ?ì§ ?¬ê???        quality_result = await self.reviewer.process(
            input_data={
                'pptx_file_path': pptx_file_path, # Pass PPTX path
                'insights': result['data_extraction']['insights'],
                'pyramid': result['document_analysis']['pyramid']
            },
            context=context
        )
        result['quality_review'] = quality_result
        
        return result
    
    async def _update_progress(self, job_id: str, stage: str, progress: int):
        """
        Redis??ì§í ?í© ???        
        ????ì:
        {
            'stage': str,
            'progress': int (0-100),
            'timestamp': str
        }
        """
        try:
            redis_client = RedisClient()
            progress_data = {
                'current_stage': stage,
                'progress': progress,
                'updated_at': datetime.now().isoformat()
            }
            await redis_client.update_ppt_status(job_id, progress_data)
            logger.debug(f"Progress updated: {job_id} - {stage} ({progress}%)")
        except Exception as e:
            logger.warning(f"Failed to update progress: {e}")
    
    def _compile_ppt_data(self, result: Dict) -> Dict:
        """
        ìµì¢ PPT ?°ì´??êµ¬ì¡° ?ì±
        
        Returns:
            {
                'slides': List[Dict],      # ?ì±???¬ë¼?´ë
                'metadata': Dict,          # ë©í??°ì´??                'quality_report': Dict     # ?ì§ ë¦¬í¬??            }
        """
        # styled_slides = result.get('design_application', {}).get('styled_slides', []) # No longer needed directly
        pptx_file_path = result.get('generated_pptx_path', '') # Get the generated PPTX path
        quality_scores = result.get('quality_review', {}).get('quality_scores', {})
        speaker_notes = result.get('story_construction', {}).get('speaker_notes', [])

        # Note: speaker_notes integration into styled_slides is now handled by PptxGeneratorService
        # if we want to store speaker notes with the final PPT data, we might need to adjust this.
        # For now, we'll assume the generated PPTX is the primary output.

        return {
            'pptx_file_path': pptx_file_path, # Return the path to the generated PPTX
            'metadata': {
                'total_slides': len(result.get('design_application', {}).get('styled_slides', [])), # Still need slide count
                'quality_score': quality_scores.get('total_score', 0),
                'framework_used': result.get('document_analysis', {}).get('framework', {}).get('framework_name', 'N/A'),
                'generation_timestamp': datetime.now().isoformat()
            },
            'quality_report': {
                'scores': quality_scores,
                'so_what_results': result.get('quality_review', {}).get('so_what_results', []),
                'improvements': result.get('quality_review', {}).get('improvements', [])
            }
        }
    
    async def get_progress(self, job_id: str) -> Dict:
        """
        ?ì ì§í ?í© ì¡°í
        
        Returns:
            {
                'job_id': str,
                'stage': str,
                'progress': int,
                'timestamp': str
            }
        """
        try:
            redis_client = RedisClient()
            progress_data = await redis_client.get_ppt_status(job_id)
            
            if progress_data:
                return progress_data
            else:
                return {
                    'job_id': job_id,
                    'stage': 'not_found',
                    'progress': 0,
                    'timestamp': None
                }
                
        except Exception as e:
            logger.error(f"Failed to get progress: {e}")
            return {
                'job_id': job_id,
                'stage': 'error',
                'progress': 0,
                'error': str(e)
            }
