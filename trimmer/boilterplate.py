import os
import sys

# Returns something like "C:/Program Files/Blackmagic Design/DaVinci Resolve"
def find_davinci_resolve_folder():
    program_files_path = os.environ.get("ProgramFiles").replace("\\", "/")
    if not program_files_path:
        print("ERROR: Program Files path not found.")
        exit(1)

    blackmagic_folder = os.path.join(program_files_path, "Blackmagic Design").replace("\\", "/")
    if not os.path.exists(blackmagic_folder):
        print(f"ERROR: Folder does not exist : {blackmagic_folder}")
        exit(1)

    resolve_folder = os.path.join(blackmagic_folder, "DaVinci Resolve").replace("\\", "/")
    if not os.path.exists(resolve_folder):
        print(f"ERROR: Folder does not exist : {resolve_folder}")
        exit(1)
    return resolve_folder


# Returns something like "C:/ProgramData/Blackmagic Design/DaVinci Resolve"
def find_davinci_resolve_data_folder():
    program_data_path = os.environ['PROGRAMDATA']
    resolve_data_folder = os.path \
    .join(program_data_path, "Blackmagic Design/DaVinci Resolve") \
    .replace("\\", "/") 

    if not os.path.exists(resolve_data_folder):
        print(f"ERROR: Folder does not exist : {resolve_data_folder}")
        exit(1)
    return resolve_data_folder



def init_env_variables(resolve_folder, resolve_data_folder):
    # # As per https://deric.github.io/DaVinciResolve-API-Docs/ create env variable RESOLVE_SCRIPT_API
    # resolve_script_api = os.environ.get("RESOLVE_SCRIPT_API")
    # if not resolve_script_api:
    #     resolve_script_api = os.path.join(resolve_data_folder, "Support/Developer/Scripting").replace("\\", "/")
    #     print(f"Setting RESOLVE_SCRIPT_API to value : {resolve_script_api}")
    #     os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api

    # # As per https://deric.github.io/DaVinciResolve-API-Docs/ create env variable RESOLVE_SCRIPT_LIB
    # resolve_script_lib = os.environ.get("RESOLVE_SCRIPT_LIB")
    # if not resolve_script_lib:
    #     resolve_script_lib = os.path.join(resolve_folder, "fusionscript.dll").replace("\\", "/")
    #     print(f"Setting RESOLVE_SCRIPT_LIB to value : {resolve_script_lib}")
    #     os.environ["RESOLVE_SCRIPT_LIB"] = resolve_script_lib

    # # As per https://deric.github.io/DaVinciResolve-API-Docs/ update PYTHONPATH
    # pythonpath = os.environ.get("PYTHONPATH")
    # modulespath = f"{resolve_script_api}/Modules/"
    # if pythonpath is None :
    #     pythonpath = f"\"{modulespath}\""
    #     os.environ["PYTHONPATH"] = pythonpath
    # elif not "Modules" in pythonpath:
    #     pythonpath = f"{pythonpath};\"{modulespath}\""
    #     print(f"Setting PYTHONPATH to value : {pythonpath}")
    #     os.environ["PYTHONPATH"] = pythonpath

    # # Just in case, help Python find even more modules
    # if not any("Modules" in path for path in sys.path):
    #     sys.path.append(modulespath.replace("/", "\\"))

    # # Just in case, help Python find even more modules
    # if not any(resolve_folder in path for path in sys.path):
    #     sys.path.append(resolve_folder.replace("/", "\\"))

    # Optional. For debug.
    print("")
    print(f'PYTHONPATH: {os.environ["PYTHONPATH"]}')
    print("")
    print(f'Sys path: {sys.path}')
    print("")