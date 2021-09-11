import pygame, keyboard, random, sys, time, json, os.path
pygame.init()
window = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Snake 🐍')
myfont = pygame.font.SysFont('Comic Sans MS', 24)

clock = pygame.time.Clock()

size = 35
x,y= int((500/size)/2),int((500/size)/2)
direction = "none"
score = 3

snake = [(int((500/size)/2),int((500/size)/2),score)]

highscore = 0

appleX, appleY = random.randint(0, int(500/size)-1), random.randint(0, int(500/size)-1)

devideTicks = 0
devideTicksMax = 1

removePart = 'nothing'

wait = True

colorPalette = ((182,196,84),(230, 211, 163),(115, 121, 12),(240, 240, 255),(216, 209, 116),(145, 151, 42),(200,181,133))

data = {
    "highscore":0
}
if os.path.isfile('./data.json') == True:
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        highscore = data['highscore']
else:
    with open('data.json','w') as dataFile:
        json.dump(data, dataFile)

def addApple():
    global score,snake, appleX, appleY
    score+=1
    for index in range(len(snake)):
        snake[index] = (snake[index][0], snake[index][1], snake[index][2]+1)
    appleX, appleY = random.randint(0, int(500/size)-1), random.randint(0, int(500/size)-1)

    for index in range(len(snake)):
        if (appleX,appleY,index) in snake:
            addApple()


def dead():
    global x,y,score,direction,snake, removePart, wait
    score = 3
    removePart = 'nothing'
    direction = 'none'
    snake = [(int((500/size)/2),int((500/size)/2),score)]
    x,y = int((500/size)/2),int((500/size)/2)
    wait = True
    time.sleep(1)

run = True

while run:
    devideTicks += 1
    if devideTicksMax < devideTicks:
        devideTicks = 0

    if score > highscore:
        highscore+=1
    data['highscore'] = highscore
    window.fill(colorPalette[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('data.json','w') as dataFile:
                json.dump(data,dataFile)
            run = False
            sys.exit()

    # draw grid
    for gridX in range(int(500/size)):
        for gridY in range(int(500/size)):
            if (gridX+gridY) % 2 == 0: pygame.draw.rect(window, colorPalette[1],(gridX*size+.5,gridY*size+.5,size-1,size-1))
            else: pygame.draw.rect(window, colorPalette[6],(gridX*size+.5,gridY*size+.5,size-1,size-1))

    # controlls
    if (keyboard.is_pressed('up') or keyboard.is_pressed('w')) and direction != 'down':
        direction = 'up'
        wait = False
    elif (keyboard.is_pressed('down') or keyboard.is_pressed('s')) and direction != 'up':
        direction = 'down'
        wait = False
    elif (keyboard.is_pressed('left') or keyboard.is_pressed('a')) and direction != 'right':
        direction = 'left'
        wait = False
    elif (keyboard.is_pressed('right') or keyboard.is_pressed('d')) and direction != 'left':
        direction = 'right'
        wait = False

    # movement
    if wait == False:
        if devideTicks == devideTicksMax:

            if direction == 'up': y-=1
            elif direction == 'down': y+=1
            elif direction == 'left': x-=1
            elif direction == 'right': x+=1
            snake.append((x,y,score))


            for index in range(len(snake)):
                snake[index] = (snake[index][0], snake[index][1], snake[index][2]-1)

                if snake[index][2]-1 < 1: 
                    removePart = snake[index]

                else:
                    # draw snake

                    tempX, tempY = snake[index][0], snake[index][1]
                    pygame.draw.rect(window, colorPalette[2],(tempX*size+4,tempY*size+4,size-8,size-8))
            if removePart in snake:
                snake.remove(removePart)

        # apple stuff
        if x == appleX and y == appleY:
            addApple()

        #dying
        if x >= 500/size-1: dead()
        elif x <= -1: dead()
        elif y >= 500/size-1: dead()
        elif y <= -1: dead()

        for index in range(len(snake)):
            if (x,y,index) in snake:
                dead()

    # draw apple
    pygame.draw.circle(window, (206, 200, 10),(appleX*size+(size/2),appleY*size+(size/2)),(7.5))

    # draw head
    pygame.draw.rect(window, colorPalette[5],(x*size+4,y*size+4,size-8,size-8))

    # draw ui background
    pygame.draw.rect(window, colorPalette[4],(14.3*size,0,200,490))

    # -------- Text

    textSurface = myfont.render("Score: "+str(score-3), False, colorPalette[3])
    window.blit(textSurface,(505,0))

    textSurface = myfont.render("HighScore: "+str(highscore-3), False, colorPalette[3])
    window.blit(textSurface,(505,30))

    textSurface = myfont.render("controlls:", False, colorPalette[3])
    window.blit(textSurface,(505,390))
    textSurface = myfont.render("w,a,s,d", False, colorPalette[3])
    window.blit(textSurface,(505,420))
    textSurface = myfont.render("or arrow keys.", False, colorPalette[3])
    window.blit(textSurface,(505,450))

    if devideTicks == devideTicksMax:
        pygame.display.flip()
    clock.tick(15)

pygame.quit()
exit()
