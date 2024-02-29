# Behavior Lab

This repo builds a unique *Behavior Lab* for each student.
A behavior lab consists of *N* programs for which a student must identify certain characteristics.
These characteristics will be need to be logged in an *answers* CSV file and compared to the solution for grading.


## Installation

```bash
pip install -r requirements.txt
```


## Usage

### Generating

If you have Python 3.X, you can run:

```bash
./generate.sh
```

or:

```bash
python3 generate.py
```

For `generate.py` to work, you will need to add a `students.json` file with the following structure:

```
{
    "<student 1 identifier>": {
        // Other info (not currently used)
    },
    "<student 2 identifier>": {
        // Other info (not currently used)
    }
    ...
}
```


### Grading

Grading is done with `grade.py`.

