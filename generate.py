import json
import os
import random
from string import Template
from config import variants

BUILD_DIR_NAME = "build"
TEMPLATE_DIR_NAME = "templates"
BASE_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR_NAME, "base.c")
SOLUTION_FILE_NAME = "solution.txt"
STUDENTS_FILE = "students.json"
SUPPORTED_INT_OPERAND_TYPES = ["int8_t", "int16_t", "int32_t",
                               "uint8_t", "uint16_t", "uint32_t"]
SUPPORTED_FLOAT_OPERAND_TYPES = ["float", "double"]

random.seed(42)


class TemplatesMixin:
    def _read_template(self, template_path):
        with open(template_path) as template:
            return template.read()

    def render(self, template_path, **kwargs):
        return Template(
            self._read_template(template_path)
        ).substitute(**kwargs)


def sample_args(kwarg_variants: dict) -> dict:
    sampled_args = {}
    operand_type = kwarg_variants["operand_type"]
    for k, v in kwarg_variants.items():
        if isinstance(v, tuple):
            min_value, max_value = v
            if operand_type in SUPPORTED_INT_OPERAND_TYPES:
                sampled_args[k] = random.randint(min_value, max_value)
            elif operand_type in SUPPORTED_FLOAT_OPERAND_TYPES:
                sampled_args[k] = random.uniform(min_value, max_value)
            else:
                raise ValueError(f"{operand_type} is not supported!")
        elif isinstance(v, list):
            sampled_args[k] = random.choice(v)
        else:
            sampled_args[k] = v

    if sampled_args["minor_version"] < sampled_args["major_version"]:
        sampled_args["secret_key"] = random.randint(
            sampled_args["minor_version"],
            sampled_args["major_version"]
        )
    else:
        sampled_args["secret_key"] = random.randint(
            sampled_args["major_version"],
            sampled_args["minor_version"]
        )
    sampled_args = {k: str(v) for k, v in sampled_args.items()}
    return sampled_args


templator = TemplatesMixin()
with open(STUDENTS_FILE, "r") as fin:
    students = json.load(fin)

for sid, _ in students.items():
    build_basedir = os.path.join(BUILD_DIR_NAME, sid)
    os.makedirs(build_basedir, exist_ok=True)
    solutions_path = os.path.join(BUILD_DIR_NAME, sid + ".solution.csv")

    solutions = []
    for conf in variants:
        operand_zero_or_nonzero = conf["kwarg_variants"]["operand_zero_or_nonzero"]
        sampled_args = sample_args(conf["kwarg_variants"])
        template_file_path = os.path.join(
            TEMPLATE_DIR_NAME,
            conf["template_file"]
        )

        cfile_contents = templator.render(template_file_path, **sampled_args)
        cfile_contents = templator.render(
            BASE_TEMPLATE_PATH,
            body=cfile_contents,
            **sampled_args
        )

        cfile_name = conf["file_name"] + ".c"
        cfile_path = os.path.join(build_basedir, cfile_name)
        with open(cfile_path, "w") as fout:
            fout.write(cfile_contents)

        solution_operand = sampled_args["operand"]
        if operand_zero_or_nonzero and \
           solution_operand != "None":
            solution_operand = int(solution_operand)
            if solution_operand > 0:
                solution_operand = "Nonzero"
            else:
                solution_operand = "Zero"
        solutions.append((
            conf["file_name"],
            sampled_args["operator"],
            str(solution_operand),
            "{}.{}".format(sampled_args["major_version"],
                           sampled_args["minor_version"]),
            sampled_args["secret_key"]
        ))

    with open(solutions_path, "w") as fout:
        fout.write("file_name,operator,operand,version,secret\n")
        for s in solutions:
            fout.write(",".join(s) + "\n")
