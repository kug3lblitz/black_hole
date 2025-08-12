from vpython import *
import numpy as np
import random

# Set up the VPython canvas
scene = canvas(title="Black Hole Simulation", width=1000, height=800,
               background=color.black)
scene.range = 15  # Set the initial view range
scene.forward = vector(0, -0.3, -1)  # Slightly angled view

# Create instructions text
instructions = label(pos=vector(0, 14, 0), text="Drag to rotate view. Scroll to zoom.",
                     height=16, color=color.white, box=False, opacity=0.7)
speed_label = label(pos=vector(0, 12, 0),
                    text="Speed: 1.0x (use arrow keys to adjust)",
                    height=14, color=color.white, box=False, opacity=0.7)

# Simulation parameters
sim_speed = 1.0
black_hole_radius = 1.0
schwarzschild_radius = 1.0  # Scaled for visualization
n_particles = 200
n_disk_particles = 300
trail_length = 15

# Create the black hole
black_hole = sphere(pos=vector(0, 0, 0), radius=schwarzschild_radius,
                   color=color.black, opacity=1.0, emissive=False)

# Add a thin glowing edge to the black hole
event_horizon = ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0),
                    radius=schwarzschild_radius, thickness=0.05,
                    color=color.purple, opacity=0.6, emissive=True)

# Create accretion disk
accretion_disk = []
for i in range(n_disk_particles):
    theta = random.uniform(0, 2*np.pi)
    r = random.uniform(1.5, 4.0) * schwarzschild_radius
    phi = random.uniform(-0.1, 0.1)  # Small variation in disk plane

    # Position on disk
    x = r * cos(theta)
    y = r * sin(theta) * sin(phi)
    z = r * sin(theta) * cos(phi)

    # Colors from inner (hot) to outer (cooler) disk
    disk_color = color.hsv_to_rgb(vector(0.05 + 0.2*(r/4), 1, 1))

    # Create the particle
    particle = sphere(pos=vector(x, y, z), radius=0.05, color=disk_color,
                     opacity=0.8, emissive=True, make_trail=True,
                     trail_type="points", interval=5,
                     retain=trail_length)

    # Calculate orbital velocity (simplified)
    v_mag = sqrt(0.5/r)
    v_x = -v_mag * sin(theta)
    v_y = v_mag * cos(theta) * sin(phi)
    v_z = v_mag * cos(theta) * cos(phi)

    particle.velocity = vector(v_x, v_y, v_z)
    accretion_disk.append(particle)

# Create particles for orbital trajectories around the black hole
particles = []
trails = []

for i in range(n_particles):
    # Random spherical coordinates
    phi = random.uniform(0, 2*np.pi)
    theta = random.uniform(0, np.pi)
    r = random.uniform(3.0, 10.0) * schwarzschild_radius

    # Convert to cartesian
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    # Create the particle
    particle = sphere(pos=vector(x, y, z), radius=0.05,
                     color=color.blue, opacity=0.8, make_trail=True,
                     trail_type="points", interval=5, retain=trail_length)

    # Velocity components for orbital motion
    v_mag = sqrt(0.3/r)

    # Create a random orbital plane
    v_phi = random.uniform(0, 2*np.pi)
    v_x = v_mag * sin(v_phi)
    v_y = v_mag * cos(v_phi)
    v_z = random.uniform(-0.1, 0.1) * v_mag

    particle.velocity = vector(v_x, v_y, v_z)
    particle.alive = True
    particles.append(particle)

# Create stars (background)
n_stars = 500
stars = []
for i in range(n_stars):
    # Random position in a large sphere
    r = 25  # Far away
    phi = random.uniform(0, 2*np.pi)
    theta = random.uniform(0, np.pi)

    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    star = sphere(pos=vector(x, y, z), radius=random.uniform(0.02, 0.08),
                 color=color.white, opacity=0.8, emissive=True)
    stars.append(star)

# Create a gravitational lensing effect (artistic interpretation)
lensing_effect = ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0),
                     radius=schwarzschild_radius*1.5, thickness=0.8,
                     color=color.blue, opacity=0.15)

# Add a bit of ambient light glow around the black hole
glow = local_light(pos=vector(0, 0, 0), color=color.purple)

# Physics calculation functions
def gravitational_force(pos):
    """Calculate gravitational acceleration at position pos"""
    r_vector = pos
    r = mag(r_vector)

    if r < schwarzschild_radius:
        return vector(0, 0, 0)  # Inside black hole

    # Force magnitude (simplified)
    force_magnitude = 0.2 / (r**2)

    # Direction (normalized)
    direction = -norm(r_vector)

    return direction * force_magnitude

# Keyboard controls for simulation speed
def keyboard_control(evt):
    global sim_speed

    if evt.key == 'up':
        sim_speed *= 1.2
        speed_label.text = f"Speed: {sim_speed:.1f}x (use arrow keys to adjust)"
    elif evt.key == 'down':
        sim_speed /= 1.2
        speed_label.text = f"Speed: {sim_speed:.1f}x (use arrow keys to adjust)"
    elif evt.key == 'r':  # Reset view
        scene.camera.pos = vector(0, 0, 15)
        scene.forward = vector(0, 0, -1)

scene.bind('keydown', keyboard_control)

# Animation loop
dt = 0.05
t = 0
respawn_probability = 0.05  # Probability to respawn a captured particle

while True:
    rate(60)  # VPython's way to control the frame rate

    # Apply simulation speed
    time_step = dt * sim_speed
    t += time_step

    # Rotate the event horizon ring slowly
    event_horizon.rotate(angle=0.01, axis=vector(0, 1, 0))
    lensing_effect.rotate(angle=0.005, axis=vector(0, 1, 0))

    # Update disk particles
    for p in accretion_disk:
        pos = p.pos
        vel = p.velocity

        # Distance to black hole
        r = mag(pos)

        # Check if particle is captured by black hole
        if r < schwarzschild_radius:
            # Respawn the particle at the edge of the disk
            theta = random.uniform(0, 2*np.pi)
            r_new = random.uniform(3.0, 4.0) * schwarzschild_radius
            phi = random.uniform(-0.1, 0.1)

            p.pos = vector(r_new * cos(theta),
                          r_new * sin(theta) * sin(phi),
                          r_new * sin(theta) * cos(phi))

            # New orbital velocity
            v_mag = sqrt(0.5/r_new)
            p.velocity = vector(-v_mag * sin(theta),
                              v_mag * cos(theta) * sin(phi),
                              v_mag * cos(theta) * cos(phi))

            # Change color based on distance (hotter closer to black hole)
            p.color = color.hsv_to_rgb(vector(0.05 + 0.2*(r_new/4), 1, 1))

            # Clear the trail
            p.clear_trail()
            continue

        # Calculate acceleration due to gravity
        accel = gravitational_force(pos)

        # Update velocity
        p.velocity = p.velocity + accel * time_step

        # Update position
        p.pos = p.pos + p.velocity * time_step

        # Color based on speed (redshift/blueshift effect)
        speed = mag(p.velocity)
        p.color = color.hsv_to_rgb(vector(0.05 + 0.2*(r/4),
                                         min(1, 0.4 + speed),
                                         min(1, 0.4 + speed)))

    # Update orbital particles
    for p in particles:
        if not p.alive:
            continue

        pos = p.pos
        vel = p.velocity

        # Distance to black hole
        r = mag(pos)

        # Check if particle is captured by black hole
        if r < schwarzschild_radius:
            p.alive = False
            p.visible = False

            # Randomly respawn some particles
            if random.random() < respawn_probability:
                phi = random.uniform(0, 2*np.pi)
                theta = random.uniform(0, np.pi)
                r_new = random.uniform(6.0, 12.0) * schwarzschild_radius

                p.pos = vector(r_new * sin(theta) * cos(phi),
                             r_new * sin(theta) * sin(phi),
                             r_new * cos(theta))

                v_mag = sqrt(0.3/r_new)
                v_phi = random.uniform(0, 2*np.pi)

                p.velocity = vector(v_mag * sin(v_phi),
                                  v_mag * cos(v_phi),
                                  random.uniform(-0.1, 0.1) * v_mag)

                p.alive = True
                p.visible = True
                p.clear_trail()

            continue

        # Calculate acceleration due to gravity
        accel = gravitational_force(pos)

        # Update velocity
        p.velocity = p.velocity + accel * time_step

        # Update position
        p.pos = p.pos + p.velocity * time_step

        # Color based on speed
        speed = mag(p.velocity)
        p.color = color.hsv_to_rgb(vector(0.6, min(1, 0.4 + speed), min(1, 0.4 + speed)))
