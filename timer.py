from datetime import datetime

times = {}

def timer(value):
    times[value] = datetime.now() 

def print_times(start_time_key, end_time_key):
    start_time = times[start_time_key]
    end_time   = times[end_time_key]
    time_elapsed = end_time - start_time
    with open("results.txt", 'a+') as results:
        results.writelines(f"Time elapsed between {start_time_key} and {end_time_key}: {time_elapsed}\n")
    print(f"Time elapsed between {start_time_key} and {end_time_key}: {time_elapsed}")