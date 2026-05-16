import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('TkAgg')

# figure creation
fig, ax = plt.subplots()

# Time values
x = np.linspace(0, 10, 500)

# first waveform
y = np.sin(x)

# line plot
line, = ax.plot(x, y)

# Graph settings
ax.set_title("Simulated Seismic Waveform")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.set_ylim(-3, 3)

# Update function
def update(frame):

    # Simulated seismic signal
    noise = np.random.normal(0, 0.3, len(x))

    seismic_wave = (
        np.sin(x * 2 + frame * 0.1)
        + 0.5 * np.sin(x * 6 + frame * 0.05)
        + noise
    )

    line.set_ydata(seismic_wave)

    return line,

# Animation of seismic waveform
ani = FuncAnimation(
    fig,
    update,
    interval=50,
    blit=True,
    cache_frame_data=False
)

# Show graph
plt.show()