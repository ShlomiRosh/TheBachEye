import unittest
from datetime import datetime
from Core.runMeasurements import RunMeasurements


class TestRunMeasurements(unittest.TestCase):

    def test_init(self):
        # test success call for init
        m_result = ['1', 2]
        rm = RunMeasurements(m_result,None)
        self.assertIsInstance(rm.measurements, cls=type(m_result))
        self.assertEqual(rm.measurements, m_result)


if __name__ == '__main__':
    unittest.main()
