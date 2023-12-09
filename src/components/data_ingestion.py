import pandas as pd
import os, sys
from src.utils import CustomTrainTestSplit
from src.exception import CustomException
from src.logger import logging
import src.constants as cns
from dataclasses import dataclass


@dataclass
class DataIngestionConfig():
    train_data_path: str = os.path.join("Data","train.csv")
    test_data_path: str = os.path.join("Data","test.csv")
    raw_data_path: str = os.path.join("Data","raw.csv")


class DataIngestion:
    def __init__(self) -> str:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, pollen_type: str) -> str:
        logging.info("Enter the data ingestion method or component")
        try:
            df = pd.read_csv("../../pochas_result/pollen/04_with_Outliers_pollen_feat_2000_2019.csv", parse_dates=["datetime"], usecols=cns.pollen[pollen_type]["features"]) # Since there was some personal info, I decided not use exact path
            logging.info("Read the datasets as dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            stat_pollen = pd.read_csv("../../pochas_result/pollen/03_pollen_daily_stats.csv",parse_dates=["datetime"], usecols=cns.pollen[pollen_type]["stats"])
            df = df.merge(stat_pollen, left_on="datetime", right_on="datetime").dropna(subset=[cns.pollen[pollen_type]["type"]]).reset_index(drop=True)
            logging.info("Pollen country-wide data was merged to dataframe")
            df['PollenSeason'] = df['datetime'].apply(lambda x: 1 if x.month >= cns.pollen[pollen_type]["season_start"]  and x.month <= cns.pollen[pollen_type]["season_end"] else 0)
            logging.info(f"Pollen Season Column was created for {pollen_type}")
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info(f"Train-test split initiated for {pollen_type} pollen")
            train_set, test_set = CustomTrainTestSplit(df,test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of the data is completed")

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        except Exception as e:
            raise CustomException(e,sys)

    