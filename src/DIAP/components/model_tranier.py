import os
import sys
from dataclasses import dataclass
from urllib.parse import urlparse

import mlflow
import numpy as np
import dagshub
import joblib

# Scikit-learn models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
# from xgboost import xgb
# import lightgbm as LGBMClassifier

from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    f1_score,
    confusion_matrix,
)

from src.DIAP.logger import logging
from src.DIAP.exception import CustomException
from src.DIAP.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def eval_metrics(self, actual, pred):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred)
        f1 = f1_score(actual, pred)
        return accuracy, precision, f1

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            logging.info("Splitting done")

            models = {
                "Logistic Regression": LogisticRegression(),
                "Naive Bayes": GaussianNB(),
                "KNN": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "SVC": SVC(),
                # "lightgbm": LGBMClassifier()
            }

            params = {
                "Logistic Regression": {},
                "Naive Bayes": {},
                "KNN": {},
                "Decision Tree": {},
                "Random Forest": {},
                "SVC": {},
                # "lightgbm": {}
            }

            model_report: dict = evaluate_models(
                X_train, y_train, X_test, y_test, models, params
            )

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            print("This is the best model:")
            print(best_model_name)

            best_params = params[best_model_name]

            # Initialize Dagshub for MLflow tracking
            dagshub.init(
                repo_owner="harshal3558",
                repo_name="Diabetes-Prediction",
                mlflow=True
            )
            mlflow.set_registry_uri("https://dagshub.com/harshal3558/Diabetes-Prediction.mlflow")

            with mlflow.start_run():
                predicted_qualities = best_model.predict(X_test)

                accuracy, precision, f1 = self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_params(best_params)
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("f1", f1)

                # Save the model using your utility function
                save_object(
                    file_path=self.model_trainer_config.trained_model_file_path,
                    obj=best_model
                )

                # Log saved model as an artifact to Dagshub
                mlflow.log_artifact(self.model_trainer_config.trained_model_file_path)

            if best_model_score < 0.6:
                raise CustomException("No suitable model found with accuracy > 0.6")

            logging.info("Best model selected and saved successfully.")

            # Final performance logging
            predicted = best_model.predict(X_test)
            acc_score = accuracy_score(y_test, predicted)
            return acc_score

        except Exception as e:
            raise CustomException(e, sys)
