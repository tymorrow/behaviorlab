import csv
import json
import os

import distance
import fire

CORRECT_THRESHOLD = 5
SECRET_THRESHOLD = 8
MAX_DIST = 0
SUBMISSIONS_DIR_NAME = "submissions"
BUILD_DIR_NAME = "build"
STUDENTS_FILE = "students.json"
SECRET_HEADER_NAME = "secret"
SECRET_REQUIRED = False
COL_WIDTH = 20
PADDING = " ".ljust(COL_WIDTH)
CHECK_MARK = "\u2705"
X_MARK = "\u274C"
MISSING_MARK = "\u2B55"
WRONG_MARK = "\U0001F53B"


def get_student_submission(sid):
    submission = {}
    submission_path = os.path.join(SUBMISSIONS_DIR_NAME, sid + "_answers.csv")
    no_submission = not os.path.exists(submission_path)
    if not no_submission:
        submission_reader = csv.DictReader(open(submission_path), skipinitialspace=True)
        for r in submission_reader:
            header_file_name = r["file_name"].strip()
            submission[header_file_name] = dict(r)
    return submission


def get_student_solution(sid):
    solution = {}
    solution_path = os.path.join(BUILD_DIR_NAME, sid + ".solution.csv")
    no_solution = not os.path.exists(solution_path)
    if not no_solution:
        solution_reader = csv.DictReader(open(solution_path), skipinitialspace=True)
        for r in solution_reader:
            solution[r["file_name"]] = dict(r)
    return solution


def compare_submission_and_solution(truth: dict, attempt: dict, verbose=False):
    file_name_header = "file_name"
    operator_header = "operator"
    operand_header = "operand"
    version_header = "version"
    secret_header = "secret"
    missing_attempt = not attempt
    if missing_attempt:
        attempt = {
            "file_name": None,
            "operator": None,
            "operand": None,
            "version": None,
            "secret": None,
        }

    operator_truth, operator_attempt = truth[operator_header], attempt[operator_header]
    operand_truth, operand_attempt = truth[operand_header], attempt[operand_header]
    version_truth, version_attempt = truth[version_header], attempt[version_header]
    secret_truth, secret_attempt = truth[secret_header], attempt[secret_header]
    operator_truth, operator_attempt = str(operator_truth).lower().strip(), str(operator_attempt).lower().strip()
    operand_truth, operand_attempt = str(operand_truth).lower().strip(), str(operand_attempt).lower().strip()
    version_truth, version_attempt = str(version_truth).lower().strip(), str(version_attempt).lower().strip()
    secret_truth, secret_attempt = str(secret_truth).lower().strip(), str(secret_attempt).lower().strip()

    operand_truth_value = None
    try:
        operand_truth_value = int(operand_truth, base=(16 if operand_truth.startswith("0x") else 10))
    except ValueError:
        pass
    operand_attempt_value = None
    try:
        operand_attempt_value = int(operand_attempt, base=(16 if operand_attempt.startswith("0x") else 10))
    except ValueError:
        pass

    # Special cases / adjustments
    if operator_truth == "!":
        operand_truth = "none"  # corrects typo in config

    if operand_truth == "zero" and operand_attempt_value == 0:
        operand_attempt = operand_truth
    elif operand_attempt_value == 0 and operand_attempt == "zero":
        operand_attempt = operand_truth
    elif operand_truth == "none" and not operand_attempt:
        operand_attempt = operand_truth
    elif operand_truth == "nonzero" and operand_attempt_value and operand_attempt_value > 0:  # EXTRA NICE
        operand_attempt = operand_truth

    if operator_truth == "!" and operand_truth == "none" and \
       operator_attempt == "==" and (operand_attempt == "zero" or operand_attempt == "0"):
        operator_truth = operator_attempt
        operand_truth = operand_attempt
    elif operator_truth == "&&" and operand_truth == "nonzero" and \
            operator_attempt == "!=" and (operand_attempt == "zero" or operand_attempt == "0"):
        operator_truth = operator_attempt
        operand_truth = operand_attempt
    elif operator_truth == "!=" and operand_truth == "zero" and \
            operator_attempt == "||" and (operand_attempt == "zero" or operand_attempt == "0"):
        operator_truth = operator_attempt
        operand_truth = operand_attempt
    elif operator_truth == "||" and operand_truth == "zero" and \
            operator_attempt == "!=" and (operand_attempt == "zero" or operand_attempt == "0"):
        operator_truth = operator_attempt
        operand_truth = operand_attempt
    elif operator_truth == "~" and operand_truth == "none" and \
            operator_attempt == "^" and operand_attempt_value == 2**32 - 1:
        operator_truth = operator_attempt
        operand_truth = operand_attempt

    # Compare everything
    operator_is_correct = operator_truth == operator_attempt
    operand_is_correct = operand_truth == operand_attempt or \
        (operand_truth_value == operand_attempt_value and
            operand_truth_value is not None and operand_attempt_value is not None)
    version_is_correct = version_truth == version_attempt or \
        distance.levenshtein(version_truth, version_attempt) <= 1
    secret_is_correct = secret_truth == secret_attempt
    is_correct = \
        operator_is_correct and \
        operand_is_correct and \
        version_is_correct and \
        (not SECRET_REQUIRED or secret_is_correct)

    display_file_name = (truth[file_name_header] + ":").rjust(COL_WIDTH, "_").upper()
    if is_correct:
        print(f"{display_file_name} {CHECK_MARK}")
    else:
        print(f"{display_file_name} {MISSING_MARK if missing_attempt else X_MARK}")
    if verbose:
        def print_details(n, t, a, r):
            name_display = f"{'' if r else WRONG_MARK} {n}:".rjust(
                COL_WIDTH if r else COL_WIDTH - 1
            )
            truth_display = t.ljust(COL_WIDTH)
            attempt_display = a.ljust(COL_WIDTH)
            print(f"{name_display} {truth_display} {attempt_display}")
        print_details("operator", operator_truth, operator_attempt, operator_is_correct)
        print_details("operand", operand_truth, operand_attempt, operand_is_correct)
        print_details("version", version_truth, version_attempt, version_is_correct)
        print_details("secret", secret_truth, secret_attempt, secret_is_correct)

    return is_correct, secret_is_correct


def get_student_score(sid, verbose=False):
    submission = None
    try:
        submission = get_student_submission(sid)
    except Exception as e:
        print(f"  {MISSING_MARK} SUBMISSION FORMAT INVALID")

    solution = get_student_solution(sid)
    if not submission or not solution:
        return None if not submission else "?", None if not solution else len(solution), None

    num_correct = 0
    num_secrets_correct = 0
    for k, truth in sorted(solution.items(), key=lambda i: i[1]["file_name"]):
        attempt = submission[k] if k in submission else None
        is_correct, secret_is_correct = compare_submission_and_solution(truth, attempt, verbose=verbose)
        if is_correct:
            num_correct += 1
        if secret_is_correct:
            num_secrets_correct += 1

    total_possible = len(solution)
    return num_correct, total_possible, num_secrets_correct


def grade(selections: list = None, verbose: bool = False):
    selections = [str(s) for s in selections] if selections else None
    total_correct = 0
    total_passed = 0
    with open(STUDENTS_FILE, "r") as fin:
        students = json.load(fin)
    for sid, s in sorted(students.items(), key=lambda i: i[1]["last_name"]):
        if selections and sid not in selections:
            continue
        student_id = sid.ljust(COL_WIDTH)
        last_name = s["last_name"]
        first_name = s["first_name"].split(" ")[0]
        id_and_name = f"{student_id} {last_name}, {first_name}"
        print(id_and_name)

        num_correct, total_possible, num_secrets_correct = get_student_score(sid, verbose=verbose)

        above_threshold = num_correct and num_correct >= CORRECT_THRESHOLD
        passed = " PASSED" if num_correct and above_threshold else ""
        secret_passed = " + SECRET" if num_secrets_correct and num_secrets_correct >= SECRET_THRESHOLD else ""
        status = f"{passed}{secret_passed}".ljust(COL_WIDTH)
        print(f"{num_correct} / {total_possible} {status}")
        print()

        total_correct += num_correct if num_correct else 0
        total_passed += 1 if above_threshold else 0
    print(f"TOTAL CORRECT: {total_correct}")
    print(f"TOTAL PASSED: {total_passed} / {len(students)}")


if __name__ == "__main__":
    fire.Fire(grade)
