"""
Rate Limiter for API calls
Prevents rate limit errors by controlling request frequency
"""

import asyncio
import time
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket algorithm based rate limiter
    """
    
    def __init__(
        self, 
        requests_per_minute: int = 10,
        tokens_per_minute: int = 10000,
        burst_size: int = 5
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests per minute
            tokens_per_minute: Maximum tokens per minute
            burst_size: Maximum burst requests allowed
        """
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute
        self.burst_size = burst_size
        
        # Request tracking
        self.request_times = []
        self.token_usage = []
        
        # Lock for thread safety
        self.lock = asyncio.Lock()
        
    async def acquire(self, estimated_tokens: int = 1000):
        """
        Acquire permission to make API call
        
        Args:
            estimated_tokens: Estimated tokens for this request
        """
        async with self.lock:
            current_time = time.time()
            
            # Clean old entries (older than 1 minute)
            self.request_times = [
                t for t in self.request_times 
                if current_time - t < 60
            ]
            self.token_usage = [
                (t, tokens) for t, tokens in self.token_usage 
                if current_time - t < 60
            ]
            
            # Check request rate
            if len(self.request_times) >= self.requests_per_minute:
                # Calculate wait time
                oldest_request = self.request_times[0]
                wait_time = 60 - (current_time - oldest_request) + 1
                
                if wait_time > 0:
                    logger.warning(f"Rate limit approaching, waiting {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
                    return await self.acquire(estimated_tokens)
            
            # Check token rate
            total_tokens = sum(tokens for _, tokens in self.token_usage)
            if total_tokens + estimated_tokens > self.tokens_per_minute:
                # Calculate wait time based on token usage
                if self.token_usage:
                    oldest_token_time = self.token_usage[0][0]
                    wait_time = 60 - (current_time - oldest_token_time) + 1
                    
                    if wait_time > 0:
                        logger.warning(f"Token limit approaching, waiting {wait_time:.1f}s")
                        await asyncio.sleep(wait_time)
                        return await self.acquire(estimated_tokens)
            
            # Record this request
            self.request_times.append(current_time)
            self.token_usage.append((current_time, estimated_tokens))
            
            # Add small delay to prevent burst
            if len(self.request_times) > self.burst_size:
                await asyncio.sleep(60 / self.requests_per_minute)
    
    def reset(self):
        """Reset rate limiter state"""
        self.request_times = []
        self.token_usage = []


# Global rate limiters for different APIs
claude_rate_limiter = RateLimiter(
    requests_per_minute=5,  # Conservative limit for Claude
    tokens_per_minute=5000,
    burst_size=2
)

openai_rate_limiter = RateLimiter(
    requests_per_minute=20,  # Higher limit for OpenAI
    tokens_per_minute=40000,
    burst_size=10
)