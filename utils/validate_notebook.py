"""
utils/validate_notebook.py
Validation logic for NLP workshop notebook submissions.
Checks required Markdown, functions, runs quick tests,
and provides point-based scoring with logging to CSV.
"""

import nbformat
import sys
import json
import os
import csv
from datetime import datetime
from types import FunctionType


def load_requirements(config_path="config/required_items.json"):
    if not os.path.exists(config_path):
        return {"required_functions": {}, "required_markdown": {}}
    with open(config_path, "r") as f:
        return json.load(f)


def exec_notebook(path: str) -> dict:
    """
    Execute notebook cells in a safe environment and return namespace.
    WARNING: Runs student code.
    """
    nb = nbformat.read(path, as_version=4)
    env = {}

    for cell in nb.cells:
        if cell.cell_type == "code":
            try:
                exec(cell.source, env)
            except Exception as e:
                print(f"⚠️ Warning: Error executing cell:\n{e}")
    return env


def log_submission(student_id, notebook, score, total, status, logfile="utils/submissions_log.csv"):
    """Append submission results to CSV gradebook."""
    log_exists = os.path.exists(logfile)
    with open(logfile, "a", newline="", encoding="utf-8") as f:  # <-- force UTF-8
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["timestamp", "student_id", "notebook", "score", "max_score", "status"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            student_id,
            notebook,
            score,
            total,
            status
        ])


def validate_notebook(path: str, student_id: str, config_path="config/required_items.json") -> bool:
    nb = nbformat.read(path, as_version=4)
    reqs = load_requirements(config_path)

    errors = []
    warnings = []
    total_points = 0
    earned_points = 0

    if len(nb.cells) == 0:
        errors.append("❌ Notebook is empty!")

    # --- Rule 1: Required Markdown filled ---
    md_found = {item: False for item in reqs["required_markdown"]}
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown":
            if "TODO:" in cell.source or "Write your answer here" in cell.source:
                errors.append(f"❌ Markdown cell {i} still contains placeholder text.")
            for item in reqs["required_markdown"]:
                if item.lower() in cell.source.lower() and len(cell.source.strip()) > len(item):
                    md_found[item] = True

    for item, found in md_found.items():
        total_points += reqs["required_markdown"][item]
        if found:
            earned_points += reqs["required_markdown"][item]
        else:
            errors.append(f"❌ Required markdown section '{item}' is missing or empty.")

    # --- Rule 2: No empty code scaffolds ---
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            stripped = cell.source.strip()
            if stripped in ("", "pass", "# TODO"):
                errors.append(f"❌ Code cell {i} is incomplete or empty.")

    # --- Rule 3: Required functions exist + run ---
    env = exec_notebook(path)

    for func_name, test_case in reqs["required_functions"].items():
        points = test_case.get("points", 0)
        total_points += points

        if func_name not in env or not isinstance(env[func_name], FunctionType):
            errors.append(f"❌ Required function '{func_name}' not found in notebook.")
            continue

        func = env[func_name]
        try:
            result = func(*test_case["test_input"])
            expected_type = test_case.get("expected_type")
            if expected_type:
                if result is None:
                    errors.append(f"❌ Function '{func_name}' returned None, expected {expected_type}.")
                elif result.__class__.__name__ != expected_type:
                    errors.append(
                        f"❌ Function '{func_name}' returned {type(result).__name__}, expected {expected_type}."
                    )
                else:
                    earned_points += points
            else:
                earned_points += points
        except Exception as e:
            errors.append(f"❌ Function '{func_name}' failed when tested: {e}")

    # --- Optional: Execution check ---
    unexecuted = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and c.execution_count is None]
    if unexecuted:
        warnings.append(f"⚠️ Warning: Some code cells were never executed: {unexecuted}")

    # --- Results ---
    print("\n=== Validation Report ===")
    if errors:
        print("\n".join(errors))
        status = "❌ Failed"
    else:
        print("✅ All required checks passed.")
        status = "✅ Passed"

    if warnings:
        print("\n".join(warnings))

    print(f"\nScore: {earned_points} / {total_points} points")

    # Always log submission attempt
    log_submission(student_id, path, earned_points, total_points, status)

    # Return True if passed, False if failed
    return len(errors) == 0
