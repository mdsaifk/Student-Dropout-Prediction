# ------------------------------ Importing Required Libraries ------------------------------
from pymongo import MongoClient

class Database:
    def __init__(self):
        try:
            # self.client = MongoClient('localhost', 27017)
            # self.db = self.client['stdDropoutDB']
            # self.collectionD = self.db['MOOC_Visual']
            self.client = MongoClient("mongodb+srv://gowtham136:user136@cluster0.heyil.mongodb.net/<dbname>?retryWrites=true&w=majority")
            self.db = self.client['stdDropoutDB']
            # self.collectionT = self.db['MOOC_Visual']
        except Exception as ex:
            print(ex)

    # To update the record
    def update_record(self, df):
        self.collectionT = self.db['MOOC_Visual']
        input_record = df.to_dict(orient='records')[0]
        # ----------- Verifying the above record is existing in the database --------------
        for rec in self.collectionT.find():
            if list(input_record.values()) == list(rec.values())[1:]:
                message = f"Record is already presenting in the database at index {list(rec.values())[0]}"
                return message

        # -------- Inserting the above record into database if it is not presenting in the database -------
        n_db_records = self.collectionT.find().count()  # Finding number of records
        record = {"_id": n_db_records+1}
        record.update(input_record)
        self.collectionT.insert_one(record)     # Inserting Record
        message = f"Record is successfully inserted at place {n_db_records+1}"  # Sending Message
        self.client.close()
        return message

    def update_file(self, df, file_name):
        # Converting dataframe into dictionary files -------
        input_records = df.to_dict(orient='records')

        # Connecting to table in MongoDB  and Extracting "enrollment_id" column data -------------------
        self.collectionT = self.db[file_name]
        n_db_records = self.collectionT.find().count()  # Finding number of records
        DB_enrollment_ids = [list(record.values())[1] for idx, record in enumerate(self.collectionT.find({}, {'enrollment_id'}))]

        for input_record in input_records[0:100]:

            if (n_db_records==0):
                record = {"_id": n_db_records + 1}
                record.update(input_record)
                self.collectionT.insert_one(record)  # Inserting Record
                n_db_records += 1

            elif (input_record["enrollment_id"] not in DB_enrollment_ids):
                record = {"_id": n_db_records + 1}
                record.update(input_record)
                self.collectionT.insert_one(record)  # Inserting Record
                n_db_records += 1
        self.client.close()
        return file_name + ", "