import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def voxels_to_quads(voxel_map):
    max_i, max_j, max_k = voxel_map.voxels.shape
    quads = []

    def point(i, j, k):
        return np.array((
            voxel_map.lo[0] + i * voxel_map.resolution,
            voxel_map.lo[1] + j * voxel_map.resolution,
            voxel_map.lo[2] + k * voxel_map.resolution,
        ))

    for j in range(max_j):
        for k in range(max_k):
            last_val = 0
            for i in range(max_i):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    norm = np.array((1, 0, 0))
                else:
                    norm = np.array((-1, 0, 0))
                quads.append(([
                    point(i, j, k),
                    point(i, j+1, k),
                    point(i, j+1, k+1),
                    point(i, j, k+1),
                ], norm))
            if last_val:
                quads.append(([
                    point(i+1, j, k),
                    point(i+1, j+1, k),
                    point(i+1, j+1, k+1),
                    point(i+1, j, k+1),
                ], np.array((-1, 0, 0))))

    for i in range(max_i):
        for k in range(max_k):
            last_val = 0
            for j in range(max_j):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    norm = np.array((0, 1, 0))
                else:
                    norm = np.array((0, -1, 0))
                quads.append(([
                    point(i, j, k),
                    point(i+1, j, k),
                    point(i+1, j, k+1),
                    point(i, j, k+1),
                ], norm))
            if last_val:
                quads.append(([
                    point(i, j+1, k),
                    point(i+1, j+1, k),
                    point(i+1, j+1, k+1),
                    point(i, j+1, k+1),
                ], np.array((0, -1, 0))))

    for i in range(max_i):
        for j in range(max_j):
            last_val = 0
            for k in range(max_k):
                val = voxel_map.voxels[i, j, k]
                if val == last_val:
                    continue
                last_val = val
                if val == 1:
                    norm = np.array((0, 0, 1))
                else:
                    norm = np.array((0, 0, -1))
                quads.append(([
                    point(i, j, k),
                    point(i+1, j, k),
                    point(i+1, j+1, k),
                    point(i, j+1, k),
                ], norm))
            if last_val:
                quads.append(([
                    point(i, j, k+1),
                    point(i+1, j, k+1),
                    point(i+1, j+1, k+1),
                    point(i, j+1, k+1),
                ], np.array((0, 0, -1))))

    return quads

def draw_quads(quads, rot):
    glPushMatrix()
    glColor3fv((1., 0.7, 0.))
    glRotatef(4, 1, 0, 0)

    glPushMatrix()
    glRotatef(rot, 0, 1, 0)                    
    glBegin(GL_QUADS)
    for quad, normal in quads:
        glNormal3f(*normal)
        for pt in quad:
            glVertex3f(*pt)
    glEnd()
    glPopMatrix()

    glPopMatrix()

def show_voxels(voxel_map):
    dist = -np.linalg.norm(voxel_map.hi - voxel_map.lo)
    w = 800
    h = 800
    pygame.init()
    pygame.display.set_mode((w, h), OPENGL|DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)
    glClearColor(.2, .2, .3, 1.)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
    glTranslatef(0.0, -2.0, dist)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.2, .2, .2, 1.))
    glLightfv(GL_LIGHT0, GL_POSITION, (dist, dist, 0, 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1., .5, 0., 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1., 1., 1., 1.))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, (50.,))

    quads = voxels_to_quads(voxel_map)
    rot = 0
    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_quads(quads, rot)
        pygame.display.flip()
        pygame.time.wait(3)
        rot += 2.
