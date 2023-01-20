from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests, time_interval_secs):
        self.max_requests = max_requests
        self.time_interval = timedelta(seconds=time_interval_secs)
        self.request_times_dict = {}
        
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

    def calculate_seconds_to_retry(self, request_times: list) -> int:
        earliest_request_time_within_time_limit = request_times[0]
        next_possible_request_time = earliest_request_time_within_time_limit + self.time_interval
        seconds_to_retry = (next_possible_request_time - datetime.now()).seconds

        return seconds_to_retry