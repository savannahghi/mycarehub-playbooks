#! /usr/bin/python3

#===========================================
import os
import time
import glob
import contextlib
from google.cloud import storage
#===========================================

TIMESTAMP = time.strftime('%d_%m_%Y_%H_%M_%S')

MYSQLDUMP_BIN_PATH = "{{ db_backup_mysqldump_binary_path }}"
DB_HOST = "{{ db_backup_mysql_host }}"
DB_USER = "{{ db_backup_mysql_user }}"
DB_PASSWORD = "{{ db_backup_mysql_user_password }}"
DB_PORT = "{{ db_backup_mysql_port }}"
BACKUP_NAME = "{{ db_backup_location_code }}"
DB_BACKUP_PATH = "{{ db_backup_backup_dir }}"
BACKUP_FILE_NAME = BACKUP_NAME+'_'+TIMESTAMP

dump_cmd = "{0} -h '{1}' -P '{2}' -u '{3}' --password='{4}' --all-databases | gzip > {5}/{6}.sql.gz".format(MYSQLDUMP_BIN_PATH,DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_BACKUP_PATH,BACKUP_FILE_NAME)
list_of_files = glob.glob(DB_BACKUP_PATH+'/*')
dump_count = len(list_of_files)


def oldest_local_backup():
    list_of_files = glob.glob(DB_BACKUP_PATH+'/*')
    return min(list_of_files, key=os.path.getctime)

def newest_local_backup():
    list_of_files = glob.glob(DB_BACKUP_PATH+'/*')
    return max(list_of_files, key=os.path.getctime)


def create_local_backup():
    if dump_count <= 4:
        os.system(dump_cmd)  
    elif dump_count == 5:
        '''
        - remove older local backups
        - create/push newer one to backup directory
        '''
        with contextlib.suppress(FileNotFoundError):
            if os.path.exists(oldest_local_backup()):
                os.remove(oldest_local_backup())
                os.system(dump_cmd)
    else:
        '''
        - if dump_count > 5, keep deleting older files
        '''
        with contextlib.suppress(FileNotFoundError):
            if os.path.exists(oldest_local_backup()):
                os.remove(oldest_local_backup())

    
create_local_backup()

#=======================================================================
# Create gcp bucket and necessary backup object (folder) if not exist.
#=======================================================================

GCP_BUCKET_LOCATION = "{{ db_backup_gcp_bucket_location }}"
GCP_BUCKET_STORAGE_CLASS= "{{ db_backup_gcp_bucket_storage_class }}"
GCP_BUCKET_NAME = "{{ db_backup_gcp_bucket_name }}"
GCP_BUCKET_SUBFOLDER = BACKUP_NAME

GCP_APP_CREDENTIALS  = "{{ db_backup_gcp_app_credentials }}"
storage_client = storage.Client.from_service_account_json(GCP_APP_CREDENTIALS)

def create_gcp_bucket(bucket_name):
    emr_bucket = storage_client.bucket(bucket_name)
    if not emr_bucket.exists():
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = GCP_BUCKET_STORAGE_CLASS
        return storage_client.create_bucket(bucket, location = GCP_BUCKET_LOCATION)
    return emr_bucket
    

def setup_gcp_bucket(bucket_name, subfolder_name):
    bucket = create_gcp_bucket(bucket_name)
    blobs_specific = list(bucket.list_blobs(prefix=subfolder_name+"/"))
    if len(blobs_specific)>=1:
        return subfolder_name + " folder already exists"
    else:
        blob = bucket.blob(subfolder_name + "/")
        blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        return "Created " + subfolder_name + " folder"


setup_gcp_bucket(GCP_BUCKET_NAME, GCP_BUCKET_SUBFOLDER)


#====================================================================
# Upload dumps to gcp
#====================================================================


bucket = storage_client.get_bucket(GCP_BUCKET_NAME)

def upload_dump_to_gcp():
    bucket_files =  list(bucket.list_blobs(prefix=GCP_BUCKET_SUBFOLDER+"/"))

    files_total = len(bucket_files)
    if files_total <= 4:
        '''
        - upload latest backup from local storage
        '''
        newest_local_file = newest_local_backup()
        blob_name = newest_local_backup().split("/")[-1]

        blob = bucket.blob(GCP_BUCKET_SUBFOLDER + "/" + blob_name)
        blob.upload_from_filename(newest_local_file)

    elif files_total >= 5:
        '''
        - delete oldest file fom the bucket
        - upload the latest from local storage
        '''
        oldest_file = bucket_files[0].name
        blob = bucket.blob(oldest_file)
        blob.delete()

        newest_local_file = newest_local_backup()
        blob_name = newest_local_backup().split("/")[-1]

        blob = bucket.blob(GCP_BUCKET_SUBFOLDER + "/" + blob_name)
        blob.upload_from_filename(newest_local_file)
    else:
        '''
        - if bucket files_count > 5, keep deleting older files
        '''
        oldest_file = bucket_files[0].name
        blob = bucket.blob(oldest_file)
        blob.delete()

upload_dump_to_gcp()
