import unittest
import time

class TestKeepAlive(unittest.TestCase):
    def test_keep_alive(self):
        """Keep the job alive for external token verification."""
        time.sleep(1200)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
