"""
StructureEvaluator (UTF-8)

Computes structure score using MECE, Flow, and Pyramid heuristics.
"""
from typing import Dict, Any, List
from app.services.mece_validator import MECEValidator
from app.services.logic_flow_analyzer import LogicFlowAnalyzer
import re

class StructureEvaluator:
    def evaluate(self, slide_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        mece = MECEValidator().validate_mece(slide_specs)
        flow = LogicFlowAnalyzer().analyze_flow(slide_specs)
        pyramid = self._evaluate_pyramid(slide_specs)
        score = mece.score * 0.40 + flow.transition_quality * 0.35 + pyramid * 0.25
        return {
            'score': max(0.0, min(1.0, score)),
            'mece_score': mece.score,
            'flow_quality': flow.transition_quality,
            'pyramid_score': pyramid,
            'mece_overlaps': [(o.slide1, o.slide2, o.similarity) for o in mece.overlaps],
            'mece_gaps': [g.area for g in mece.gaps],
            'flow_gaps': flow.logic_gaps,
            'suggestions': mece.suggestions + flow.improvement_suggestions,
        }

    def _evaluate_pyramid(self, slides: List[Dict[str, Any]]) -> float:
        if not slides:
            return 0.0
        first = (slides[0].get('headline') or slides[0].get('title') or '').lower()
        has_conclusion = bool(re.search(r'(결론|권고|요약|summary|recommend)', first))
        support = any(len((s.get('content') or [])) >= 2 for s in slides[1:])
        score = (0.6 if has_conclusion else 0.0) + (0.4 if support else 0.0)
        return score
