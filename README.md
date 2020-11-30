# CLIPS - Minesweeper

## Structure

### *gui.py*
GUI-based for display predicted bomb in game Minesweeper

### *main.py*
CLI-based for display predicted bomb in game Minesweeper included Board structure class 

### *input.in*
Input file example

### *minesweeper.clp*
CLIPS file for updating and inferencing facts. 

## User Manual
### Prerequisite
Make sure `python >3.7` installed with library:
1. `clipspy`
2. `tkinter` 

### CLI
Run:
```
python main.py < input.in
```

### GUI
Run:
```
python gui.py < input.in
```

`input.in` is text file with specification below:
1. First row is size of board (NxN)
2. Second row is sum of bomb (X)
3. X next row is bomb coordinat with format “i, j” (without quotes)


## Contributors
Name | NIM
---- | ----
Ilham Syahid Syamsudin | 13518028
Okugata Fahmi N. Y. F. | 13518031
Taufiq Husada D. | 13518058
Dhafin Rayhan Ahmad | 13518063