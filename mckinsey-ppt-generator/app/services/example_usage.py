"""
Example usage of PPT generation services.

This file demonstrates how to use the PPT generation services
to create professional McKinsey-style presentations.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add the app directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent))

from services.ppt_generator import PPTGenerator, SlideContent, PresentationMetadata
from services.template_manager import TemplateManager
from services.mckinsey_styles import SlideLayoutType


def create_sample_presentation():
    """Create a sample presentation demonstrating all features"""
    
    # Mock database session (in real usage, this would be a proper SQLAlchemy session)
    class MockDB:
        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass
        def rollback(self): pass
        def query(self, model): 
            class MockQuery:
                def filter(self, condition): return self
                def first(self): return None
                def all(self): return []
                def distinct(self): return self
                def order_by(self, field): return self
            return MockQuery()
    
    mock_db = MockDB()
    
    # Initialize services
    template_manager = TemplateManager(mock_db)
    ppt_generator = PPTGenerator(mock_db, template_manager=template_manager)
    
    # Create slide content
    slides_content = [
        # Title slide
        SlideContent(
            title="Strategic Digital Transformation Initiative",
            subtitle="Executive Summary & Implementation Roadmap\nMcKinsey & Company",
            layout_type=SlideLayoutType.TITLE.value
        ),
        
        # Executive summary
        SlideContent(
            title="Executive Summary",
            content=[
                "Digital transformation presents $2.5B market opportunity",
                "Three-phase implementation strategy over 18 months",
                "Expected ROI of 300% within 24 months",
                "Key risks identified and mitigation strategies developed"
            ],
            layout_type=SlideLayoutType.CONTENT.value,
            speaker_notes="Emphasize the strong business case and ROI projections. Address any concerns about timeline."
        ),
        
        # Market analysis with chart
        SlideContent(
            title="Market Analysis & Growth Projections",
            content=[
                "Current market size: $2.1B globally",
                "Projected CAGR of 15% through 2026",
                "Key growth drivers identified",
                "Competitive positioning analysis"
            ],
            layout_type=SlideLayoutType.CHART.value,
            charts=[{
                "type": "column",
                "title": "Market Growth Projection (2023-2026)",
                "categories": ["2023", "2024", "2025", "2026"],
                "series": [{
                    "name": "Market Size ($B)",
                    "values": [2.1, 2.4, 2.8, 3.2]
                }, {
                    "name": "Our Target Share ($B)",
                    "values": [0.15, 0.25, 0.42, 0.65]
                }]
            }],
            speaker_notes="Walk through the growth trajectory and highlight our increasing market share target."
        ),
        
        # Two-column comparison
        SlideContent(
            title="Current State vs. Future State",
            content=[
                "Current Challenges:",
                "• Legacy systems limiting agility",
                "• Manual processes reducing efficiency",
                "• Limited data analytics capabilities",
                "• Siloed organizational structure",
                "Future Vision:",
                "• Cloud-native architecture",
                "• Automated workflows and AI integration",
                "• Advanced analytics and insights",
                "• Cross-functional collaborative teams"
            ],
            layout_type=SlideLayoutType.TWO_COLUMN.value,
            speaker_notes="Contrast the current pain points with the future state benefits."
        ),
        
        # Implementation roadmap table
        SlideContent(
            title="Implementation Roadmap",
            layout_type=SlideLayoutType.TABLE.value,
            tables=[{
                "headers": ["Phase", "Duration", "Key Activities", "Deliverables", "Investment ($M)"],
                "rows": [
                    ["Phase 1: Foundation", "Months 1-6", "Infrastructure setup, Team building", "Cloud platform, Core team", "2.5"],
                    ["Phase 2: Development", "Months 7-12", "Platform development, Integration", "MVP platform, Integrations", "4.2"],
                    ["Phase 3: Scale", "Months 13-18", "Full deployment, Optimization", "Production system, ROI", "3.8"]
                ]
            }],
            speaker_notes="Emphasize the phased approach reduces risk and allows for iterative learning."
        ),
        
        # Key recommendations
        SlideContent(
            title="Key Recommendations",
            content=[
                "Immediate Actions (Next 30 days):",
                "• Secure executive sponsorship and funding approval",
                "• Establish program management office",
                "• Begin core team recruitment",
                "",
                "Success Factors:",
                "• Strong change management program",
                "• Continuous stakeholder engagement",
                "• Agile development methodology",
                "• Regular progress reviews and adjustments"
            ],
            layout_type=SlideLayoutType.CONTENT.value,
            speaker_notes="Call for decision and next steps. Emphasize urgency of starting soon."
        )
    ]
    
    # Create presentation metadata
    metadata = PresentationMetadata(
        title="Strategic Digital Transformation Initiative",
        author="McKinsey & Company",
        subject="Digital Transformation Strategy",
        category="Strategic Planning",
        ai_model="Claude-3.5-Sonnet",
        ai_tokens_used=5420
    )
    
    # Generate presentation
    print("Creating presentation...")
    file_path, presentation_model = ppt_generator.create_presentation(
        slides_content=slides_content,
        metadata=metadata,
        template_name="McKinsey Professional",
        save_to_db=False  # Skip database save for this example
    )
    
    if file_path:
        print(f"✅ Presentation created successfully!")
        print(f"📁 File saved to: {file_path}")
        print(f"📊 Slides created: {len(slides_content)}")
        print(f"⏱️  Generation time: {metadata.generation_time:.2f} seconds")
        
        # Get presentation info
        info = ppt_generator.get_presentation_info(file_path)
        print(f"📏 File size: {info.get('file_size', 0) / 1024:.1f} KB")
        print(f"💬 Word count: {metadata.word_count}")
    else:
        print("❌ Failed to create presentation")
    
    return file_path


def demonstrate_template_features():
    """Demonstrate template management features"""
    
    print("\n" + "="*50)
    print("Template Management Features")
    print("="*50)
    
    # Mock database
    class MockDB:
        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass
        def rollback(self): pass
        def query(self, model): 
            class MockQuery:
                def filter(self, condition): return self
                def first(self): return None
                def all(self): return []
                def distinct(self): return self
                def order_by(self, field): return self
            return MockQuery()
    
    mock_db = MockDB()
    template_manager = TemplateManager(mock_db)
    
    # Show available layout types
    print("📐 Available Layout Types:")
    for layout in SlideLayoutType:
        print(f"   • {layout.value}: {layout.name}")
    
    # Show McKinsey color palette
    from services.mckinsey_styles import McKinseyColors
    print("\n🎨 McKinsey Color Palette:")
    print(f"   • Primary Blue: RGB{McKinseyColors.PRIMARY_BLUE}")
    print(f"   • Secondary Blue: RGB{McKinseyColors.SECONDARY_BLUE}")
    print(f"   • Chart Colors: {len(McKinseyColors.CHART_COLORS)} colors available")
    
    # Show font specifications
    from services.mckinsey_styles import McKinseyFonts
    print("\n🔤 Font Specifications:")
    print(f"   • Primary Font: {McKinseyFonts.PRIMARY_FONT}")
    print(f"   • Title Size: {McKinseyFonts.TITLE_SIZE}")
    print(f"   • Body Size: {McKinseyFonts.BODY_SIZE}")


def main():
    """Main demonstration function"""
    print("McKinsey PPT Generator - Service Demonstration")
    print("=" * 55)
    
    try:
        # Create sample presentation
        file_path = create_sample_presentation()
        
        # Demonstrate template features
        demonstrate_template_features()
        
        print("\n✨ Demonstration completed successfully!")
        print("\nKey Features Demonstrated:")
        print("• Professional McKinsey-style formatting")
        print("• Multiple slide layouts (title, content, two-column, chart, table)")
        print("• Chart generation with data visualization")
        print("• Table creation with styling")
        print("• Speaker notes integration")
        print("• Metadata tracking and file management")
        print("• Template management system")
        
        if file_path and os.path.exists(file_path):
            print(f"\n📂 Open the generated presentation: {file_path}")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()