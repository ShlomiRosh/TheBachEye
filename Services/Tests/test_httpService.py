import unittest
from unittest.mock import patch
from Services import httpService
from mock import mock_open


class TestHttpService(unittest.TestCase):
    def setUp(self):
        self.mocked_url = 'http://mock-url.com'
        self.mocked_success_text = 'SuccessCall'
        self.mocked_failure_text = 'FailedCall'
        self.mocked_data = 'MockData'

    def test_post(self):
        with patch('requests.post') as mocked_post:
            # test success call
            mocked_post.return_value.ok = True
            result = httpService.post(self.mocked_url, self.mocked_data)
            mocked_post.assert_called_with(self.mocked_url, json=self.mocked_data, verify=False)
            self.assertIsNotNone(result)
            self.assertTrue(result.ok)

            # test case of url is None
            result = httpService.post(None, self.mocked_data)
            self.assertIsNone(result)

            # test case of data is None
            result = httpService.post(self.mocked_url, None)
            self.assertIsNone(result)

            # test case of failure call
            mocked_post.return_value.ok = False
            result = httpService.post(self.mocked_url, self.mocked_data)
            mocked_post.assert_called_with(self.mocked_url, json=self.mocked_data,verify=False)
            self.assertFalse(result.ok)

    def test_put(self):
        with patch('requests.put') as mocked_put:
            # test success call
            mocked_put.return_value.ok = True
            result = httpService.put(self.mocked_url, self.mocked_data)
            mocked_put.assert_called_with(self.mocked_url, json=self.mocked_data, verify=False)
            self.assertIsNotNone(result)
            self.assertTrue(result.ok)

            # test case of url is None
            result = httpService.put(None, self.mocked_data)
            self.assertIsNone(result)

            # test case of data is None
            result = httpService.put(self.mocked_url, None)
            self.assertIsNone(result)

            # test case of failure call
            mocked_put.return_value.ok = False
            result = httpService.put(self.mocked_url, self.mocked_data)
            mocked_put.assert_called_with(self.mocked_url, json=self.mocked_data, verify=False)
            self.assertFalse(result.ok)

    def test_post_image_data(self):
        with patch('requests.post') as mocked_post:
            with patch("builtins.open", mock_open(read_data=self.mocked_data.encode()), create=True) as mocked_file:
                # test success call
                mocked_post.return_value.ok = True
                result = httpService.post_image_data(self.mocked_url, self.mocked_data, mocked_file)
                self.assertTrue(result)

                # test case of url is None
                result = httpService.post_image_data(None, self.mocked_data, mocked_file)
                self.assertFalse(result)

                # test case of data is None
                result = httpService.post_image_data(self.mocked_url, None, mocked_file)
                self.assertFalse(result)

                # test case of file is None
                result = httpService.post_image_data(self.mocked_url, self.mocked_data, None)
                self.assertFalse(result)

                # test case of failure call
                mocked_post.return_value.ok = False
                result = httpService.post_image_data(self.mocked_url, self.mocked_data, mocked_file)
                self.assertFalse(result)

    def test_get(self):
        with patch('requests.get') as mocked_get:
            # test success call
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = self.mocked_success_text
            result = httpService.get(self.mocked_url)
            mocked_get.assert_called_with(self.mocked_url, None, verify=False)
            self.assertEqual(result.ok, True)
            self.assertEqual(result.text, self.mocked_success_text)

            # test case of url is None
            result = httpService.get(None)
            self.assertIsNone(result)

            # test case of failure call
            mocked_get.return_value.ok = False
            mocked_get.return_value.text = self.mocked_failure_text
            result = httpService.get(self.mocked_url)
            mocked_get.assert_called_with(self.mocked_url, None, verify=False)
            self.assertEqual(result.ok, False)
            self.assertEqual(result.text, self.mocked_failure_text)

    def test_head(self):
        with patch('requests.head') as mocked_head:
            # test success call
            mocked_head.return_value.ok = True
            result = httpService.head(self.mocked_url)
            mocked_head.assert_called_with(self.mocked_url, verify=False)
            self.assertTrue(result, True)

            # test case of url is None
            result = httpService.head(None)
            self.assertFalse(result)

            # test case of failure call
            mocked_head.return_value.ok = False
            mocked_head.return_value.text = self.mocked_failure_text
            result = httpService.head(self.mocked_url)
            mocked_head.assert_called_with(self.mocked_url, verify=False)
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
