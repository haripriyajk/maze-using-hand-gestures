# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 23:05:30 2020

@author: HP
"""

from tkinter import *
from random import randint
 
 
cell_size = 50 #pixels
ms = 10 # rows and columns
 
# creates a list with 50 x 50 "w" items
T=[[1,0,0,0,0,0,1,1,1,1],
   [1,1,1,1,1,0,1,0,1,1],
   [1,1,1,0,1,0,1,1,1,1],
   [1,0,1,0,1,0,1,0,0,1],
   [1,0,1,0,1,0,1,0,1,1],
   [1,0,0,0,1,0,1,0,1,0],
   [1,0,1,1,1,0,1,0,1,0],
   [1,0,1,0,0,0,1,0,1,1],
   [0,1,1,1,1,1,1,0,1,1],
   [1,1,1,1,0,0,0,0,1,1]] 
 
def create():
    "Create a rectangle with draw function (below) with random color"
    for row in range(ms):
        for col in range(ms):
            if T[row][col] == 0:
                color = 'grey'
            elif T[row][col] == 1:
                #color = 'black'
                color = 'white'
            draw(row, col, color)
 
 
def draw(row, col, color):
    x11 = col * cell_size
    y11 = row * cell_size
    x22 = x11 + cell_size
    y22 = y11 + cell_size
    ffs.create_rectangle(x11, y11, x22, y22, fill=color)
 

scr = 1
scc = ms-1
ccr, ccc = scr, scc
x1 = 0
y1 = 0
print(scr, scc)
print(ccr, ccc)
 
 
window = Tk()
window.title('Maze')
canvas_side = ms*cell_size
ffs = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
ffs.pack()
 
 
create()
x1 = 0
y1 = 0
start_color = 'blue'
end_color = 'green'
draw(0, 0, start_color)
draw(ms-1, ms-1, end_color)


def draw_rect():
    draw(x1, y1,"blue")


def del_rect():
    draw(x1, y1,"white")


def move(event):
    global x1, y1
    # print(event.char)
    del_rect()
    #col = w = x1
    #row = h = y1
    #print("before", T[row][col])
    print(x1,y1)
    if event.char == "a":
        if(y1 - 1 >= 0  and y1 - 1 < ms):
            if T[x1][y1 - 1] == 1:
                y1 -= 1
    elif event.char == "d":
        if (y1 + 1 >= 0 and y1 + 1 < ms):
            if T[x1][y1 + 1] == 1:
                y1 += 1
    elif event.char == "w":
        if (x1 - 1 >= 0 and x1 - 1 < ms):
            if T[x1 - 1][y1] == 1:
                x1 -= 1
    elif event.char == "s":
        if (x1 + 1 >= 0 and x1 + 1 < ms):
            if  T[x1 + 1][y1] == 1:
                x1 += 1

    draw_rect()
    if(x1 == ms-1 and y1 == ms-1):
        window.quit()

    #col = w = x1 // cell_size
    #row = h = y1 // cell_size
    #print(w, h)
    #print("after", T[row][col])


window.bind("<Key>", move)

window.mainloop()