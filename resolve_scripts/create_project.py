# This file must be placed somewhere in C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
# It can be run fro inside DaVinci Resolve : Menu "Workspace" > "Scripts" > "Utility" > <this_script_name>

import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()
projectManager = resolve.GetProjectManager()
# projectManager.CreateProject("Hello World")


# project = assert(projectManager:GetCurrentProject(), "Couldn't get current project")

print("Hello, world!")