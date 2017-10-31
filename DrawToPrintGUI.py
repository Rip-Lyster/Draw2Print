#Copyright: Rip Lyster 2016

#Barebones.py taken from the barebones example on the 112 website

from tkinter import *
from DrawToPrintBackEnd import *
import copy
import random

def init(data):
    data.profiles = []
    data.numProfiles = 0
    data.points = []
    data.width = 800
    data.height = 800
    data.outlineColor = "#990033"
    data.bgColor = "#666699"
    data.bBgColor = "white"
    data.shapeColor = "black"
    data.gridColor = "grey"
    data.gridPos = (0,0)
    data.gridSpacing = 60
    data.dBoxX = 20
    data.dBoxY = 20
    data.dBoxW = 600
    data.dBoxH = 600
    data.pointRad = 4
    data.mBoxX = 640
    data.mBoxY = 20
    data.mBoxW = 180
    data.mBoxH = 200
    data.message = ""
    data.coordinates = []
    data.sliceButtX = 640
    data.sliceButtY = 640
    data.sliceButtW = 140
    data.sliceButtH = 140
    data.settingH = 125
    data.settingW = 125
    data.objHX = 40
    data.objHY = 650
    data.objHeight = 1.0
    data.layerHX = 185
    data.layerHY = 650
    data.layerHeight = 0.2
    data.bedHeight = 200
    data.profileX = 650
    data.profileY = 480
    data.extrusionX = 330
    data.extrusionY = 650
    data.extrusion = 1
    data.bufferX = 475
    data.bufferY = 650
    data.buffer = 1.4
    data.splash = 1
    data.help = 0
    data.splashClickSize = 35
    data.splashClickSizeDS = 1
    data.splashFunTexts = [FunText(),FunText(),FunText(),FunText(),FunText(),FunText(),FunText()]

class FunText(object):
    text1 = ["so much",
            "such",
            "very",
            "much",
            "good",
            "wow"]

    text2 = ["3d",
            "print",
            "draw",
            "generative",
            "doge",
            "112",
            "polygon",
            "layers",
            "additive"]

    color = ["red","orange","blue","indigo","violet","pink"]

    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 800)
        self.dx = random.randint(-9, 9)
        self.dy = random.randint(-9, 9)
        self.id1 = random.randint(0,5)
        self.id2 = random.randint(0,8)
        self.color = random.randint(0,5)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDx(self):
        self.x += self.dx

    def getDy(self):
        self.y += self.dy

    def getText(self):
        return FunText.text1[self.id1] + " " + FunText.text2[self.id2]

    def getColor(self):
        return FunText.color[self.color]

def drawSplashScreen(canvas,data):
    canvas.create_rectangle(0,0,data.width+10,data.height+10,fill="#e6ffcc")

    for text in data.splashFunTexts:
        x1 = text.getX()
        # print(x1)
        y1 = text.getY()
        # print(y1)
        if(x1 < data.width and x1 > 0 and
               y1 < data.height and y1 > 0):
            text.getDx()
            text.getDy()
            canvas.create_text(text.getX(),text.getY(),fill=text.getColor(),
                           text=text.getText(),
                           font="Haettenschweiler 30",
                           justify=CENTER,anchor=CENTER)
        else:
            text.__init__()

    canvas.create_text(data.width/2,data.height/3,fill="#248f24",
                       text="Draw2Print",font="Haettenschweiler 90",
                       justify=CENTER,anchor=CENTER)
    canvas.create_text(data.width/2,data.height-30,fill="#248f24",
                       text="A project by Rip Lyster",font="Haettenschweiler 25",
                       justify=CENTER,anchor=CENTER)

    clickFont = "Haettenschweiler %d" %data.splashClickSize
    canvas.create_text(data.width/2,2*data.height/3,fill="#248f24",
                       text="Click Anywhere To Start",font=clickFont,
                       justify=CENTER,anchor=CENTER)

    if(data.splashClickSize > 40):
        data.splashClickSizeDS = -1
    elif(data.splashClickSize < 30):
        data.splashClickSizeDS = 1
    data.splashClickSize += data.splashClickSizeDS

def drawHelpScreen(canvas,data):
    canvas.create_rectangle(0,0,data.width+10,data.height+10,fill="LightSalmon2")
    canvas.create_rectangle(20,150,data.width-20,data.height-20,
                            fill="white",width=5,outline="grey")
    canvas.create_text(data.width/2,75,text="Help",fill="grey",
                       font="Haettenschweiler 80")
    helpText = """    Draw2Print allows you to take any 2d image and create a 3d printable file from it. You
    can create profiles and build up object complexity using simple drawing techniques.
    To create objects, use the following steps:

        1.  Click on the canvas to draw the desired shape

        2.  Select the height of that profile using the profile height setting

        3.  If you want to add another profile, click the add profile button and continue drawing
            the next profile

        4.  When you're satisfied with the object, modify the layer height and buffer options to
            the desired values

        5.  When you're completely satisfied with all of the settings select the SLICE OBJECT
            button

        6.  Open the folder that you run this program from and find the gcode.txt file

        7.  Use this gcode.txt file as input into your 3d printer to print your object

    Click anywhere to return to the canvas
    """
    canvas.create_text(40,170,anchor=NW,font="Haettenschweiler 19",
                       justify=LEFT,width=720,text=helpText,
                       fill="grey25")

def initMessage(data):
    data.message = """
    Instructions:\n
    1. Draw your profile\n
    2. Save profiles\n
    3. Modify settings\n
    4. Slice your model\n
    5. Print\n\n\n\n\n
    Press H for help"""

def drawPrevProfile(canvas,data):
    if(len(data.profiles) > 0):
        for profile in data.profiles:
            canvas.create_polygon(getPoints(profile[1]),fill=data.gridColor,
                                  stipple="gray50")
            prevPoint=None
            for point in getPoints(profile[1]):
                canvas.create_oval(point[0]-data.pointRad,point[1]-data.pointRad,
                                   point[0]+data.pointRad,point[1]+data.pointRad,
                                   fill=data.gridColor)
                if(prevPoint!=None):
                    canvas.create_line(prevPoint,point,fill=data.outlineColor)
                prevPoint = point
            canvas.create_line(getPoints(profile[1])[0],getPoints(profile[1])[-1],fill=data.outlineColor)

def drawSettings(canvas,data):
    def drawNumSetting(x,y,var,text,units):
        canvas.create_rectangle(x,y,
                                x+data.settingW,
                                y+data.settingH,
                                fill = data.bBgColor,
                                outline = data.gridColor,
                                width=2)
        canvas.create_text(x+data.settingW-10,
                           y+4*data.settingH/5,
                           anchor=E,justify="center",
                           text = "+", font = "Sans 40",
                           fill="grey")
        canvas.create_text(x+12,
                           y+4*data.settingH/5-6,
                           anchor=W,justify="center",
                           text = "-", font = "Sans 40",
                           fill="grey")
        canvas.create_text(x+data.settingW/2,
                           y-2, anchor=S,
                           justify="center",text="%s" %(text),
                           font = "Sans 11")
        canvas.create_text(x+data.settingW/2,
                           y+2*data.settingH/5,
                           anchor=CENTER,justify="center",
                           text=("%.2f%s" %(var,units)) if isinstance(var,float) else ("%d%s" %(var,units)),
                           font="Sans 22" if units != "" else "Sans 27")
    drawNumSetting(data.objHX,data.objHY,data.objHeight,"Object Height","mm")
    drawNumSetting(data.layerHX,data.layerHY,data.layerHeight,"Layer Height","mm")
    drawNumSetting(data.profileX,data.profileY,data.numProfiles,"Profiles","")
    drawNumSetting(data.extrusionX,data.extrusionY,data.extrusion,"Extrude Per MM","")
    drawNumSetting(data.bufferX,data.bufferY,data.buffer,"Stroke Buffer","mm")

def drawSliceButt(canvas,data):
    canvas.create_rectangle(data.sliceButtX,data.sliceButtY,
                            data.sliceButtX+data.sliceButtW,data.sliceButtY+data.sliceButtH,
                            fill = data.bBgColor,outline = data.gridColor,width=2)
    canvas.create_text(data.sliceButtX+data.sliceButtW/2,
                       data.sliceButtY+data.sliceButtH/2,
                       justify = "center",text = "SLICE\nOBJECT",
                       font = "Sans 24")

def drawDBox(canvas,data):
    canvas.create_rectangle(data.dBoxX,data.dBoxY,
                                  data.dBoxX+data.dBoxW,
                                  data.dBoxY+data.dBoxH,
                                  outline=data.gridColor,width=2,
                                  fill=data.bBgColor)
    for lineX in range(data.gridSpacing,data.dBoxW+60,data.gridSpacing):
        canvas.create_line(data.dBoxX+lineX, data.dBoxY,
                           data.dBoxX+lineX, data.dBoxH+data.dBoxY,
                           fill=data.gridColor)
        canvas.create_text(data.dBoxX+lineX-12,data.dBoxY+10,
                           text=str(int(lineX/3)),
                           fill=data.gridColor)
    for lineY in range(data.gridSpacing,data.dBoxH+60,data.gridSpacing):
        canvas.create_line(data.dBoxX,data.dBoxY+lineY,
                           data.dBoxW+data.dBoxX,data.dBoxX+lineY,
                           fill=data.gridColor)
        canvas.create_text(data.dBoxX+12,data.dBoxY+lineY-10,
                           text=str(int(lineY/3)),
                           fill=data.gridColor)

def drawShape(canvas, data):
    if(len(data.points) > 0):
        canvas.create_polygon(data.points,fill=data.shapeColor)
        prevPoint=None
        for point in data.points:
            canvas.create_oval(point[0]-data.pointRad,point[1]-data.pointRad,
                               point[0]+data.pointRad,point[1]+data.pointRad,
                               fill=data.outlineColor)
            if(prevPoint!=None):
                canvas.create_line(prevPoint,point,fill=data.outlineColor)
            prevPoint = point
        canvas.create_line(data.points[0],data.points[-1],fill=data.outlineColor)

def drawMessageBox(canvas,data):
    initMessage(data)
    canvas.create_text(625, 20, text=data.message, anchor=NW,
                       font="Sans 12")

def createCoords(points):
    coords = []
    for point in points:
        coord = ((point[0]-20)/3,(point[1]-20)/3)
        coords.append(coord)
    return coords

def getPoints(coords):
    points = []
    for coord in coords:
        point = ((coord[0]*3+20),(coord[1]*3+20))
        points.append(point)
    return points

def pressedArea(event,x,y,h,w):
    return(event.y > y and event.x > x and
           event.y < y + h and event.x < x + w)

def mousePressed(event, data):
    if(data.splash == 0 and data.help == 0):
        if(pressedArea(event,data.dBoxX,data.dBoxY,data.dBoxH,data.dBoxW)):
            data.points.append((event.x,event.y))
            data.coordinates = createCoords(data.points)
        if(pressedArea(event,data.sliceButtX,data.sliceButtY,data.sliceButtH,data.sliceButtW)):
            if(data.numProfiles == 0):
                writeFile("gcode.txt",getGCode(data.coordinates,data.extrusion,data.layerHeight,data.buffer,
                                               200,data.objHeight))
            elif(data.numProfiles > 0):
                writeFile("gcode.txt",getProfilesGCode(data.profiles,data.extrusion,data.layerHeight,data.buffer,
                                                       200))
            print("Written to file gcode.txt")

        #Object Height
        if(pressedArea(event,data.objHX,data.objHY,data.settingH,data.settingW/4)):
            if(data.objHeight > 0.2): data.objHeight -= 1.0
        if(pressedArea(event,data.objHX+3*data.settingW/4,data.objHY,data.settingH,data.settingW/4)):
            data.objHeight += 1.0

        #Layer Height
        if(pressedArea(event,data.layerHX,data.layerHY,data.settingH,data.settingW/4)):
            if(data.layerHeight > 0.1): data.layerHeight -= 0.1
        if(pressedArea(event,data.layerHX+3*data.settingW/4,data.layerHY,data.settingH,data.settingW/4)):
            data.layerHeight += 0.1

        #Extrusion
        if(pressedArea(event,data.extrusionX,data.extrusionY,data.settingH,data.settingW/4)):
            if(data.extrusion > 0.1): data.extrusion -= 0.1
        if(pressedArea(event,data.extrusionX+3*data.settingW/4,data.extrusionY,data.settingH,data.settingW/4)):
            data.extrusion += 0.1

        #Buffer
        if(pressedArea(event,data.bufferX,data.bufferY,data.settingH,data.settingW/4)):
            if(data.buffer > 0.2): data.buffer -= 0.2
        if(pressedArea(event,data.bufferX+3*data.settingW/4,data.bufferY,data.settingH,data.settingW/4)):
            data.buffer += 0.2


        #Profiles
        if(pressedArea(event,data.profileX,data.profileY,data.settingH,data.settingW/4)):
            if(data.numProfiles > 0):
                data.numProfiles -= 1
                data.points = getPoints(data.profiles.pop()[1])
        if(pressedArea(event,data.profileX+3*data.settingW/4,data.profileY,data.settingH,data.settingW/4) and
           len(data.points) > 2):
            data.numProfiles += 1
            data.profiles.append((data.objHeight,copy.deepcopy(data.coordinates)))
            data.points = []
            data.coordinates = []
            data.objHeight = 1.0

    if(data.splash == 1 and data.help == 0):
        data.splash = 0
    if(data.splash == 0 and data.help == 1):
        data.help = 0

def keyPressed(event, data):
    if(data.splash == 0 and data.help == 0):
        if(event.keysym == "Delete"):
            data.points.pop()
            data.coordinates.pop()
        if(event.keysym == "h"):
            data.help = 1

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if(data.splash == 0 and data.help == 0):
        canvas.create_rectangle(0,0,data.width+10,data.height+10,fill=data.bgColor)
        drawDBox(canvas,data)
        drawPrevProfile(canvas,data)
        drawShape(canvas,data)
        drawMessageBox(canvas,data)
        drawSliceButt(canvas,data)
        drawSettings(canvas,data)
    if(data.splash == 1 and data.help == 0):
        drawSplashScreen(canvas,data)
    if(data.splash == 0 and data.help == 1):
        drawHelpScreen(canvas,data)

#Run function taken from Barebones.py on the course website
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("Good bye!")

run(800, 800)