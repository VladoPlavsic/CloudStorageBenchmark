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

file_name = "results/download_1000nodes_1pc_take2.txt"

with open(file_name) as file_:
    for num, line in enumerate(file_, 1):
        if YANDEX_START in line:
            YANDEX_START_LINE = num
        elif YANDEX_STOP in line:
            YANDEX_STOP_LINE = num
        elif DROPBOX_START in line:
            DROPBOX_START_LINE = num
        elif DROPBOX_STOP in line:
            DROPBOX_STOP_LINE = num

with open(file_name) as file_:
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


YANDEX_LINES.append(YANDEX_STOP_LINE)
DROPBOX_LINES.append(DROPBOX_STOP_LINE)

with open(file_name) as file_:
    index = 0
    count = 0
    dropbox_errors = 0
    yandex_errors = 0
    dropobx_mins = []
    yandex_mins = []
    temp_dropbox_secs = 0
    temp_yandex_secs = 0
    for num, line in enumerate(file_, 1):
        if num < DROPBOX_START_LINE:
            if num > YANDEX_LINES[index] and num < YANDEX_LINES[index + 1]:
                time = (line.split(':')[1:])
                if not time:
                    yandex_errors += 1
                else:
                    temp_yandex_secs += float(time[1]) * 60 + (float(time[2]))
                count += 1
            elif num == YANDEX_LINES[index + 1]:
                yandex_mins.append(temp_yandex_secs / count)
                temp_yandex_secs = 0
                index += 1
                count = 0
        elif num == DROPBOX_START_LINE:
            index = 0
            count = 0
        elif num <= DROPBOX_STOP_LINE:
            if num > DROPBOX_LINES[index] and num < DROPBOX_LINES[index + 1]:
                time = (line.split(':')[1:])
                if not time:
                    dropbox_errors += 1
                else:
                    temp_dropbox_secs += float(time[1]) * 60 + (float(time[2]))
                count += 1
            elif num == DROPBOX_LINES[index + 1]:
                dropobx_mins.append(temp_dropbox_secs / count)
                temp_dropbox_secs = 0
                index += 1
                count = 0
   

with open(f"results_{file_name.split('/')[-1]}", 'w+') as results:
    results.write(f"YANDEX TOTAL ERRORS: {yandex_errors}\n")
    results.write(f"DROPOBX TOTAL ERRORS: {dropbox_errors}\n")

    for i in range (0, len(yandex_mins)):
        results.write(f"Yandex s3 average for {NODES_COUNT[i]}: {yandex_mins[i]} c\n")

    results.write("**************************************\n")

    for i in range (0, len(dropobx_mins)):
        results.write(f"Dropbox average for {NODES_COUNT[i]} nodes: {dropobx_mins[i]} c\n")