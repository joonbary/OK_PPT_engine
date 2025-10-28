from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.templates.layout_registry import LayoutRegistry

router = APIRouter(prefix="/layouts", tags=["layouts"])
registry = LayoutRegistry()


@router.get("/")
async def list_layouts():
    return {"layouts": registry.list(), "categories": registry.categories()}


@router.post("/")
async def add_layout(payload: Dict[str, Any]):
    try:
        entry = registry.add(
            value=str(payload.get("value", "")).strip(),
            label=str(payload.get("label", "")).strip(),
            category=str(payload.get("category", "content")).strip(),
            description=str(payload.get("description", "")).strip(),
        )
        return {"layout": entry}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

