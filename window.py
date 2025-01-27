from tkinter import *
from calcZoom import *
import random as rand
from math import *
import sys

class BarWindow:
    def __init__(self, root, file):
        self.root = root
        pic_label = Label(root, text='Click to Draw a Line along the Scale Bar')
        pic_label.pack()

        self.original = Image.open(file) # Load Image
        self.width, self.height = self.original.size
        
        # Initialize Frame and make scrollable
        self.canvasFrame = Frame(root)
        self.canvasFrame.pack(fill='both', expand=True)

        # Create an initial size for Image
        self.aspect_ratio = self.original.width / self.original.height
        self.curr_width, self.curr_height = self.setInitialDim()

        # Make a canvas
        self.app = calcZoom(self.canvasFrame, file)
        self.app.canvas.config(width=self.curr_width, height=self.curr_height)
        self.app.grid(row=0, column=0)  # show widget

        # Resize the image to the initial display size
        self.curr_image = self.original.resize((self.curr_width, self.curr_height), Image.LANCZOS)
        
        # Set the initial window size to match the scaled image dimensions
        win_width = self.curr_width + 15
        win_height = self.curr_height + 70
        self.root.geometry(f"{win_width}x{win_height}+15+15")

        # Set minimum window size
        self.root.minsize(win_width, win_height)

        # Bottom Frame Submit Section
        bottom_frame = Frame(root)
        bottom_frame.pack(side="bottom", fill="x", pady=5)
        
        self.zoom_factor = self.original.width / self.curr_width
        self.points = []
        self.ratio = 0

        lenLabel = Label(bottom_frame, text="Length of Scale Bar (mm)")
        lenLabel.pack(side="left", padx=5)
        self.lenInput = Entry(bottom_frame, justify="right")
        self.lenInput.insert(0, "150") 
        self.lenInput.pack(side="left", padx=5)

        submitBut = Button(bottom_frame, text='Enter', command=self.finish)
        self.app.canvas.bind('<Return>', self.enter)
        submitBut.pack(side="left", padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def enter(self, event):
        self.finish()

    # Find dimensions for the image to be a reasonable size for the computer
    # Hard coded to be 750 x 1000
    def setInitialDim(self):
        maxwidth = 1000    
        maxheight = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Adjust max dimensions to account for the Dock height (100px assumed for macOS)
        max_height = min(maxheight, screen_height - 200)  # Reduce height by Dock area
        max_width = min(maxwidth, screen_width)  # Ensure it doesn't exceed screen width

        if self.original.width > max_width or self.original.height > max_height:
            if self.original.width / max_width > self.original.height / max_height:
                # Width is the limiting factor
                return max_width, int(max_width / self.aspect_ratio)
            else:
                # Height is the limiting factor
                return int(max_height * self.aspect_ratio), max_height
        else:
            # If the image is smaller than the maximum allowed size, scale it up to the max size
            if self.original.width < max_width and self.original.height < max_height:
                if self.aspect_ratio > max_width / max_height:
                    return max_width, int(max_width / self.aspect_ratio)
                else:
                    return int(max_height * self.aspect_ratio), max_height
            else:
                # Use the original size if it fits within the maximum dimensions
                return self.original.width, self.original.height

    # closes window but allows for collection of data before destroying root
    def finish(self):
        if len(self.app.points) == 2:
            self.root.quit()

    # returns ratio mm : pixel
    def getConversion(self):
        if (len(self.app.points) == 2) & (self.lenInput != ""):
            return float(self.lenInput.get())  / self.app.getPixelLen()
        else: 
            return False
    
    def on_close(self):
        sys.exit(1)


# Recieve How big of a split the user would like the photo
class ResponseWindow:
    def __init__(self, root, path):
        self.root = root
        self.root.geometry("+15+15")
        self.split = 0 # the resulting split given by user

        # display the image to the user
        self.original= Image.open(path)
        s = self.original.resize(self.setInitialDim(), Image.LANCZOS)
        image = ImageTk.PhotoImage(s)
        panel = Label(root, image = image)
        panel.image = image
        panel.pack(side = "top", fill = "both", expand = "yes")

        # have the choices displayed at the bottom as buttons
        frame = tk.Frame(root)
        frame.pack(side='bottom')
        sizeLabel = tk.Label(frame, text="Choose Sizing:")
        sizeLabel.pack(side='left')
        lButton = tk.Button(frame, text='Cobble (1)', command= lambda: self.choose(1))
        mButton = tk.Button(frame, text='Mixed (4)', command= lambda: self.choose(4))
        sButton = tk.Button(frame, text='Small (16)', command= lambda: self.choose(16))
        lButton.pack(side='left')
        mButton.pack(side='left')
        sButton.pack(side='left')

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setInitialDim(self):
        maxwidth = 1000    
        maxheight = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        aspect_ratio = self.original.width / self.original.height

        # Adjust max dimensions to account for the Dock height (100px assumed for macOS)
        max_height = min(maxheight, screen_height - 200)  # Reduce height by Dock area
        max_width = min(maxwidth, screen_width)  # Ensure it doesn't exceed screen width

        if self.original.width > max_width or self.original.height > max_height:
            if self.original.width / max_width > self.original.height / max_height:
                # Width is the limiting factor
                return max_width, int(max_width / aspect_ratio)
            else:
                # Height is the limiting factor
                return int(max_height * aspect_ratio), max_height
        else:
            # If the image is smaller than the maximum allowed size, scale it up to the max size
            if self.original.width < max_width and self.original.height < max_height:
                if aspect_ratio > max_width / max_height:
                    return max_width, int(max_width / aspect_ratio)
                else:
                    return int(max_height * aspect_ratio), max_height
            else:
                # Use the original size if it fits within the maximum dimensions
                return self.original.width, self.original.height
    
    # collects the response choice of the user and closes window
    def choose(self, split):
        self.split = split
        self.root.quit()

    def on_close(self):
        sys.exit(1)

# handles the grain labelling
# ranges is a 2d array [divisions x 4] of the pixel bounds in the original image for the subimages
# n is the number of points to label
class CollectionWindow:
    def __init__(self, root, path, ranges, n, padx = 50, pady = 50):
        self.root = root
        self.n = n
        self.padx = padx
        self.pady = pady
        self.scale = 0 # true pixels / display pixels
        self.ranges = ranges # range of the cropped image from the original
        self.orig_image = Image.open(path).convert('L')
        self.width, self.height = self.initializeSize()
        self.curr_id = 0                        # the current subimage being labelled
        self.curr_im = None
    
        self.curr_max =  0                      # max number of points for current image
        self.current_point = 0                  # current rand point to be labelled (will be colored yellow)
        self.madePoints = []                    # list of user made points on canvas
        self.madeLines = []                     # list of lines on canvas
        self.data = []                          # collection of all line lengths in pixels of the scaled image

        self.root.title("Place lines along each grain's intermediate axis")
        frame = Frame(root, background='white')
        frame.pack(fill='x', side='bottom')
        nextButton = Button(frame, text='next', command=self.nextImage)
        nextButton.pack(side='right', padx=15)
        self.info = StringVar(value=f'{len(self.madeLines)} points labelled out of {self.curr_max}')
        label = Label(frame, textvariable=self.info, background='white', foreground='black')
        label.pack(side='left', padx=15)

        toolbar_height = frame.winfo_height()
        self.root.geometry(f"{self.width + 2*padx}x{self.height + 2* pady + toolbar_height}+100+0")

        # create random points
        self.randomPoints = self.createRandomPoints(n)       # create all the locations of the random points
        self.displayedPnts = []

        # Initialize Canvas
        self.canvas = Canvas(root, background='dark blue')
        self.canvas.pack(fill='both', expand=True)  # Ensure canvas resizes correctly
        self.curr_im = self.getImagePortion()

        self.canvas.config(width=self.width + 2 * padx, height=self.height + 2 * pady)
        self.canvas.create_image(padx, pady, image=self.curr_im, anchor='nw')

        # ability to make points and draw lines
        self.canvas.bind('<Button-1>', self.makePoint)
        self.root.bind('<BackSpace>', self.removeLast) # backspace availability to remove last
        self.root.bind('<Return>', self.enter)

        # add dots
        self.addDots()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def enter(self, event):
        self.nextImage()

    # creates random points for the user to label on the subimages
    def createRandomPoints(self, n):
        array = [[] for i in range(len(self.ranges))]
        for i in range(n):
            x = rand.randint(0, self.orig_image.width)
            y = rand.randint(0, self.orig_image.height)
            for j in range(len(self.ranges)):
                rang = self.ranges[j]
                if x >= rang[0] and x <= rang[2] and y >= rang[1] and y <= rang[3]:
                    array[j].append((x, y))
                    break
        return array
    # set initial size for the window
    def initializeSize(self):
        maxwidth = 1000    
        maxheight = 750

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Adjust max dimensions to account for the Dock height (100px assumed for macOS)
        max_height = min(maxheight, screen_height - 200)  # Reduce height by Dock area
        max_width = min(maxwidth, screen_width)  # Ensure it doesn't exceed screen width

        div = int(sqrt(len(self.ranges)))
        orig = np.array(self.orig_image.size) / div
        max_ratio = max_width / max_height
        orig_ratio = orig[0] / orig[1]

        if orig_ratio > max_ratio: # wider compared to max
            width = max_width
            self.scale = orig[0] / max_width
            height = int(orig[1] / self.scale)
            return (width, height)
        else:                      # tall compared to max
            height = max_height
            self.scale = orig[1] / max_height
            width = int(orig[0] / self.scale)
            return (width, height)

    # returns data scaled back to the original image's pixels
    def getData(self):
        results = np.array(self.data)
        pointLocations = [() for i in range(self.n)]
        k = 0
        for i in range(len(self.randomPoints)):
            for j in range(len(self.randomPoints[i])):
                x, y = self.randomPoints[i][j]
                pointLocations[k] = (x, y)
                k += 1
        return (pointLocations, results * self.scale)

    # shows the next subimage on the canvas if all points have been labelled on the current one 
    def nextImage(self):
        if len(self.madeLines) != self.curr_max:
            tk.messagebox.showerror('Error', f'Only {len(self.madeLines)} out of {self.curr_max} points have been labelled')
        else:
            self.addToData()
            if self.curr_id == len(self.ranges) - 1:
                self.root.quit()
            else:
                self.curr_id += 1
                self.canvas.delete('all')
                self.madeLines = []
                self.madePoints = []
                self.displayedPnts = []
                self.curr_im = self.getImagePortion()
                self.canvas.create_image(self.padx, self.pady, image = self.curr_im, anchor = 'nw')
                self.addDots()
    
    # returns the current subimage
    def getImagePortion(self):
        image = self.orig_image.crop(self.ranges[self.curr_id])
        image = image.resize((self.width, self.height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    # adds the length of the drawn lines to the data
    def addToData(self):
        data = []
        for line in self.madeLines:
            box = self.canvas.coords(line)
            data.append(self.length_of_line(box))
        self.data.extend(data)
    
    # Calculates length of a line
    def length_of_line(self, box):
        x0, y0, x1, y1 = box
        hyp = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        return hyp

    # allows for going backwards if a mistake was made by pressing backspace
    def removeLast(self, event):
        if len(self.madePoints) > 0:
            self.canvas.delete(self.madePoints[len(self.madePoints) - 1])
            if len(self.madePoints) % 2 == 0 and len(self.madeLines) > 0:
                self.canvas.delete(self.madeLines[len(self.madeLines) - 1])
                self.madeLines.pop()
                self.info.set(value = f'{len(self.madeLines)} points labelled out of {self.curr_max}')
                if self.current_point < len(self.displayedPnts):
                    self.canvas.itemconfig(self.displayedPnts[self.current_point], fill='red')
                self.current_point -= 1
                self.canvas.itemconfig(self.displayedPnts[self.current_point], fill='yellow')
            self.madePoints.pop()

    # drawing points. Called when canvas is clicked
    def makePoint(self, event):
        if len(self.madeLines) < self.curr_max:
            self.madePoints.append(self.placePoint(event.x, event.y))
            if len(self.madePoints) % 2 == 0:
                self.madeLines.append(self.drawLine())
                self.info.set(value = f'{len(self.madeLines)} points labelled out of {self.curr_max}')
                self.canvas.itemconfig(self.displayedPnts[self.current_point], fill='red')
                self.current_point += 1
                if self.current_point < len(self.displayedPnts):
                    self.canvas.itemconfig(self.displayedPnts[self.current_point], fill='yellow')


    # draw a line whenever 2 points are made
    def drawLine(self):
        # gather last two points and convert them to coordinates
        pnt1 = self.canvas.bbox(self.madePoints[len(self.madePoints) - 1])
        pnt1 = self.center(pnt1)
        pnt2 = self.canvas.bbox(self.madePoints[len(self.madePoints) - 2])
        pnt2 = self.center(pnt2)
        return self.canvas.create_line(pnt1[0], pnt1[1], pnt2[0], pnt2[1], fill='red', width=3)

    # place randomly placed dots on the subimage for the user to label the grains they land on
    def addDots(self):
        self.curr_max = len(self.randomPoints[self.curr_id])
        # create points
        for pnt in self.randomPoints[self.curr_id]:
            x, y = pnt
            x = (x - self.ranges[self.curr_id][0]) / self.scale
            y = (y - self.ranges[self.curr_id][1]) / self.scale
            dot = self.placePoint(x + self.padx, y + self.pady)
            self.displayedPnts.append(dot)
        self.current_point = 0
        if self.curr_max > 0:
            self.canvas.itemconfig(self.displayedPnts[0], fill='yellow')
        self.info.set(value = f'{len(self.madeLines)} points labelled out of {self.curr_max}')
    
    # gets the coordinate of the point given its circle bbox
    def center(self, pntbox):
        return (mean((pntbox[0], pntbox[2])),mean((pntbox[1], pntbox[3])))
    
    # place a point on the canvas where the user had clicked
    def placePoint(self, x, y, color='red'):
        bnd = 3
        return self.canvas.create_oval(x-bnd, y-bnd, x+bnd, y+bnd, fill=color)

    def on_close(self):
        sys.exit(1)



