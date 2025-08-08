# Makefile for OpenGL programs on macOS
CXX = g++
CXXFLAGS = -std=c++11 -Wall -O2
INCLUDES = -I/opt/homebrew/include
LIBS = -L/opt/homebrew/lib -lglfw -lGLEW -framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo

# All target executables
TARGETS = 2D_lensing black_hole ray_tracing

# Source files
SOURCES_2D = 2D_lensing.cpp
SOURCES_BH = black_hole.cpp
SOURCES_RT = ray_tracing.cpp

# Object files
OBJECTS_2D = $(SOURCES_2D:.cpp=.o)
OBJECTS_BH = $(SOURCES_BH:.cpp=.o)
OBJECTS_RT = $(SOURCES_RT:.cpp=.o)

# Default target - build all
all: $(TARGETS)

# Build individual targets
2D_lensing: $(OBJECTS_2D)
	$(CXX) $(OBJECTS_2D) -o $@ $(LIBS)

black_hole: $(OBJECTS_BH)
	$(CXX) $(OBJECTS_BH) -o $@ $(LIBS)

ray_tracing: $(OBJECTS_RT)
	$(CXX) $(OBJECTS_RT) -o $@ $(LIBS)

# Compile source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS_2D) $(OBJECTS_BH) $(OBJECTS_RT) $(TARGETS)

# Help target
help:
	@echo "Available targets:"
	@echo "  make all         - Build all programs"
	@echo "  make 2D_lensing  - Build 2D gravitational lensing simulation"
	@echo "  make black_hole  - Build 3D black hole simulation (requires compute shader)"
	@echo "  make ray_tracing - Build ray tracing demo"
	@echo "  make clean       - Remove all build artifacts"
	@echo "  make help        - Show this help message"

# Phony targets
.PHONY: all clean help