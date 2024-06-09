
import pgzero
import pgzrun
import pygame
from pgzero.builtins import Actor
state = "starting"
topLevelText = None
level1Btn = None
WIDTH = 725
HEIGHT = 300
TITLE = "EASTER ADVENTURE"
bgColor = "skyblue"
levelOneFinished = False
eggBasketScore = 0
setupForGo = False
currentItemsAnimations = []
currentItems = []

titleScreen = Actor("logo", (500,200))
titleScreen._surf = pygame.transform.scale(titleScreen._surf, (400, 200))

decorBasket = Actor("basket", (200,200))
decorBasket._surf = pygame.transform.scale(decorBasket._surf, (200, 200))

decorBaskety = Actor("basket", (675,200))
decorBaskety._surf = pygame.transform.scale(decorBaskety._surf, (200, 200))

level1Hint = Actor("catchtheeggs", (600, 100))
level1Hint._surf = pygame.transform.scale(level1Hint._surf, (400, 120))

eggBasket = Actor("emptybasket", (0, 725))
eggBasket._surf = pygame.transform.scale(eggBasket._surf, (125, 125))
debounce = False
def draw():
    global titleScreen,HEIGHT,WIDTH,state,topLevelText,level1Hint, currentItems, debounce
    screen.fill(bgColor)
    
    if state == "starting":
        decorBasket.draw()
        decorBaskety.draw()
        titleScreen.draw()
        screen.draw.text("Press enter to begin", (290,225))
    if state == "levelScreen":
        level1Btn.draw()
        topLevelText.draw()
        if levelOneFinished == True:
            screen.draw.text("Level Finished", (239,500))
    if state == "levelOne":
        screen.draw.text("Score: " + str(eggBasketScore), (50,50))
        screen.draw.text("Press L to restart", (75,50))
        level1Hint.draw()
        eggBasket.draw()
        if debounce == False:
            debounce = True
            currentItems = makeItems(1)
        
        for item in currentItems:
            item.draw()
        
def setupGo():
    global setupForGo
    setupForGo = True

def animateItems(items):
    global currentItemsAnimations,setupGo
    for i in items:
        duration = 3
        i.anchor = ("center", "bottom")
        animation = animate(i, duration=duration,y=HEIGHT + 450, on_finished=setupGo)
        currentItemsAnimations.append(animation)
    
def makeItems(howMany):
    toCreate = ["egg1", "egg2","egg3", "egg4", "egg5"]
    newItems = createItems(toCreate)
    layoutItems(newItems)
    animateItems(newItems)
    return newItems

def update():

    global eggBasket,eggBasketScore,state,levelOneFinished,bgColor
    if state == "levelOne":
        if levelOneFinished == False and eggBasketScore == 5:
            levelOneFinished = True
            bgColor = "black"
            state = "levelScreen"
        for item in currentItems:
            if item.collidepoint(eggBasket.pos):
                if "egg" in item.image and item.image != "catchtheeggs":
                    currentItems.remove(item)
                    eggBasketScore += 1
                    print("[Game Debugging]: Egg Caught")
       

def createItems(chosenItems):
    fish = []
    for item in chosenItems:
        newItem = Actor(item)
        newItem._surf = pygame.transform.scale(newItem._surf, (50, 60))
        fish.append(newItem)
    return fish #Baked

def layoutItems(items):
    gaps = len(items) + 1
    gapSize = WIDTH / gaps
    for index,item in enumerate(items):
        x = (index + 1) * gapSize
        item.x = x
    
def loadLevelScreen():
    print("[Game Debugging]: Level Selection Screen Loaded")
    global topLevelText,level1Btn
    topLevelText = Actor("choosealevel", (460,75))
    topLevelText._surf = pygame.transform.scale(topLevelText._surf, (600, 90))

    level1Btn = Actor("level1", (300,350))


def on_key_down(key):
    global decorBasket,decorBaskety, titleScreen,state,bgColor,debounce,eggBasketScore,setupForGo
    if key == keys.RETURN and state == "starting":
        
        state = "levelScreen"
        bgColor = "black"
        global HEIGHT,WIDTH
        HEIGHT = 650
        WIDTH = 1000
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        loadLevelScreen()

    if key == 49 and state == "levelScreen" and levelOneFinished == False:
        state = "levelOne"
        bgColor = "skyBlue"
        print("[Game Debugging]: Level 1 Started")

    if key == keys.L and state == "levelOne" and setupForGo == True:
        eggBasketScore = 0
        debounce = False
    
def on_mouse_move(pos):
    global state,eggBasket
    if state == "levelOne":
        eggBasket.pos = (pos[0] + 158, eggBasket.pos[1])








print("[Game Debugging]: Game Loaded")

pgzrun.go()

