import pytest
import numpy as np
from src.components import model_trainer

def test_load_train_data(tmp_path):
    # Create dummy data and save as pkl using MainUtils
    dummy_data = np.array([[1, 2, 3], [4, 5, 6]])
    file_path = tmp_path / "train.pkl"
    from src.utils.main_utils import MainUtils
    MainUtils.save_object(str(file_path), dummy_data)
    X, y = model_trainer.load_train_data(str(file_path))
    assert X.shape == (2, 2)
    assert y.shape == (2,)
    assert np.array_equal(y, dummy_data[:, 0])

def test_train_model_default():
    # Minimal config for Linear Regression
    X = np.random.rand(10, 3)
    y = np.random.rand(10)
    config = {
        "model_trainer": {"chosen_model": "Linear Regression"},
        "model_selection": {"model": {"Linear Regression": {}}}
    }
    model = model_trainer.train_model(X, y, config)
    assert hasattr(model, "predict")
    preds = model.predict(X)
    assert preds.shape == (10,)

def test_train_model_gridsearch():
    # Minimal config for Ridge Regression with param grid
    X = np.random.rand(10, 3)
    y = np.random.rand(10)
    config = {
        "model_trainer": {"chosen_model": "Ridge Regression"},
        "model_selection": {
            "model": {
                "Ridge Regression": {
                    "search_param_grid": {"alpha": [0.1, 1.0]}
                }
            }
        }
    }
    model = model_trainer.train_model(X, y, config)
    assert hasattr(model, "predict")
    preds = model.predict(X)
    assert preds.shape == (10,)