"""
SlideFixer (UTF-8, stable)

Provides a compatible interface and delegates to slide_fixer_fallback for
robust operation. Accepts ValidationResult objects or dict-like validation
items. Includes fix_presentation helper for legacy callers.
"""

from typing import Optional, Dict, Any, List
from pptx.slide import Slide

try:
    from app.services.slide_fixer_fallback import SlideFixer as FallbackSlideFixer
except Exception:  # pragma: no cover
    FallbackSlideFixer = None  # type: ignore


class SlideFixer:
    def __init__(self) -> None:
        if FallbackSlideFixer:
            self._fallback = FallbackSlideFixer()
        else:  # pragma: no cover
            self._fallback = None

    def fix_slide(
        self,
        slide: Slide,
        validation_result: Optional[Any] = None,
        aggressive_mode: bool = False,
        slide_number: Optional[int] = None,
    ) -> Dict[str, Any]:
        if not self._fallback:  # pragma: no cover
            return {"slide_number": slide_number or 0, "fixes_applied": [], "fixes_failed": ["fallback_unavailable"]}
        # We can use validation_result to prioritize fixes later; for now delegate
        return self._fallback.fix_slide(
            slide=slide,
            validation_result=validation_result,
            aggressive_mode=aggressive_mode,
            slide_number=slide_number,
        )

    def fix_presentation(self, presentation, validation_results: Dict) -> Dict[str, Any]:
        total_applied = 0
        total_failed = 0
        slide_fixes: List[Dict[str, Any]] = []
        items = validation_results.get("slide_validations", []) if isinstance(validation_results, dict) else []
        for idx, vr in enumerate(items, 1):
            try:
                has_crit = False
                if hasattr(vr, "critical_issues"):
                    has_crit = len(vr.critical_issues) > 0
                elif isinstance(vr, dict):
                    crit = vr.get("critical_issues") or []
                    has_crit = len(crit) > 0
                if not has_crit:
                    continue
                if idx <= len(presentation.slides):
                    slide = presentation.slides[idx - 1]
                    res = self.fix_slide(slide, validation_result=vr, slide_number=idx)
                    slide_fixes.append(res)
                    total_applied += len(res.get("fixes_applied", []))
                    total_failed += len(res.get("fixes_failed", []))
            except Exception:
                continue
        return {
            "success": total_failed == 0,
            "total_fixes_applied": total_applied,
            "total_fixes_failed": total_failed,
            "slide_fixes": slide_fixes,
        }
