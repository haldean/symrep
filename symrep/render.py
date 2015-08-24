import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def draw_voxels(voxel_map):
    max_i, max_j, max_k = voxel_map.voxels.shape

    def point(i, j, k):
        glVertex3f(
            voxel_map.lo[0] + i * voxel_map.resolution,
            voxel_map.lo[1] + j * voxel_map.resolution,
            voxel_map.lo[2] + k * voxel_map.resolution,
        )

    glColor3fv((1., 0.7, 0.))
    glBegin(GL_QUADS)

    for j in range(max_j):
        for k in range(max_k):
            last_val = 0
            for i in range(max_i):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    glNormal3f(1, 0, 0)
                else:
                    glNormal3f(-1, 0, 0)
                point(i, j, k)
                point(i, j+1, k)
                point(i, j+1, k+1)
                point(i, j, k+1)
            if last_val:
                glNormal3f(-1, 0, 0)
                point(i+1, j, k)
                point(i+1, j+1, k)
                point(i+1, j+1, k+1)
                point(i+1, j, k+1)

    for i in range(max_i):
        for k in range(max_k):
            last_val = 0
            for j in range(max_j):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    glNormal3f(0, 1, 0)
                else:
                    glNormal3f(0, -1, 0)
                point(i, j, k)
                point(i+1, j, k)
                point(i+1, j, k+1)
                point(i, j, k+1)
            if last_val:
                glNormal3f(0, -1, 0)
                point(i, j+1, k)
                point(i+1, j+1, k)
                point(i+1, j+1, k+1)
                point(i, j+1, k+1)

    for i in range(max_i):
        for j in range(max_j):
            last_val = 0
            for k in range(max_k):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    glNormal3f(0, 0, 1)
                else:
                    glNormal3f(0, 0, -1)
                point(i, j, k)
                point(i+1, j, k)
                point(i+1, j+1, k)
                point(i, j+1, k)
            if last_val:
                glNormal3f(0, 0, -1)
                point(i, j, k+1)
                point(i+1, j, k+1)
                point(i+1, j+1, k+1)
                point(i, j+1, k+1)
    glEnd()

def show_voxels(voxel_map):
    dist = -np.linalg.norm(voxel_map.hi - voxel_map.lo)
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)
    glClearColor(.7, .7, .7, 1.)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.2, .2, .2, 1.))
    glLightfv(GL_LIGHT0, GL_POSITION, (0., dist, -dist, 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1., .5, 0., 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1., 1., 1., 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, (50.,))

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 640 / 480.0, 0.1, 100.0)
    glTranslatef(0.0, -2.0, dist)
    glRotatef(25, 1, 0, 0)

    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 1, 0)                    

        draw_voxels(voxel_map)
        pygame.display.flip()
        pygame.time.wait(0)
