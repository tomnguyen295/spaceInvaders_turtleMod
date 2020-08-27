import turtle as t 
import random as r
import winsound as ws 
import pygame

# Set up screen
background = "Assets/OriginalAssets/background.gif"
wn = t.Screen()
wn.setup(width=0.5, height=0.9, starty=0)
wn.bgcolor("#636363")
wn.title("Space Invsaders")
wn.bgpic(background)
# wn.tracer(0) # Shuts off all turtle screen updates, will manually update in main loop


# Background music
pygame.mixer.init()
pygame.mixer.music.load("Assets/BorrowedAssets/Lost Sky - Fearless pt.II.wav")
pygame.mixer.music.play(-1,0.0)

# Register custom shapes

# invaderShape = "Assets/OriginalAssets/invader.gif"
# invaderShape2= "Assets/OriginalAssets/invader2.gif"
invaderShape3 = "Assets/OriginalAssets/invader3.gif"

# invaderShapes = [invaderShape,invaderShape2,invaderShape3]

playerShape = "Assets/OriginalAssets/player.gif"
bulletShape = "Assets/OriginalAssets/bullet.gif"
wn.register_shape(playerShape)
# wn.register_shape(invaderShape)
# wn.register_shape(invaderShape2)
wn.register_shape(invaderShape3)
wn.register_shape(bulletShape)

# Game state
gameOn = True


# Draw border
border = t.Turtle() # turtles are drawing pens
border.hideturtle()
border.speed(0) # 0 is fastest
border.color("crimson")
border.penup() # makes sure setposition won't leave a stroke
border.setposition(-300,-300)
border.pendown()
border.pensize(3)
for side in range(4):
    border.forward(600)
    border.left(90)

# Setting score
score = 0

# Draw score
scorePen = t.Turtle()
scorePen.speed(0)
scorePen.color("#4fe8c9")
scorePen.penup()
scorePen.setpos(-290,270)
# scoreString = "Score: %s" %score - alternate syntax
# scoreString = "Score: {}".format(score) - alternate syntax
scoreString = "Score: " + str(score)
scorePen.write(scoreString, False, align="left", font=("Sans-serif",14,"italic"))
scorePen.hideturtle()



# Create player
player = t.Turtle()
player.hideturtle()
player.color("red")
player.shape(playerShape)
player.penup()
player.speed(0)
player.setheading(90) # same as .left(90), .setheading(90) is north
player.setposition(0,-250)
player.showturtle()

# Create player bullet
bullet = t.Turtle()
bullet.hideturtle()
bullet.penup()
bullet.color("purple")
bullet.shape(bulletShape)
bullet.shapesize(.5,.5)
bullet.setheading(90) 
bullet.setpos(0,-400)
bullet.speed(0)


bulletSpeed = 10
# bulletSpeed = 7

# Define bullet state
# ready - ready to fire
# fire = bullet is firing
bulletState = "ready"

# Program bullet launch
def fire():
    global bulletState # Declare bulletState as global if function needs to change state
    if (bulletState == "ready"):
        bulletState = "fire"
        bullet.setpos(player.xcor(),player.ycor() + 10)
        bullet.showturtle()
        ws.PlaySound("Assets/BorrowedAssets/laser.wav", ws.SND_ASYNC | ws.SND_ALIAS)


def isCollision(t1, t2):
    distance = ((t2.xcor()-t1.xcor())**2+(t2.ycor()-t1.ycor())**2)**0.5
    if (distance < 15):
        return True
    return False
        


# Program movement of player
playerSpeed = 20
def moveLeft():
    if (player.xcor()-playerSpeed > -285):
        player.setx(player.xcor()-playerSpeed)
    else:
        player.setx(-285)

def moveRight():
    if (player.xcor()+playerSpeed < 285):
        player.setx(player.xcor()+playerSpeed)
    else:
        player.setx(285)


# Create keyboard bindings
wn.listen()
wn.onkeypress(moveLeft,"Left")
wn.onkeypress(moveLeft,"a")
wn.onkeypress(moveRight,"Right") 
wn.onkeypress(moveRight,"d")
wn.onkeypress(fire,"space")

# Alternate way to eliminate lag
wn.delay(1)

# Create enemies
# Choose number of enemies
number_of_enemies = 5
enemies = []

enemySpeed = 0.5
# enemySpeed = 0.05
# enemiesPos = [-200, 250]

# Add enemies to list
for i in range(number_of_enemies):
    enemy = t.Turtle()
    enemy.hideturtle()
    enemy.color("yellow")
    enemy.shape(invaderShape3)
    # enemy.shape(invaderShapes[r.randint(0,2)])
    enemy.penup()
    enemy.speed(0)

    
    enemy.setpos(r.randint(-200, 200), r.randint(100, 250)) 
    
    # enemy.setpos(enemiesPos[0], enemiesPos[1])
    enemy.showturtle()
    enemies.append(enemy)
    # if ((i+1)%10 == 0):
    #     enemiesPos[0] = -200
    #     enemiesPos[1] -= 50
    # else:
    #     enemiesPos[0] += 50


# Define game over function
def gameOver():
    global gameOn
    print("Game Over")
    print("Final Score:", score)
    gameOn = False

# Main game loop
while gameOn:
    # wn.update() #Manual update
    # Move the enemies
    for enemy in enemies:
        enemy.setx(enemy.xcor() + enemySpeed)
        # Boundary check for enemies
        if (enemy.xcor() > 285 or enemy.xcor() < -285):
            if (enemySpeed > 0):
                enemySpeed = -(enemySpeed + .025)
            else:
                enemySpeed = abs(enemySpeed) + .025
            for enemy in enemies:
                enemy.sety(enemy.ycor() - 50)
        if (enemy.ycor() < -300):
            gameOver()

        # Check for kill
        if isCollision(bullet, enemy):
            # Reset bullet
            ws.PlaySound("Assets/BorrowedAssets/explosion.wav", ws.SND_ASYNC | ws.SND_ALIAS)
            bulletState = "ready"
            bullet.hideturtle()
            bullet.setpos(0, -400)


            enemy.setpos(r.randint(-200, 200), r.randint(100, 250))
            
            # "Delete" enemy
            # enemy.setpos(0, 100000)

            # Update score
            score += 1
            scoreString = "Score: " + str(score)
            scorePen.clear()
            scorePen.write(scoreString, False, align="left", font=("Sans-serif",14,"italic"))


        # Check for loss  
        if isCollision(player, enemy):
            gameOver()

        

    # Fire bullet
    if (bulletState == "fire"):
        bullet.sety(bullet.ycor() + bulletSpeed)

    # Boundary check for bullet
    if (bullet.ycor() > 285):
        bulletState = "ready"
        bullet.hideturtle()

