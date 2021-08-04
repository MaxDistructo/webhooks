from os import listdir
from os.path import isfile, join
from install_scripts import *
from build_scripts import *

def detect_type(payload) -> str:
    #Get all the files in the cloned repo's directory
    commit_id = payload["head_commit"]["id"] if 'head_commit' in payload else payload["checkout_sha"]
    onlyfiles = [f for f in listdir("/tmp/" + commit_id) if isfile(join("/tmp/" + commit_id, f))]
    if(onlyfiles.__contains__("CMakeLists.txt")):
        return "cmake"
    elif(onlyfiles.__contains__("build.gradle") or onlyfiles.__contains__("build.gradle.kts")):
        return "gradle"

def build_install_project(payload) -> bool:
    type = detect_type(payload)
    if type == "cmake":
        build_cmake(payload)
    elif type == "gradle":
        build_gradle(payload)
    install_project(payload, type)
