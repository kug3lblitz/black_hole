from vpython import *
import numpy as np
import random
from math import pi, sin, cos, sqrt

# Set up the VPython canvas with performance-friendly settings
scene = canvas(title="Optimized Black Hole Simulation", width=1000, height=800,
               background=color.black)
scene.range = 15
scene.forward = vector(0, -0.2, -1)
scene.autoscale = False  # Disable autoscaling for performance

# Create simpler instructions
instructions = label(pos=vector(0, 13, 0),
                     text="Arrow keys: adjust speed | L: toggle lensing effects",
                     height=14, color=color.white, box=False, opacity=0.8)
speed_label = label(pos=vector(0, 11.5, 0), text="Speed: 1.0x",
                     height=14, color=color.white, box=False, opacity=0.8)

# Simulation parameters - reduced for performance
sim_speed = 1.0
black_hole_radius = 1.0
n_particles = 75      # Reduced from 200
n_disk_particles = 150 # Reduced from 400
trail_length = 10     # Reduced from 20
enable_lensing = True # Toggle for most expensive effect

# Create the black hole (central object)
black_hole = sphere(pos=vector(0, 0, 0), radius=black_hole_radius,
                   color=color.black, shininess=0)

# Event horizon ring
event_horizon = ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0),
                    radius=black_hole_radius, thickness=0.08,
                    color=color.purple, opacity=0.7, emissive=True)

# More efficient lensing effect - just one ring
lensing_ring = ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0),
                   radius=black_hole_radius*1.8, thickness=0.3,
                   color=color.blue, opacity=0.15, emissive=True)

# Create a subset of stars that can be affected by lensing
n_sky_stars = 300  # Reduced from 3000
sky_stars = []

# Create fewer background stars for better performance
for i in range(n_sky_stars):
    phi = random.uniform(0, 2*pi)
    theta = random.uniform(0, pi)
    r = 30  # Distance from center

    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    star_size = random.uniform(0.05, 0.15)  # Slightly larger stars for visibility

    # Simplified color selection
    if random.random() < 0.8:  # 80% white stars
        star_color = color.white
    elif random.random() < 0.5:  # 10% blue stars
        star_color = color.cyan
    else:  # 10% red/yellow stars
        star_color = color.yellow

    star = sphere(pos=vector(x, y, z), radius=star_size,
                 color=star_color, opacity=0.8, emissive=True)
    sky_stars.append(star)

    # Store original position for lensing
    star.orig_pos = vector(x, y, z)
    star.orig_size = star_size

# --------- IMPROVED ACCRETION DISK WITH FEWER PARTICLES ---------
accretion_disk = []
for i in range(n_disk_particles):
    theta = random.uniform(0, 2*pi)
    r = (1.8 + random.random()**0.5 * 2.5) * black_hole_radius

    # Flatter disk for performance
    h = random.uniform(-0.08, 0.08)

    # Position on disk
    x = r * cos(theta)
    y = h
    z = r * sin(theta)

    # Temperature decreases with distance
    temp_factor = 1 - (r - 1.8*black_hole_radius)/(4*black_hole_radius)
    hue = 0.05 + 0.15 * (1-temp_factor)  # 0.05=red, 0.2=yellow

    # Simpler particle with shorter trails for performance
    particle = sphere(pos=vector(x, y, z), radius=0.05,
                    color=color.hsv_to_rgb(vector(hue, 0.9, 0.9)),
                    opacity=0.9, emissive=True, make_trail=(i % 3 == 0),  # Only 1/3 particles have trails
                    trail_type="points", interval=5, retain=8)

    # Calculate orbital velocity
    v_mag = sqrt(0.5/r)
    particle.velocity = vector(-v_mag * sin(theta), 0, v_mag * cos(theta))
    particle.temperature = temp_factor
    accretion_disk.append(particle)

# --------- ORBITAL PARTICLES WITH OPTIMIZED TRAILS ---------
particles = []
for i in range(n_particles):
    # Random spherical coordinates
    phi = random.uniform(0, 2*pi)
    theta = random.uniform(0, pi)
    r = random.uniform(4.0, 12.0) * black_hole_radius

    # Convert to cartesian
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    # Only create trails for some particles (1/3)
    has_trail = (i % 3 == 0)

    particle = sphere(pos=vector(x, y, z), radius=0.08,
                    color=color.cyan, opacity=0.9, emissive=True, make_trail=has_trail,
                    trail_type="points", interval=4, retain=trail_length)

    # Velocity for orbital motion
    v_mag = sqrt(0.4/r) * random.uniform(0.7, 1.3)
    v_phi = random.uniform(0, 2*pi)

    particle.velocity = vector(v_mag * sin(v_phi),
                              v_mag * cos(v_phi),
                              random.uniform(-0.2, 0.2) * v_mag)
    particle.alive = True
    particles.append(particle)

# Add one subtle light for better rendering
central_glow = local_light(pos=vector(0,0,0), color=color.purple)

# Simplified relativistic jets
jet1 = cylinder(pos=vector(0, 0.5, 0), axis=vector(0, 3, 0), radius=0.2,
              color=color.blue, opacity=0.2, emissive=True)
jet2 = cylinder(pos=vector(0, -0.5, 0), axis=vector(0, -3, 0), radius=0.2,
              color=color.blue, opacity=0.2, emissive=True)

# Optimized physics calculation
def gravitational_force(pos):
    r_vector = pos
    r_squared = r_vector.x**2 + r_vector.y**2 + r_vector.z**2
    r = sqrt(r_squared)

    if r < black_hole_radius:
        return vector(0, 0, 0)

    # More efficient calculation
    force_magnitude = 0.2 / r_squared
    direction = -r_vector / r

    return direction * force_magnitude

# Simplified lensing calculation (more efficient)
def apply_lensing():
    # Only apply lensing if enabled
    if not enable_lensing:
        # Reset stars to original positions
        for star in sky_stars:
            star.pos = star.orig_pos
            star.radius = star.orig_size
        return

    # Apply to a random subset of stars each frame for performance
    sample_size = min(50, len(sky_stars))  # Process max 50 stars per frame
    sample_stars = random.sample(sky_stars, sample_size)

    for star in sample_stars:
        # Vector from black hole to star
        r_vector = star.orig_pos
        r = mag(r_vector)

        # Direction from black hole to star
        direction = norm(r_vector)

        # Calculate simplified lensing effect
        if r > black_hole_radius * 3:
            deflection = 1.5 * black_hole_radius / r
            if deflection < 0.7:
                # Move star position slightly toward the black hole
                star.pos = star.orig_pos - direction * deflection

                # Make stars appear larger when lensed
                star.radius = star.orig_size * (1 + deflection * 2)
            else:
                # Stars that would be extremely distorted are hidden
                star.visible = False
        else:
            star.visible = False

# Keyboard controls
def keyboard_control(evt):
    global sim_speed, enable_lensing

    if evt.key == 'up':
        sim_speed *= 1.2
        speed_label.text = f"Speed: {sim_speed:.1f}x"
    elif evt.key == 'down':
        sim_speed /= 1.2
        speed_label.text = f"Speed: {sim_speed:.1f}x"
    elif evt.key == 'l':  # Toggle lensing effect
        enable_lensing = not enable_lensing
        # Show/hide the lensing ring based on the toggle
        lensing_ring.visible = enable_lensing
        instructions.text = f"Arrow keys: adjust speed | L: toggle lensing effects (currently {'ON' if enable_lensing else 'OFF'})"

scene.bind('keydown', keyboard_control)

# Animation loop with performance optimizations
dt = 0.05
t = 0
respawn_probability = 0.03  # Reduced from 0.05
frame_count = 0

# Main simulation loop
while True:
    # Reduced frame rate target for better performance
    rate(30)  # Reduced from 60

    # Time step calculation
    time_step = dt * sim_speed
    t += time_step
    frame_count += 1

    # Only rotate lensing ring every other frame
    if frame_count % 2 == 0:
        lensing_ring.rotate(angle=0.005, axis=vector(0, 1, 0))

    # Only update lensing effects every few frames
    if frame_count % 5 == 0 and enable_lensing:
        apply_lensing()

    # Update accretion disk particles
    for p in accretion_disk:
        pos = p.pos
        r = mag(pos)

        # Check if particle is captured
        if r < black_hole_radius:
            # Respawn the particle at the edge of the disk
            theta = random.uniform(0, 2*pi)
            r_new = random.uniform(2.5, 4.0) * black_hole_radius
            h = random.uniform(-0.08, 0.08)

            p.pos = vector(r_new * cos(theta), h, r_new * sin(theta))

            # New orbital velocity
            v_mag = sqrt(0.5/r_new)
            p.velocity = vector(-v_mag * sin(theta), 0, v_mag * cos(theta))

            if p.make_trail:
                p.clear_trail()
            continue

        # Calculate acceleration due to gravity
        accel = gravitational_force(pos)

        # Update velocity and position in one step
        p.velocity = p.velocity + accel * time_step
        p.pos = p.pos + p.velocity * time_step

        # Only update color on some frames for performance
        if frame_count % 3 == 0 and p.temperature > 0.5:
            speed = mag(p.velocity)
            p.color = color.hsv_to_rgb(vector(0.05 + 0.15*(1-p.temperature),
                                            min(1, 0.7 + 0.3*speed),
                                            min(1, 0.7 + 0.3*speed)))

    # Update orbital particles
    active_count = 0
    for p in particles:
        if not p.alive:
            continue

        active_count += 1
        pos = p.pos
        r = mag(pos)

        # Check if particle is captured
        if r < black_hole_radius:
            p.alive = False
            p.visible = False

            # Randomly respawn some particles (less frequently)
            if random.random() < respawn_probability:
                phi = random.uniform(0, 2*pi)
                theta = random.uniform(0, pi)
                r_new = random.uniform(6.0, 12.0) * black_hole_radius

                p.pos = vector(r_new * sin(theta) * cos(phi),
                             r_new * sin(theta) * sin(phi),
                             r_new * cos(theta))

                v_mag = sqrt(0.4/r_new) * random.uniform(0.8, 1.2)
                v_phi = random.uniform(0, 2*pi)

                p.velocity = vector(v_mag * sin(v_phi),
                                  v_mag * cos(v_phi),
                                  random.uniform(-0.2, 0.2) * v_mag)

                p.alive = True
                p.visible = True
                if p.make_trail:
                    p.clear_trail()
            continue

        # Calculate acceleration and update position
        accel = gravitational_force(pos)
        p.velocity = p.velocity + accel * time_step
        p.pos = p.pos + p.velocity * time_step

        # Only update color occasionally for performance
        if frame_count % 5 == 0 and p.make_trail:
            speed = mag(p.velocity)
            # Simplified color calculation
            p.color = color.hsv_to_rgb(vector(0.6, min(1, 0.4 + speed), 0.9))
