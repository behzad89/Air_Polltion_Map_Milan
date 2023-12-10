import pandas as pd
import numpy as np
from feature_engine.datetime import DatetimeFeatures
from feature_engine.creation import CyclicalFeatures
from sklearn.preprocessing import MinMaxScaler
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.pipeline import Pipeline

import sys,os
from src.exception import CustomException
import src.constants as cns
from src.utils import save_object
from src.logger import logging
from dataclasses import dataclass


@dataclass
class DataTransformationConfig():
    preprocessor_obj_file_path = os.path.join("Artifacts","preprocessor.pkl")


class DataTransformation():
    def __init__(self,pollen_type:str):
        self.data_transformation_config = DataTransformationConfig()
        self.pollen_type = pollen_type    

    def get_data_transformer_object(self):
        try:
            DATE_FTS = cns.pollen[self.pollen_type]["features"][0]
            NUM_FTS = cns.pollen[self.pollen_type]["features"][3:]
            processor = Pipeline(steps=[
                        ("dtfs", DatetimeFeatures(
                                variables=DATE_FTS,
                                features_to_extract=["quarter", "week", "month", "day_of_year"],
                                drop_original=True)),
                        ('cyclical', CyclicalFeatures(
                                variables=["datetime_quarter", "datetime_week", "datetime_month", "datetime_day_of_year"],
                                drop_original = True)),
                        ("scaler", SklearnTransformerWrapper(MinMaxScaler(), variables = NUM_FTS))
                ])

            return processor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def data_treansformation(self, train_path:str, test_path:str):
        try:
            logging.info("Data transformation started")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train & test data into dataframe")

            logging.info("Obtaning preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()
            

            TARGET_COL = cns.pollen[self.pollen_type]["type"]

            input_feature_train_df = train_df.drop(columns=[TARGET_COL],axis=1)
            target_feature_train_df = train_df[TARGET_COL]

            input_feature_test_df = test_df.drop(columns=[TARGET_COL],axis=1)
            target_feature_test_df = test_df[TARGET_COL]

            logging.info("Applying preprocessing object on train & test data")

            input_feature_train_transform = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_transform = preprocessing_obj.transform(input_feature_test_df)

            train_df_transform = pd.concat([input_feature_train_transform, target_feature_train_df], axis=1)
            test_df_transform = pd.concat([input_feature_test_transform, target_feature_test_df], axis=1)

            logging.info(f"Saved preprocessing object.")

            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj)

            return (
                train_df_transform,
                test_df_transform,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)