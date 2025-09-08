#!/usr/bin/env python3
"""
submit_assignment.py

Automates submission of the workshop notebook to GitHub.
Each student/team has their own submission branch:
	submissions/<student_id>

Workflow:
1. Validate notebook (markdown + code + scoring).
2. Checkout or create submission branch.
3. Overwrite branch with notebook.
4. Commit & push to remote.
"""

import argparse
import sys
from git import Repo, GitCommandError
sys.path.append("utils")

from validate_notebook import validate_notebook


def submit(notebook: str, student_id: str) -> None:
	repo = Repo(".")
	branch_name = f"submissions/{student_id}"

	try:
		# Branch setup
		if branch_name in repo.heads:
			repo.git.checkout(branch_name)
			repo.git.reset("--hard", "origin/main")
		else:
			repo.git.checkout("main")
			repo.git.pull("origin", "main")
			repo.git.checkout("-b", branch_name)

		# Stage + commit
		repo.index.add([notebook])
		repo.index.commit(f"Submission from {student_id}")

		# Force push
		repo.git.push("origin", branch_name, force=True)
		print(f"✅ Submission pushed to branch: {branch_name}")

	except GitCommandError as e:
		print(f"❌ Git error: {e}")
		sys.exit(1)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Submit NLP Workshop Notebook")
	parser.add_argument("--notebook", required=True, help="Path to notebook (.ipynb)")
	parser.add_argument("--student_id", required=True, help="Student or team ID")
	args = parser.parse_args()

	passed = validate_notebook(args.notebook, args.student_id)
	if passed:
		submit(args.notebook, args.student_id)
	else:
		print("❌ Submission blocked due to validation errors.")
