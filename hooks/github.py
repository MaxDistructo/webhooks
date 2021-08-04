import subprocess

def clone_repo(payload):
    head_id = payload["head_commit"]["id"] if 'head_commit' in payload else None
    if head_id == None:
        head_id = payload["checkout_sha"] if 'checkout_sha' in payload else None
    url = payload["repository"]["url"] if "repository" in payload else None
    if url == None:
        url = payload["project"]["url"]
    subprocess.run(["git", "clone", "--recurse", url, "/tmp/" + head_id])
