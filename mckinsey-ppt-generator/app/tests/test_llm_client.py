"""
LLM 클라이언트 테스트
Claude-3 Opus와 GPT-4 Turbo 연결 테스트
"""

import pytest
import asyncio
import os
from app.core.llm_client import LLMClient, get_llm_client
from app.core.config import settings

@pytest.mark.asyncio
async def test_gpt4_call():
    """GPT-4 Turbo API 호출 테스트"""
    
    if not settings.OPENAI_API_KEY:
        pytest.skip("OPENAI_API_KEY not configured")
    
    client = get_llm_client("gpt-4-turbo")
    
    # 간단한 테스트
    prompt = "What is 2+2? Answer with just the number."
    response = await client.generate(
        prompt=prompt,
        temperature=0,
        max_tokens=10
    )
    
    assert response is not None
    assert len(response) > 0
    assert "4" in response
    
    print(f"GPT-4 response: {response}")

@pytest.mark.asyncio
async def test_claude_call():
    """Claude-3 Opus API 호출 테스트"""
    
    if not settings.ANTHROPIC_API_KEY:
        pytest.skip("ANTHROPIC_API_KEY not configured")
    
    client = get_llm_client("claude-3-opus")
    
    # 간단한 테스트
    prompt = "What is 2+2? Answer with just the number."
    response = await client.generate(
        prompt=prompt,
        temperature=0,
        max_tokens=10
    )
    
    assert response is not None
    assert len(response) > 0
    assert "4" in response
    
    print(f"Claude-3 response: {response}")

@pytest.mark.asyncio
async def test_caching():
    """LLM 응답 캐싱 테스트"""
    
    if not settings.OPENAI_API_KEY:
        pytest.skip("OPENAI_API_KEY not configured")
    
    client = get_llm_client("gpt-4-turbo")
    
    # 고유한 프롬프트 생성
    import time
    unique_prompt = f"Test prompt at {time.time()}: What is 1+1?"
    
    # 첫 번째 호출 (캐시 미스)
    response1 = await client.generate(
        prompt=unique_prompt,
        temperature=0,
        max_tokens=10,
        use_cache=True
    )
    
    # 두 번째 호출 (캐시 히트)
    response2 = await client.generate(
        prompt=unique_prompt,
        temperature=0,
        max_tokens=10,
        use_cache=True
    )
    
    # 동일한 응답 확인
    assert response1 == response2
    print("Caching test passed: responses match")

@pytest.mark.asyncio
async def test_structured_generation():
    """구조화된 응답 생성 테스트"""
    
    if not settings.OPENAI_API_KEY:
        pytest.skip("OPENAI_API_KEY not configured")
    
    client = get_llm_client("gpt-4-turbo")
    
    prompt = "Generate a simple business metric"
    response_format = {
        "metric": "string",
        "value": "number",
        "unit": "string"
    }
    
    response = await client.generate_structured(
        prompt=prompt,
        response_format=response_format,
        temperature=0.5
    )
    
    assert isinstance(response, dict)
    assert "metric" in response or "error" in response
    
    print(f"Structured response: {response}")

@pytest.mark.asyncio
async def test_token_counting():
    """토큰 카운팅 테스트"""
    
    client = get_llm_client("gpt-4-turbo")
    
    test_text = "This is a test sentence for token counting."
    token_count = client.count_tokens(test_text)
    
    assert token_count > 0
    assert token_count < 100  # 간단한 문장은 100토큰 미만
    
    print(f"Token count for '{test_text}': {token_count}")

@pytest.mark.asyncio
async def test_batch_generation():
    """배치 생성 테스트"""
    
    if not settings.OPENAI_API_KEY:
        pytest.skip("OPENAI_API_KEY not configured")
    
    client = get_llm_client("gpt-4-turbo")
    
    prompts = [
        "What is 1+1? Answer with just the number.",
        "What is 2+2? Answer with just the number.",
        "What is 3+3? Answer with just the number."
    ]
    
    responses = await client.batch_generate(
        prompts=prompts,
        temperature=0,
        max_tokens=10
    )
    
    assert len(responses) == 3
    assert all(response is not None for response in responses)
    
    print(f"Batch responses: {responses}")

@pytest.mark.asyncio
async def test_system_prompt():
    """시스템 프롬프트 테스트"""
    
    if not settings.OPENAI_API_KEY:
        pytest.skip("OPENAI_API_KEY not configured")
    
    client = get_llm_client("gpt-4-turbo")
    
    system_prompt = "You are a helpful assistant that always responds in Korean."
    prompt = "Say hello"
    
    response = await client.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.7,
        max_tokens=50
    )
    
    assert response is not None
    # 한글이 포함되어 있는지 확인 (간단한 체크)
    has_korean = any(ord(char) >= 0xAC00 and ord(char) <= 0xD7AF for char in response)
    
    print(f"Response with Korean system prompt: {response}")
    print(f"Contains Korean: {has_korean}")

if __name__ == "__main__":
    # 동기적으로 테스트 실행
    async def run_tests():
        print("LLM 클라이언트 테스트 시작...\n")
        
        # GPT-4 테스트
        try:
            await test_gpt4_call()
            print("✅ GPT-4 Turbo 호출 테스트 통과\n")
        except Exception as e:
            print(f"❌ GPT-4 Turbo 호출 테스트 실패: {e}\n")
        
        # Claude-3 테스트
        try:
            await test_claude_call()
            print("✅ Claude-3 Opus 호출 테스트 통과\n")
        except Exception as e:
            print(f"❌ Claude-3 Opus 호출 테스트 실패: {e}\n")
        
        # 캐싱 테스트
        try:
            await test_caching()
            print("✅ 캐싱 테스트 통과\n")
        except Exception as e:
            print(f"❌ 캐싱 테스트 실패: {e}\n")
        
        # 구조화된 생성 테스트
        try:
            await test_structured_generation()
            print("✅ 구조화된 생성 테스트 통과\n")
        except Exception as e:
            print(f"❌ 구조화된 생성 테스트 실패: {e}\n")
        
        # 토큰 카운팅 테스트
        try:
            await test_token_counting()
            print("✅ 토큰 카운팅 테스트 통과\n")
        except Exception as e:
            print(f"❌ 토큰 카운팅 테스트 실패: {e}\n")
        
        # 배치 생성 테스트
        try:
            await test_batch_generation()
            print("✅ 배치 생성 테스트 통과\n")
        except Exception as e:
            print(f"❌ 배치 생성 테스트 실패: {e}\n")
        
        # 시스템 프롬프트 테스트
        try:
            await test_system_prompt()
            print("✅ 시스템 프롬프트 테스트 통과\n")
        except Exception as e:
            print(f"❌ 시스템 프롬프트 테스트 실패: {e}\n")
        
        print("모든 테스트 완료!")
    
    asyncio.run(run_tests())