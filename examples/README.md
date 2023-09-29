# Examples

To run one of the examples, simply run this command from the root directory :

```bash
$ python3 -m examples/<example_name>
```

Note that credentials will be asked for each example to access the ADE website.

- [Simple](examples/simple.py)
- [ADE Printer](examples/ade_printer.py)
- [ADE ncurses](examples/ade_ncurses.py)

## Simple
[Simple](examples/simple.py) shows an example of how to use the module to get some information from the ADE website.

## ADE Printer
[ADE Printer](examples/ade_printer.py) prints the schedule of a student on the terminal using a grid layout.

## ADE ncurses
[ADE ncurses](examples/ade_ncurses.py) is a dynamic ncurses interface to display the schedule of a student.

Once the user has logged in, the schedule of today and tomorrow is displayed. The user can then navigate through the schedule using the arrow keys or `q` to quit:

- `>` : Next day
- `<` : Previous day
- `v` : Next week
- `^` : Previous week
- `q` : Quit