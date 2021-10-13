import unittest
from EmailMessagingSystem import emailSystem as es


class TestEmailSystem(unittest.TestCase):

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

    def test_send_email_correctly(self):
        print('test_send_email_correctly')
        res1 = es.EmailSystem().send_email('hi' ,'abra cadabra', 'abra@cadabra.com')
        self.assertEqual(res1, True)

    def test_send_email_numbers(self):
        print('test_send_email_numbers')
        res2 = es.EmailSystem().send_email('vat', 'abra cadabra', '1234')
        self.assertEqual(res2, False)


if __name__ == '__main__':
    unittest.main()
