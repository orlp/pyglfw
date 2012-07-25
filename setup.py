#!/usr/bin/env python

from distutils.core import setup

import sys
import os
import shutil

command = sys.argv[1] if len(sys.argv) >= 2 else ""
is_build = command.startswith("build") or command.startswith("install") or command.startswith("bdist")

if sys.platform == "win32":
    package_data = {"glfw": ["glfw.dll"]}
    
    # pre-built
    shutil.copyfile("glfw-2.7.5/lib/win32/glfw.dll", "glfw/glfw.dll")
    
elif sys.platform == "darwin":
    package_data = {"glfw": ["libglfw.dylib"]}
    
    if not os.path.exists("glfw/libglfw.dylib") and is_build:
        # let's cross our fingers and hope the build goes smooth (without user intervention)
        os.chdir("glfw-2.7.5")
        
        if os.system("make cocoa"):
            print("Error while building libglfw.dylib")
            sys.exit(1)
            
        os.chdir("..")
            
    shutil.copyfile("glfw-2.7.5/lib/cocoa/libglfw.dylib", "glfw/libglfw.dylib")
        
else:
    package_data = {"glfw": ["libglfw.so"]}
    
    if not os.path.exists("glfw/libglfw.so") and is_build:
        os.chdir("glfw-2.7.5")
        
        if os.system("make x11"):
            print("Error while building libglfw.so")
            sys.exit(1)
            
        os.chdir("..")
        
    shutil.copyfile("glfw-2.7.5/lib/x11/libglfw.so", "glfw/libglfw.so")


setup_info = {
    "name": "pyglfw",
    "version": "0.1.0",
    "author": "Orson Peters",
    "author_email": "orsonpeters@gmail.com",
    "url": "http://github.com/nightcracker/pyglfw",
    "description": "GLFW bindings for Python",
    "license": "NC Labs license - BSD-style attribution-only license",
    "classifiers": [
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    "packages": ["glfw", "glfw.ext"],
    "package_data": package_data,
}
    
setup(**setup_info)