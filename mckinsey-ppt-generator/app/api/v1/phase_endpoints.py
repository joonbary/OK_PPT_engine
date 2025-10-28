from fastapi import APIRouter, HTTPException
from typing import Optional

from app.core.phase_manager import PhaseManager
from app.core.state_manager import StateManager, PhaseName
from app.models.phase_models import PhaseRequest


router = APIRouter()
pm = PhaseManager()
sm = StateManager()


@router.post("/analyze")
async def phase_analyze(req: PhaseRequest):
    if not req.document:
        raise HTTPException(status_code=400, detail="document is required")
    try:
        res = await pm.run_analyze(req.project_id, req.document, req.language or "ko")
        return {"project_id": req.project_id, "phase": "analyze", "status": "completed", "result": res}
    except Exception as e:
        # Surface underlying error for easier debugging
        import logging, traceback
        logging.getLogger(__name__).exception("Analyze failed: %s", e)
        raise HTTPException(status_code=500, detail=f"analyze_failed: {str(e)}")


@router.post("/structure")
async def phase_structure(req: PhaseRequest):
    if not req.document:
        raise HTTPException(status_code=400, detail="document is required")
    try:
        res = await pm.run_structure(req.project_id, req.document, req.num_slides or 10, req.language or "ko")
        return {"project_id": req.project_id, "phase": "structure", "status": "completed", "result": res}
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Structure failed: %s", e)
        raise HTTPException(status_code=500, detail=f"structure_failed: {str(e)}")


@router.post("/content")
async def phase_content(req: PhaseRequest):
    if not req.document:
        raise HTTPException(status_code=400, detail="document is required")
    res = await pm.run_content(req.project_id, req.document, req.num_slides or 10, req.language or "ko")
    return {"project_id": req.project_id, "phase": "content", "status": "completed", "result": res}


@router.post("/design")
async def phase_design(req: PhaseRequest):
    res = await pm.run_design(req.project_id)
    return {"project_id": req.project_id, "phase": "design", "status": "completed", "result": res}


@router.post("/review")
async def phase_review(req: PhaseRequest):
    res = await pm.run_review(req.project_id)
    return {"project_id": req.project_id, "phase": "review", "status": "completed", "result": res}


@router.get("/status/{project_id}/{phase}")
async def phase_status(project_id: str, phase: str):
    try:
        p = PhaseName(phase)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid phase")
    s = await sm.get_status(project_id, p)
    if not s:
        raise HTTPException(status_code=404, detail="not found")
    return s


@router.post("/retry/{project_id}/{phase}")
async def phase_retry(project_id: str, phase: str, req: PhaseRequest):
    try:
        p = PhaseName(phase)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid phase")
    if p == PhaseName.ANALYZE:
        return await phase_analyze(PhaseRequest(project_id=project_id, document=req.document, language=req.language))
    if p == PhaseName.STRUCTURE:
        return await phase_structure(PhaseRequest(project_id=project_id, document=req.document, num_slides=req.num_slides, language=req.language))
    if p == PhaseName.CONTENT:
        return await phase_content(PhaseRequest(project_id=project_id, document=req.document, num_slides=req.num_slides, language=req.language))
    if p == PhaseName.DESIGN:
        return await phase_design(PhaseRequest(project_id=project_id))
    if p == PhaseName.REVIEW:
        return await phase_review(PhaseRequest(project_id=project_id))
    raise HTTPException(status_code=400, detail="invalid phase")


@router.post("/export")
async def phase_export(req: PhaseRequest):
    if not req.document:
        raise HTTPException(status_code=400, detail="document is required")
    try:
        res = await pm.export(req.project_id, req.document, req.num_slides or 10, req.language or "ko")
        return {"project_id": req.project_id, "phase": "export", "status": "completed" if res.get("success") else "failed", "result": res}
    except Exception as e:
        # 실패 사유를 그대로 전달(디버깅 가시성)
        return {"project_id": req.project_id, "phase": "export", "status": "failed", "error": str(e)}
