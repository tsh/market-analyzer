import time


class TokenBucket:
    def __int__(self, start_tokens, bucket_capacity, refill_rate_per_minute):
        self.bucket_capacity = bucket_capacity
        self.tokens = start_tokens
        self.refill_rate_per_minute = refill_rate_per_minute
        self.last_time = time.time()

    def is_allowed(self):
        now = time.time()
        elapsed_minutes = (now - self.last_time) / 60
        self.tokens = min(self.bucket_capacity, self.tokens + elapsed_minutes * self.refill_rate_per_minute)
        self.last_time = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False