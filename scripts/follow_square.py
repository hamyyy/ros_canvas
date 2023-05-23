#!/usr/bin/env python3

import rospy
from p5 import *

from std_msgs.msg import Bool


class Node:

    def __init__(self):
        rospy.init_node('follow_square_node', anonymous=True)
        
        self.pixels_per_mm = 1.0

        self.rect_pos = Vector(100, 100) * self.pixels_per_mm
        self.rect_size = Vector(600, 600) * self.pixels_per_mm

        self.circle_pos = self.rect_pos + self.rect_size
        self.circle_speed = 5  # 5 pixels at 30 fps
        self.switch_sub = rospy.Subscriber('/switch', Bool, self.switch_callback)
        self.switch = False

        self.show_circle = True
        self.circle_size = 50
        self.move_circle = False
        self.show_debug = True

        self.circle_state = 0

        self.mouse_button = None

    def setup(self):
        size(800, 800)  # set size of the window

    def draw(self):
        background(0)  # set background color to black

        if self.move_circle:
            self.update_state()

        if self.show_debug:
            push()
            noFill()
            strokeWeight(2)
            stroke(100)
            rect(self.rect_pos.x, self.rect_pos.y, self.rect_size.x, self.rect_size.y)  # draw a rectangle
            pop()

        push()
        noFill()
        strokeWeight(4)
        stroke(255, 0, 0)
        ellipse(self.circle_pos.x, self.circle_pos.y, self.circle_size, self.circle_size)  # draw a circle
        pop()

        if self.show_debug:
            push()

            fill(255)
            text_size(20)
            text(f"Speed: {self.circle_speed * self.pixels_per_mm} mm/s", 10, 20)

            translate(0, 60)
            text_size(15)
            text("Space: Play/Reset", 10, 0)
            text("Q: Hide Debug", 10, 20)
            text("Mouse Wheel: Adjust Speed", 10, 40)
            text("Shift Left Click: Adjust Rectancle Position", 10, 60)
            text("Shift Right Click: Adjust Rectancle Size", 10, 80)

            pop()

    def mouse_pressed(self, event):
        self.mouse_button = event.button

    def mouse_moved(self, event):
        global mouse_x, mouse_y

        if not self.show_debug:
            return

        if event.pressed and "Shift" in event.modifiers:
            if self.mouse_button == "LEFT":
                self.rect_pos = Vector(mouse_x, mouse_y)
            elif self.mouse_button == "RIGHT":
                self.rect_size = Vector(mouse_x, mouse_y) - self.rect_pos
            self.reset_circle()

    def mouse_wheel(self, event):
        if not self.show_debug:
            return

        if key == "SHIFT":
            self.rect_size.x += event.count
            self.rect_size.x = max(1, self.rect_size.x)
            self.reset_circle()
        elif key == "CONTROL":
            self.rect_size.y += event.count
            self.rect_size.y = max(1, self.rect_size.y)
            self.reset_circle()
        else:
            self.circle_speed += event.count * 0.2
            self.circle_speed = max(1, self.circle_speed)

    def key_pressed(self, event):
        global key
        if key == "Q":
            self.show_debug = not self.show_debug
        if key == " ":
            if self.move_circle:
                self.reset_circle()
            else:
                self.start_circle()
        if key == "C":
            self.move_circle = not self.move_circle

    def update_state(self):
        if self.circle_state == 0:
            self.circle_pos.y -= self.circle_speed * self.pixels_per_mm
            if self.circle_pos.y <= self.rect_pos.y:
                self.circle_pos.y = self.rect_pos.y
                self.circle_state = 1
        elif self.circle_state == 1:
            self.circle_pos.x -= self.circle_speed * self.pixels_per_mm
            if self.circle_pos.x <= self.rect_pos.x:
                self.circle_pos.x = self.rect_pos.x
                self.circle_state = 2
        elif self.circle_state == 2:
            self.circle_pos.y += self.circle_speed * self.pixels_per_mm
            if self.circle_pos.y >= self.rect_pos.y + self.rect_size.y:
                self.circle_pos.y = self.rect_pos.y + self.rect_size.y
                self.circle_state = 3
        elif self.circle_state == 3:
            self.circle_pos.x += self.circle_speed * self.pixels_per_mm
            if self.circle_pos.x >= self.rect_pos.x + self.rect_size.x:
                self.circle_pos.x = self.rect_pos.x + self.rect_size.x
                self.circle_state = 0

    def stop_circle(self):
        self.move_circle = False
    
    def reset_circle(self):
        self.circle_state = 0
        self.circle_pos = self.rect_pos + self.rect_size
        self.move_circle = False
        
    def start_circle(self):
        self.move_circle = True
    
    def switch_callback(msg: Bool):
        switch = msg.data


def mouse_pressed(event):
    node.mouse_pressed(event)


def mouse_moved(event):
    node.mouse_moved(event)


def mouse_dragged(event):
    node.mouse_moved(event)


def key_pressed(event):
    node.key_pressed(event)


def mouse_wheel(event):
    node.mouse_wheel(event)


if __name__ == '__main__':
    node = Node()
    run(frame_rate=30, mode="P2D", sketch_setup=node.setup, sketch_draw=node.draw, renderer="skia")