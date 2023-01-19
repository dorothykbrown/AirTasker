import unittest
from rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):

    def test_rate_limiter(self):
        ONE_HOUR_IN_SECONDS = 60 * 60
        MAX_REQUESTS_PER_HOUR = 100
        
        limiter = RateLimiter(MAX_REQUESTS_PER_HOUR, ONE_HOUR_IN_SECONDS)

        request_ip1 = "ip address 1"

        for i in range(MAX_REQUESTS_PER_HOUR):
            self.assertEqual(limiter.make_request(request_ip1), "Request processed", "Request should be processed")
        self.assertEqual(limiter.make_request(request_ip1), "Rate limit exceeded. Try again", "Request should not be processed")

if __name__ == '__main__':
    unittest.main()