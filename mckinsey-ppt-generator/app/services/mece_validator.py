"""
MECEValidator (UTF-8)

Lightweight MECE (Mutually Exclusive, Collectively Exhaustive) checker for
slide content. Uses keyword-based similarity and simple coverage heuristics.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import re


@dataclass
class Overlap:
    slide1: int
    slide2: int
    similarity: float
    overlapping_concepts: List[str] = field(default_factory=list)


@dataclass
class Gap:
    area: str
    importance: float
    suggestion: str


@dataclass
class MECEResult:
    is_exclusive: bool
    is_exhaustive: bool
    overlaps: List[Overlap]
    gaps: List[Gap]
    suggestions: List[str]
    score: float


class MECEValidator:
    def __init__(self) -> None:
        self.similarity_threshold = 0.75
        self.coverage_threshold = 0.85

    def validate_mece(self, slides: List[Dict[str, Any]]) -> MECEResult:
        overlaps = self._check_mutual_exclusivity(slides)
        gaps = self._check_collective_exhaustiveness(slides)
        suggestions = self._generate_mece_suggestions(overlaps, gaps)
        score = self._calculate_mece_score(overlaps, gaps)
        return MECEResult(
            is_exclusive=len(overlaps) == 0,
            is_exhaustive=len(gaps) == 0,
            overlaps=overlaps,
            gaps=gaps,
            suggestions=suggestions,
            score=score,
        )

    def _extract_text(self, slide: Dict[str, Any]) -> str:
        if isinstance(slide, dict):
            if 'content' in slide and isinstance(slide['content'], dict):
                parts = []
                for _, v in slide['content'].items():
                    if isinstance(v, list):
                        parts.extend([str(x) for x in v])
                    else:
                        parts.append(str(v))
                return ' '.join(parts)
            if 'content' in slide and isinstance(slide['content'], list):
                return ' '.join([str(x) for x in slide['content']])
            if 'headline' in slide:
                return str(slide.get('headline', ''))
        return str(slide)

    def _check_mutual_exclusivity(self, slides: List[Dict[str, Any]]) -> List[Overlap]:
        overlaps: List[Overlap] = []
        texts = [self._extract_text(s).lower() for s in slides]
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                sim = self._calculate_semantic_similarity(texts[i], texts[j])
                if sim > self.similarity_threshold:
                    overlaps.append(Overlap(
                        slide1=i, slide2=j, similarity=sim,
                        overlapping_concepts=self._extract_common_concepts(texts[i], texts[j])
                    ))
        return overlaps

    def _check_collective_exhaustiveness(self, slides: List[Dict[str, Any]]) -> List[Gap]:
        framework = self._identify_framework(slides)
        covered = self._extract_covered_areas(slides, framework)
        expected = self._get_expected_areas(framework)
        gaps: List[Gap] = []
        for area in expected:
            if area not in covered:
                gaps.append(Gap(
                    area=area,
                    importance=self._assess_gap_importance(area, framework),
                    suggestion=self._generate_gap_suggestion(area)
                ))
        return gaps

    def _calculate_semantic_similarity(self, t1: str, t2: str) -> float:
        kw1 = self._extract_keywords(t1)
        kw2 = self._extract_keywords(t2)
        if not kw1 and not kw2:
            return 0.0
        common = set(kw1) & set(kw2)
        union = set(kw1) | set(kw2)
        if not union:
            return 0.0
        return len(common) / len(union)

    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r"[A-Za-z가-힣0-9]+", text.lower())
        stops = {"the", "and", "for", "with", "of", "to", "in", "on", "by", "at", "a", "an"}
        return [w for w in words if len(w) > 2 and w not in stops][:50]

    def _extract_common_concepts(self, t1: str, t2: str) -> List[str]:
        kw1 = set(self._extract_keywords(t1))
        kw2 = set(self._extract_keywords(t2))
        return list((kw1 & kw2))[:10]

    def _identify_framework(self, slides: List[Dict[str, Any]]) -> str:
        frameworks = {
            "3C": ["company", "competitor", "customer", "회사", "경쟁", "고객"],
            "4P": ["product", "price", "place", "promotion", "제품", "가격", "유통", "촉진"],
            "SWOT": ["strength", "weakness", "opportunity", "threat", "강점", "약점", "기회", "위협"],
            "Porter5": ["rivalry", "supplier", "buyer", "substitute", "entrant", "경쟁", "공급", "구매"],
            "7S": ["strategy", "structure", "systems", "shared", "skills", "staff", "style"],
        }
        slide_text = ' '.join([self._extract_text(s).lower() for s in slides])
        for fw, kws in frameworks.items():
            if any(kw in slide_text for kw in kws):
                return fw
        return "CUSTOM"

    def _extract_covered_areas(self, slides: List[Dict[str, Any]], framework: str) -> List[str]:
        covered = []
        for s in slides:
            txt = self._extract_text(s).lower()
            kws = self._extract_keywords(txt)
            covered.extend(kws[:5])
        return list(set(covered))

    def _get_expected_areas(self, framework: str) -> List[str]:
        maps = {
            "3C": ["company", "competitor", "customer"],
            "4P": ["product", "price", "place", "promotion"],
            "SWOT": ["strength", "weakness", "opportunity", "threat"],
            "Porter5": ["rivalry", "supplier", "buyer", "substitute", "entrant"],
            "7S": ["strategy", "structure", "systems", "shared", "skills", "staff", "style"],
            "CUSTOM": [],
        }
        return maps.get(framework, [])

    def _assess_gap_importance(self, area: str, framework: str) -> float:
        return 1.0 if framework != "CUSTOM" else 0.5

    def _generate_gap_suggestion(self, area: str) -> str:
        return f"Add coverage for '{area}' with supporting data and actions."

    def _generate_mece_suggestions(self, overlaps: List[Overlap], gaps: List[Gap]) -> List[str]:
        sugg = []
        for ov in overlaps:
            sugg.append(
                f"Slides {ov.slide1+1} and {ov.slide2+1} overlap; merge or clarify distinct scopes."
            )
        for g in gaps:
            sugg.append(g.suggestion)
        return sugg

    def _calculate_mece_score(self, overlaps: List[Overlap], gaps: List[Gap]) -> float:
        base = 1.0
        penalty = 0.1 * len(overlaps) + 0.08 * len(gaps)
        return max(0.0, min(1.0, base - penalty))

