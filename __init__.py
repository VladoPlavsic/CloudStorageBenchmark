from dropbox_ import run_dropbox_benchmark, multiple_node_read as multiple_node_read_dropbox
from yandex_s3 import run_yandex_benchmark, multiple_node_read as multiple_node_read_yandex
import sys

images5 = {"images5/": 5}
images15 = {"images15/": 15}
images30 = {"images30/": 30}
images100 = {"images100/": 100}

images = [images5, images15, images30, images100]

def header_upload() -> str:
    header = \
    "************************************\n" \
    "* Dropbox vs Yandex s3 benchmark   *\n" \
    "************************************\n"\
    "*                                  *\n"\
    "*                                  *\n"\
    "* In this benchmark we will see 4  *\n"\
    "* of most common operations on     *\n"\
    "* cloud stored files:              *\n"\
    "*                                  *\n"\
    "* 1. Upload files                  *\n"\
    "* 2. List folder                   *\n"\
    "* 3. Create sharing links          *\n"\
    "* 4. Download files                *\n"\
    "* Total file count: 5              *\n"\
    "* Total file count: 15             *\n"\
    "* Total file count: 30             *\n"\
    "* Total file count: 100            *\n"\
    "* Average file size: 8200 bytes    *\n"\
    "* File type: .jpg                  *\n"\
    "*                                  *\n"\
    "************************************\n"\
    "\n"
    return header

def header_multi_thread_download() -> str:
    header = \
    "************************************\n" \
    "* Dropbox vs Yandex s3 benchmark   *\n" \
    "************************************\n"\
    "*                                  *\n"\
    "*                                  *\n"\
    "* In this benchmark we will see how*\n"\
    "* node count affects access speed  *\n"\
    "* for cloud stored files:          *\n"\
    "*                                  *\n"\
    "* Total node count: 2              *\n"\
    "* Total node count: 4              *\n"\
    "* Total node count: 8              *\n"\
    "* Total node count: 16             *\n"\
    "* Total node count: 32             *\n"\
    "*                                  *\n"\
    "* File count 30                    *\n"\
    "* Average file size: 8200 bytes    *\n"\
    "* File type: .jpg                  *\n"\
    "*                                  *\n"\
    "************************************\n"\
    "\n"
    return header

def header_all() -> str:
    header = \
    "*----------------------------------------------------------------------------------*\n"\
    "*                      Dropbox vs Yandex s3 benchmark                              *\n"\
    "*----------------------------------------------------------------------------------*\n"\
    "*                                                                                  *\n"\
    "* In this benchmark we will see 3 of most common operations on  cloud stored files *\n"\
    "*                                                                                  *\n"\
    "************************************************************************************\n"\
    "* 1. Upload files                                                                  *\n"\
    "* 2. List folder                                                                   *\n"\
    "* 3. Create sharing links                                                          *\n"\
    "* Total file count: 5                                                              *\n"\
    "* Total file count: 15                                                             *\n"\
    "* Total file count: 30                                                             *\n"\
    "* Total file count: 100                                                            *\n"\
    "************************************************************************************\n"\
    "*                                                                                  *\n"\
    "* And see how node count affects access speed for stored files:                    *\n"\
    "*                                                                                  *\n"\
    "************************************************************************************\n"\
    "* Total node count: 2                                                              *\n"\
    "* Total node count: 4                                                              *\n"\
    "* Total node count: 8                                                              *\n"\
    "* Total node count: 16                                                             *\n"\
    "* Total node count: 32                                                             *\n"\
    "* Total node count: 64                                                             *\n"\
    "* Total node count: 128                                                            *\n"\
    "* File count 30                                                                    *\n"\
    "* Average file size: 8200 bytes                                                    *\n"\
    "* File type: .jpg                                                                  *\n"\
    "************************************************************************************\n"\
    "\n"
    return header


def write_and_print(text, overwrite=False):
    print(text, end='')
    with open ('results.txt', 'a+' if not overwrite else 'w+') as results:
        results.writelines(text)

def upload_share_download():
    # dropbox benchmark
    write_and_print("---------------------------- DROPBOX UPLOAD, LIST, SHARE BENCHMARK START ----------------------------\n")
    for image in images:
        write_and_print(f"***STARTING BENCHMARK FOR: {list(image.values())[0]} images***\n")
        run_dropbox_benchmark(images_folder=list(image.keys())[0])
    write_and_print("---------------------------- DROPBOX UPLOAD, LIST, SHARE BENCHMARK STOP ----------------------------\n")
    # yandex benchmark
    write_and_print("--------------------------- YANDEX UPLOAD, LIST, SHARE S3 BENCHMARK START ---------------------------\n")
    for image in images:
        write_and_print(f"***STARTING BENCHMARK FOR: {list(image.values())[0]} images***\n")
        run_yandex_benchmark(folder_name=list(image.keys())[0])
    write_and_print("--------------------------- YANDEX UPLOAD, LIST, SHARE S3 BENCHMARK STOP  ---------------------------\n")


def multiple_node_download():
    node_counts = [1, 2, 4, 8, 16, 32, 64, 128]
    write_and_print("---------------------------- DROPBOX DOWNLOAD BENCHMARK START ----------------------------\n")
    for node_count in node_counts:
        write_and_print(f"***STARTING BENCHMARK FOR: {node_count} nodes***\n")
        multiple_node_read_dropbox(images_folder="images30/", node_count=node_count)
    write_and_print("---------------------------- DROPBOX DOWNLOAD BENCHMARK STOP  ----------------------------\n")
    write_and_print("--------------------------- YANDEX DOWNLOAD S3 BENCHMARK START ---------------------------\n")
    for node_count in node_counts():
        write_and_print(f"***STARTING BENCHMARK FOR: {node_count} nodes***\n")
        multiple_node_read_yandex(images_folder="images30/", node_count=node_count)
    write_and_print("--------------------------- YANDEX DOWNLOAD S3 BENCHMARK STOP  ---------------------------\n")

  
if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "-m":
        write_and_print(header_multi_thread_download(), overwrite=True)
        multiple_node_download()
    elif arg == "-u":
        write_and_print(header_upload(), overwrite=True)
        upload_share_download()
    elif arg == "-a":
        write_and_print(header_all(), overwrite=True)
        upload_share_download()
        write_and_print("\n\n")
        multiple_node_download()