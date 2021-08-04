from shutil import ExecError
import subprocess
from os import listdir
from os.path import isfile, join
from os import makedirs as mkdirs

def build_cmake(payload):
    commit_id = payload["head_commit"]["id"] if 'head_commit' in payload else payload["checkout_sha"]
    try:
        mkdirs("/tmp/" + commit_id + "/build")
    except(FileExistsError):
        print("Path already exists! Are you re-delivering a hook?")

    cmd2 = subprocess.run(["/usr/bin/cmake", "-B/tmp/" + commit_id + "/build", "-S/tmp/" + commit_id + "/"])
    if(cmd2.returncode != 0):
        print("Issues running cmake on your project. Please check it can be configured.")
        raise ExecError
    cmd3 = subprocess.run(["/usr/bin/make", "-C /tmp/" + commit_id + "/build","-j4"])
    if(cmd3.returncode != 0):
        print("Issues building your project.")
        raise ExecError

def build_gradle(payload):
    commit_id = payload["head_commit"]["id"] if 'head_commit' in payload else payload["checkout_sha"]
    #Default our executable to gradle.
    executable = "gradle"
    #Get all files in the repo's source dir
    onlyfiles = [f for f in listdir("/tmp/" + commit_id) if isfile(join("/tmp/" + commit_id, f))]
    #If we find a gradle wrapper, use it instead of the pre-installed gradle
    if(onlyfiles.__contains__("gradlew")):
        executable = "/tmp/" + commit_id + "/gradlew"
    cmd = subprocess.run([executable, "build"])
    if(cmd.returncode != 0):
        print("Issue building your gradle project.")