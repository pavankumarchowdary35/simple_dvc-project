import pandas as pd
import argparse
from src.utils.common_utils import (
    read_params,
    save_reports,
)
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=logging_str)


def eval_metrices(actual,pred):
    rmse = mean_squared_error(actual,pred)
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def evaluate(config_path):
    config = read_params(config_path)
    artifacts = config["artifacts"]
    split_data = artifacts["split_data"]
    test_data_path = split_data["test_path"]
    
    model_dir = artifacts["model_dir"]
    model_path = artifacts["model_path"]

    base = config["base"]
    target = base["target_col"]

    reports = artifacts["reports"]
    reports_dir = reports["reports_dir"]
    scores_file = reports["scores"]

    test = pd.read_csv(test_data_path, sep=",")

    test_y = test[target]
    test_x = test.drop(target, axis=1)

    lr = joblib.load(model_path)
    logging.info(f'model is loaded from {model_path}')
    y_pred = lr.predict(test_x)

    rmse, mae, r2 = eval_metrices(test_y, y_pred)

    scores = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    }

    save_reports(scores_file, scores)



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        data = evaluate(config_path=parsed_args.config)
        logging.info("evaluation stage completed")

    except Exception as e:
        logging.error(e)
        # raise e


