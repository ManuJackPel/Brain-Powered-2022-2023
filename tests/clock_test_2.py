import time

t_start = time.time()

for i in range(5):
    time.sleep(1)

print(time.time() - t_start)
