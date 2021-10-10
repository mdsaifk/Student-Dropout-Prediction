# ------------------------------ Importing Required Libraries ------------------------------
from sklearn.preprocessing import StandardScaler
import datetime
import pandas as pd
import numpy as np

class Preprocessing:
    def __init__(self):
        pass

    def processing(self, df):
        # Converting Dates into ordinals
        df = self.dates_to_ordinals(df)
        # Extracting new "present_days" feature from "start_date" and "end_date" features
        df = self.extract_features(df)
        # Scaling the values
        df = self.stadardise_values(df)
        return df

    # Converting Dates into ordinals
    def dates_to_ordinals(self, df):
        df['start_date'] = pd.to_datetime(df['start_date']).apply(lambda x : x.toordinal())
        df['end_date'] = pd.to_datetime(df['end_date']).apply(lambda x : x.toordinal())
        return df

    # Extracting new "present_days" feature from "start_date" and "end_date" features
    def extract_features(self, df):
        present_days = df['end_date'] - df['start_date'] + 1
        df.insert(2, 'present_days', present_days)
        return df

    # Scaling the values
    def stadardise_values(self, df):
        scale = StandardScaler()
        arr = scale.fit_transform(df)
        df = pd.DataFrame(arr, columns=df.columns)
        return df