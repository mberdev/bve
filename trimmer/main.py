import importlib
from boilterplate import find_davinci_resolve_data_folder, find_davinci_resolve_folder, init_env_variables

#
#           IMPORTANT : 
#           You must use Python 3.6 or at most 3.11 so that the DaVinci Resolve API works.
#           You can tell that it doesn't work if deprecated module "imp" cannot get 
#           imported at all inside DaVinciResolveScript.py.
#

resolve_folder = find_davinci_resolve_folder()


resolve_data_folder = find_davinci_resolve_data_folder()

init_env_variables(resolve_folder, resolve_data_folder)

# Now that we know where it is, load the dvr module dynamically
try:
    # dvr = importlib.import_module('DaVinciResolveScript')
    import DaVinciResolveScript as dvr
except ImportError:
    print("could not import DaVinciResolveScript")
    exit(1)

# Create a new project
projectManager = dvr.scriptapp("ProjectManager")
project = projectManager.CreateProject()

# Set project properties
project.SetSetting("timelineFrameRate", "30")
project.SetSetting("timelineResolutionWidth", "1920")
project.SetSetting("timelineResolutionHeight", "1080")

# Save the project
project.SaveAs("path/to/project.drp")

