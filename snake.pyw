import pygame, keyboard, random, sys,time, json, os.path
from pygame import mixer

mixer.init()
pygame.init()

window = pygame.display.set_mode((710, 500))
pygame.display.set_caption('Snake')

if os.path.isfile('icon.png'):
    snakeLogo = pygame.image.load('icon.png')
    snakeLogo = pygame.transform.scale(snakeLogo, (160, 160))
    pygame.display.set_icon(snakeLogo)

myfont = pygame.font.SysFont('Comic Sans MS', 24)
titleFont = pygame.font.SysFont('Comic Sans MS', 48)


window.fill((182,196,84))
pygame.display.flip()
textSurface = titleFont.render("Loading...", False, (240, 240, 255))
window.blit(textSurface,(200,200))
if os.path.isfile('icon.png'):
    window.blit(snakeLogo, (500,150))
    snakeLogo = pygame.transform.scale(snakeLogo, (120, 120))
pygame.display.flip()

if os.path.isfile('music.mp3'):
    mixer.Channel(0).play(pygame.mixer.Sound('music.mp3'))
    mixer.Channel(0).set_volume(.4)
    mixer.Channel(1).set_volume(.2)

clock = pygame.time.Clock()
tick = 0
tickMax = 20

size = 35
x,y= int((500/size)/2),int((500/size)/2)
direction = "none"
SetDirection = 'none'
score = 3

snake = [(int((500/size)/2),int((500/size)/2),score)]

highscore = 0

appleX, appleY = random.randint(0, int(500/size)-1), random.randint(0, int(500/size)-1)

devideTicks = 0
devideTicksMax = 2

removePart = 'nothing'

wait = True


data = {
    "highscore":0,"MuteMusic":False, "MuteSFX":False,"showFPS":False
}
if os.path.isfile('./data.json') == True:
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        highscore = data['highscore']
        if data["MuteMusic"] == True:
            mixer.stop()
else:
    with open('data.json','w') as dataFile:
        json.dump(data, dataFile)

def addApple():
    global score,snake, appleX, appleY
    if data["MuteSFX"] == False and os.path.isfile('asset/music.mp3'): mixer.Channel(1).play(pygame.mixer.Sound('asset/coin.mp3'))
    for index in range(len(snake)):
        snake[index] = (snake[index][0], snake[index][1], snake[index][2]+1)
    appleX, appleY = random.randint(0, int(500/size)-1), random.randint(0, int(500/size)-1)
    for i in range(len(snake)):
        for index in range(len(snake)):
            if (appleX,appleY,index) == snake[i]:
                addApple()
            


def dead():
    global x,y,score,direction,snake, removePart, wait, appleX, appleY
    appleX, appleY = random.randint(0, int(500/size)-1), random.randint(0, int(500/size)-1)
    score = 3
    removePart = 'nothing'
    direction = 'none'
    snake = [(int((500/size)/2),int((500/size)/2),score)]
    x,y = int((500/size)/2),int((500/size)/2)
    wait = True
    time.sleep(.5)

run = True

while run:
    tick +=1
    if tick == tickMax+1:
        tick = 0
    if score > highscore:
        highscore+=1
    data['highscore'] = highscore
    window.fill((182,196,84))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('data.json','w') as dataFile:
                json.dump(data,dataFile)
            run = False
            sys.exit()

    # draw grid
    pygame.draw.rect(window, (130,130,130),(4,4,491,491))
    for gridX in range(int(500/size)):
        for gridY in range(int(500/size)):
            if (gridX+gridY) % 2 == 0: pygame.draw.rect(window, (230, 211, 163),(gridX*size+5.5,gridY*size+5.5,size-1,size-1))
            else: pygame.draw.rect(window, (200,181,133),(gridX*size+5.5,gridY*size+5.5,size-1,size-1))

    # controlls
    if (keyboard.is_pressed('up') or keyboard.is_pressed('w')) and direction != 'down':
        SetDirection = 'up'
        wait = False
    elif (keyboard.is_pressed('down') or keyboard.is_pressed('s')) and direction != 'up':
        SetDirection = 'down'
        wait = False
    elif (keyboard.is_pressed('left') or keyboard.is_pressed('a')) and direction != 'right':
        SetDirection = 'left'
        wait = False
    elif (keyboard.is_pressed('right') or keyboard.is_pressed('d')) and direction != 'left':
        SetDirection = 'right'
        wait = False

    # movement
    if wait == False and tick == tickMax:
        direction = SetDirection

        if direction == 'up': y-=1
        elif direction == 'down': y+=1
        elif direction == 'left': x-=1
        elif direction == 'right': x+=1
        snake.append((x,y,score))


    for index in range(len(snake)):
        if tick == tickMax:
            snake[index] = (snake[index][0], snake[index][1], snake[index][2]-1)

        if snake[index][2]-1 <= 0 and tick == tickMax:
            removePart = snake[index]

        else:
            # draw snake

            tempX, tempY = snake[index][0], snake[index][1]
            if index%2 == 0:pygame.draw.rect(window, (115, 121, 12),(tempX*size+5,tempY*size+5,size,size))
            else: pygame.draw.rect(window, (90, 106, 0),(tempX*size+5,tempY*size+5,size,size))

    if removePart in snake:
        snake.remove(removePart)

    # apple stuff
    if x == appleX and y == appleY:
        addApple()
        score+=1

    #dying
    if x >= 500/size-1: dead()
    elif x <= -1: dead()
    elif y >= 500/size-1: dead()
    elif y <= -1: dead()

    for index in range(len(snake)):
        if (x,y,index) in snake: dead()

    # draw apple
    pygame.draw.circle(window, (220, 220, 10),(appleX*size+(size/2)+5,appleY*size+(size/2)+5),(7.5))

    # draw head
    pygame.draw.rect(window, (115, 121, 12),(x*size+5,y*size+5,size,size))

    # draw ui background
    pygame.draw.rect(window, (130,130,130),(14.3*size+4,4,202,492))
    pygame.draw.rect(window, (216, 209, 116),(14.3*size+5,5,200,490))

    # -------- Text

    textSurface = myfont.render("Score: "+str(score-3), False, (240, 240, 255))
    window.blit(textSurface,(510,0))

    textSurface = myfont.render("HighScore: "+str(highscore-3), False, (240, 240, 255))
    window.blit(textSurface,(510,30))

    textSurface = myfont.render("controlls:", False, (240, 240, 255))
    window.blit(textSurface,(510,390))
    textSurface = myfont.render("w,a,s,d", False, (240, 240, 255))
    window.blit(textSurface,(510,420))
    textSurface = myfont.render("or arrow keys.", False, (240, 240, 255))
    window.blit(textSurface,(510,450))

    if data['showFPS'] == True:
        textSurface = myfont.render(str(clock)[11:][:3], False, (240, 0, 0))
        window.blit(textSurface,(10,5))



    if os.path.isfile('asset/icon.png'):
        window.blit(snakeLogo, (540,200))

    
    pygame.display.flip()
    clock.tick(150)

pygame.quit()
sys.exit()
