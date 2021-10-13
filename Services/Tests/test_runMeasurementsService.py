import logging
import unittest
from unittest.mock import patch, mock_open

import config
from Services.runMeasurementsService import MeasurementsService


class TestRunMeasurementsService(unittest.TestCase):

    def test_init(self):
        # test success call for init function
        result = MeasurementsService()
        self.assertIsInstance(result.measurements_stack, cls=list)
        self.assertEqual(result.measurements_stack, [])

    def test_post_measurements(self):
        with patch('requests.post') as mocked_post:
            with patch("builtins.open", mock_open(read_data="MockData"), create=True):
                fake_measurements = [1,2,3]

                # test success post measurements which means the measurements_stack should be []
                mocked_post.return_value.ok = True
                ms = MeasurementsService()
                ms.post_measurements(fake_measurements)
                self.assertIsInstance(ms.measurements_stack, cls=list)
                self.assertEqual(ms.measurements_stack, [])

                # test failure post measurements which means the measurements_stack should not be []
                mocked_post.return_value.ok = False
                ms = MeasurementsService()
                ms.post_measurements(fake_measurements)
                self.assertIsInstance(ms.measurements_stack, cls=list)
                self.assertEqual(ms.measurements_stack, [fake_measurements])


if __name__ == '__main__':
    unittest.main()
