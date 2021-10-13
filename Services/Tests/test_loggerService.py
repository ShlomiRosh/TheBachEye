import logging
import unittest
from unittest.mock import patch, mock_open

import config
from Services import loggerService


class TestHealthChecksService(unittest.TestCase):

    def test_get_logger(self):
        log_file_name = './Logs/back_eye.log'
        config.LOG_FILES['default'] = log_file_name

        # test success call for get logger
        result = loggerService.get_logger()
        self.assertIsInstance(result,cls=logging.Logger)
        self.assertEqual(result.name,log_file_name)

    def test_send_log_reports(self):
        log_file_name = './Logs/back_eye.log'
        config.LOG_FILES['default'] = log_file_name

        with patch('requests.post') as mocked_post:
            with patch("builtins.open", mock_open(read_data="MockData"), create=True):
                # test success call
                mocked_post.return_value.ok = True
                result = loggerService.send_log_reports()
                self.assertTrue(result)

                # test failure call
                mocked_post.return_value.ok = False
                result = loggerService.send_log_reports()
                self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
