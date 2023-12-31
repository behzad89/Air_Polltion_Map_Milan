import pandas as pd
from sklearn.metrics import r2_score
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
import os,sys
from src.exception import CustomException
import dill
import src.constants as cns
from sklearn.model_selection import GridSearchCV, KFold, GroupKFold, train_test_split

def CustomTrainTestSplit(pollen_data: pd.DataFrame, test_size: float=0.2) -> pd.DataFrame:
    """
    - We iterate through each unique station name.
    - For each station, we split the data into pollen season and not pollen season samples.
    - We ensure that we select the same number of pollen season (1) and not pollen season (0) samples from each station for the test dataset.
    - 20% of the entire dataset is used for testing, and the remaining 80% will be used for training

    This approach guarantees that you have an equal number of pollen season and not pollen season samples for each station in your test dataset.
    """
    try:
        test_data = pd.DataFrame(columns=pollen_data.columns).dropna(axis=1, how='all', inplace=True)

        # Iterate through unique station names
        for station in pollen_data['Name_stati'].unique():
            # Split the data for the current station into pollen season and not pollen season
            station_data = pollen_data[pollen_data['Name_stati'] == station]
            pollen_season_data = station_data[station_data['PollenSeason'] == 1]
            not_pollen_season_data = station_data[station_data['PollenSeason'] == 0]

            # Determine the number of samples to include from each category for the test dataset
            min_samples = min(len(pollen_season_data), len(not_pollen_season_data))
            max_samples = max(len(pollen_season_data), len(not_pollen_season_data))
            test_size_pollen_season_samples = int(test_size * max_samples)
            test_size_not_pollen_season_samples = int(test_size * min_samples)

            # Randomly select samples from both categories for the test dataset
            pollen_season_samples = pollen_season_data.sample(n=test_size_pollen_season_samples, random_state=42)
            not_pollen_season_samples = not_pollen_season_data.sample(n=test_size_not_pollen_season_samples, random_state=42)

            # Concatenate the selected samples to the test dataset
            test_data = pd.concat([test_data, pollen_season_samples, not_pollen_season_samples], ignore_index=True)

        # The test_data DataFrame now contains 30% of the entire dataset for testing with the same number of pollen season and not pollen season samples for each station
        # You can obtain the training data by excluding the test data
        train_data = pollen_data.drop(index=test_data.index)

        return train_data, test_data
    
    except Exception as e:
        raise CustomException(e, sys)


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
  

    def evaluate_model(X_train: pd.DataFrame, y_train:pd.DataFrame,X_test:pd.DataFrame,y_test:pd.DataFrame,models:dict):
        try:
            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]

                model_pipline = Pipeline(steps=[
                    ('feature_selection', SelectFromModel(model(random_state=42))),
                    ('Regressor', model(random_state=42))
                ])

                grid_search = GridSearchCV(estimator=model_pipline, param_grid=cns.params[list(models.keys())[i]], 
                                           cv=?????, scoring='neg_root_mean_squared_error',n_jobs=100)

                y_train_pred = grid_search.predict(X_train)
                y_test_pred = grid_search.predict(X_test)

                train_model_score = r2_score(y_train,y_train_pred)
                test_model_score = r2_score(y_test,y_test_pred)

                report[list(models.key()[i])] = test_model_score
            return report

        except Exception as e:
            raise CustomException(e,sys)