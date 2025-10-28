import os
import asyncio
from pathlib import Path

# Ensure package on path
import sys
ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "mckinsey-ppt-generator"
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from app.services.workflow_orchestrator import WorkflowOrchestrator
from app.models.workflow_models import GenerationRequest


def sample_document():
    return (
        "Our FY plan targets 15% revenue growth via market expansion and CX improvements. "
        "We analyzed customer trends, competitive landscape, and operational efficiency. "
        "Phased implementation with measurable milestones is recommended."
    )


async def main():
    # Force AI-integrated path
    os.environ['USE_AI_INTEGRATED'] = '1'

    req = GenerationRequest(
        document=sample_document(),
        num_slides=6,
        target_audience="executive",
    )

    orchestrator = WorkflowOrchestrator(
        max_iterations=2,
        target_quality_score=0.85,
        aggressive_fix=True,
        timeout_minutes=5,
    )

    res = await orchestrator.execute(req)
    print("status:", "success" if res.success else "failed")
    print("pptx:", res.pptx_path)
    print("quality:", res.quality_score)

    if res.pptx_path:
        print("Saved:", res.pptx_path)


if __name__ == "__main__":
    asyncio.run(main())
