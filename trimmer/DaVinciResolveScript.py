#
#   This is an alternative version to the official DaVinciResolveScript.py
#   that is shipped with DaVinci Resolve.
#
#   This version uses the new "importlib" library (compatible with Python 3.12+)
#   instead of the deprecated "imp" library (to be used with Python 3.6, which 
#   is the version that DaVinci Resolve demands according to the docs).
#
#   Unfortunately, it doesn't work. I don't know why. Maybe fusionscript.dll
#   is not in the right format to be used with importlib.
#

import importlib
import sys
import os

script_module = None
try:
    import fusionscript as script_module
except ImportError:
    # Look for installer based environment variables:
    lib_path=os.getenv("RESOLVE_SCRIPT_LIB")
    if lib_path:
        try:
            #+EDIT
            path = os.path.dirname(lib_path)
            if path not in sys.path:
                sys.path.insert(0, path)
            script_module = importlib.import_module("fusionscript")
            #-EDIT
            # script_module = imp.load_dynamic("fusionscript", lib_path)
        except ImportError:
            pass
    if not script_module:
        # Look for default install locations:
        ext=".so"
        if sys.platform.startswith("darwin"):
            path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            ext = ".dll"
            path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
        elif sys.platform.startswith("linux"):
            path = "/opt/resolve/libs/Fusion/"

        try:
            #+EDIT	
            dll_file_name = "fusionscript" + ext
            file_path = os.path.join(path, dll_file_name)

            if path not in sys.path:
                sys.path.insert(0, path)

            script_module = importlib.import_module("fusionscript") # ok for dll
            #-EDIT

            # script_module = imp.load_dynamic("fusionscript", path + "fusionscript" + ext)
        except ImportError:
            pass

if script_module:
    sys.modules[__name__] = script_module
else:
    raise ImportError("Could not locate module dependencies")
