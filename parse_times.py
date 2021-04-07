YANDEX_START = "--------------------------- YANDEX DOWNLOAD S3 BENCHMARK START ---------------------------"
YANDEX_STOP  = "--------------------------- YANDEX DOWNLOAD S3 BENCHMARK STOP  ---------------------------"


DROPBOX_START = "---------------------------- DROPBOX DOWNLOAD BENCHMARK START ----------------------------"
DROPBOX_STOP  = "---------------------------- DROPBOX DOWNLOAD BENCHMARK STOP  ----------------------------"

DROPBOX_START_LINE = 0 
DROPBOX_STOP_LINE = 0
YANDEX_START_LINE = 0
YANDEX_STOP_LINE = 0

NODES_LINE_TEMPLATE = "***STARTING BENCHMARK FOR: {0} nodes***"

NODES_COUNT = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000, None]

with open("results/download_1000nodes_1pc.txt") as file_:
    for num, line in enumerate(file_, 1):
        if YANDEX_START in line:
            YANDEX_START_LINE = num
        elif YANDEX_STOP in line:
            YANDEX_STOP_LINE = num
        elif DROPBOX_START in line:
            DROPBOX_START_LINE = num
        elif DROPBOX_STOP in line:
            DROPBOX_STOP_LINE = num

print(DROPBOX_START_LINE)
print(DROPBOX_STOP_LINE)
print(YANDEX_START_LINE)
print(YANDEX_STOP_LINE)

with open("results/download_1000nodes_1pc.txt") as file_:
    index = 0
    YANDEX_LINES = []
    DROPBOX_LINES = []
    for num, line in enumerate(file_, 1):
        if num > YANDEX_START_LINE and num < YANDEX_STOP_LINE:
            if NODES_LINE_TEMPLATE.format(NODES_COUNT[index]) in line:
                YANDEX_LINES.append(num)
                index += 1
        elif num == YANDEX_STOP_LINE:
            index = 0
        if num > DROPBOX_START_LINE and num < DROPBOX_STOP_LINE:
            if NODES_LINE_TEMPLATE.format(NODES_COUNT[index]) in line:
                DROPBOX_LINES.append(num)
                index += 1

print(YANDEX_LINES)
print(DROPBOX_LINES)

