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

def draw_points(points, rot, res):
    glPushMatrix()
    glColor3fv((1., 0.7, 0.))
    glRotatef(4, 1, 0, 0)

    glPushMatrix()
    glRotatef(rot, 0, 1, 0)
    glBegin(GL_TRIANGLES)
    for point in points:
        glNormal3f(1, 0, 0)
        for delta in [[0, 0, 0], [0, res, 0], [0, 0, res]]:
            glVertex3f(*(point[:3] + delta))
        # glNormal3f(0, 0, 1)
        # for delta in [[0, 0, 0], [0, res, 0], [res, 0, 0]]:
        #     glVertex3f(*(point[:3] + delta))
    glEnd()
    glPopMatrix()

    glPopMatrix()


def draw_loop(draw_func, size):
    dist = -np.linalg.norm(size)
    w = 800
    h = 800
    pygame.init()
    pygame.display.set_mode((w, h), OPENGL|DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)
    glClearColor(.0, .0, .1, 1.)

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

    rot = 0
    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_func(rot=rot)
        pygame.display.flip()
        rot += 2.
