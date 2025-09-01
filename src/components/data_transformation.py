import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from collections import namedtuple
from src.constants import *
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import MainUtils



def initiate_data_transformation():
    """
    Method Name :   initiate_data_transformation
    Description :   This method initiates the data transformation process.
    Output      :   data transformation artifact is created and returned
    On Failure  :   Write an exception log and then raise an exception
    """
    logging.info("Entered initiate_data_transformation method")
    try:
        # Load train and test data
        train_data = pd.read_csv('./data/raw/train.csv')
        test_data = pd.read_csv('./data/raw/test.csv')
        logging.info('Train and test data loaded for transformation')

        # Separate features and target
        X_train = train_data.drop(columns=[TARGET_COLUMN])
        y_train = train_data[TARGET_COLUMN]
        X_test = test_data.drop(columns=[TARGET_COLUMN])
        y_test = test_data[TARGET_COLUMN]

        # Fit and transform scaler on train, transform on test
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Save the scaler object for later use
        scaler_path = './models/scaler.pkl'
        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        MainUtils.save_object(scaler_path, scaler)
        logging.info('Scaler object saved at %s', scaler_path)

        # Combine features and target for saving
        train_arr = np.c_[X_train_scaled, np.array(y_train)]
        test_arr = np.c_[X_test_scaled, np.array(y_test)]


        return train_arr, test_arr
    except Exception as e:
        raise MyException(e, sys) 

def main():
    try:
        # Transform the data
        train_processed_data,test_processed_data = initiate_data_transformation()
        
        # Store the data inside data/processed
        data_path = os.path.join("./data", "interim")
        os.makedirs(data_path, exist_ok=True)
        MainUtils.save_object(os.path.join(data_path, "train_processed.pkl"), train_processed_data)
        MainUtils.save_object(os.path.join(data_path, "test_processed.pkl"), test_processed_data)
        logging.info('Processed data saved to %s', data_path)

    except Exception as e:
        logging.error('Failed to complete the data transformation process: %s', e)
        raise MyException(e, sys)

if __name__ == '__main__':
    main()
