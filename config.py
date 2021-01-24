variants = [
    {
        "file_name": "fish_paste",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "<<",
                ">>",
            ],
            "operand": (1, 7),
            "operand_zero_or_nonzero": False,
            "operand_type": "uint8_t",
            "operand_fmt": "%u",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "P",
        },
    },
    {
        "file_name": "tartar_sauce",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "<<",
                ">>",
            ],
            "operand": (1, 15),
            "operand_zero_or_nonzero": False,
            "operand_type": "int16_t",
            "operand_fmt": "%d",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "L",
        },
    },
    {
        "file_name": "neptune",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "&",
                "|",
            ],
            "operand": (1, 4294967295),
            "operand_zero_or_nonzero": False,
            "operand_type": "uint32_t",
            "operand_fmt": "%u",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "A",
        }
    },
    {
        "file_name": "mother_of_pearl",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "^"
            ],
            "operand": (1, 4294967295),
            "operand_zero_or_nonzero": False,
            "operand_type": "uint32_t",
            "operand_fmt": "%u",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "N",
        }
    },
    {
        "file_name": "jumping_jellyfish",
        "template_file": "operator_only.template",
        "kwarg_variants": {
            "operator": [
                "~"
            ],
            "operand": None,
            "operand_zero_or_nonzero": False,
            "operand_type": "uint32_t",
            "operand_fmt": "%u",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "K",
        }
    },
    {
        "file_name": "flappin_flounders",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "||",
                "&&"
            ],
            "operand": (0, 1),
            "operand_zero_or_nonzero": True,
            "operand_type": "uint32_t",
            "operand_fmt": "%u",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "T",
        }
    },
    {
        "file_name": "barnacle_head",
        "template_file": "operator_operand.template",
        "kwarg_variants": {
            "operator": [
                "==",
                "!="
            ],
            "operand": (0, 1),
            "operand_zero_or_nonzero": True,
            "operand_type": "int16_t",
            "operand_fmt": "%d",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "O",
        }
    },
    {
        "file_name": "kelp_for_brains",
        "template_file": "operator_only.template",
        "kwarg_variants": {
            "operator": [
                "!"
            ],
            "operand": None,
            "operand_zero_or_nonzero": False,
            "operand_type": "int16_t",
            "operand_fmt": "%d",
            "major_version": (1, 20),
            "minor_version": (1, 20),
            "secret": "N",
        }
    }
]
