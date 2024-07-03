import csv
from app import create_app, db
from app.models import User, Competition
from app import bcrypt
import os

def read_true_values(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [int(row['y']) for row in reader]

app = create_app()

with app.app_context():
    db.create_all()
    
    # Create Users
    hashed_password = bcrypt.generate_password_hash('chem5spider').decode('utf-8')
    user1 = User(username='Banana', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('be3keeper').decode('utf-8')
    user2 = User(username='Apple', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('almdu6ler').decode('utf-8')
    user3 = User(username='Peach', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('winetas7ing').decode('utf-8')
    user4 = User(username='Grape', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash('radiant8').decode('utf-8')
    user5 = User(username='administrator', password=hashed_password)
    
    # Read true values from files
    bank_marketing_true_values = read_true_values('bank_marketing_true_values.csv')
    white_wine_true_values = read_true_values('white_wine_true_values.csv')



    white_wine_competition = Competition(
        name='White Wine Tasting',
        description='The data is related to white vinho verde wine samples, from the north of Portugal. The goal is to model wine quality based on physicochemical tests.',
        image_path='images/white_wine_tasting.png',
        true_values=white_wine_true_values,
        is_classification=False
    )

    # Create Competitions
    bank_marketing_competition = Competition(
        name='Bank Marketing',
        description='The data is related with direct marketing campaigns (phone calls) of a Portuguese banking institution. The classification goal is to predict if the client will subscribe a term deposit (variable y).',
        image_path='images/credit_card_scoring.png',
        true_values=bank_marketing_true_values,
        is_classification=True
    )
    
    db.session.add_all([user1, user2, user3, user4, user5, white_wine_competition, bank_marketing_competition])
    db.session.commit()

    # Create uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
