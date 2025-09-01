# data ingestion
import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
from src.data_access.visibility_data import ProjData
from src.constants import COLLECTION_NAME 
from src.utils.main_utils import MainUtils

import os
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import MyException
import sys


    

def fetch_data(collection_name: str) -> pd.DataFrame:
    """Fetch data from the MongoDB collection."""
    try:
        proj_data = ProjData()
        df = proj_data.export_collection_as_dataframe(collection_name=collection_name)
        return df
    except Exception as e:
        logging.error('Failed to fetch data from MongoDB: %s', e)
        raise MyException(e, sys)
    

def drop_schema_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Drop schema columns from the DataFrame."""
    try:
        proj_data = ProjData()
        df = proj_data.drop_schema_columns(dataframe)
        logging.info('Schema columns dropped successfully')
        return df
    except Exception as e:
        logging.error('Failed to drop schema columns: %s', e)
        raise MyException(e, sys)
    

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logging.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise MyException(e, sys)

def main():
    try:

        params = MainUtils.load_params(params_path='.config/params.yaml')
        test_size = params['data_ingestion']['test_size']
        # test_size = 0.2

        #use this when not using external source like mongodb or aws
        # df = load_data(data_url='https://github.com/PWskills-DataScienceTeam/Climate-Visibility/blob/main/notebooks/data.csv?raw=true')

        df = fetch_data(collection_name=COLLECTION_NAME)
        df = drop_schema_columns(df)

         # Split the data into training and testing sets
        train_data, test_data = train_test_split(df, test_size=test_size, random_state=42)
        save_data(train_data, test_data, data_path='./data')

    except Exception as e:
        logging.error('Failed to complete the data ingestion process: %s', e)
        raise MyException(e, sys)

if __name__ == '__main__':
    main()