import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, f1_score

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filepath, competition):
    delimiters = [',', ';', '\t', ' ']
    for delimiter in delimiters:
        try:
            df = pd.read_csv(filepath, delimiter=delimiter)
            if 'prediction' not in df.columns:
                df.columns = ['prediction']
            predictions = df['prediction']
            if len(predictions) != len(competition.true_values):
                raise ValueError('The number of predictions does not match the number of true values.')
            return True
        except Exception as e:
            continue
    return False

def calculate_score(filepath, competition):
    delimiters = [',', ';', '\t', ' ']
    for delimiter in delimiters:
        try:
            df = pd.read_csv(filepath, delimiter=delimiter)
            if 'prediction' not in df.columns:
                df.columns = ['prediction']
            predictions = df['prediction']
            if competition.is_classification:
                true_values = competition.true_values
                score = f1_score(true_values, predictions, average='weighted')
            else:
                score =  mean_squared_error(y_true=np.array(true_values, dtype=np.float32), y_pred=np.array(predictions.to_list(), dtype=np.float32))
            return score
        except Exception as e:
            continue
    raise ValueError('Could not process the file to calculate the score.')
