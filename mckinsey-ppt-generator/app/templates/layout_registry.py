from typing import List, Dict, Any
import json
import os


DEFAULT_LAYOUTS: List[Dict[str, Any]] = [
    {"value": "title_slide", "label": "Title Slide", "category": "intro", "description": "Title + subtitle"},
    {"value": "dual_header", "label": "Executive Summary", "category": "summary", "description": "Top message + key points"},
    {"value": "title_and_content", "label": "Title & Content", "category": "content", "description": "General content slide"},
    {"value": "two_column", "label": "Two Column", "category": "comparison", "description": "Two columns of content"},
    {"value": "three_column", "label": "Three Column", "category": "comparison", "description": "Three columns of content"},
    {"value": "matrix", "label": "Matrix (2x2)", "category": "matrix", "description": "2x2 matrix layout"},
    {"value": "chart_slide", "label": "Chart Slide", "category": "data", "description": "Chart with commentary"},
    {"value": "bullet_slide", "label": "Bullets", "category": "content", "description": "Bulleted list"},
    {"value": "image", "label": "Image", "category": "visual", "description": "Image-centric"},
    {"value": "comparison", "label": "Comparison", "category": "comparison", "description": "Side-by-side"},
]


class LayoutRegistry:
    def __init__(self, json_path: str = "/app/app/templates/layouts.json") -> None:
        self.json_path = json_path
        self._layouts: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, "r", encoding="utf-8") as f:
                    self._layouts = json.load(f)
            else:
                self._layouts = DEFAULT_LAYOUTS.copy()
        except Exception:
            self._layouts = DEFAULT_LAYOUTS.copy()

    def list(self) -> List[Dict[str, Any]]:
        return list(self._layouts)

    def add(self, value: str, label: str, category: str, description: str = "") -> Dict[str, Any]:
        if any(x.get("value") == value for x in self._layouts):
            raise ValueError("Layout value already exists")
        entry = {"value": value, "label": label, "category": category, "description": description}
        self._layouts.append(entry)
        self._save()
        return entry

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self._layouts, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def categories(self) -> List[str]:
        return sorted({x.get("category", "content") for x in self._layouts})

