import subprocess
from os import makedirs as mkdirs
from os.path import exists as path_exists
from shutil import copyfile as copy

def install_project(payload, project_type):
    repo_slug = payload["repository"]["name"].split('/')[1] if 'repository' in payload else payload["project"]["name"]
    install_dir = "/opt/" + repo_slug
    commit_id = payload["head_commit"]["id"] if 'head_commit' in payload else payload["checkout_sha"]
    if not path_exists(install_dir):
            mkdirs(install_dir)
    if project_type == "gradle":
        copy("/tmp/" + commit_id + "/build/libs/" + repo_slug + "-all.jar", install_dir + "/" + repo_slug + "-all.jar")
    if project_type == "cmake":
        if not repo_slug.contains("-cpp"):
            copy("/tmp/" + commit_id + "/build/" + repo_slug)
        else:
            copy("/tmp/" + commit_id + "/build/" + repo_slug.replace("-cpp", ""))