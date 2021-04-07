import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

from timer import timer, print_times

import requests

import dropbox
from dropbox import Dropbox

import threading

from config import OAUTHTOKEN

OAuthToken = OAUTHTOKEN

def create_dropbox_instance():
    return Dropbox(oauth2_access_token=OAuthToken)


dropbox_ = create_dropbox_instance()
dir_path = os.path.dirname(os.path.relpath(__file__))
downloads_folder = dir_path + 'downloaded/dropbox/'

def upload_files(folder_name):
    # list images
    images_folder = dir_path + 'files/' + folder_name
    images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]

    # add start time
    timer(f"dropbox start upload {folder_name}")

    upload_entry_list = []
    for image in images:
        f = open(images_folder + image, 'rb')
        dropbox_.files_upload(f=f.read(), path=f"/{folder_name}{image}")
    #add stop time
    timer(f"dropbox stop upload {folder_name}")


def list_folder(folder_name):
    timer(f"dropbox start list folder {folder_name}")
    r = dropbox_.files_list_folder(path=f'/{folder_name}')
    timer(f"dropbox stop list folder {folder_name}")
    return r

def create_links_from_list(list_, folder_name):
    timer(f"dropbox start create sharing links {folder_name}")

    for file_ in list_:
        dropbox_.sharing_create_shared_link(file_.path_display)

    timer(f"dropbox stop create sharing links {folder_name}")

def download_files_from_folder(list_, folder_name, thread, node_count):
    dropbox_ = create_dropbox_instance()
    timer(f"dropbox start download files {folder_name} node {thread}")
    for file_ in list_:
        try:
            meta, res = dropbox_.files_download(path=file_.path_display)
        except Exception as e:
            with open("results.txt", 'a+') as results:
                results.writelines(f"Error raised trying to download file from dropbox in node {thread}. Max retries achived\n")
                continue
    timer(f"dropbox stop download files {folder_name} node {thread}")
    print_times(f"dropbox start download files {folder_name} node {thread}", f"dropbox stop download files {folder_name} node {thread}")


def run_dropbox_benchmark(images_folder):
    folder_name = images_folder
    upload_files(folder_name)
    print_times(f"dropbox start upload {folder_name}", f"dropbox stop upload {folder_name}")
    list_ = list_folder(folder_name).entries
    print_times(f"dropbox start list folder {folder_name}", f"dropbox stop list folder {folder_name}")
    create_links_from_list(list_, folder_name)
    print_times(f"dropbox start create sharing links {folder_name}", f"dropbox stop create sharing links {folder_name}")


def create_folder_structure_for_nodes(node_count):
    for i in range (0, node_count):
        Path(f"{downloads_folder}{node_count}/node{i}").mkdir(parents=True, exist_ok=True)

def multiple_node_read(images_folder, node_count):
    create_folder_structure_for_nodes(node_count=node_count)
    folder_name = images_folder
    list_ = list_folder(folder_name).entries
    # create threads
    threads = []
    for i in range (0,node_count):
        threads.append(threading.Thread(target=download_files_from_folder, args=(list_, images_folder, i, node_count)))

    # start threads
    for thread in threads:
        thread.start()

    # wait threads
    for thread in threads:
        thread.join()
