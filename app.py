# Importing libraries
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from datetime import datetime
from glob import glob
import os
from werkzeug.datastructures import FileStorage

# Work flow
# ===================================
# 1. Extracting data from the form
#    1. Single Record
#    2. Single File
#    3. Batch Files
# 2. Preprocessing data
#    1. Conversion Dates into ordinals
#    2. Extracting New feature
#    3. Scaling Data and File
# 3. Predicting Result
#    1. Predicting Record
#    2. Predicting File
# 4. Update data into Data-base
# ===================================

# Initialising flask object
app = Flask(__name__)

# HOME PAGE --------------------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Main Home page
@app.route("/")
def home():
    return render_template("home_page.html")

# Sub Home page
@app.route("/home_type", methods = ["POST"])
def home_type():
    input_type = request.form['input_type']
    if input_type == 'Single_Record':
        return render_template('home_single_record.html')
    elif input_type == 'Single_File':
        return render_template('home_single_file.html')
    elif input_type == 'Batch_Files':
        return render_template("home_batch_files.html")
    else:
        return render_template("home_page.html")

# Input as Single Record :  ---------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# resultStatus = ["Result", "DBMessage"]
@app.route("/predict_single_data", methods = ["POST"])
def predict_single_data():
    # ======================================================================================
    # Input Example:
    # ["start_date", "end_date", "access", "discussion", "navigate", "page_close", "problem", "video", "wiki"]
    # ["14-12-2020", "19-12-2020", 74, 14, 12, 22, 2, 1, 2]
    # ======================================================================================
    resultStatus = dict()
    # -------------------------- Extracting values from the form --------------------------
    cols = ['start_date', 'end_date', 'access', 'discussion', 'navigate', 'page_close', 'problem', 'video', 'wiki']
    in_features = [[request.form[col] for col in cols]]
    try:
        DB_Update = request.form["DB_Update"]
    except:
        DB_Update = 'no'

    # -------------------- Creating a Data frame with the input values --------------------
    df = pd.DataFrame(np.array(in_features), columns=cols)    # Creating Data Frame with input values
    X = df.copy()   # Copying Input values for purpose of exporting into MongoDB

    # ------------------------------ Preprocessing the data -------------------------------
    from preprocessingPy import Preprocessing
    pre_process = Preprocessing()
    df = pre_process.processing(df)

    # ------------------------------ Predicting the result ------------------------------
    from predictPy import Predicting
    pred = Predicting()
    X['result'] = pred.predict_df(df)

    # --------------------------------- Storing the data ---------------------------------
    # Storing the data in MongoDB
    resultStatus["DBMessage"] = 'Not Stored in MongoDB'
    if DB_Update == "yes":
        from databasePy import Database
        db = Database()
        resultStatus["DBMessage"] = db.update_record(X)

    # ---------------------------- Finding the result ----------------------------
    if X['result'][0] == "0":
        resultStatus["Result"] = "0 - Student will not Drop from the course"
    else:
        resultStatus["Result"] = "1 - Student will Drop from the course"

    # ---------------------------- Displaying the output ----------------------------
    return render_template("result_page.html", type="single_record", resultStatus=resultStatus)


# Input as Single File : ---------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# resultStatus = ["File_Name", "PreProcessing", "Predicting", "DBMessage", "Result", "Files_Stored_Path"]
@app.route("/predict_single_file", methods=["POST"])
def predict_single_file():
    # ======================================================================================
    # Uploading file must contain the below column names:
    # ["start_date", "end_date", "access", "discussion", "navigate", "page_close", "problem", "video", "wiki"]
    # ======================================================================================
    resultStatus = dict()

    # ------------------------------- Getting the current directory -------------------------------
    resultStatus["Files_Stored_Path"] = os.getcwd() + "/Data/Single_File/"  # For Cloud deployment

    # ------------------------------- Extracting file from the form -------------------------------
    in_file = request.files['in_file']   # Loading the file
    resultStatus["File_Name"] = in_file.filename         # Extracting file name
    try:
        DB_Update = request.form["DB_Update"]
    except:
        DB_Update = 'no'
    try:
        Current_Dir_Update = request.form["Current_Dir_Update"]
    except:
        Current_Dir_Update = 'no'

    # ---------------------- Creating a Data frame directly from input file  ----------------------
    df = pd.read_csv(FileStorage(in_file).stream)
    
    ''' No need this code
    =============================
    resultStatus["URL"] = os.environ["Local_Path_forward_slash"]
    try:
        in_file.save(resultStatus["URL"])
        resultStatus["URL"] = resultStatus["URL"] + " --> File Saved Successfully"
    except:
        resultStatus["URL"] = resultStatus["URL"] + " --> Error in Saving"
     
    try:
        df = pd.read_csv(resultStatus["URL"])
        resultStatus["URL"] = resultStatus["URL"] + " --> DF Created"
    except:
        resultStatus["URL"] = resultStatus["URL"] + " --> Error in Creating DF"
    '''

    # ------------------ Verifying the incoming file was already predicted or not ------------------
    if df.columns[-1]=='result':
        resultStatus["Result"] = "This file was already Predicted"
        resultStatus["DBMessage"] = 'Not Stored in MongoDB'
        return render_template("result_page.html", type="single_file", resultStatus=resultStatus)

    # ----------------------------- Continue for predicting the result -----------------------------
    else:
        X = df.copy()  # Copying Input values for purpose of exporting into MongoDB or local drive

        # ---------------------- Loading the data frame with required columns ----------------------
        cols = ['start_date', 'end_date', 'access', 'discussion', 'navigate', 'page_close', 'problem', 'video', 'wiki']
        df = df[cols]

        # ------------------------------ Preprocessing the data -------------------------------
        from preprocessingPy import Preprocessing
        pre_process = Preprocessing()
        df = pre_process.processing(df)

        # ------------------------------ Predicting the result ------------------------------
        from predictPy import Predicting
        pred = Predicting()
        X['result'] = pred.predict_df(df)

        # --------------------------------- Storing the data ---------------------------------
        # Storing the data in MongoDB ----------------------------
        resultStatus["DBMessage"] = 'Not Stored in MongoDB'

        if DB_Update == "yes":
            from databasePy import Database
            db = Database()
            resultStatus["DBMessage"] = resultStatus["DBMessage"] + db.update_file(X, resultStatus["File_Name"].split(".")[0])

        # Storing the data in current directory ------------------
        if Current_Dir_Update == "yes":
            file_path = os.path.join(resultStatus["Files_Stored_Path"], resultStatus["File_Name"])  # Creating path of the file to be stored
            X.to_csv(file_path, index=False)

        # ---------------------------- Finding the result ----------------------------
        resultStatus["Result"] = "File is Successfully Predicted"
        resultStatus["sampleData"] = X.copy()

        # ---------------------------- Displaying the output ----------------------------
        return render_template("result_page.html", type="single_file", resultStatus=resultStatus)


# Input as Batch Files : ---------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# resultStatus = ["Predicted_Files", "Skipped_Files", "DBMessage", "Result", "Files_Stored_Path"]
@app.route("/predict_batch_files", methods=["POST"])
def predict_batch_files():
    resultStatus = dict()

    # --------------------- Extracting the csv files from the user given path ---------------------
    InCsvDir = os.getcwd() + request.form['path']       # Input Path: "/Data/Batch_Files/Input_Files/"
    resultStatus["Files_Stored_Path"] = os.getcwd() + "/Data/Batch_Files/Predicting_Files/"  # For Cloud deployment
    CsvFiles = glob(os.path.join(InCsvDir, '*.csv'))    # Get all CSV files including paths

    try:
        DB_Update = request.form["DB_Update"]
    except:
        DB_Update = 'no'
    try:
        Current_Dir_Update = request.form["Current_Dir_Update"]
    except:
        Current_Dir_Update = 'no'

    skipped_files = []
    predicted_files = []

    # --------------------- For loop to extract and predict files one-by-one ---------------------
    for i in range(len(CsvFiles)):
        df = pd.read_csv(CsvFiles[i])   # Loading the Data Frame from the path
        file_name = os.path.split(CsvFiles[i])[1]  # Extracting name of the file

        # -------------------- Verifying a file was already predicted or not --------------------
        if df.columns[-1] == 'result':
            skipped_files.append(file_name)

        # -------------------------- Continue for predicting the result -------------------------
        else:
            X = df.copy()  # Copying Input values for purpose of exporting into MongoDB
            cols = ['start_date', 'end_date', 'access', 'discussion', 'navigate', 'page_close', 'problem', 'video', 'wiki']
            df = df[cols]

            # ------------------------------ Preprocessing the data -------------------------------
            from preprocessingPy import Preprocessing
            pre_process = Preprocessing()
            df = pre_process.processing(df)

            # ------------------------------ Predicting the result ------------------------------
            from predictPy import Predicting
            pred = Predicting()
            X['result'] = pred.predict_df(df)
            predicted_files.append(file_name)

            # --------------------------------- Storing the data ---------------------------------
            # Storing the data in MongoDB ----------------------------
            resultStatus["DBMessage"] = 'Not Stored in MongoDB'
            if DB_Update == "yes":
                from databasePy import Database
                db = Database()
                resultStatus["DBMessage"] = ""
                resultStatus["DBMessage"] = resultStatus["DBMessage"] + db.update_file(X, resultStatus["File_Name"].split(".")[0])

            # Storing the data in current directory ------------------
            if Current_Dir_Update == "yes":
                file_store_path = os.path.join(resultStatus["Files_Stored_Path"], file_name)  # Location of the file stored
                X.to_csv(file_store_path, index=False)

    else:
        resultStatus["Predicted_Files"] = predicted_files
        resultStatus["Skipped_Files"] = skipped_files
        if len(resultStatus["DBMessage"])>(2*len(os.path.split(CsvFiles[0])[1])):
            resultStatus["DBMessage"] = resultStatus["DBMessage"] + " are updated"


    # ------------------------------------ Displaying the output -----------------------------------
    return render_template("result_page.html", type="batch_files", resultStatus=resultStatus)

if __name__ == "__main__":
    app.run(debug=True, port=5101)
