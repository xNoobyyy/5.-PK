import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

plt.rcParams["toolbar"] = "None"

MAX_HISTORY = 10000  # Maximum number of points to keep in history

# Physical constants and simulation parameters
G = 1  # Universal gravitational constant
m1 = 10000  # Mass of Planet 1
m2 = 10000  # Mass of Planet 2
m3 = 10000  # Mass of Planet 3

# Initial conditions: [x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3]
state = np.array([-5, 10, 0, 0, 12, -7, 0, 0, -7, -3, 0, 0])
history = [state.copy()]

# Set up the plotting window
fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
plt.subplots_adjust(bottom=0.1)

fig.set_facecolor("white")
ax.set_facecolor("white")
ax.spines[["bottom", "left", "top", "right"]].set_color("black")
ax.tick_params(axis="x", colors="black")
ax.tick_params(axis="y", colors="black")

ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.grid(color="black", linewidth=0.2, alpha=0.4)
ax.set_box_aspect(1)

planet1 = ax.plot(
    [], [], "o", color="#00aaaa", markersize=10, label="Planet 1", alpha=0.8
)[0]
planet2 = ax.plot(
    [], [], "o", color="#aa00aa", markersize=10, label="Planet 2", alpha=0.8
)[0]
planet3 = ax.plot(
    [], [], "o", color="#aaaa00", markersize=10, label="Planet 3", alpha=0.8
)[0]

trail1 = ax.plot([], [], "-", color="#00aaaa", alpha=0.3, linewidth=1)[0]
trail2 = ax.plot([], [], "-", color="#aa00aa", alpha=0.3, linewidth=1)[0]
trail3 = ax.plot([], [], "-", color="#aaaa00", alpha=0.3, linewidth=1)[0]


def acceleration(state):
    # Unpack state for planets
    x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = state

    # Calculate relative positions
    r12 = np.array([x2 - x1, y2 - y1])
    r13 = np.array([x3 - x1, y3 - y1])
    r23 = np.array([x3 - x2, y3 - y2])

    # Calculate distances
    r12_mag = np.linalg.norm(r12)
    r13_mag = np.linalg.norm(r13)
    r23_mag = np.linalg.norm(r23)

    # Calculate gravitational accelerations
    a1 = G * (m2 * r12 / r12_mag**3 + m3 * r13 / r13_mag**3)
    a2 = G * (m1 * (-r12) / r12_mag**3 + m3 * r23 / r23_mag**3)
    a3 = G * (m1 * (-r13) / r13_mag**3 + m2 * (-r23) / r23_mag**3)

    return np.array(
        [vx1, vy1, a1[0], a1[1], vx2, vy2, a2[0], a2[1], vx3, vy3, a3[0], a3[1]]
    )


def euler(state, dt=0.01):
    return state + acceleration(state) * dt


def rk4(state, dt=0.001):
    k1 = acceleration(state)
    k2 = acceleration(state + dt * k1 / 2)
    k3 = acceleration(state + dt * k2 / 2)
    k4 = acceleration(state + dt * k3)
    return state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def update(frame):
    # Update the state of the system
    global history
    history.append(rk4(history[-1]))
    if len(history) > MAX_HISTORY:
        history.pop(0)
    points = np.array(history)

    # Update the positions of the planets and their trails
    planet1.set_data(np.array([points[-1, 0]]), np.array([points[-1, 1]]))
    planet2.set_data(np.array([points[-1, 4]]), np.array([points[-1, 5]]))
    planet3.set_data(np.array([points[-1, 8]]), np.array([points[-1, 9]]))
    trail1.set_data(np.array([points[:, 0]]), np.array([points[:, 1]]))
    trail2.set_data(np.array([points[:, 4]]), np.array([points[:, 5]]))
    trail3.set_data(np.array([points[:, 8]]), np.array([points[:, 9]]))


def reset(event):
    # Reset the simulation to the initial conditions
    global history
    history = [state.copy()]

    planet1.set_data([], [])
    planet2.set_data([], [])
    planet3.set_data([], [])
    trail1.set_data([], [])
    trail2.set_data([], [])
    trail3.set_data([], [])
    plt.draw()


# Create a button to reset the simulation
reset_button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), "Reset")
reset_button.on_clicked(reset)

# Start animation
ani = FuncAnimation(fig, update, interval=10, cache_frame_data=False)
plt.show()
