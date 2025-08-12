import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects

# Set up a dark background style for better visuals
plt.style.use('dark_background')

# Create custom colormap for particles (blue to red hot)
colors = [(0, 0, 0.8), (0, 0.8, 1), (1, 1, 1), (1, 0.8, 0), (1, 0, 0)]
custom_cmap = LinearSegmentedColormap.from_list('custom_hot', colors)

# Initialize particles
n_particles = 300
particles = np.random.rand(n_particles, 4)
particles[:, 0] = (particles[:, 0] - 0.5) * 20  # x position
particles[:, 1] = (particles[:, 1] - 0.5) * 20  # y position
particles[:, 2] = (particles[:, 2] - 0.5) * 0.8  # x velocity
particles[:, 3] = (particles[:, 3] - 0.5) * 0.8  # y velocity

# Create some background stars (non-moving)
n_stars = 500
stars_x = np.random.uniform(-10, 10, n_stars)
stars_y = np.random.uniform(-10, 10, n_stars)
star_sizes = np.random.uniform(0.05, 0.3, n_stars)

# Keep track of particle trails (last 20 positions for each particle)
trail_length = 20
trails = [[] for _ in range(n_particles)]

# Parameters for the black hole
black_hole_radius = 0.5
accretion_disk_radius = 1.2

# Figure setup with high resolution and correct aspect ratio
fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
fig.tight_layout()

# Set up the plot
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.axis('off')  # Hide the axes

# Draw stars
stars = ax.scatter(stars_x, stars_y, s=star_sizes, color='white', alpha=0.7)

# Create accretion disk (for visual effect)
theta = np.linspace(0, 2*np.pi, 150)
r = np.random.uniform(black_hole_radius, accretion_disk_radius, 150)
x = r * np.cos(theta)
y = r * np.sin(theta)
disk_points = np.column_stack([x, y])
disk_colors = np.sqrt(x**2 + y**2)
disk = ax.scatter(x, y, c=disk_colors, cmap='plasma', s=3, alpha=0.8)

# Draw the black hole
black_hole = plt.Circle((0, 0), black_hole_radius, color='black', zorder=10)
black_hole_glow = plt.Circle((0, 0), black_hole_radius*1.1, color='#303030',
                           alpha=0.6, zorder=9)
black_hole_edge = plt.Circle((0, 0), black_hole_radius, color='#8A2BE2',
                          fill=False, linewidth=1.5, alpha=0.8, zorder=11)
ax.add_patch(black_hole_glow)
ax.add_patch(black_hole)
ax.add_patch(black_hole_edge)

# Initial particle scatter plot
scatter = ax.scatter([], [], s=[], c=[], cmap=custom_cmap, alpha=0.8, zorder=5)

# Create line collections for trails
line_segments = LineCollection([], linewidths=0.5, zorder=4)
ax.add_collection(line_segments)

# Title with glow effect
title = ax.text(0.5, 0.95, 'BLACK HOLE SIMULATION',
                horizontalalignment='center',
                transform=ax.transAxes, color='white',
                fontsize=18, fontweight='bold')
title.set_path_effects([path_effects.Stroke(linewidth=3, foreground='#303030'),
                       path_effects.Normal()])

def update(frame):
    global particles, trails

    # Calculate physics for each particle
    for i in range(len(particles)):
        # Calculate distance to center (black hole)
        r = np.sqrt(particles[i, 0]**2 + particles[i, 1]**2)

        # If particle gets too close to black hole, create a new one
        if r < black_hole_radius:
            # Spawn new particle on the edge
            angle = np.random.uniform(0, 2*np.pi)
            particles[i, 0] = 8 * np.cos(angle)  # Spawn from distance
            particles[i, 1] = 8 * np.sin(angle)
            particles[i, 2] = np.random.uniform(-0.5, 0.5)  # Random velocity
            particles[i, 3] = np.random.uniform(-0.5, 0.5)
            trails[i] = []  # Reset trail
            continue

        # Calculate gravitational force (stronger near black hole)
        force_magnitude = 0.2 / (r**1.5)  # Adjusted for visual effect

        # Force direction (towards center)
        fx = -particles[i, 0] / r * force_magnitude
        fy = -particles[i, 1] / r * force_magnitude

        # Update velocity
        particles[i, 2] += fx
        particles[i, 3] += fy

        # Add some randomness for visual interest
        if frame % 10 == 0 and np.random.random() < 0.1:
            particles[i, 2] += np.random.uniform(-0.05, 0.05)
            particles[i, 3] += np.random.uniform(-0.05, 0.05)

        # Update position
        particles[i, 0] += particles[i, 2]
        particles[i, 1] += particles[i, 3]

        # Update trails
        trails[i].append((particles[i, 0], particles[i, 1]))
        if len(trails[i]) > trail_length:
            trails[i].pop(0)

    # Update scatter plot
    speeds = np.sqrt(particles[:, 2]**2 + particles[:, 3]**2)
    distances = np.sqrt(particles[:, 0]**2 + particles[:, 1]**2)
    sizes = 2 + 8 * speeds  # Particle size based on speed

    # Update particle positions and colors
    scatter.set_offsets(particles[:, :2])
    scatter.set_sizes(sizes)
    scatter.set_array(speeds)  # Color based on speed

    # Update trails
    segments = [trail for trail in trails if len(trail) > 1]
    line_segments.set_segments(segments)

    # Calculate trail colors based on position in the trail
    colors = []
    for trail in trails:
        if len(trail) > 1:
            # Fade from particle color to transparent
            for i in range(len(trail)-1):
                alpha = 0.1 + 0.9 * i / (len(trail)-1)
                colors.append(np.array([1, 1, 1, alpha]))

    if colors:
        line_segments.set_color(np.array(colors))

    return scatter, line_segments

# Create animation with faster frame rate for smoother motion
animation = FuncAnimation(fig, update, frames=200, interval=25, blit=True)
plt.show()
