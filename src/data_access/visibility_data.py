import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
from src.utils.main_utils import MainUtils

class ProjData:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fecthed with len: {len(df)}")
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df


        except Exception as e:
            raise MyException(e, sys)
        


    def drop_schema_columns(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        Method Name :   drop_schema_columns
        Description :   This method reads the schema.yml file and drops the column in th dataset based on the schema given. 
        
        Output      :   a pd.DataFrame dropping the schema columns
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:

            self.utils = MainUtils()
            _schema_config = self.utils.read_schema_config_file()
            df = dataframe.drop(columns =  _schema_config["drop_columns"])

            return df
        except Exception as e:
            raise MyException(e,sys)