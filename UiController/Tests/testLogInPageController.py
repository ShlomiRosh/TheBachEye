import unittest
from UiController import logInPageController as lc


class TestLoginPageController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_check_validation_password(self):
        print('test_check_validation_password')
        self.lc = lc.LoginController('', '123456789')
        res = self.lc.check_validation()
        self.assertEqual(res['Password'], 'Password cannot be empty.\n')

        self.lc = lc.LoginController('רא', '123456789')
        res = self.lc.check_validation()
        self.assertEqual(res['Password'], 'Password not in ascii.\n')

        self.lc = lc.LoginController('123', '123456789')
        res = self.lc.check_validation()
        self.assertEqual(res['Password'], '')

    def test_check_validation_code(self):
        print('test_check_validation_code')
        self.lc = lc.LoginController('123', '')
        res = self.lc.check_validation()
        self.assertEqual(res['Class Code'], 'Class Code cannot be empty.\n')

        self.lc = lc.LoginController('123', 'שדג')
        res = self.lc.check_validation()
        self.assertEqual(res['Class Code'], 'Class Code not in ascii.\n')

        self.lc = lc.LoginController('123', '123456789')
        res = self.lc.check_validation()
        self.assertEqual(res['Class Code'], '')


if __name__ == '__main__':
    unittest.main()
