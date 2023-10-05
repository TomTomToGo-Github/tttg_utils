"""
Description of the aws_RDS functions.

The functions in this module can create a new database
or delete an existing one.

Important features:
    - Basic DB-properties are fixed (Storage size, storage type, engine, etc.)
    - Name and identifier are passed by the code calling the functions.
"""


import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError
import time
import boto3
from datetime import datetime

load_dotenv()
# ACCESS_KEY = os.getenv("AWS_AK")
# SECRET_KEY = os.getenv("AWS_SK")
# if ACCESS_KEY is None:
#     print("No AWS credentials found in .env file")


def aws_rds_create_new_db(db_name, db_identifier):
    rds = boto3.client('rds')  # , aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        rds.create_db_instance(DBInstanceIdentifier=db_identifier,
                               AllocatedStorage=20,  # in GiB
                               DBName=db_name,
                               Engine='postgres',
                               # EngineVersion='13.3',  # Default:Latest
                               StorageType='gp2',  # General purpose SSD
                               StorageEncrypted=False,
                               AutoMinorVersionUpgrade=False,
                               MultiAZ=False,
                               MasterUsername=os.getenv("Master_user_name"),
                               MasterUserPassword=os.getenv("Master_user_pw"),
                               VpcSecurityGroupIds=[os.getenv("sg1"), os.getenv("sg2")],
                               DBInstanceClass='db.t3.micro',
                               BackupRetentionPeriod=0,  # Integer -> 0: disabled
                               # PreferredMaintenanceWindow='Sun:23:59-Mon:01:00' # For retention
                               # AvailabilityZone='eu-west-1c'  # Default: Currently used?
                               CopyTagsToSnapshot=False  # Default: False
                               # Tags=[{'Key': 'tag_DB' + dt_str, 'Value': 'value_DB' + dt_str}]
                               )
        print('\nStarting RDS instance with ID: {}'.format(db_identifier))
    except ClientError as e:
        if 'DBInstanceAlreadyExists' in e.__dict__['response']['Error']['Code']:
            print('DB instance {} exists already. checking status...'.format(db_identifier))
        else:
            raise

    running = True
    while running:
        response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
        db_instances = response['DBInstances']
        if len(db_instances) != 1:
            raise Exception('More than one DB instance returned; this should never happen...')
        db_instance = db_instances[0]
        status = db_instance['DBInstanceStatus']
        dt = datetime.today()
        day_today = "{}-{:2}-{:2}".format(dt.year, dt.month, dt.day)
        day_today = day_today.replace("- ", "-0")
        time_now = " | {:2}:{:2}:{:2}".format(dt.hour, dt.minute, dt.second)
        time_now = time_now.replace(": ", ":0")
        time_now = time_now.replace("|  ", "| 0")
        print('     -> Last DB status [ {} ]: {}'.format(day_today + time_now, status))
        if status == 'available':
            endpoint = db_instance['Endpoint']
            host = endpoint['Address']
            # port = endpoint['Port']
            print('\nDB instance ready with host: {}'.format(host))
            running = False
            return True
        else:
            time.sleep(30)


def aws_rds_delete_instance(db_identifier):
    rds = boto3.client('rds')  # , aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        print('\nDeleting RDS instance with ID: {}'.format(db_identifier))
        rds.delete_db_instance(DBInstanceIdentifier=db_identifier,
                               SkipFinalSnapshot=True,
                               DeleteAutomatedBackups=True
                               )
    # Options: https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DeleteDBInstance.html
    except NoCredentialsError as e:
        if 'DBInstanceNotFound' in e.message:
            print('No credentials found. DB instance {} not deleted.'.format(db_identifier))
        else:
            raise
    except ClientError as e:
        err_code = e.__dict__['response']['Error']['Code']
        if 'DBInstanceNotFound' in err_code:
            print('DB could not be found. DB instance {} not deleted.'.format(db_identifier))
            return False
        elif 'DBSnapshotAlreadyExists' in err_code:
            print('Snapshot of DB {} already exists. No snapshot created ...'.format(db_identifier))
            return False
        else:
            raise
    running = True
    while running:
        try:
            response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
            db_instances = response['DBInstances']
            if len(db_instances) != 1:
                raise Exception('More than one DB instance returned; this should never happen')

            db_instance = db_instances[0]
            status = db_instance['DBInstanceStatus']
            dt = datetime.today()
            day_today = "{}-{:2}-{:2}".format(dt.year, dt.month, dt.day)
            day_today = day_today.replace("- ", "-0")
            time_now = " | {:2}:{:2}:{:2}".format(dt.hour, dt.minute, dt.second)
            time_now = time_now.replace(": ", ":0")
            time_now = time_now.replace("|  ", "| 0")
            print('     -> Last DB status [ {} ]: {}'.format(day_today + time_now, status))
            if status != 'deleting':
                endpoint = db_instance['Endpoint']
                host = endpoint['Address']
                print('\nStrange: DB with {} should be in status "deleting" .'.format(host))
                running = False
            else:
                time.sleep(30)
        except ClientError as e:
            err_code = e.__dict__['response']['Error']['Code']
            if 'DBInstanceNotFound' in err_code:
                print("\n\nDB not found anymore - deletion completed successfully!")
                return True