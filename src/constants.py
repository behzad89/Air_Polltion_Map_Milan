GRASS_FTS = [
    'datetime', 'Name_stati', 'Grasses', 'y', 'agri_area_1000m',
    'broad_leaved_forest_1000m', 'conifirous_forest_1000m',
    'grassland_1000m', 'mixed_forest_1000m', 'openSpace_1000m',
    'urban_area_1000m', 'water_area_1000m', 'agri_area_100m',
    'broad_leaved_forest_100m', 'conifirous_forest_100m', 'grassland_100m',
    'mixed_forest_100m', 'openSpace_100m', 'urban_area_100m',
    'water_area_100m', 'agri_area_2000m', 'broad_leaved_forest_2000m',
    'conifirous_forest_2000m', 'grassland_2000m', 'mixed_forest_2000m',
    'openSpace_2000m', 'urban_area_2000m', 'water_area_2000m',
    'agri_area_200m', 'broad_leaved_forest_200m', 'conifirous_forest_200m',
    'grassland_200m', 'mixed_forest_200m', 'openSpace_200m',
    'urban_area_200m', 'water_area_200m', 'windSpeed',
    'boundaryLayerHeight', 't2m', 'totalPrecipitation', 'rh',
    'windDirection', 'dem', 'NDVI', 'agri_area_10000m',
    'broad_leaved_forest_10000m', 'conifirous_forest_10000m',
    'grassland_10000m', 'mixed_forest_10000m', 'openSpace_10000m',
    'urban_area_10000m', 'water_area_10000m', 'red', 'green', 'blue', 'NIR',
    'SWIR1', 'SWIR2', 'agri_area_500m', 'broad_leaved_forest_500m',
    'conifirous_forest_500m', 'grassland_500m', 'mixed_forest_500m',
    'openSpace_500m', 'urban_area_500m', 'water_area_500m',
    'agri_area_5000m', 'broad_leaved_forest_5000m',
    'conifirous_forest_5000m', 'grassland_5000m', 'mixed_forest_5000m',
    'openSpace_5000m', 'urban_area_5000m', 'water_area_5000m'
    ]

BIRCH_FTS =[
    'datetime', 'Name_stati', 'Birch', 'y', 'agri_area_1000m',
    'broad_leaved_forest_1000m', 'conifirous_forest_1000m',
    'grassland_1000m', 'mixed_forest_1000m', 'openSpace_1000m',
    'urban_area_1000m', 'water_area_1000m', 'agri_area_100m',
    'broad_leaved_forest_100m', 'conifirous_forest_100m', 'grassland_100m',
    'mixed_forest_100m', 'openSpace_100m', 'urban_area_100m',
    'water_area_100m', 'agri_area_2000m', 'broad_leaved_forest_2000m',
    'conifirous_forest_2000m', 'grassland_2000m', 'mixed_forest_2000m',
    'openSpace_2000m', 'urban_area_2000m', 'water_area_2000m',
    'agri_area_200m', 'broad_leaved_forest_200m', 'conifirous_forest_200m',
    'grassland_200m', 'mixed_forest_200m', 'openSpace_200m',
    'urban_area_200m', 'water_area_200m', 'windSpeed',
    'boundaryLayerHeight', 't2m', 'totalPrecipitation', 'leafAreaIndex',
    'rh', 'windDirection', 'dem', 'NDVI', 'agri_area_10000m',
    'broad_leaved_forest_10000m', 'conifirous_forest_10000m',
    'grassland_10000m', 'mixed_forest_10000m', 'openSpace_10000m',
    'urban_area_10000m', 'water_area_10000m', 'red', 'green', 'blue', 'NIR',
    'SWIR1', 'SWIR2', 'Broadleaves', 'BetulaSpp', 'agri_area_500m',
    'broad_leaved_forest_500m', 'conifirous_forest_500m', 'grassland_500m',
    'mixed_forest_500m', 'openSpace_500m', 'urban_area_500m',
    'water_area_500m', 'agri_area_5000m', 'broad_leaved_forest_5000m',
    'conifirous_forest_5000m', 'grassland_5000m', 'mixed_forest_5000m',
    'openSpace_5000m', 'urban_area_5000m', 'water_area_5000m'
]


pollen = {"grass": {"type": "Grasses", "season_start": 4, "season_end": 9, "stats":['Grasses_avg_daily','Grasses_std_daily'], "features":GRASS_FTS}, 
          "birch": {"type": "Birch", "season_start": 3, "season_end": 5, "stats":['Birch_avg_daily','Birch_std_daily'],"features":BIRCH_FTS}}


column_to_drop = ["Name_stati", "PollenSeason"]


params={

        "Random Forest":{
            'Regressor__n_estimators': [150],
            'Regressor__max_depth': [8],
            'Regressor__max_features': ['sqrt'],
            'Regressor__random_state': [42]
        },
        "XGBRegressor":{
            'Regressor__learning_rate': [0.01, 0.1, 0.3],
            'Regressor__n_estimators': [100],
            'Regressor__max_depth': [1, 5, 10],
            'Regressor__min_child_weight': [1, 5, 10],
            'Regressor__subsample': [0.65],
            'Regressor__colsample_bytree': [0.7, 1]
        }
                
            }



