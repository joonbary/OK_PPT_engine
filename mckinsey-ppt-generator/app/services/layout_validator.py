"""
LayoutValidator (UTF-8)

Normalizes slide spec for template application:
- Limits number of bullets/items to avoid overflow
- Ensures simple defaults for missing headers
"""

from typing import Dict, Any, List


class LayoutValidator:
    def normalize(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        s = dict(spec)
        # Limit bullets
        # Limit bullets
        for key in ("content", "bullets", "left", "right"):
            if isinstance(s.get(key), list):
                s[key] = s[key][:7]
        cols = s.get("columns")
        if isinstance(cols, list):
            s["columns"] = [self._trim_list(c) for c in cols[:3]]
        # Matrix size guard
        if isinstance(s.get("matrix"), list):
            m = s["matrix"]
            if len(m) >= 2 and all(isinstance(row, list) for row in m):
                s["matrix"] = [row[:2] for row in m[:2]]
        # Ensure title presence
        if not s.get("title") and s.get("headline"):
            s["title"] = s["headline"]
        return s\n\n    def _trim_list(self, items: Any) -> List[str]:
        try:
            return [str(x) for x in items][:7]
        except Exception:
            return []


