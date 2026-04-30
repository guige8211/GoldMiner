import subprocess
result = subprocess.run(["git", "pull", "--rebase", "origin_guige", "main"], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
