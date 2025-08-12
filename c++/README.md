# Black Hole Simulation Project

A collection of OpenGL-based simulations demonstrating gravitational lensing and black hole physics.

## Overview

This project contains three different simulations:

1. **2D Lensing** (`2D_lensing.cpp`) - Interactive 2D visualization of light ray paths around a Schwarzschild black hole
2. **3D Black Hole** (`black_hole.cpp`) - 3D black hole simulation with GPU compute shaders
3. **Ray Tracing** (`ray_tracing.cpp`) - Basic ray tracing demonstration

## Features

- Real-time gravitational lensing simulation
- Interactive camera controls
- Accurate Schwarzschild metric calculations
- GPU-accelerated computations (3D version)
- Customizable ray spawning

## Dependencies

### Required Libraries
- **GLFW** (3.3+) - Window management and input handling
- **GLEW** (2.0+) - OpenGL extension loading
- **GLM** - OpenGL Mathematics library
- **OpenGL** (3.3+) - Graphics rendering

### Installation

#### macOS (via Homebrew)
```bash
brew install glew glfw glm
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install libglew-dev libglfw3-dev libglm-dev
```

#### Windows (MSYS2)
```bash
pacman -S mingw-w64-x86_64-glew mingw-w64-x86_64-glfw mingw-w64-x86_64-glm
```

## Building

### Using Make (macOS/Linux)
```bash
# Build all programs
make all

# Build individual programs
make 2D_lensing
make black_hole
make ray_tracing

# Clean build artifacts
make clean
```

### Compilation Status

- ✅ **2D_lensing** - Compiles and runs successfully on macOS
- ❌ **black_hole** - Requires C++11 initializer list support; may need additional fixes for macOS
- ✅ **ray_tracing** - Compiles with minor warnings

### Manual Compilation (macOS)
```bash
g++ -std=c++11 -O2 -I/opt/homebrew/include 2D_lensing.cpp -o 2D_lensing \
    -L/opt/homebrew/lib -lglfw -lGLEW -framework OpenGL -framework Cocoa \
    -framework IOKit -framework CoreVideo
```

### Manual Compilation (Linux)
```bash
g++ -std=c++11 -O2 2D_lensing.cpp -o 2D_lensing -lGL -lGLEW -lglfw
```

## Usage

### 2D Lensing Simulation

Run the simulation:
```bash
./2D_lensing
```

**Controls:**
- **Left Click**: Create a ray at mouse position (traveling rightward at speed c)
- **Middle Mouse + Drag**: Pan the view
- **Scroll**: Zoom in/out
- **Space**: Create a circle of rays around the black hole
- **C**: Clear all rays
- **ESC**: Exit

The simulation shows light rays bending around a Schwarzschild black hole (modeled after Sagittarius A*).

### 3D Black Hole Simulation

**Note**: Requires a GPU with compute shader support. Currently has compilation issues on macOS that need to be resolved.

```bash
./black_hole
```

This simulation uses GPU compute shaders (`geodesic.comp`) for high-performance geodesic calculations.

### Ray Tracing Demo

```bash
./ray_tracing
```

Basic ray tracing demonstration for testing the rendering pipeline.

## Physics

The simulations implement the Schwarzschild metric for non-rotating black holes:

- Schwarzschild radius: `rs = 2GM/c²`
- Geodesic equations for null rays (photons)
- Proper Runge-Kutta 4th order integration
- Conservation of energy and angular momentum

## Project Structure

```
black_hole/
├── 2D_lensing.cpp      # 2D gravitational lensing simulation
├── black_hole.cpp      # 3D black hole simulation (GPU)
├── geodesic.comp       # Compute shader for geodesic calculations
├── ray_tracing.cpp     # Ray tracing demo
├── Makefile           # Build configuration
└── README.md          # This file
```

## Video Tutorial

For a detailed explanation of the code and physics, check out the YouTube video:
https://www.youtube.com/watch?v=8-B6ryuBkCM

## Troubleshooting

### macOS Issues
- If you get linking errors, ensure Homebrew is installed in `/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel)
- For older macOS versions, you may need to add `-std=c++11` flag
- The 3D black_hole simulation currently has C++11 compatibility issues on macOS
- If the window appears blank in 2D_lensing, click to create rays or press Space for a ray circle

### Linux Issues
- If GLFW fails to create a window, ensure you have a display server running (X11/Wayland)
- You may need to install additional Mesa drivers for OpenGL support

### General Issues
- Black screen: Check that rays are being created (uncomment the initial ray in main())
- Performance issues: Reduce the number of rays or integration steps
- Compile errors: Ensure all dependencies are properly installed

## Future Improvements

1. Accretion disk visualization
2. Spacetime curvature grid overlay
3. Real-time performance optimizations
4. Kerr (rotating) black hole support
5. Relativistic jet simulation

## License

This project is open source. Feel free to use and modify for educational purposes.

## Acknowledgments

- Schwarzschild metric implementation based on general relativity principles
- GLFW/GLEW for cross-platform OpenGL support
- GLM for mathematical operations