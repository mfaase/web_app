import unittest
from app import create_app, db
from app.models import User, Competition, Submission
from app import bcrypt

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            hashed_password = bcrypt.generate_password_hash('password1').decode('utf-8')
            user1 = User(username='Banana', password=hashed_password)
            credit_card_true_values = [25000, 36000, 12000, 50000, 10000, 23000]
            competition1 = Competition(name='Credit Card Scoring', true_values=credit_card_true_values, is_classification=False)

            db.session.add(user1)
            db.session.add(competition1)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_logout(self):
        with self.client:
            response = self.client.post('/login', data=dict(username='Banana', password='password1'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Competitions', response.data)

            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_competition_page(self):
        with self.client:
            self.client.post('/login', data=dict(username='Banana', password='password1'), follow_redirects=True)
            response = self.client.get('/competition/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Leaderboard - Credit Card Scoring', response.data)

    def test_file_upload(self):
        with self.client:
            self.client.post('/login', data=dict(username='Banana', password='password1'), follow_redirects=True)
            data = {
                'file': (open('tests/credit_card_predictions.csv', 'rb'), 'credit_card_predictions.csv')
            }
            response = self.client.post('/competition/1', data=data, content_type='multipart/form-data', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File successfully uploaded and scored', response.data)

if __name__ == '__main__':
    unittest.main()
