
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys

WIDTH, HEIGHT = 1000, 600

START_X = 155
FINISH_X = 850
CAR_LENGTH = 78

cars = []

signal_green = False
race_started = False
race_over = False
winner = ""

countdown = 3



def reset_race():

    global cars, signal_green, race_started
    global race_over, winner, countdown

    cars = [
        {
            "name": "RED CAR",
            "color": (1.0, 0.08, 0.08),
            "x": START_X,
            "y": 170,
            "speed": 0.4
        },

        {
            "name": "BLUE CAR",
            "color": (0.05, 0.35, 1.0),
            "x": START_X,
            "y": 270,
            "speed": 0.5
        },

        {
            "name": "YELLOW CAR",
            "color": (1.0, 0.8, 0.0),
            "x": START_X,
            "y": 370,
            "speed": 0.6
        }
    ]

    signal_green = False
    race_started = False
    race_over = False
    winner = ""
    countdown = 3

def text(x, y, message, color=(1, 1, 1),
         font=GLUT_BITMAP_HELVETICA_18):

    glColor3f(*color)
    glRasterPos2f(x, y)

    for char in message:
        glutBitmapCharacter(font, ord(char))

def rectangle(x, y, w, h, color):

    glColor3f(*color)

    glBegin(GL_QUADS)

    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)

    glEnd()

def circle(cx, cy, radius, color):

    glColor3f(*color)

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(cx, cy)

    for i in range(41):

        angle = 2 * math.pi * i / 40

        glVertex2f(
            cx + radius * math.cos(angle),
            cy + radius * math.sin(angle)
        )

    glEnd()

def draw_background():

    rectangle(0, 0, WIDTH, HEIGHT, (0.55, 0.82, 1.0))

    rectangle(0, 80, WIDTH, 400, (0.20, 0.62, 0.27))

    rectangle(0, 125, WIDTH, 330, (0.20, 0.21, 0.24))

    rectangle(0, 125, WIDTH, 5, (1, 1, 1))
    rectangle(0, 450, WIDTH, 5, (1, 1, 1))

    for y in [240, 340]:

        for x in range(0, WIDTH, 65):

            rectangle(x, y, 35, 4, (1, 1, 1))

    for x in [30, 300, 500, 960]:

        rectangle(
            x + 12, 460, 12, 35,
            (0.40, 0.20, 0.05)
        )

        circle(
            x + 18, 500, 24,
            (0.03, 0.42, 0.12)
        )

    text(
        350, 555,
        "3 CAR RACING CHAMPIONSHIP",
        (0.05, 0.12, 0.25)
    )


def draw_signal():

   
    rectangle(48, 455, 10, 80, (0.25, 0.25, 0.28))
    rectangle(30, 450, 46, 8, (0.15, 0.15, 0.18))

 
    rectangle(25, 505, 56, 78, (0.10, 0.10, 0.12))


    red = (
        (1, 0.02, 0.02)
        if not signal_green
        else (0.35, 0.05, 0.05)
    )

    green = (
        (0.02, 1, 0.12)
        if signal_green
        else (0.03, 0.30, 0.06)
    )

    circle(53, 562, 13, red)
    circle(53, 526, 13, green)

    text(90, 562, "RED", (0.8, 0, 0))
    text(90, 526, "GREEN", (0, 0.3, 0))



def draw_start_finish():


    rectangle(START_X - 7, 130, 5, 320, (1, 1, 1))

    text(95, 465, "START", (1, 1, 1))

    square = 15

    for row in range(22):

        for col in range(2):

            color = (
                (1, 1, 1)
                if (row + col) % 2 == 0
                else (0, 0, 0)
            )

            rectangle(
                FINISH_X + col * square,
                130 + row * square,
                square,
                square,
                color
            )

    text(FINISH_X - 4, 465, "FINISH", (1, 1, 1))

    text(FINISH_X + 2, 110, "STOP", (1, 0.05, 0.05))



def draw_car(car):

    x = car["x"]
    y = car["y"]
    color = car["color"]

   
    rectangle(x, y, 78, 27, color)

    glColor3f(*color)

    glBegin(GL_POLYGON)

    glVertex2f(x + 14, y + 27)
    glVertex2f(x + 25, y + 43)
    glVertex2f(x + 54, y + 43)
    glVertex2f(x + 67, y + 27)

    glEnd()

   
    rectangle(x + 28, y + 30, 12, 10, (0.65, 0.9, 1))
    rectangle(x + 43, y + 30, 10, 10, (0.65, 0.9, 1))


    circle(x + 17, y - 1, 9, (0.04, 0.04, 0.04))
    circle(x + 61, y - 1, 9, (0.04, 0.04, 0.04))

    circle(x + 17, y - 1, 4, (0.65, 0.65, 0.65))
    circle(x + 61, y - 1, 4, (0.65, 0.65, 0.65))

  
    rectangle(x + 74, y + 12, 5, 7, (1, 1, 0.5))


    text(
        x, y + 52,
        car["name"],
        (1, 1, 1),
        GLUT_BITMAP_HELVETICA_12
    )



def draw_restart_button():

    rectangle(
        820, 20, 145, 45,
        (0.05, 0.25, 0.65)
    )

   
    rectangle(820, 20, 145, 3, (1, 1, 1))
    rectangle(820, 62, 145, 3, (1, 1, 1))

    text(
        845, 36,
        "RESTART",
        (1, 1, 1),
        GLUT_BITMAP_HELVETICA_18
    )



def display():

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_background()
    draw_signal()
    draw_start_finish()

    for car in cars:

        draw_car(car)

  
    if not signal_green:

        text(
            370, 70,
            "GET READY! RED LIGHT",
            (1, 0.05, 0.05)
        )

    elif not race_over:

        text(
            390, 70,
            "GO! GO! GO!",
            (0, 0.3, 0)
        )

    else:

        rectangle(
            275, 15, 450, 48,
            (0.08, 0.08, 0.12)
        )

        text(
            310, 34,
            "WINNER: " + winner,
            (1, 0.85, 0.05)
        )


    draw_restart_button()

    text(
        15, 20,
        "Press R to Restart",
        (1, 1, 1),
        GLUT_BITMAP_HELVETICA_12
    )

    glutSwapBuffers()


def update(value):

    global countdown, signal_green, race_started
    global race_over, winner

    if not race_over:

       
        if not signal_green:

            countdown -= 1

            if countdown <= 0:

                signal_green = True
                race_started = True

      
        elif race_started:

            for car in cars:

             
                car["x"] += car["speed"]

           
                if car["x"] + CAR_LENGTH >= FINISH_X + 30:

                    race_over = True
                    winner = car["name"]

                    break

    glutPostRedisplay()

    
    glutTimerFunc(16, update, 0)



def keyboard(key, x, y):

    if key in (b'r', b'R'):

        reset_race()

    if key == b'\x1b':

        sys.exit(0)

    glutPostRedisplay()



def mouse(button, state, x, y):

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        
        mouse_x = x
        mouse_y = HEIGHT - y

      
        if (
            820 <= mouse_x <= 965
            and 20 <= mouse_y <= 65
        ):

            reset_race()

            glutPostRedisplay()



def main():

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    glutInitWindowSize(WIDTH, HEIGHT)

    glutInitWindowPosition(100, 50)

    glutCreateWindow(b"3 Car Racing Game")

    glClearColor(0, 0, 0, 1)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    reset_race()

    glutDisplayFunc(display)

    glutKeyboardFunc(keyboard)

    glutMouseFunc(mouse)

    glutTimerFunc(16, update, 0)

    glutMainLoop()


if __name__ == "__main__":

    main()
