from boto3 import Session

import os
from os import listdir
from os.path import join, isfile
from pathlib import Path

import threading

from timer import timer, print_times

from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, YANDEX_S3_ENDPOINT, BUCKET

session = Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
client = session.client(service_name="s3", endpoint_url=YANDEX_S3_ENDPOINT, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

dir_path = os.path.dirname(os.path.relpath(__file__))
downloads_folder = dir_path + 'downloaded/' + 's3/'

def upload_files(folder_name):
    # list images
    images_folder = dir_path + 'files/' + folder_name
    images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]

    # add start time
    timer(f"yandex s3 start upload {folder_name}")

    upload_entry_list = []
    for image in images:
        f = open(images_folder + image, 'rb')
        response = client.upload_fileobj(f, BUCKET, f"{folder_name}{image}")
    #add stop time
    timer(f"yandex s3 stop upload {folder_name}")


def list_bucket(folder_name):
    timer(f"yandex s3 start list folder {folder_name}")
    r = client.list_objects_v2(Bucket=BUCKET, Prefix=folder_name)
    timer(f"yandex s3 stop list folder {folder_name}")
    return r

def create_links_from_list(list_):
    timer(f"yadnex s3 start create sharing links {BUCKET}")
    for file_ in list_:
        client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key':file_['Key']}, ExpiresIn=3600)
    timer(f"yandex s3 stop create sharing links {BUCKET}")

def get_objects_from_folder(list_, folder_name, thread, node_count):
    client = session.client(service_name="s3", endpoint_url=YANDEX_S3_ENDPOINT, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    timer(f"yandex s3 start get objects {BUCKET} node {thread}")
    for file_ in list_:
        if file_['Key'] == folder_name:
            continue
        try:
            downloaded = client.get_object(Bucket=BUCKET, Key=file_['Key'])
        except Exception as e:
            with open("restults.txt", 'a+') as results:
                results.writelines(f"Error raised trying to download file from s3 in node {thread}. Max retries achived\n")
                continue
    timer(f"yandex s3 stop get objects {BUCKET} node {thread}")
    print_times(f"yandex s3 start get objects {BUCKET} node {thread}", f"yandex s3 stop get objects {BUCKET} node {thread}")


def run_yandex_benchmark(folder_name):
    folder_name = folder_name
    upload_files(folder_name)
    print_times(f"yandex s3 start upload {folder_name}", f"yandex s3 stop upload {folder_name}")
    list_ = list_bucket(folder_name=folder_name)
    print_times(f"yandex s3 start list folder {folder_name}", f"yandex s3 stop list folder {folder_name}")
    create_links_from_list(list_=list_['Contents'])
    print_times(f"yadnex s3 start create sharing links {BUCKET}", f"yandex s3 stop create sharing links {BUCKET}")

def create_folder_structure_for_nodes(node_count):
    for i in range (0, node_count):
        Path(f"{downloads_folder}{node_count}/node{i}").mkdir(parents=True, exist_ok=True)

def multiple_node_read(images_folder, node_count):
    #create_folder_structure_for_nodes(node_count=node_count)
    folder_name = images_folder
    list_ = list_bucket(folder_name=folder_name)
    list_ = list_['Contents']
    # create threads
    threads = []
    for i in range (0,node_count):
        threads.append(threading.Thread(target=get_objects_from_folder, args=(list_, folder_name, i, node_count)))

    # start threads
    for thread in threads:
        thread.start()

    # wait threads
    for thread in threads:
        thread.join()
