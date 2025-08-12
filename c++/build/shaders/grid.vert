#version 330 core

layout(location = 0) in vec3 aPos;      // Vertex position
layout(location = 1) in vec3 aColor;    // Vertex color

out vec3 vColor;

uniform mat4 uViewProj; // Combined view-projection matrix

void main()
{
    gl_Position = uViewProj * vec4(aPos, 1.0);
    vColor = aColor;
}