import unittest, sys

sys.path.append('../ReIntern') # imports python file from parent directory
from app import app 
from test_users import UsersTests

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to ReIntern', response.data)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Sign Up', response.data)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Login', response.data)


    def test_calendar_page(self):
        response = self.app.get('/calendar_display', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Calendar', response.data)

    def test_wiki_page(self):
        response = self.app.get('/wiki', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wiki', response.data)

    def test_settings_page(self):
        response = self.app.get('/settings', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Settings', response.data)

if __name__ == "__main__":
    unittest.main()
