import csv
from app import create_app, db
from app.models import User, Competition
from app import bcrypt
import os

def read_true_values(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [int(row['true_values']) for row in reader]

app = create_app()

with app.app_context():
    db.create_all()
    
    # Create Users
    hashed_password = bcrypt.generate_password_hash('password1').decode('utf-8')
    user1 = User(username='Banana', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('password2').decode('utf-8')
    user2 = User(username='Apple', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('password3').decode('utf-8')
    user3 = User(username='Peach', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('password4').decode('utf-8')
    user4 = User(username='Grape', password=hashed_password)
    
    # Read true values from files
    credit_card_true_values = read_true_values('credit_card_true_values.csv')
    titanic_true_values = read_true_values('titanic_true_values.csv')

    # Create Competitions
    credit_card_competition = Competition(
        name='Credit Card Scoring',
        description='Predict the credit card scores.',
        image_path='images/credit_card_scoring.png',
        true_values=credit_card_true_values,
        is_classification=False
    )

    titanic_classification_competition = Competition(
        name='Titanic Classification',
        description='Classify the survival status on the Titanic.',
        image_path='images/titanic_classification.png',
        true_values=titanic_true_values,
        is_classification=True
    )
    
    db.session.add_all([user1, user2, user3, user4, credit_card_competition, titanic_classification_competition])
    db.session.commit()

    # Create uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
