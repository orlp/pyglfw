# --------------------------------------------------------------------------
# Copyright 2012 Orson Peters. All rights reserved.
#
# Redistribution of this work, with or without modification, is permitted if
# Orson Peters is attributed as the original author or licensor of
# this work, but not in any way that suggests that Orson Peters endorses
# you or your use of the work.
#
# This work is provided by Orson Peters "as is" and any express or implied
# warranties are disclaimed. Orson Peters is not liable for any damage
# arising in any way out of the use of this work.
# --------------------------------------------------------------------------

import ctypes as _ctypes
import glfw as _glfw


import os

if os.name == "nt":
    from glfw.ext import win32 as _win32
    
    _functype = _ctypes.WINFUNCTYPE
    
    def get_native_handle():
        """Returns a native handle to the GLFW window.
        
        If the function failed (for example when there is no window open) a
        RuntimeError is raised."""
        
        return _win32.get_hwnd()
    
    
    def set_icons(icons):
        """Sets the window icons."""
        
        _win32.set_icons(icons)
        
else:
    _functype = _ctypes.CFUNCTYPE
    
    def get_native_handle():
        """Returns a native handle to the GLFW window.
        
        If the function failed (for example when there is no window open) a
        RuntimeError is raised."""
        
        pass
    
    
    def set_icons(icons):
        """Sets the window icons."""
        
        pass
        
del os


class OpenGLWrapper(object):
    """Wraps OpenGL functions using _ctypes and glfw.GetProcAddress.
    
    When created with OpenGLWrapper(funcname, restype, argtypes), the object
    will behave like a ctypes function with `restype` as result type and
    `argtypes` as argument types. The ctypes function is initialized using an
    OpenGL function pointer retrieved by passing `funcname` into glfw.GetProcAddress.
    
    This creates a lazy wrapper - the function address is not looked up until
    the first call. This is useful because the function address can not be
    retrieved until there is a opened window.
    
    For example, to wrap `void glClear(unsigned int mask);`:
    
        >>> GL_COLOR_BUFFER_BIT = 0x00004000 # constant from gl.h
        >>> glClear = glfw.ext.OpenGLWrapper("glClear", None, _ctypes.c_uint)
        
    And then the usage is simple:
    
        >>> glClear(GL_COLOR_BUFFER_BIT)
    
    """
    
    def __init__(self, funcname, restype, *argtypes):
        self.funcname = funcname
        self.restype = restype
        self.argtypes = argtypes
        self.funcprototype = _functype(restype, *argtypes)
        self.glfunc = None
    
    def __call__(self, *args, **kwargs):
        if self.glfunc is None:
            proc_addr = _glfw.GetProcAddress(self.funcname)
            
            if proc_addr is None:
                raise RuntimeError("Couldn't load OpenGL function " + self.funcname)
            
            self.glfunc = self.funcprototype(proc_addr)
        
        return self.glfunc(*args, **kwargs)
    
    def __repr__(self):
        return "glfw.ext.OpenGLWrapper(%s, %s, %s)" % (repr(self.funcname), repr(self.restype), repr(self.argtypes))