import time

frequency = 256
while_tick_rate = 1/frequency
duration = 10

durations = [1, 5, 10, 20, 100]

for duration in durations:
    time_start = time.time()
    for i in range(frequency * duration):
        now = time.time()
        # print(i)
        elapsed = time.time()  - now
        time.sleep(while_tick_rate - elapsed)

    time_end = time.time()
    elapsed_time = time_end - time_start
    print(f"Total Time: {duration}, {elapsed_time}")
    
    
