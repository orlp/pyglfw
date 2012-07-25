#!/usr/bin/env python

import time
import os

import glfw
import ctypes


GL_COLOR_BUFFER_BIT = 0x00004000
glClear = glfw.ext.OpenGLWrapper("glClear", None, ctypes.c_uint)


# create icon (simple GLFW logo)
icon = """
................
................
...0000..0......
...0.....0......
...0.00..0......
...0..0..0......
...0000..0000...
................
................
...000..0...0...
...0....0...0...
...000..0.0.0...
...0....0.0.0...
...0....00000...
................
................
"""

icon = [s.strip() for s in icon.split("\n") if s.strip()]
icon_width = len(icon[0])
icon_height = len(icon)
icon_data = "".join([s.replace("0", "\x3f\x60\x60\xff").replace(".", "\x00\x00\x00\x00") for s in icon[::-1]])


def log(msg):
    # print("%06d %s" % (log.eventid, msg))
    log.eventid += 1
    
log.eventid = 0


# callback functions
def on_resize(w, h):
    log("Window resize: %d, %d" % (w, h))
    
    
def on_key(key, pressed):
    if pressed:
        log("Key press: %s" % str(key))
    else:
        log("Key release: %s" % str(key))
    
    
def on_char(char, pressed):
    if pressed:
        log("Char press: %s" % char)
    else:
        log("Char release: %s" % char)
    
    
def on_button(button, pressed):
    if pressed:
        log("Button press: %d" % button)
    else:
        log("Button release: %d" % button)


def on_pos(x, y):
    log("Mouse pos: %d %d" % (x, y))
    
    
def on_scroll(pos):
    log("Scroll: %d" % pos)


def on_close():
    log("Close (press escape to exit)")
    
    return False
    
    
def on_refresh():
    log("Refresh")
    
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.SwapBuffers()


glfw.Init()

print("Available video modes:\n%s\n" % "\n".join(map(str, glfw.GetVideoModes())))
print("Desktop video mode:\n%s\n" % glfw.GetDesktopMode())
print("GLFW Version: %d.%d.%d" % glfw.GetVersion())

glfw.OpenWindow(800, 600, 0, 0, 0, 8, 0, 0, glfw.WINDOW)

print("OpenGL version: %d.%d.%d\n" % glfw.GetGLVersion())

glfw.ext.set_icons([(icon_data, icon_width, icon_height)])
glfw.SetWindowTitle("pyglfw test")
glfw.Disable(glfw.AUTO_POLL_EVENTS)
glfw.Enable(glfw.KEY_REPEAT)

center_x = glfw.GetDesktopMode().Width / 2 - glfw.GetWindowSize()[0] / 2
center_y = glfw.GetDesktopMode().Height / 2 - glfw.GetWindowSize()[1] / 2

glfw.SetWindowPos(center_x, center_y)

glfw.SetWindowSizeCallback(on_resize)
glfw.SetWindowCloseCallback(on_close)
glfw.SetWindowRefreshCallback(on_refresh)
glfw.SetKeyCallback(on_key)
glfw.SetCharCallback(on_char)
glfw.SetMouseButtonCallback(on_button)
glfw.SetMousePosCallback(on_pos)
glfw.SetMouseWheelCallback(on_scroll)



while glfw.GetWindowParam(glfw.OPENED):
    glfw.PollEvents()
    
    if glfw.GetKey(glfw.KEY_ESC):
        break
    
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.SwapBuffers()

glfw.CloseWindow()
glfw.Terminate()