import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication
from pymongo import MongoClient, errors
from datetime import datetime, timezone
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Load the UI file
            uic.loadUi('main.ui', self)

            


            # Set fixed size based on loaded UI
            self.setFixedSize(self.size())

            self.connect_bt.clicked.connect(self.connect_server)
            self.save_bt.clicked.connect(self.insert_data)
            self.search_bt.clicked.connect(self.search_data)
            self.refresh_query_bt.clicked.connect(self.show_database)
            self.save_update_bt.clicked.connect(self.update_data)

            self.model_1 = QStandardItemModel()
            self.model_1.setHorizontalHeaderLabels(['school_id','first_name','last_name','birthday','gender','school_year','phone_number'])
            self.tableView.setModel(self.model_1)

            # get the mongo ling of your database
            self.show_database()

            self.school_id = self.school_id_input.text()
            self.first_name = self.first_name_input.text()
            self.last_name = self.last_name_input.text()
            self.birthday = self.birthday_input.text()
            self.gender = self.gender_input.currentText()
            self.school_year = self.school_year_input.currentText()
            self.phone_number = self.phone_input.text()
            self.address = self.address_input.text()
            self.postal = self.postal_input.text()
            self.city = self.city_input.text()







        except FileNotFoundError:
            print("UI file 'main.ui' not found.")




    def connect_server(self):
        """
        This will connect you to your MongoDB.
        """
        self.mongo_link =  self.database_input.text()
        self.client = MongoClient(self.mongo_link)
        try:
            self.client = MongoClient(self.mongo_link)
            self.client.admin.command('ping')  # Force connection check
            self.validation_label.setStyleSheet("color: green; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Connected to MongoDB server at {self.mongo_link}")
            print(f"Connected to MongoDB server at {self.mongo_link}")
            self.create_database()
            self.show_database()

        except errors.ServerSelectionTimeoutError:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Failed to connect to MongoDB server at {self.mongo_link}")
            print(f"Failed to connect to MongoDB server at {self.mongo_link}")

        except ValueError as e1:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Invalid MongoDB URI: {e1}")
            print(f"ValueError: {e1}")
            
        except Exception as e:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

    def create_database(self):
        '''This will create your databases in your MongoDB.'''
        try:
            self.client = MongoClient(self.mongo_link)
            self.db = self.client["school_database"]
            self.collection = self.db["students"]  # Create or use the 'students' collection
            print('Database and collection created')
        except AttributeError:
            print('Connection not established. Please connect to the server first.')

    def insert_data(self):
        '''This will insert data into your MongoDB collection.'''
        
        # Ensure the connection and collection are properly set
        if not hasattr(self, 'collection'):
            print('Database or collection not initialized. Please ensure you have connected to the server and created the database.')
            return
        
        post = {
            "school_id": self.school_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "school_year": self.school_year,
            "phone_number": self.phone_number,
            "address": {
                "address_line": self.address,
                "postal_code": self.postal,
                "city": self.city,
            },
            "date_created": datetime.now(timezone.utc),  # Ensure datetime is timezone aware
        }
        
        try:
            result = self.collection.insert_one(post)
            print(f"Data inserted with record id {result.inserted_id}")
            self.school_id_input.clear()
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.birthday_input.text()
            self.gender_input.currentText()
            self.school_year_input.currentText()
            self.phone_input.clear()
            self.address_input.clear()
            self.postal_input.clear()
            self.city_input.clear()
        

        except Exception as e:
            print(f"An error occurred: {e}")

    def show_database(self):
        try:
            self.client = MongoClient(self.mongo_link)  # Connect to the MongoDB server using the provided link
            self.database = self.client['school_database']  # Access the 'school_database'
            self.collection = self.database['students']  # Access the 'students' collection within the database

            # Query the 'students' collection to find all documents, but only retrieve specific fields and exclude the '_id' field
            self.rows = self.collection.find({}, {'_id': 0, 'school_id': 1, 'first_name': 1, 'last_name': 1, 'birthday': 1, 'gender': 1, 'school_year': 1, 'phone_number': 1})

            self.model_1.removeRows(0, self.model_1.rowCount())  # Clear the existing data in the model

            self.fetched_data = list(self.rows)  # Convert the cursor result into a list

            # Iterate over each document in the fetched data
            for row_data in self.fetched_data:
                # Create a list of QStandardItem objects from the values of the current document
                items = [QStandardItem(str(data)) for data in row_data.values()]
                self.model_1.appendRow(items)  # Append the items as a new row in the model

            print('Data Fetched Successfully')  # Print a success message
        except Exception as e:  # Catch any exceptions that occur during the process
            print(f'Sqlite error: {e}')  # Print the exception message (Note: This should be updated to 'MongoDB error' instead of 'Sqlite error')
        finally:
            print('close po')  # Print a message indicating the end of the method (Note: This doesn't close the MongoDB connection)


    def search_data(self):

        self.school_id = self.school_id_search.text()
        try:
            self.client = MongoClient(self.mongo_link)
            self.database = self.client['school_database']
            self.collection = self.database['students']

            self.model_1.removeRows(0, self.model_1.rowCount())  # Clear the existing data in the model

            self.fetched_data = list(self.rows)  # Convert the cursor result into a list

            # Iterate over each document in the fetched data
            for row_data in self.fetched_data:
                # Create a list of QStandardItem objects from the values of the current document
                items = [QStandardItem(str(data)) for data in row_data.values()]
                self.model_1.appendRow(items)  # Append the items as a new row in the model
          
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client.close()
    
    def update_data(self):
        self.school_id_update = self.school_id_update_input.text()
        self.school_year_update = self.school_year_update_input.currentText()
        self.client = MongoClient(self.mongo_link)
        self.database = self.client['school_database']
        self.collection = self.database['students']
        try:
            
            
            myquery = {'school_id': self.school_id_update}
            new_value = {'$set': {'school_year': self.school_year_update}}
            self.collection.update_one(myquery, new_value)
            self.validation_label_2.setText(f'school id of:{self.school_id_update} was updated into{self.school_year_update}')

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyApp()
    main_app.show()
    sys.exit(app.exec())
