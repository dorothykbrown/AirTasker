from datetime import datetime, timedelta
from typing import Any, Dict

class RateLimiter:
    def __init__(self, max_requests, time_interval_secs):
        self.max_requests = max_requests
        self.time_interval = timedelta(seconds=time_interval_secs)
        self.request_times_dict: Dict[str, Any] = {}
        
    def make_request(self, request_ip: str):
        current_time = datetime.now()
        
        self.request_times_dict.setdefault(request_ip, [])

        request_times = [time for time in self.request_times_dict[request_ip] if current_time - time < self.time_interval]

        self.request_times_dict[request_ip] = request_times

        if len(request_times) >= self.max_requests:
            seconds_to_retry = self.calculate_seconds_to_retry(request_times)
            return f"429 - Rate limit exceeded. Try again in {seconds_to_retry} seconds"
        else:
            self.request_times_dict[request_ip].append(current_time)
            return "Request processed"

    def make_request_figma_strategy(self, request_ip: str):
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        self.request_times_dict.setdefault(request_ip, {current_time: 0})

        # for every minute, add timestamp: num requests to request dict for that user
        user_requests = {
            timestamp: num_requests
            for timestamp, num_requests in self.request_times_dict[request_ip].items()
            if current_time - timestamp < self.time_interval
        }

        if sum(user_requests.values()) >= self.max_requests:
            seconds_to_retry = self.calculate_seconds_to_retry(sorted(user_requests))
            return f"429 - Rate limit exceeded. Try again in {seconds_to_retry} seconds"
        else:
            user_requests[current_time] += 1
            self.request_times_dict[request_ip] = user_requests
            return "Request processed"

    def calculate_seconds_to_retry(self, request_times: list) -> int:
        earliest_request_time_within_time_limit = request_times[0]
        next_possible_request_time = earliest_request_time_within_time_limit + self.time_interval
        seconds_to_retry = (next_possible_request_time - datetime.now()).seconds

        return seconds_to_retry