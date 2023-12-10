import pandas as pd
import os, sys
from src.utils import CustomTrainTestSplit
from src.exception import CustomException
from src.logger import logging
import src.constants as cns
from src.components.data_transformation import DataTransformation
from dataclasses import dataclass



@dataclass
class DataIngestionConfig():
    train_data_path = os.path.join("Artifacts","train.csv")
    test_data_path = os.path.join("Artifacts","test.csv")
    raw_data_path = os.path.join("Artifacts","raw.csv")


class DataIngestion():
    def __init__(self,pollen_type: str) -> str:
        self.ingestion_config = DataIngestionConfig()
        self.pollen_type = pollen_type

    def initiate_data_ingestion(self) -> str:
        logging.info("Start the data ingestion")
        try:
            df = pd.read_csv("../../pochas_result/pollen/04_with_Outliers_pollen_feat_2000_2019.csv", parse_dates=["datetime"], usecols=cns.pollen[self.pollen_type]["features"]) # Since there was some personal info, I decided not use exact path
            logging.info("Read the datasets as dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            stat_pollen = pd.read_csv("../../pochas_result/pollen/03_pollen_daily_stats.csv",parse_dates=["datetime"], usecols=cns.pollen[self.pollen_type]["stats"] + ["datetime"])
            df = df.merge(stat_pollen, left_on="datetime", right_on="datetime").dropna(subset=[cns.pollen[self.pollen_type]["type"]]).reset_index(drop=True)
            logging.info("Pollen country-wide data was merged to dataframe")
            df['PollenSeason'] = df['datetime'].apply(lambda x: 1 if x.month >= cns.pollen[self.pollen_type]["season_start"]  and x.month <= cns.pollen[self.pollen_type]["season_end"] else 0)
            logging.info(f"Pollen Season Column was created for {self.pollen_type}")
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info(f"Train-test split initiated for {self.pollen_type} pollen")
            train_set, test_set = CustomTrainTestSplit(df,test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info(f"Ingestion of the data is completed for {self.pollen_type}")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
     obj = DataIngestion("birch")
     train_data, test_data = obj.initiate_data_ingestion()

     data_transformation = DataTransformation("birch")
     a,b,c = data_transformation.data_treansformation(train_data,test_data)
     print(a.shape)

