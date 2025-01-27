from tkinter import filedialog, simpledialog
import pandas as pd 
import os
from func_mm2pix import *

# Step 1:  Get Photos
file_paths = filedialog.askopenfilenames(
    title="Select .jpg files",  # Window title
    filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],  # Allowed file types
    initialdir=os.path.dirname(os.path.abspath(__file__))  # Set initial directory to the script's folder
)

file_names = [os.path.basename(path) for path in file_paths]

Table = {'File_Name': file_names} # Dictionary to eventually convert to pandas table

if not file_names:
    sys.exit(1)

# Get output file
output = filedialog.asksaveasfile(initialfile = 'Untitled.xlsx', defaultextension=".xlsx", initialdir=os.path.dirname(os.path.abspath(__file__)), 
                                  filetypes=[("Excel Documents","*.xlsx")])

if not output:
    sys.exit(1)

# Step 2:  Set Parameters and prep output

# Asks user how many points they would like to label per image
n = simpledialog.askinteger("Input", "How many points do you want to analyze in each photo?", initialvalue=100)
if not n:
    n = 10 

pointEsimates = np.zeros((len(file_paths), n))
grainLoc = [[() for i in range(n)] for j in range(len(file_paths))]
dateTaken = [""] * len(file_paths)
ratios = np.zeros(len(file_paths))
meanGsmm = np.zeros(len(file_paths))

# Step 3:  Process

for i in range(len(file_paths)):
    # get mm : pixel ratio5
    ratios[i] = mm2pix(file_paths[i])

    # Get how big of a split the user would like for the photo
    sizing = getSize(file_paths[i])

    # Draw the lines on the grains and returns data (in pixels)
    locations, lengths = action(n, sizing, file_paths[i])

    # Convert data to mm
    true_data = np.array(lengths) * ratios[i]
    grainLoc[i] = locations
    pointEsimates[i] = true_data
    meanGsmm[i] = mean(true_data)

# Add all the data to the dictionary
Table['Date_Taken'] = dateTaken
Table['mm to Pixel Conversion'] = ratios
Table['Mean GS (mm)'] = meanGsmm
for i in range(n): 
    name = 'Grain ' + str(i + 1) + " Size (mm)"
    Table[name] = pointEsimates[:, i]
    name = 'Grain ' + str(i + 1) + " Location (pxls)"
    Table[name] = [row[i] for row in grainLoc]

# convert dictionary into a dataframe
df = pd.DataFrame(Table)

# write dataframe to output file
df.to_excel(output.name)

    

