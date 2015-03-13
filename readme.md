Introduction
------------
This is pyglfw, Python bindings for GLFW 2.7.5 using ctypes. It's a very light
set of bindings, the API is nearly the same from Python as from C, except that
the C and ctypes details are hidden from the user.

Usage
-----
Everything works as described in the GLFW reference manual, with a few changes:

 * All glfwFooBar functions should be accessed like glfw.FooBar. All
   GLFW_FOO_BAR constants should be accessed like glfw.FOO_BAR.
 * The threading and image loading functions have been removed from the API. The
   same goes for related defines, constants, etc. This was done because they are
   a deprecated featureset from the GLFW library, removed in version 3.0. On top
   of that, the threading is not very useful for Python, even potentially
   dangerous with the GIL. The image loading is hardly useful either, because it
   only loads TARGA files, and better image loading options exist for Python.
 * The functions glfwGetTime, glfwSetTime and glfwSleep are removed because they
   are unnessecary in Python (use the `time` module).
 * The function glfwGetProcAddress returns the memory location as an integer.
 * Functions returning arguments by having types passed in as a pointer now
   return the values directly without accepting the argument. For example
   void glfwGetVersion(int *major, int *minor, int *rev); is wrapped as a
   function called glfw.GetVersion() taking no arguments and returning a tuple
   of 3 integers, respectively major, minor and rev. Similarly,
   glfw.GetWindowSize() returns a tuple of two integers giving the size of the
   window.
 * All of glfwGetVideoModes's arguments have been removed, and it simply returns
   a list of video modes.
 * The GLFWvidmode struct has been replaced with the class vidmode, who's
   member variables have the same names and meaning as GLFWvidmode's.
 * Type/value checking has been added to some functions, for example passing a
   negative size into glfw.OpenWindow raises a ValueError, so does passing a
   list into glfw.SetWindowTitle. This is done because GLFW 2.7.5 has no error
   messages, and thus this will ease debugging.
 * glfw.Init does not return an integer indicating the status, instead it
   always returns None and raises an EnvironmentError if the initialization
   failed.
 * The callback function typedefs have been removed.
 * Callback functions can be passed regular Python functions taking the
   appropriate number of arguments.
 * GLFW_KEY_SPACE is removed.
 * The functions/callbacks taking/returning either a latin-1 character or an
   integer in C take and return either a unicode or an int in the wrapper. Any
   integer value < 256 gets converted to a one-character unicode. This is the
   reason why GLFW_KEY_SPACE is removed - for unambigous checking. Otherwise the
   comparison key == GLFW_KEY_SPACE will fail when key == u" ", which is a hard
   situation to debug.
 * The callback set with glfw.SetCharCallback always gets called with a
   one-character unicode string and never with an integer value.
   
Other than the above changes everything works exactly as in the GLFW reference
manual (see docs/reference.pdf).

Dependencies
------------
pyglfw depends on a Python version greater or equal than 2.5. It also depends on
GLFW 2.7.5, although any larger 2.x.x version should work (not GLFW 3, that's
incompatible).

pyglfw needs a shared library version of GLFW to run. For Windows users it's
easy - pyglfw comes shipped with a Windows GLFW DLL pre-built. Users on other
OS's must compile a shared version of GLFW themselves. Make sure that the shared
library follows your system's naming scheme for the library "glfw" (so, for
example, on Linux this would be libglfw.so) and copy the file to the glfw/
directory before installing.

pyglfw comes with the GLFW documentation. They can be found in the folder docs.
For the GLFW source code (needed to build a GLFW shared library) download a copy
from http://glfw.org/.
