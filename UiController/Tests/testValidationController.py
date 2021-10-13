import unittest
from UiController import validationController as vc


class TestValidationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.vc = vc.ValidationController()

    def tearDown(self):
        print('tearDown\n')

    def test_check_email(self):
        print('test_check_email')
        res = self.vc.check_email('sdfgf/@fgh')
        self.assertEqual(res, 'Invalid Email')

        res = self.vc.check_email('rshalom8@gmail.com')
        self.assertEqual(res, 'OK')

    def test_check_code(self):
        print('test_check_code')
        res = self.vc.check_code('123')
        self.assertEqual(res, 'Code need to be in len: 6.')

        res = self.vc.check_code('123asd')
        self.assertEqual(res, 'Code need to be only numbers.')

        res = self.vc.check_code('123456')
        self.assertEqual(res, 'This is not the correct code.')

        res = self.vc.check_code(str(self.vc.code))
        self.assertEqual(res, 'OK')

    def test_send_validation_email(self):
        print('test_send_validation_email')
        res = self.vc.send_validation_email('rshalom8@gmail.com')
        self.assertEqual(res, True)

        res = self.vc.send_validation_email('qwe')
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()
