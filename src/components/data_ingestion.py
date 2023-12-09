import pandas as pd
from sklearn.model_selection import train_test_split
import os, sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class DataIngestionConfig():
    train_data_path: str = os.path.join("Data","train.csv")
    test_data_path: str = os.path.join("Data","test.csv")
    raw_data_path: str = os.path.join("Data","raw.csv")


class DataIngestion:
    def __init__(self) -> str:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> str:
        logging.info("Enter the data ingestion method or component")
        try:
            df = pd.read_csv("../../pochas_result/pollen/04_with_Outliers_pollen_feat_2000_2019.csv")
            logging.info("Read the datasets as dataframe")

            # make a directory to save the file
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train-test split initiated")
            train_set, test_set = train_test_split(df,test_size=0.2, random_state=123)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of the data is completed")

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()