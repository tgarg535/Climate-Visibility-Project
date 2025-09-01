import numpy as np
import pandas as pd
import pickle
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
from src.logger import logging
from src.utils.main_utils import MainUtils



def evaluate_model(clf, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """Evaluate the regression model and return the evaluation metrics."""
    try:

        y_pred = clf.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        metrics_dict = {
            'mse': mse,
            'mae': mae,
            'r2': r2
        }
        logging.info('Model evaluation metrics calculated')
        logging.info('Metrics: %s', metrics_dict)
        return metrics_dict
    except Exception as e:
        logging.error('Error during model evaluation: %s', e)
        raise


def save_metrics(metrics: dict, file_path: str) -> None:
    """Save the evaluation metrics to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logging.info('Metrics saved to %s', file_path)
    except Exception as e:
        logging.error('Error occurred while saving the metrics: %s', e)
        raise




def main():
    try:
        clf = MainUtils.load_object('models/trained_model.pkl')
        test_data = MainUtils.load_object('./data/interim/test_processed.pkl')

        X_test = test_data[:, 1:] 
        y_test = test_data[:, 0] 

        metrics = evaluate_model(clf, X_test, y_test)
        
        # Save metrics locally
        save_metrics(metrics, 'reports/metrics.json')
        

    except Exception as e:
        logging.error('Failed to complete the model evaluation process: %s', e)
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
