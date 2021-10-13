import unittest
from UiController import healthCheckPageController as hc


class TestHealthCheckPageController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.hc = hc.HealthCheckPageController()

    def tearDown(self):
        print('tearDown\n')

    def test_get_health_map(self):
        print('test_get_health_map')
        res = self.hc.get_health_map()
        self.assertEqual(res, {'zoom installed'.upper(): True, 'manycam installed'.upper(): True,
            'manycam running'.upper(): True, 'alive'.upper(): True, 'camera source'.upper(): True,
            'sound ok'.upper(): True})

    def test_is_ready(self):
        print('test_is_ready')
        res = self.hc.is_ready()
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
