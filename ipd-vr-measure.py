#!/usr/bin/python

import pygame
import sys
import os

os.environ ['SDL_VIDEO_WINDOW_POS'] = '3840,0'
#os.environ ['SDL_VIDEO_WINDOW_POS'] = '0,0'
pygame.init ()
pygame.mouse.set_visible (False)
pygame.key.set_repeat (10000, 10000)

screen_width = 2400
screen_height = 1200
circle_radius = 20
circle_color = (255, 255, 255)
line_color = (255, 255, 255)

screen = pygame.display.set_mode ((screen_width, screen_height), pygame.NOFRAME)

initial_ipd = 80.
axes_distance = 68.

def pixels_to_ipd (x):
    return (axes_distance * x / (screen_width / 2.))

def ipd_to_pixels (x):
    return (int ((screen_width / 2.) * x / axes_distance))

x = int ((screen_width - ipd_to_pixels (initial_ipd)) / 2)
y = int ((screen_height - circle_radius) / 2)

def cross (screen, col, pos, size, wid):
    pygame.draw.line (screen, col, (pos [0] - size, pos [1]), (pos [0] + size, pos [1]), wid)
    pygame.draw.line (screen, col, (pos [0], pos [1] - size), (pos [0], pos [1] + size), wid)    

clock = pygame.time.Clock ()

state = 'converge'

while True:

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if state == 'converge':
                x_min  = x
                state = 'diverge'
            else:
                x_max  = x
                state = 'quit'
            for e in pygame.event.get ():
                pass

    if state == 'quit':
        break

    if state == 'converge':
        x = min (screen_width / 2 - circle_radius, x + 1)
    else:
        x = max (1, x - 1)
    
    screen.fill ((0, 0, 0))
    pygame.draw.circle (screen, circle_color, (x, y), circle_radius, 1)
    pygame.draw.circle (screen, circle_color, (screen_width - x, y), circle_radius, 1)
    cross (screen, line_color, (x, y), circle_radius, 1)
    cross (screen, line_color, (screen_width - x, y), circle_radius, 1)

    pygame.display.flip ()

    sys.stdout.write ('\r%.3f' % pixels_to_ipd (screen_width - 2 * x))
    sys.stdout.flush ()
    
    clock.tick (2)

ipd_max = screen_width - (2 * x_max) 
ipd_min = screen_width - (2 * x_min)

pygame.quit ()
print ("\nL'IPD min est de %f mm\nL'IPD max est de %f mm"
       % (pixels_to_ipd (ipd_min), pixels_to_ipd (ipd_max)))
