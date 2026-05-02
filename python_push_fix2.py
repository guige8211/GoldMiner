import subprocess
result = subprocess.run(["git", "push", "origin_guige", "jules-12780988291585688461-9b1a9625:main", "--force"], capture_output=True, text=True)
