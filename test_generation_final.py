"""Final test script for PPT generation after JSON parsing fixes"""
import asyncio
import aiohttp
import json
import time

async def test_ppt_generation():
    """Test PPT generation via API"""
    
    test_document = """
    Digital Transformation Strategy Report

    Executive Summary:
    Our organization faces critical digital transformation challenges in 2024. 
    Market analysis shows competitors achieving 45% operational efficiency gains through digital initiatives.
    
    Current State Analysis:
    - Legacy systems consuming 70% of IT budget
    - Customer satisfaction score: 6.5/10 
    - Digital channel adoption: 32%
    - Manual processes: 65% of operations
    
    Key Opportunities:
    1. Cloud Migration: Potential 40% infrastructure cost reduction
    2. Process Automation: 50% efficiency gain in operations
    3. Data Analytics: Real-time insights for decision making
    4. Customer Experience: Omnichannel platform implementation
    
    Strategic Recommendations:
    - Phase 1: Infrastructure modernization (Q1-Q2 2024)
    - Phase 2: Process digitization (Q3-Q4 2024)  
    - Phase 3: Advanced analytics deployment (Q1 2025)
    
    Expected ROI:
    - Year 1: 25% cost reduction
    - Year 2: 40% revenue growth
    - Customer satisfaction target: 8.5/10
    
    Investment Required:
    Total budget: $5.2M over 18 months
    Expected breakeven: Month 14
    """
    
    url = "http://localhost:8000/api/v1/ppt/generate"
    
    # Prepare form data
    form_data = aiohttp.FormData()
    form_data.add_field('document_text', test_document)
    form_data.add_field('num_slides', '10')
    form_data.add_field('target_audience', 'executive')
    form_data.add_field('presentation_purpose', 'strategic')
    
    print("\n" + "="*80)
    print("PPT GENERATION TEST - POST JSON PARSING FIX")
    print("="*80)
    
    async with aiohttp.ClientSession() as session:
        print(f"\n[1] Sending request to {url}...")
        print(f"    Document length: {len(test_document)} chars")
        print(f"    Slides requested: 10")
        
        start_time = time.time()
        
        try:
            async with session.post(url, data=form_data) as response:
                result = await response.json()
                
                elapsed_time = time.time() - start_time
                
                print(f"\n[2] Response received in {elapsed_time:.2f}s")
                print(f"    Status: {response.status}")
                
                if response.status == 200:
                    print("\n[3] SUCCESS - PPT Generation Details:")
                    print(f"    Job ID: {result.get('job_id')}")
                    print(f"    Message: {result.get('message')}")
                    
                    # Poll for status
                    job_id = result.get('job_id')
                    if job_id:
                        print(f"\n[4] Polling job status...")
                        
                        for i in range(60):  # Poll for up to 60 seconds
                            await asyncio.sleep(2)
                            
                            status_url = f"http://localhost:8000/api/v1/ppt/status/{job_id}"
                            async with session.get(status_url) as status_response:
                                status_data = await status_response.json()
                                
                                progress = status_data.get('progress', 0)
                                stage = status_data.get('current_stage', 'unknown')
                                print(f"    [{i+1}] Progress: {progress}% - Stage: {stage}")
                                
                                if status_data.get('status') == 'completed':
                                    print("\n[5] GENERATION COMPLETE!")
                                    print(f"    Download URL: {status_data.get('download_url')}")
                                    print(f"    Total time: {time.time() - start_time:.2f}s")
                                    
                                    # Check for quality metrics
                                    if 'quality_score' in status_data:
                                        print(f"    Quality Score: {status_data['quality_score']:.3f}")
                                    
                                    print("\n[6] TEST PASSED ✅")
                                    return True
                                    
                                elif status_data.get('status') == 'failed':
                                    print("\n[ERROR] Generation failed!")
                                    print(f"    Error: {status_data.get('error')}")
                                    return False
                        
                        print("\n[TIMEOUT] Generation took too long")
                        return False
                        
                else:
                    print(f"\n[ERROR] API returned error status {response.status}")
                    print(f"    Error details: {result}")
                    return False
                    
        except Exception as e:
            print(f"\n[EXCEPTION] Error during test: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    success = asyncio.run(test_ppt_generation())
    exit(0 if success else 1)