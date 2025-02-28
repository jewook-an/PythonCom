import unittest
from common.CeleryCm import RedisManager

class TestRedisManagerSetUp(unittest.TestCase):
    def setUp(self):
        # Use environment variable for Redis password for security
        import os
        redis_password = os.getenv('REDIS_PASSWORD', 'default_password')
        self.redis_manager = RedisManager(db=15, password=redis_password)

    def test_redis_manager_initialization(self):
        self.assertIsNotNone(self.redis_manager)
        self.assertEqual(self.redis_manager.redis_client.connection_pool.connection_kwargs['db'], 15)

    def test_redis_manager_password(self):
        import os
        redis_password = os.getenv('REDIS_PASSWORD', 'default_password')
        self.assertEqual(self.redis_manager.redis_client.connection_pool.connection_kwargs['password'], redis_password)

if __name__ == '__main__':
    unittest.main()
