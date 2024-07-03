import git
from git import Repo
# Repo.clone_from(url = "", to_path = "C:\Aligne\experiments")
repo = Repo("C:\Aligne\experiments")
repo.git.execute("git status")
repo.status("git status")
repo.git.pull()
repo.git.execute("git pull")
repo.git.execute("git checkout -b my_branch")
repo.git.add(".")
repo.git.execute("git add .")
repo.git.commit(m = "my commit message 'message commiting ' ")
repo.git.execute("git push -u origin my_branch")