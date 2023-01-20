import unittest
import time
from rate_limiter import RateLimiter
from datetime import datetime, timedelta

class TestRateLimiter(unittest.TestCase):

    def test_rate_limiter(self):
        MAX_REQUESTS_PER_HOUR = 100
        ONE_HOUR_IN_SECONDS = 60 * 60
        
        limiter = RateLimiter(MAX_REQUESTS_PER_HOUR, ONE_HOUR_IN_SECONDS)

        request_ip1 = "ip address 1"

        for i in range(MAX_REQUESTS_PER_HOUR):
            self.assertEqual(limiter.make_request(request_ip1), "Request processed", "Request should be processed")

        earliest_request_time_within_hour = limiter.request_times_dict[request_ip1][0]
        next_possible_request_time = earliest_request_time_within_hour + timedelta(seconds=ONE_HOUR_IN_SECONDS)
        seconds_to_retry = (next_possible_request_time - datetime.now()).seconds

        self.assertEqual(limiter.make_request(request_ip1), f"429 - Rate limit exceeded. Try again in {seconds_to_retry} seconds", "Request should not be processed")


if __name__ == '__main__':
    unittest.main()