# import matplotlib.pyplot as plt
# import numpy as np

# # create initial plot
# fig, ax = plt.subplots()
# line, = ax.plot([], [], 'r-', linewidth=2)
# ax.set_xlim(0, 10)
# ax.set_ylim(-1, 1)

# # generate data
# t = np.linspace(0, 10, 1000)
# y = np.sin(t)

# # continuously update plot
# for i in range(1000):
#     line.set_data(t[:i], y[:i])
#     ax.draw_artist(ax.patch)
#     ax.draw_artist(line)
#     fig.canvas.blit(ax.bbox)
#     plt.pause(0.001)
 
import matplotlib.pyplot as plt
import numpy as np

# Generate initial data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure and axis objects
fig, ax = plt.subplots()

# Plot initial data
line, = ax.plot(x, y)

# Continuously update the plot
while True:
    # Update the data
    x += 0.3
    y = np.sin(x)
    # Update the plot
    line.set_ydata(y)
    # ax.relim()
    # ax.autoscale_view()
    # Redraw the plot
    fig.canvas.draw()
    # Pause for a short time
    plt.pause(0.0001)
