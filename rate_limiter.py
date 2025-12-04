"""
Rate Limiter - Controls API request rate with exponential backoff
"""

import time
from collections import deque
from typing import Optional
import threading


class RateLimiter:
    """Thread-safe rate limiter with exponential backoff"""
    
    def __init__(self, max_requests: int = 60, time_window: int = 60):
        """
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds (default: 60s per minute)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.lock = threading.Lock()
        self.retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff seconds
    
    def acquire(self, retry_count: int = 0) -> bool:
        """
        Acquire permission to make a request.
        Blocks if rate limit would be exceeded.
        
        Args:
            retry_count: Current retry attempt number
        
        Returns:
            True if request can proceed
        """
        with self.lock:
            now = time.time()
            
            # Remove old requests outside time window
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()
            
            # Check if we're at limit
            if len(self.requests) >= self.max_requests:
                # Calculate wait time
                oldest_request = self.requests[0]
                wait_time = (oldest_request + self.time_window) - now
                
                # Add exponential backoff if this is a retry
                if retry_count > 0:
                    backoff_index = min(retry_count - 1, len(self.retry_delays) - 1)
                    wait_time += self.retry_delays[backoff_index]
                
                if wait_time > 0:
                    print(f"⏳ Rate limit reached. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    return self.acquire(retry_count)  # Try again
            
            # Record this request
            self.requests.append(now)
            return True
    
    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        with self.lock:
            now = time.time()
            # Remove old requests
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()
            
            current_count = len(self.requests)
            return {
                "current_requests": current_count,
                "max_requests": self.max_requests,
                "usage_percent": (current_count / self.max_requests * 100) if self.max_requests > 0 else 0,
                "time_window": self.time_window
            }
    
    def reset(self):
        """Reset the rate limiter"""
        with self.lock:
            self.requests.clear()


# Global rate limiter instance
# Gemini 2.5 Flash: 60 requests per minute
rate_limiter = RateLimiter(max_requests=60, time_window=60)
