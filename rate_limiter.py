

class RateLimiter:
    def __init__(self, max_requests, time_interval):
        self.max_requests = max_requests
        self.time_interval = time_interval
        self.request_times_dict = {}
        
    def make_request(self, request_ip):
        pass
