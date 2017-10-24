import pygame
import math
import time

pygame.init()

input = "poolrad2.jpg"
inputImg = pygame.image.load(input)
screen = pygame.display.set_mode((inputImg.get_width() * 4, inputImg.get_height()))
rendered = []
rendered.append(inputImg)
currentType = 1
w = inputImg.get_width()
h = inputImg.get_height()

# Colour spectrums/referneces
references = [
    pygame.image.load("colourReferences/normal.png"),
    pygame.image.load("colourReferences/deuteranopia.png"),
    pygame.image.load("colourReferences/protanopia.png"),
    pygame.image.load("colourReferences/tritanopia.png")
]
names = [
    "normal",
    "deuteranopia",
    "protanopia",
    "tritanopia"
]

def colorDistance(col1, col2):
    red=col1.r
    green=col1.g
    blue=col1.b

    red2=col2.r
    green2=col2.g
    blue2=col2.b

    distance = math.sqrt(pow((red - red2),2) + pow((green - green2),2) + pow((blue - blue2),2))
    return distance

def closestColour(col, ref):
    closestCol = (0,0,0)
    closestDis = 0

    for i in xrange(w):
        refCol = references[ref].get_at((i,0))
        if colorDistance(col, refCol) < closestDis:
            closestCol = refCol
            closestDis = colorDistance(col, refCol)
    return closestCol

lastTick = time.clock()

def convertImage(img, ref):
    print(img)
    new_img = pygame.Surface((img.get_width(), img.get_height()))
    global loopCount
    global lastTick
    global totalCount
    global w
    global h
    loopCount = 0
    totalCount = 0
    for x in xrange(w):
        for y in xrange(h):
            new_img.set_at((x, y), closestColour(img.get_at((x,y)), ref))
            loopCount += 1
            if lastTick < math.floor(time.clock()):
                totalCount += loopCount
                out = "    " + str(loopCount) + "/s"
                out += "    " + str(totalCount) + "/" + str(w * h)
                loopCount = 0
                lastTick = time.clock() + 1
                print(out)
    return new_img

def convertAll():
    global currentType
    global rendered
    global toShow
    if currentType < references.__len__():
        print(currentType)
        rendered.append(convertImage(inputImg, currentType))
        pygame.image.save(rendered[-1], names[currentType] + "_" + input)
        currentType += 1
        convertAll()
convertAll()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    screen.fill((0,0,0))
    for i in xrange(len(rendered)):
        screen.blit(rendered[i],(w * i,0))
    pygame.display.flip()