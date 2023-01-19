from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests, time_interval_secs):
        self.max_requests = max_requests
        self.time_interval = timedelta(seconds=time_interval_secs)
        self.request_times_dict = {}
        
    def make_request(self, request_ip):
        current_time = datetime.now()
        
        self.request_times_dict.setdefault(request_ip, [])

        request_times = [time for time in self.request_times_dict[request_ip] if current_time - time < self.time_interval]

        self.request_times_dict[request_ip] = request_times

        if len(request_times) >= self.max_requests:
            return "429 - Rate limit exceeded. Try again"
        else:
            self.request_times_dict[request_ip].append(current_time)
            return "Request processed"
