# Behavior Lab

This repo builds a unique *Behavior Lab* for each student.
A behavior lab consists of *N* programs for which a student must identify certain characteristics.
These characteristics will be need to be logged in an *answers* CSV file and compared to the solution for grading.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

This isn't a python package, nor does it currently have dependencies.
If you have Python 3.X, just run the following on a Linux-based system:

```bash
./generate.sh
```

Alternatively, if you don't have bash, you can run:

```bash
python3 generate.py
```

### Students

For `generate.py` to work, you will need to add a `students.json` file in the same directory.

The file should follow the following structure:

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
