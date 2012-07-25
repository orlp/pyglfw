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
#
# Some code from pyglet is used here - this is the copyright notice:
#
# --------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------

from ctypes import *
from ctypes.wintypes import *


# dlls
user32 = windll.LoadLibrary("user32")
kernel32 = windll.LoadLibrary("kernel32")
gdi32 = windll.LoadLibrary("gdi32")

BI_BITFIELDS = 3
GCL_HICON = -14
GCL_HICONSM = -34
DIB_RGB_COLORS = 0
SM_CXICON = 11
SM_CYICON = 12
SM_CXSMICON = 49
SM_CYSMICON = 50
    
WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
user32.EnumThreadWindows.restype = BOOL
user32.EnumThreadWindows.argtypes = [DWORD, WNDENUMPROC, LPARAM]

user32.GetWindowThreadProcessId.restype = DWORD
user32.GetWindowThreadProcessId.argtypes = [HWND, POINTER(DWORD)]

kernel32.GetCurrentProcessId.restype = DWORD
kernel32.GetCurrentProcessId.argtypes = []

user32.GetSystemMetrics.restype = c_int
user32.GetSystemMetrics.argtypes = [c_int]


class CIEXYZ(Structure):
    _fields_ = [
        ("ciexyzX", DWORD),
        ("ciexyzY", DWORD),
        ("ciexyzZ", DWORD),
    ]

    
class CIEXYZTRIPLE(Structure):
    _fields_ = [
        ("ciexyzRed", CIEXYZ),
        ("ciexyzBlue", CIEXYZ),
        ("ciexyzGreen", CIEXYZ),
    ]


class BITMAPV5HEADER(Structure):
    _fields_ = [
        ("bV5Size", DWORD),
        ("bV5Width", LONG),
        ("bV5Height", LONG),
        ("bV5Planes", WORD),
        ("bV5BitCount", WORD),
        ("bV5Compression", DWORD),
        ("bV5SizeImage", DWORD),
        ("bV5XPelsPerMeter", LONG),
        ("bV5YPelsPerMeter", LONG),
        ("bV5ClrUsed", DWORD),
        ("bV5ClrImportant", DWORD),
        ("bV5RedMask", DWORD),
        ("bV5GreenMask", DWORD),
        ("bV5BlueMask", DWORD),
        ("bV5AlphaMask", DWORD),
        ("bV5CSType", DWORD),
        ("bV5Endpoints", CIEXYZTRIPLE),
        ("bV5GammaRed", DWORD),
        ("bV5GammaGreen", DWORD),
        ("bV5GammaBlue", DWORD),
        ("bV5Intent", DWORD),
        ("bV5ProfileData", DWORD),
        ("bV5ProfileSize", DWORD),
        ("bV5Reserved", DWORD),
    ]
    
    
class ICONINFO(Structure):
    _fields_ = [
        ("fIcon", BOOL),
        ("xHotspot", DWORD),
        ("yHotspot", DWORD),
        ("hbmMask", HANDLE),
        ("hbmColor", HANDLE)
    ]

    
def get_hwnd():
    current_process = kernel32.GetCurrentProcessId()
    
    def callback(hwnd, lparam):
        process_id = DWORD()
        user32.GetWindowThreadProcessId(hwnd, byref(process_id))
        
        if process_id.value != current_process:
            return True
            
        classname = create_string_buffer(8)
        user32.GetClassNameA(hwnd, classname, len(classname))
        
        if classname.value != "GLFW27":
            return True
            
        callback.result = hwnd
        return False

    callback.result = None
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    
    if callback.result is None:
        raise RuntimeError("no handle found")
    
    return callback.result

    
def set_icons(images):
    def get_icon(image):
        image_data, image_width, image_height = image
        
        if len(image_data) != image_width * image_height * 4:
            raise RuntimeError("image data size is incorrect")
            
        # convert RGBA to BGRA
        new_image_data = []
        for i in range(0, len(image_data), 4):
            new_image_data.append(image_data[i+2] + image_data[i+1] + image_data[i] + image_data[i+3])
        image_data = "".join(new_image_data)

        header = BITMAPV5HEADER()
        header.bV5Size = sizeof(header)
        header.bV5Width = image_width
        header.bV5Height = image_height
        header.bV5Planes = 1
        header.bV5BitCount = 32
        header.bV5Compression = BI_BITFIELDS
        header.bV5RedMask =   0x00ff0000
        header.bV5GreenMask = 0x0000ff00
        header.bV5BlueMask =  0x000000ff
        header.bV5AlphaMask = 0xff000000
        
        hdc = user32.GetDC(None)
        dataptr = c_void_p()
        bitmap = gdi32.CreateDIBSection(hdc, byref(header), DIB_RGB_COLORS, byref(dataptr), None, 0)
        user32.ReleaseDC(None, hdc)
        
        memmove(dataptr, image_data, len(image_data))
        
        mask = gdi32.CreateBitmap(image_width, image_height, 1, 1, None)

        iconinfo = ICONINFO()
        iconinfo.fIcon = True
        iconinfo.hbmMask = mask
        iconinfo.hbmColor = bitmap
        icon = user32.CreateIconIndirect(byref(iconinfo))

        gdi32.DeleteObject(mask)
        gdi32.DeleteObject(bitmap)
        
        return icon
    
    def best_image(width, height):
        # a heuristic for finding closest sized image to required size.
        image = images[0]
        for img in images:
            if img[1] == width and img[2] == height:
                # exact match always used
                return img
            elif img[1] >= width:
                # at least wide enough, closest (preferably larger) area
                target_area = width * height
                

                if img[1] * img[2] < image[1] * image[2]:
                    if img[1] * img[2] >= target_area:
                        image = img
                else:
                    if image[1] * image[2] < target_area:
                        image = img
                        
        return image
    
    hwnd = get_hwnd()
    image = best_image(user32.GetSystemMetrics(SM_CXICON), user32.GetSystemMetrics(SM_CYICON))
    user32.SetClassLongW(hwnd, GCL_HICON, get_icon(image))
    
    image = best_image(user32.GetSystemMetrics(SM_CXSMICON), user32.GetSystemMetrics(SM_CYSMICON))
    user32.SetClassLongW(hwnd, GCL_HICONSM, get_icon(image))