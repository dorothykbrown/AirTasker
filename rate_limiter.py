from datetime import datetime, timedelta
from typing import Any, Dict, Union

class RateLimiter:
    def __init__(self, max_requests, time_interval_secs):
        self.max_requests = max_requests
        self.time_interval = timedelta(seconds=time_interval_secs)
        self.request_times_dict: Dict[str, Any] = {}
        
    def make_request(self, request_ip: str):
        current_time = datetime.now()
        
        self.request_times_dict.setdefault(request_ip, [])

        request_times = self.update_request_window(
            current_time=current_time,
            request_times=self.request_times_dict[request_ip]
        )

        if len(request_times) >= self.max_requests:
            seconds_to_retry = self.calculate_seconds_to_retry(request_times)
            return f"429 - Rate limit exceeded. Try again in {seconds_to_retry} seconds"
        else:
            request_times.append(current_time)
            self.request_times_dict[request_ip] = request_times
            return "Request processed"

    def make_request_figma_strategy(self, request_ip: str):
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        self.request_times_dict.setdefault(request_ip, {current_time: 0})

        user_requests = self.update_request_window(
            current_time=current_time,
            request_times=self.request_times_dict[request_ip]
        )

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

    def update_request_window(self, current_time: datetime, request_times: Union[list, dict]) -> list:

        if type(request_times) == list:
            for time in request_times:
                if current_time - time <= self.time_interval:
                    break
                else:
                    request_times.remove(time)
        else:
            for timestamp in sorted(request_times):

                if current_time - timestamp <= self.time_interval:
                    break
                else:
                    del request_times[timestamp]

        return request_times