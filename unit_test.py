import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test database and Flask test client."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()
            # Add a test user
            hashed_password = generate_password_hash('password123', method='pbkdf2:sha256', salt_length=8)
            user = User(username='testuser', password=hashed_password)
            db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test database."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """Test the registration of a new user."""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration

        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.username, 'newuser')

    def test_login(self):
        """Test user login."""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on successful login

    def test_login_invalid(self):
        """Test invalid login credentials."""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertIn(b'Invalid username or password', response.data)

    def test_upload_image_with_login(self):
        """Test image upload after login."""
        # Login first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        # Simulate an image upload
        with open('ISIC_0031309.jpg', 'rb') as img:
            response = self.client.post('/upload', data={
                'file': (img, 'test_image.jpg')
            }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detected Skin Disease', response.data)  # Check the result page

    def test_logout(self):
        """Test user logout."""
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Should redirect to index
