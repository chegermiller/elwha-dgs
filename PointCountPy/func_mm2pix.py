from window import *
import sys

# handles the meathod for calculating the mm to pixel ratio
def mm2pix(image_path):
    root = tk.Tk()
    root.title('Draw a Line along the Scale Bar')
    root.geometry('1000x750+0+0')
    window = BarWindow(root, image_path)
    root.mainloop()
    ratio = window.getConversion()
    try:
        root.destroy()
    except:
        pass
    return ratio

# asks user what size divisions they want their image
def getSize(image_path):
    root = tk.Tk()
    window1 = ResponseWindow(root, image_path)
    root.mainloop()
    split = window1.split
    try:
        root.destroy()
    except:
        pass
    return split

# handles the grain labeling operation
def action(n, sizing, image_path):
    original_im = Image.open(image_path)
    im_wid, im_height = original_im.size

    # calculate the range of each cropped image
    unitDim =  int(sqrt(sizing))
    if unitDim == 0:
        sys.exit(1)
    imageRanges = [[0 for i in range(4)] for j in range(sizing)]
    widthBit = im_wid // unitDim
    heightBit = im_height // unitDim
    for i in range(unitDim):
        for j in range(unitDim):
            imageRanges[i * unitDim + j] = [i * widthBit, 
                              j * heightBit,
                              (i + 1) * widthBit,
                              (j + 1) * heightBit]
    root = tk.Tk()
    window = CollectionWindow(root, image_path, imageRanges, n)
    root.mainloop()
    data = window.getData()
    try:
        root.destroy()
    except:
        pass
    return data
