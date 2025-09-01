from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from src.constants import *
from src.logger import logging
from src.utils.main_utils import MainUtils
import numpy as np
from src.exception import MyException
import sys

def load_train_data(file_path: str) -> tuple[np.ndarray, np.ndarray]:
    """Load training data from a pkl file"""
    try:
        logging.info("Loading training data from %s", file_path)
        data = MainUtils.load_object(file_path)
        X = data[:, 1:]  # All columns except first
        y = data[:, 0]   # First column
        logging.info("Training data loaded successfully. Shape: X=%s, y=%s", X.shape, y.shape)
        return X, y
    except Exception as e:
        logging.error("Error in loading training data: %s", e)
        raise MyException(e, sys)

def train_model(X_train: np.ndarray, y_train: np.ndarray, config: dict):
    """Train the model with hyperparameter tuning based on params.yaml."""
    try:
        logging.info("Starting model training process.")
        chosen_model = config["model_trainer"]["chosen_model"]
        model_configs = config["model_selection"]["model"]

        # Map model names to sklearn classes
        model_map = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(),
            "Lasso Regression": Lasso(),
            "Random Forest Regression": RandomForestRegressor(),
            "Gradient Boosting Regression": GradientBoostingRegressor(),
            "DecisionTreeRegressor": DecisionTreeRegressor(),
        }

        logging.info("Chosen model: %s", chosen_model)
        if chosen_model not in model_map:
            logging.error("Unsupported model: %s", chosen_model)
            raise ValueError(f"Unsupported model: {chosen_model}")

        base_model = model_map[chosen_model]

        # Get param grid for chosen model
        param_grid = model_configs.get(chosen_model, {}).get("search_param_grid", {})

        if not param_grid:
            logging.warning("No hyperparameters found for %s. Training with default params.", chosen_model)
            best_model = base_model.fit(X_train, y_train)
            logging.info("Model trained with default parameters.")
        else:
            logging.info("Running GridSearchCV for %s with params: %s", chosen_model, param_grid)
            grid_search = GridSearchCV(
                estimator=base_model,
                param_grid=param_grid,
                cv=3,
                n_jobs=-1,
                scoring="r2"   # 👈 change if you want MAE/MSE etc.
            )
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            logging.info("Best params for %s: %s", chosen_model, grid_search.best_params_)
            logging.info("Model trained with best parameters from GridSearchCV.")

        logging.info("%s training completed", chosen_model)
        return best_model

    except Exception as e:
        logging.error("Error in training model: %s", e)
        raise MyException(e, sys)

def main():
    try:
        logging.info("Starting main model training workflow.")
        # Load params
        config_path = "./config/params.yaml"
        logging.info("Loading model parameters from %s", config_path)
        model_params = MainUtils.load_params(config_path)

        # Load training data
        logging.info("Loading training data for model training.")
        X_train, y_train = load_train_data('./data/interim/train_processed.pkl')

        # Train model
        logging.info("Initiating model training.")
        clf = train_model(X_train, y_train, model_params)
        
        # Save model 
        trained_model_path = os.path.join("./models", "trained_model.pkl")
        os.makedirs("./models", exist_ok=True)
        
        MainUtils.save_object(trained_model_path, clf)
        logging.info("Model training workflow completed successfully.")

    except Exception as e:
        logging.error("Failed to complete the model building process: %s", e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()