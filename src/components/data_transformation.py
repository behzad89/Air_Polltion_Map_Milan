import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from feature_engine.datetime import DatetimeFeatures
from feature_engine.creation import CyclicalFeatures
from sklearn.preprocessing import MinMaxScaler
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
    date_feature_generator_obj_file_path = os.path.join("Artifacts","date_feature_generator.pkl")


class DataTransformation():
    def __init__(self,pollen_type:str):
        self.data_transformation_config = DataTransformationConfig()
        self.pollen_type = pollen_type

    def get_date_fearure_object(self):
        try:
            DATE_FTS = cns.pollen[self.pollen_type]["features"][0]
            date_pipeline = Pipeline(steps=[
                        ("dtfs", DatetimeFeatures(
                                variables=DATE_FTS,
                                features_to_extract=["quarter", "week", "month", "day_of_year"],
                                drop_original=True)),
                        ('cyclical', CyclicalFeatures(
                                variables=["datetime_quarter", "datetime_week", "datetime_month", "datetime_day_of_year"],
                                drop_original = True))
                ])
            
            logging.info("Temporal features were created")
            return date_pipeline
            
        except Exception as e:
            raise CustomException(e,sys)
        

    def get_data_transformer_object(self):
        try:
            NUM_FTS = cns.pollen[self.pollen_type]["features"][3:]
            

            num_pipeline = Pipeline(
                steps=[
                    ("scaler", MinMaxScaler()),
                    ]
                )
            processor = ColumnTransformer([("num_pipeline", num_pipeline, NUM_FTS)])
            logging.info("Data was standardized")

            return processor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def data_treansformation(self, train_path:str, test_path:str):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train & test data into dataframe")

            logging.info("Obtaning preprocessing object")
            date_obj = self.get_date_fearure_object()
            preprocessing_obj = self.get_data_transformer_object()
            

            TARGET_COL = cns.pollen[self.pollen_type]["type"]
            STAT_COL = cns.pollen[self.pollen_type]["stats"]

            input_feature_train_df=train_df.drop(columns=[TARGET_COL],axis=1)
            target_feature_train_df=train_df[TARGET_COL]

            input_feature_test_df=test_df.drop(columns=[TARGET_COL],axis=1)
            target_feature_test_df=test_df[TARGET_COL]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

            stats_feature_train_arr=input_feature_train_df[STAT_COL].values
            date_feature_train_arr=date_obj.fit_transform(input_feature_train_df).iloc[:,-8:].values
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)

            stats_feature_test_arr=input_feature_test_df[STAT_COL].values
            date_feature_test_arr=date_obj.transform(input_feature_test_df).iloc[:,-8:]
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)


            train_arr = np.c_[input_feature_train_arr, stats_feature_train_arr,date_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,stats_feature_test_arr, date_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj)
            
            save_object(file_path=self.data_transformation_config.date_feature_generator_obj_file_path,
                        obj=date_obj)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
                self.data_transformation_config.date_feature_generator_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)