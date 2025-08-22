import os
import sys
from dataclasses import dataclass
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import dagshub


# Importing classification model
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
# from xgboost import xgb
import lightgbm as LGBMClassifier
from sklearn.metrics import classification_report,accuracy_score,precision_score,f1_score,recall_score,confusion_matrix

from src.DIAP.logger import logging
from src.DIAP.exception import CustomException
from src.DIAP.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def eval_metrics(self,actual, pred):
        # class_report = (classification_report(actual, pred))
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred)
        f1 = f1_score(actual, pred)
        # recall = recall_score(actual, pred)
        # confusion_mat = confusion_matrix(actual, pred)
        return accuracy,precision,f1  #recall,#confusion_mat, class_report

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Splitting training and testing input data')
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            logging.info('Splitting done')

            models={
                'Logistic Regression':LogisticRegression(),
                'Naive Bayes':GaussianNB(),
                'KNN':KNeighborsClassifier(),
                'Decision Tree':DecisionTreeClassifier(),
                'Random Forest':RandomForestClassifier(),
                # 'SVC':SVC(),
                # 'lightgbm':LGBMClassifier(),
            }
            params={
                "Logistic Regression":{},
                "Naive Bayes":{
                    # 'var_smoothing': np.logspace(0,-9, num=100)
                },
                "KNN":{
                    # 'n_neighbors':5,
                    # 'weights':'uniform',
                    # 'algorithm':'auto',
                    # 'leaf_size':30,
                    # 'p':2,
                    # 'metric':'minkowski',
                    # 'metric_params':None,
                    # 'n_jobs':None,
                    # 'n_neighbors': [3, 5, 7, 9, 11],  # Test odd values of k
                    # 'weights': ['uniform', 'distance'],  # Weighting options
                    # 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],  # Algorithm options
                    # 'leaf_size': [30, 40, 50],  # Leaf size for tree-based algorithms
                    # 'metric': ['euclidean', 'manhattan', 'minkowski'],  # Distance metrics
                    # 'p': [1, 2]  # Power parameter for Minkowski distance
                },
                "Decision Tree":{
                    # 'criterion':['gini','entropy','log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_depth': [None, 5, 10],
                    # 'min_samples_split': [2, 5], 
                    # 'min_samples_leaf': [1, 2], 
                    # 'min_weight_fraction_leaf':0.1,
                    # 'max_features':None, 
                    # 'random_state':None, 
                    # 'max_leaf_nodes':None, 
                    # 'min_impurity_decrease':0.0, 
                    # 'class_weight':None, 
                    # 'ccp_alpha':0.0, 
                    # 'monotonic_cst':None,
                },
                "Random Forest":{
                    # 'n_estimators': [100, 200],
                    # 'max_depth': [None, 10, 20],
                    # 'min_samples_split': [2, 5],
                    # 'min_samples_leaf': [1, 2]
                },
                # "SVC":{
                    # 'C': [0.1, 1, 10],
                    # 'kernel': ['linear', 'rbf'],
                    # 'gamma': ['scale', 'auto']
                # },
                # "lightgbm":{
                #     'learning_rate': [0.01, 0.05, 0.1],
                #     'n_estimators': [100, 200],
                #     'max_depth': [-1, 10, 20],
                #     'num_leaves': [31, 50, 100],
                #     'min_data_in_leaf': [20, 30],
                #     'feature_fraction': [0.8, 0.9],
                #     'bagging_fraction': [0.8, 0.9],
                #     'bagging_freq': [1, 5],
                #     'lambda_l1': [0, 0.1],
                #     'lambda_l2': [0, 0.1]
                # }
            }

            model_report:dict=evaluate_models(X_train,y_train,X_test,y_test,models,params)

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

             ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            print("This is the best model:")
            print(best_model_name)

            model_names = list(params.keys())

            actual_model=""

            for model in model_names:
                if best_model_name == model:
                    actual_model = actual_model + model
            
            best_params = params[actual_model]

            # dagshub.init(repo_owner='harshal3558', repo_name='ML-Project', mlflow=True)
            mlflow.set_registry_uri("https://dagshub.com/harshal3558/Credit-Card-Default-Prediction.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # mlflow

            # import dagshub
            dagshub.init(repo_owner='harshal3558', repo_name='Credit-Card-Default-Prediction', mlflow=True)
            with mlflow.start_run():

                predicted_qualities = best_model.predict(X_test)

                (accuracy, precision, f1) = self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_params(best_params)

                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("f1", f1)
                # mlflow.log_metric('recall',recall)


                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(best_model, "model", registered_model_name=actual_model)
                else:
                    mlflow.sklearn.log_model(best_model, "model")


            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            acc_score = accuracy_score(y_test, predicted)
            return acc_score



        except Exception as e:
            raise CustomException(e,sys)