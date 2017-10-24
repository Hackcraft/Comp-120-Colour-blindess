import pygame
import math
import time

pygame.init()

input = "lily.jpg"
inputImg = pygame.image.load(input)
screen = pygame.display.set_mode((inputImg.get_width() * 4, inputImg.get_height()))
rendered = []
rendered.append(inputImg)
w = inputImg.get_width()
startTime = time.clock()

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

def colourDistance(col1, col2):
    distance = math.sqrt(pow((col1.r - col2.r),2) + pow((col1.g - col2.g),2) + pow((col1.b - col2.b),2))
    return distance

def closestColourPos(img, col):
    closestCol = 0
    closestDis = colourDistance(col, references[0].get_at((0,0)))
    w = references[0].get_width()

    for i in xrange(w):
        refCol = references[0].get_at((i,0))
        if colourDistance(col, refCol) < closestDis:
            closestDis = colourDistance(col, refCol)
            closestCol = i
    return closestCol

def convertImage(img, refs):
    images = []
    w = img.get_width()
    h = img.get_height()

    loopCount = 0
    lastTick = time.clock()
    totalCount = 0

    for i in xrange(refs):
        images.append(pygame.Surface((w, h)))

    for x in xrange(w):
        for y in xrange(h):
            closest = closestColourPos(img, img.get_at((x, y)))
            for i in xrange(refs):
                images[i].set_at((x, y), references[i+1].get_at((closest, 0)))

            loopCount += 1
            if lastTick < math.floor(time.clock()):
                totalCount += loopCount
                out = "    " + str(loopCount * refs) + "/s"
                out += "    " + str(totalCount * refs) + "/" + str(w * h * refs)
                loopCount = 0
                lastTick = time.clock() + 1
                print(out)
    return images

def convertAll():
        total = len(references) - 1
        images = convertImage(inputImg, len(references) - 1)
        for i in xrange(total):
            pygame.image.save(images[i], names[i+1] + "_" + input)
            rendered.append(images[i])

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