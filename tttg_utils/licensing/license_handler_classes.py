## built-in modules
import os
import uuid
import datetime
## pip installed modules
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
## self made modules
from tttg_utils.connectors.database import QueryDB

load_dotenv()


class LicenseHandler(QueryDB):
    """Generate License
    
    Use name of customer and current date to generate a uuid.
    Connect to DB and store the license with start and expiration
    date.
    """
    def __init__(self, db_connection=None):
        super().__init__(db_connection)
        self.db_name = 'licenses.sqlite'
        self.db_table = 'licenses'

    def generate_new_license_key(self, user_name, purchased_months):
        # Compute license key
        current_time = datetime.datetime.now()
        license_str = user_name + current_time.strftime('%Y%m%d-%H%M%S') + os.getenv('LICENSE_ID_EXTENSION')
        license_key = str(uuid.uuid5(uuid.NAMESPACE_DNS, license_str))

        # Compute license expiration
        created_at = current_time.date()
        expiration_date = created_at + relativedelta(months=purchased_months)
        expiration_date = expiration_date

        # Add new license to license DB
        db_entry = {
            'db_name': self.db_name,
            'db_table': self.db_table,
            'user_name': user_name,
            'license_key': license_key,
            'created_at': str(created_at),
            'expiration_date': expiration_date
        }
        self.db_schema = {
            'user_name': 'TEXT NOT NULL',
            'license_key': 'TEXT',
            'created_at': 'DATE',
            'expiration_date': 'DATE'
        }
        self.store_license(db_entry, self.db_schema)

        return license_key

    def store_license(self, db_entry, db_schema):
        # Step 1: Connect to a SQLite database (creating a new db and table if it doesn't exist)
        schema_str = ', \n'.join([f"{key} {db_schema[key]}" for key in db_schema])
        create_db_if_not_exists = f'''
            CREATE TABLE IF NOT EXISTS {db_entry.get('db_table')} (
                id INTEGER PRIMARY KEY, {schema_str}
            )
        '''
        # Step 2: Insert row with new license into the table
        value_names = ",".join(key for key in db_entry if key not in ['db_name', 'db_table'])
        values = tuple(db_entry[key] for key in db_entry if key not in ['db_name', 'db_table'])
        command = f"INSERT INTO licenses ({value_names}) VALUES (?,?,?,?)"
        
        ## Execute the the specified commands to update license
        executions = [create_db_if_not_exists, (command, values)]
        self.update_db(db_entry['db_name'], executions)

    def is_valid(self, user_name):
        entries_for_user = self.fetch_from_db(self.db_name, self.db_table, 'user_name', user_name)
        expiration_dates = []
        for row in entries_for_user:
            row_dict = self.db_schema
            for entry, key in zip(row[1:], self.db_schema):
                row_dict[key] = entry
                if key == 'expiration_date':
                    expiration_dates.append(entry)
        current_date = datetime.date.today()
        return str(current_date) <= max(expiration_dates)

 
 
 

# Template directly from chatGPT


# import uuid
# import pickle

# def validate_license_key(license_key):
#     # Check if the license key exists in your database or storage
#     # Verify if the key is still valid (not expired)
#     # Check for other restrictions (e.g., maximum users, features)
#     # Return True if the key is valid, False otherwise
#     return True  # Replace with actual validation logic

# def activate_license(license_key):
#     # Mark the license as activated in your database
#     # Store activation details (e.g., activation date)
#     # Allow access to the software
#     pass

# def check_license_status():
#     # Retrieve the license details for the current user
#     # Check if it's expired or violates any restrictions
#     if expired or violates_restrictions:
#         # Disable certain features or prompt for license renewal
#         pass




# Implementing licenses for a software product in Python typically involves creating a module or component that can check and enforce licensing conditions. Here's a basic example of how you can implement a simple license validation system using Python. Please note that this is a basic example, and you may need to adapt it to your specific requirements.

# Define the License Class:


# # Generate a license with an expiration date (e.g., 365 days from today)
# expiration_date = datetime.date.today() + datetime.timedelta(days=365)
# license_key = generate_license_key()

# # Save the license key and expiration date to a file
# license_data = {'license_key': license_key, 'expiration_date': expiration_date}
# with open('license.dat', 'wb') as file:
#     pickle.dump(license_data, file)
    
    
# Generate and Save License Keys:
# You would typically generate and save license keys securely, possibly on a server, and distribute them to your customers. For simplicity, I'll provide an example of generating a license key and saving it to a file.



# Validate the License:
# In your software, you should have a module that loads and validates the license at startup.



# import pickle

# # Load the license data from the file
# try:
#     with open('license.dat', 'rb') as file:
#         license_data = pickle.load(file)
#     license_key = license_data['license_key']
#     expiration_date = license_data['expiration_date']
# except FileNotFoundError:
#     print("License file not found. Please make sure the license file is available.")
#     exit()

# # Create a License object
# license = License(license_key, expiration_date)

# # Check if the license is valid
# if license.is_valid():
#     print("License is valid. Your software is ready to use.")
# else:
#     print("License is invalid. Please purchase a valid license.")
#     exit()
# Handling License Validation Result:
# Depending on whether the license is valid or not, you can decide how your software behaves. In this example, the program will exit if the license is invalid, but you can implement any custom behavior as needed.

# Please keep in mind that this is a very basic example. In a real-world scenario, you may want to implement more advanced features, such as license activation, hardware binding, and server-based license validation for better security. Additionally, it's crucial to protect your license generation and validation mechanisms to prevent unauthorized access.
