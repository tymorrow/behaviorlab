import os
import glob

SUBMISSION_DIR_NAME = "submissions2"

all_submission_file_paths = glob.glob(os.path.join(SUBMISSION_DIR_NAME, "*"))

for f in all_submission_file_paths:
    base_dir = os.path.dirname(f)
    base_file_name = os.path.basename(f)
    parts = base_file_name.split("_")
    new_file_name = "_".join(parts[-2:])
    new_file_path = os.path.join(base_dir, new_file_name)
    os.rename(f, new_file_path)
