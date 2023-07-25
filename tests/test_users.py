import unittest, sys, os

sys.path.append('../ReIntern') # imports python file from parent directory
from app import app, db, User


class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register(self, name, email, password):
        return self.app.post('/register',
                             data=dict(name=name,
                                       email=email,
                                       password=password,
                                       confirm_password=password),
                             follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login',
                             data=dict(email=email,
                                       password=password),
                             follow_redirects=True)

    ###############
    #### tests ####
    ###############

    def test_valid_user_registration(self):
        response = self.register('test', 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered !', response.data)

    def test_valid_user_login(self):
        # Register a test user first
        self.register('test', 'test@example.com', 'FlaskIsAwesome')

        # Now, attempt to log in with the registered user's credentials
        response = self.login('test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back', response.data)

    def test_invalid_user_login(self):
        # Register a test user first
        self.register('test', 'test@example.com', 'FlaskIsAwesome')

        # Now, attempt to log in with incorrect credentials
        response = self.login('test@example.com', 'InvalidPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect email / password !', response.data)

if __name__ == "__main__":
    unittest.main()
