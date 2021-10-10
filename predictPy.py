# ------------------------------ Importing Required Libraries ------------------------------
import pickle
import pandas as pd

class Predicting:
    def __init__(self):
        pass

    # ------------------ Function to predict the result the data frame ------------------
    def predict_df(self, df):
        model = pickle.load(open("pkl_rf_model_feature_10.pkl", "rb"))
        # Model Prediction
        pred_val = model.predict(df)
        return pred_val
