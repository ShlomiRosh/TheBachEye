import unittest
from unittest.mock import patch
from Services import healthChecksService


class TestHealthChecksService(unittest.TestCase):

    def test_check_is_alive(self):
        with patch('requests.head') as mocled_head:
            # test success call
            mocled_head.return_value.ok = True
            result = healthChecksService.check_is_alive()
            self.assertEqual(result, {'is_server_alive': True})

            # test failure call
            mocled_head.return_value.ok = False
            result = healthChecksService.check_is_alive()
            self.assertEqual(result, {'is_server_alive': False})

    def test_check_if_program_installed(self):
        real_program = 'manycam'
        fake_program = 'blabla'

        # test success call
        result = healthChecksService.check_if_program_installed(real_program)
        self.assertEqual(result, {f'is_{real_program}_installed': True})

        # test failure call
        result = healthChecksService.check_if_program_installed(fake_program)
        self.assertEqual(result, {f'is_{fake_program}_installed': False})

    def test_check_if_process_is_running(self):
        real_process = 'manycam'
        fake_process = 'blabla'

        # test success call
        result = healthChecksService.check_if_process_is_running(real_process)
        self.assertEqual(result, {f'is_{real_process}_running': True})

        # test failure call
        result = healthChecksService.check_if_process_is_running(fake_process)
        self.assertEqual(result, {f'is_{fake_process}_running': False})

    def test_get_program(self):
        real_program = 'ManyCam.exe'
        fake_program = 'blabla.exe'

        # test success call
        result = healthChecksService.get_program(real_program)
        self.assertTrue(result)

        # test failure call
        result = healthChecksService.get_program(fake_program)
        self.assertIsNone(result)

    def test_check_camera_source(self):
        # test success call
        result = healthChecksService.check_camera_source()
        self.assertEqual(result, {'camera_source': True})

    def test_run_health_checks(self):
        # test success health checks calls
        expected_result = [{'is_zoom_installed': False},
                           {'is_manycam_installed': True},
                           {'is_manycam_running': True},
                           {'is_server_alive': True},
                           {'camera_source': True}]
        with patch('requests.head') as mocled_head:
            # test success call
            mocled_head.return_value.ok = True
            result = healthChecksService.run_health_checks()
            self.assertTrue(result[3]['is_server_alive'])
            self.assertEqual(result, expected_result)

            # test failure call
            mocled_head.return_value.ok = False
            result = healthChecksService.run_health_checks()
            self.assertFalse(result[3]['is_server_alive'])
            self.assertNotEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
