import asyncio
import sys
from pathlib import Path
from pptx import Presentation

# Ensure local package import
ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "mckinsey-ppt-generator"
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from app.services.content_generator import ContentGenerator


async def main():
    doc = (
        "Our company targets 15% revenue growth with a market expansion focus. "
        "Analysis covers customer trends, competitive landscape, and operational efficiency. "
        "We recommend phased implementation and clear success metrics."
    )

    gen = ContentGenerator()
    # Build 2 slides: title + 1 content
    prs: Presentation = await gen.generate_from_document_with_ai(document=doc, num_slides=2)

    out_dir = Path("output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "test_ai_slides.pptx"
    prs.save(str(out_path))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
