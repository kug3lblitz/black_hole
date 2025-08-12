cmake_minimum_required(VERSION 3.10)
project(black_hole)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenGL
find_package(OpenGL REQUIRED)

# Find GLEW
find_path(GLEW_INCLUDE_DIR GL/glew.h
    PATHS /usr/local/include /opt/homebrew/include
)
find_library(GLEW_LIBRARY NAMES GLEW glew
    PATHS /usr/local/lib /opt/homebrew/lib
)

# Find GLFW
find_path(GLFW_INCLUDE_DIR GLFW/glfw3.h
    PATHS /usr/local/include /opt/homebrew/include
)
find_library(GLFW_LIBRARY NAMES glfw
    PATHS /usr/local/lib /opt/homebrew/lib
)

include_directories(
    ${GLEW_INCLUDE_DIR}
    ${GLFW_INCLUDE_DIR}
    ${OPENGL_INCLUDE_DIR}
)

add_executable(black_hole black_hole.cpp)

target_link_libraries(black_hole
    ${GLEW_LIBRARY}
    ${GLFW_LIBRARY}
    ${OPENGL_gl_LIBRARY}
)