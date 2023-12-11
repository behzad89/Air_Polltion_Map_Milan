import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.linear_model import (Ridge, ElasticNet, Lasso)

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model
from dataclasses import dataclass
import os, sys



@dataclass
class ModelTrainConfig:
    train_model_file_path = os.path.join("Artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainConfig()

    def initiate_model_trainer(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        try:
            X_train, y_train, X_test, y_test = train_df.iloc[:,:-1], train_df.iloc[:,-1], test_df.iloc[:,:-1], test_df.iloc[:,-1]
            logging.info("Split train and test input data")

            models ={
                "Random Forest": RandomForestRegressor(),
                "XGBoost": XGBRegressor(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "Elastic net": ElasticNet()
            }


            #  model_report = evaluate_model(X_train, y_train, X_test, y_test, models=models)

            logging.info("Trained models")

            # save_object(file_path=self.model_trainer_config.train_model_file_path, )

        except:
            pass