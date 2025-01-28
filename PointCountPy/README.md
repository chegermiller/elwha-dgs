# Purpose
This tool is designed to calculate grain size estimates based off an image of grains.

# Instructions
1. Open the PointCountPy folder
2. Create a folder of images to obtain grain size data for
3. Run DigitalPebbleCountTool
4. In the pop-up, answer how many points you would like to label for each image
5. Select all images you would like to analyze from the file dialog
6. Next it will prompt you to name an excel file for output
7. Instructions for each image:
    a. Click the two ends of the scale bar to draw a line and type in the length 
       of the scale bar in mm at the bottom. Click Submit when done.
            - zoom in/out with scroll wheel
            - drawing a new line will override the old drawn line
    b. Click the sizing you would prefer for the image
    c. For each subimage draw a line for each of the points in the photo. 
        - The current grain to label will be colored yellow
        - Pressing delete will undo and pressing enter will submit the subimage
8. After everything is done, the output excel file should be filled in

# Next steps / Improvements
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

# Cite
This codebase is built off Ian Miller's Manual Point Count Code and adapted into Python
