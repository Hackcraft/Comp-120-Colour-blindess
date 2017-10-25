import pygame
import math
import time

pygame.init()

input = "lily.jpg"
inputImg = pygame.image.load(input)
screen = pygame.display.set_mode((inputImg.get_width() *
                                  4, inputImg.get_height()))
rendered = []
rendered.append(inputImg)
imgWidth = inputImg.get_width()
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


# Calculating the distance between the colour
def colourDistance(col1, col2):
    distance = math.sqrt(pow((col1.r - col2.r), 2) +
                         pow((col1.g - col2.g), 2) + pow((col1.b - col2.b), 2))
    return distance


# Compares the pixels in a normal colour spectrum to find the closest match
# And returns the position of the pixel
def closestColourPos(img, col):
    closestCol = 0
    closestDis = colourDistance(col, references[0].get_at((0, 0)))
    refWidth = references[0].get_width()

    for i in xrange(refWidth):
        refCol = references[0].get_at((i, 0))
        if colourDistance(col, refCol) < closestDis:
            closestDis = colourDistance(col, refCol)
            closestCol = i
    return closestCol


# Loops through each pixel in the input image and replaces the pixel with the
# colour from the colour blind spectrum
def convertImage(img, refs):
    images = []
    imgWidth = img.get_width()
    imgHeight = img.get_height()

    loopCount = 0
    lastTick = time.clock()
    totalCount = 0

    for i in xrange(refs):
        images.append(pygame.Surface((imgWidth, imgHeight)))

    for x in xrange(imgWidth):
        for y in xrange(imgHeight):
            closest = closestColourPos(img, img.get_at((x, y)))
            for i in xrange(refs):
                images[i].set_at((x, y), references[i+1].get_at((closest, 0)))

            loopCount += 1
            if lastTick < math.floor(time.clock()):
                totalCount += loopCount
                out = "    " + str(loopCount * refs) + "/s"
                out += "    " + str(totalCount * refs) + "/" + \
                       str(imgWidth * imgHeight * refs)
                loopCount = 0
                lastTick = time.clock() + 1
                print(out)
    return images


# Tells the convert image function how many references to process and
# saves the files in a local folder
def convertAll():
        total = len(references) - 1
        images = convertImage(inputImg, len(references) - 1)
        for i in xrange(total):
            pygame.image.save(images[i], names[i+1] + "_" + input)
            rendered.append(images[i])

convertAll()

# Displays the output of the converted images
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    screen.fill((0, 0, 0))
    for i in xrange(len(rendered)):
        screen.blit(rendered[i], (imgWidth * i, 0))
    pygame.display.flip()
