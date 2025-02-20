# Manual Point Count

## Description
This tool is designed to calculate grain size estimates given an image of grains. This program returns a `.xlsx` containing the locations and sizes of each labeled grain in the image as well as the average grain size.

## Instructions

### Initial Setup

#### Conda
It is recommended to use a conda environment to run this program. Use the code below to create a conda environment for this program called, `pointcount`

`conda env create -f pointcount.yml`

To activate the conda environment:
`conda activate pointcount`

#### Images

Create a folder containing images to gather point count data for

***Follow the instructions below to run the tool.***

### Point Count Tool - Initialization
1. Open the PointCountPy folder
3. Run DigitalPebbleCountTool: `python DigitalPebbleCountTool.py`
4. In the pop-up, select the folder containing images for grain size analysis
5. In the next window, select where you would like to save your `.xlsx` file
6. In the next window, specify how many points you would like to label for each image

### Point Count Tool - Data Gathering
1. Click the two ends of the scale bar to draw a line and type in the length of the scale bar in mm at the bottom. Click Submit when done.
    - zoom in/out with scroll wheel
    - scroll using mouse
    - drawing a new line will override the old drawn line
2. Click how many frames you would like to split the image into for point collection
    - Suggested 1 for cobble, 4 for mixed, 16 for smaller grains 
3. For each subimage draw a line for each of the points in the photo. 
    - The current grain to label will be colored yellow
    - Pressing delete will undo and pressing enter will submit the subimage
9. Once the program finished, a `.xlsx` file is created containing the location and sizes of each labeled grain

## Next steps / Improvements
- Handling Errors 
- 5) Collect metadata about date image was taken to put into the excel file
- 7a) have the ability to draw outside image boundries (in case rock is on edge)
- 7a) collect date taken data from image metadata to include into the output file 
- 7a) image should initialize being scaled into the window
- 7a) when image is zoomed in/out points remain relative to the image (will be large when zoomed in)
            - preferred the points remain the same size no matter what the zoom
- 7c) Have points show up one at a time. (Or any other ideas so points to be labelled can be located easily)
- 8) unsure if data should be formatted in which way:
     - all grain sizes and then all point locations 
     ("grain size 1", grain size 2, ... , grain location 1, grain location 2, ...)
     - grain size paired with grain location
     (grain size 1, grain location 1, grain size 2, grain location 2, ...)

### Cite
This codebase is built off Ian Miller's Manual MATLAB Point Count Code and adapted into Python
