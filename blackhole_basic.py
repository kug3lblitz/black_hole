import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# A much simpler gravity well simulation
# Just basic Newtonian physics - no relativity

particles = np.random.rand(100, 4)  # [x, y, vx, vy]
particles[:, 0] = (particles[:, 0] - 0.5) * 10  # x position
particles[:, 1] = (particles[:, 1] - 0.5) * 10  # y position
particles[:, 2] = (particles[:, 2] - 0.5) * 0.5  # x velocity
particles[:, 3] = (particles[:, 3] - 0.5) * 0.5  # y velocity

fig, ax = plt.subplots()
scatter = ax.scatter(particles[:, 0], particles[:, 1], s=1)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

def update(frame):
    # Simple gravity calculation
    for i in range(len(particles)):
        # Calculate distance to center
        r = np.sqrt(particles[i, 0]**2 + particles[i, 1]**2)
        if r < 0.1:  # Inside black hole
            particles[i, 0] = 10  # Respawn
            particles[i, 1] = 0
            particles[i, 2] = 0
            particles[i, 3] = 0.3
            continue

        # Force direction (towards center)
        fx = -particles[i, 0] / (r**3)
        fy = -particles[i, 1] / (r**3)

        # Update velocity
        particles[i, 2] += fx * 0.01
        particles[i, 3] += fy * 0.01

        # Update position
        particles[i, 0] += particles[i, 2]
        particles[i, 1] += particles[i, 3]

    scatter.set_offsets(particles[:, :2])
    return scatter,

animation = FuncAnimation(fig, update, frames=100, interval=30, blit=True)
plt.show()
