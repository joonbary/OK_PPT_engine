"""
LogicFlowAnalyzer (UTF-8)

Analyzes logical flow: SCR (Situation-Complication-Resolution), transition
coherence, and suggests optimal ordering. Lightweight heuristics.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import re


@dataclass
class SCRResult:
    score: float
    order_valid: bool


@dataclass
class TransitionResult:
    average_quality: float


@dataclass
class FlowAnalysisResult:
    scr_score: float
    transition_quality: float
    has_logic_gaps: bool
    logic_gaps: List[str]
    optimal_order: List[int]
    improvement_suggestions: List[str]


class LogicFlowAnalyzer:
    def __init__(self) -> None:
        pass

    def analyze_flow(self, slides: List[Dict[str, Any]]) -> FlowAnalysisResult:
        scr = self._validate_scr_structure(slides)
        trans = self._evaluate_transitions(slides)
        gaps = self._identify_logic_gaps(slides)
        order = self._suggest_optimal_order(slides)
        suggestions = self._generate_flow_suggestions(scr, trans, gaps)
        return FlowAnalysisResult(
            scr_score=scr.score,
            transition_quality=trans.average_quality,
            has_logic_gaps=len(gaps) > 0,
            logic_gaps=gaps,
            optimal_order=order,
            improvement_suggestions=suggestions,
        )

    def _text(self, slide: Dict[str, Any]) -> str:
        if isinstance(slide, dict):
            parts = []
            for k in ('title', 'headline'):
                if k in slide:
                    parts.append(str(slide[k]))
            c = slide.get('content')
            if isinstance(c, list):
                parts.extend([str(x) for x in c])
            elif isinstance(c, dict):
                for v in c.values():
                    parts.append(str(v))
            return ' '.join(parts).lower()
        return str(slide).lower()

    def _validate_scr_structure(self, slides: List[Dict[str, Any]]) -> SCRResult:
        labels = []
        for s in slides:
            t = self._text(s)
            if re.search(r"situation|현황|배경", t):
                labels.append('S')
            elif re.search(r"complication|문제|과제|이슈", t):
                labels.append('C')
            elif re.search(r"resolution|해결|권고|방안", t):
                labels.append('R')
            else:
                labels.append('X')
        # Check order S... C... R...
        try:
            s_idx = labels.index('S')
            c_idx = labels.index('C')
            r_idx = labels.index('R')
            order_valid = s_idx < c_idx < r_idx
        except ValueError:
            order_valid = False
        score = 0.7 if order_valid else 0.4
        score += 0.1 * labels.count('S') + 0.1 * labels.count('C') + 0.1 * labels.count('R')
        return SCRResult(score=min(1.0, score), order_valid=order_valid)

    def _evaluate_transitions(self, slides: List[Dict[str, Any]]) -> TransitionResult:
        # simple check: overlapping keywords between consecutive slides
        qualities = []
        prev = None
        for s in slides:
            txt = self._text(s)
            if prev is None:
                prev = txt; continue
            prev_kw = set(re.findall(r"[A-Za-z가-힣0-9]+", prev))
            cur_kw = set(re.findall(r"[A-Za-z가-힣0-9]+", txt))
            if not prev_kw or not cur_kw:
                qualities.append(0.5)
            else:
                inter = len(prev_kw & cur_kw)
                uni = len(prev_kw | cur_kw)
                qualities.append(inter / uni if uni else 0.5)
            prev = txt
        avg = sum(qualities) / len(qualities) if qualities else 0.6
        return TransitionResult(average_quality=avg)

    def _suggest_optimal_order(self, slides: List[Dict[str, Any]]) -> List[int]:
        # naive: keep original order
        return list(range(len(slides)))

    def _identify_logic_gaps(self, slides: List[Dict[str, Any]]) -> List[str]:
        gaps = []
        # simple: if no R found
        if not any('권고' in self._text(s) or 'resolution' in self._text(s) for s in slides):
            gaps.append('Missing resolution section')
        return gaps

    def _generate_flow_suggestions(self, scr: SCRResult, trans: TransitionResult, gaps: List[str]) -> List[str]:
        sug = []
        if not scr.order_valid:
            sug.append('Reorder slides to S→C→R (Situation→Complication→Resolution).')
        if trans.average_quality < 0.5:
            sug.append('Improve transitions by reiterating key terms between slides.')
        sug.extend(gaps)
        return sug

