# s99954fh - Frederick Hall - Assessment 2 program for COMP16321 - due Fri 13 Dec @ 18:00
# My snake game - last edited Fri 13 Dec
# Layout of game:
#     - Main menu with 4 options, START, QUIT, LEADERBOARD, CHEATS
#     - START starts the game in normal basic mode
#     - QUIT exits the application immediately after displaying a message
#     - LEADERS displays a leaderboard with names and scores
#     - CHEATS displays the 3 cheats incorporated into the game;
#           - NODIE means the user cannot die
#           - 2X SCORE means that your score increase is doubled
#           - X FOOD means that you get extra food when
#
#     - Once you die the restart or quit page is shown.
#
#     - Buttons to press in game:
#           - P causes the game to pause NOTE: works on MAC OS that the window pauses whilst the window is displayed but not the lab machine i used
#           - B causes the boss page to be displayed
#           - Q quits the current game and goes to the restart or quit page


from tkinter import Tk, PhotoImage, Button, Label, messagebox, Canvas, Entry
import random



def gameend():          # This is the function that is called when a game has been quit or the user has died, it presents the user with options to restart or quit the game
    window.destroy()    # Destroys the game window

    global gameendpage                                          # makes the module running this window global so it can be terminated from anywhere
    gameendpage = Tk()                                          # opens a new window
    gameendpage.title("Restart?")                               # Title of the new window
    gameendpage.geometry("500x500")                             # Geometry of new window
    gameendpage.configure(background = "black")                 # Background of window
    
    restartpic = PhotoImage(file = "restart.png")               # Creates restart button, assigns it a function to go back to the menu when pressed and places it somewhere in the window
    restart = Button(gameendpage, image = restartpic, width = 470, height = 160, command = lambda: menu())
    restart.place(x = 15, y = 70)

    endpic2 = PhotoImage(file = "endpic2.png")                  # Creates quit button, assigns it a function when pressed and places it in the window
    leave = Button(gameendpage, image = endpic2, width = 470, height = 160, command = lambda: endgame())
    leave.place(x = 15, y = 240)
    
    gameendpage.mainloop()                                      # runs the window
    

def placeFood():                                                # Place food function, runs again with a second set of food variables if the cheat XTRA food is chosen
    global food, foodX, foodY
    food = canvas.create_rectangle(0,0, snakeSize, snakeSize, fill="#FF0073" )      # creates the food itself
    foodX = random.randint(0, width-snakeSize)                                      # designates it a random x coordinate 
    foodY = random.randint(0, height-snakeSize)                                     # designates it a random y coordinate
    canvas.move(food, foodX, foodY)                                                 # moves the food to the random coordinates
    if cheatextrafood == True:                                                      # repeats above steps if cheat activated
        global food1, foodX1, foodY1
        food1 = canvas.create_rectangle(0,0, snakeSize, snakeSize, fill="#FF0073" )
        foodX1 = random.randint(0, width-snakeSize)
        foodY1 = random.randint(0, height-snakeSize)
        canvas.move(food1, foodX1, foodY1)


def moveSnake():                                                                    # functionality to actually move the snake
    canvas.pack()
    positions = []
    positions.append(canvas.coords(snake[0]))                                       # tells the program where the snake is at this instant in time 
    if positions[0][0] < 0:                                                                 # these next 4 statements determine what direction the snake is moving in and move it one more space in that direction
        canvas.coords(snake[0],width,positions[0][1],width-snakeSize,positions[0][3])
    elif positions[0][2] > width:
        canvas.coords(snake[0],0-snakeSize,positions[0][1], 0,positions[0][3])
    elif positions[0][3] > height:
        canvas.coords(snake[0],positions[0][0],0-snakeSize,positions[0][2],0)
    elif positions[0][1] < 0:
        canvas.coords(snake[0],positions[0][0],height ,positions[0][2],height-snakeSize)
    positions.append(canvas.coords(snake[0]))
    if direction == "left":                                                         # next 4 if statements tell the program to change the direction in which the snake is continuously moving
        canvas.move(snake[0], -snakeSize,0)
    elif direction == "right":
        canvas.move(snake[0], snakeSize,0)
    elif direction == "up":
        canvas.move(snake[0], 0,-snakeSize)
    elif direction == "down":
        canvas.move(snake[0], 0,snakeSize)
    if 'gameOver' not in locals():                                                  # checks if the snake has died, if not then keeps moving the snake
        window.after(90, moveSnake)
    for i in range(1, len(snake)):
        positions.append(canvas.coords(snake[i]))
    for i in range(len(snake) - 1):
        canvas.coords(snake[i+1],positions[i][0], positions[i][1],positions[i][2],positions[i][3])  # iterates the positions held in the variable to keep an up to date view of where the snake is 
    sHeadPos = canvas.coords(snake[0])
    foodPos = canvas.coords(food)                                   # check where the main food is to see if snake is touching it later
    if cheatextrafood == True:                                      # if the cheat for extra food is active, check where the food is to see if eaten later
        food1Pos = canvas.coords(food1)
    if overlapping(sHeadPos, foodPos):                              # if snake is touching initial food, move the food and grow the snake by 1
        moveFood()
        growSnake()
    if cheatextrafood == True:                                      # only run if cheat for extra food is active, check if snake touching it and move food1 and snake
        if overlapping(sHeadPos, food1Pos):
            moveFood1()
            growSnake()
    for i in range(1,len(snake)):
        if overlapping(sHeadPos, canvas.coords(snake[i])):          # Here the program checks if the snake is touching any section of his own body, if he is then the game will end and a messabox displayed
            if cheatnodie == False:
                gameOver = True
                messagebox.showinfo("GAME OVER", "You died")        # message displayed in seperate window telling user they have killed their player
                gameend()                                           # call the game end function to allow for a restart or not
            

    
def leftKey(event):             # Next 4 definitions are for defining what happens when the direction key is pressed
    global direction            # the definition makes the direction global so that the whole program can view its contents
    direction = "left"          # direction is changed depending on the key pressed, and when movesnake is next gone through the snake will change direction depending on that

def rightKey(event):
    global direction
    direction = "right"

def upKey(event):
    global direction
    direction = "up"

def downKey(event):
    global direction
    direction = "down"

def pauseKey(event):
    messagebox.showinfo("PAUSE", "GAME PAUSED, CLOSE WINDOW TO RESUME")     # Pause the game, window pops up saying paused, user must close window to resume playing

def bossKey(event):         #bosskey activated to hide the game using a new large window titled email which is closed normally to continue
    bosspage = Tk()
    bosspage.title("Email")
    bosspage.geometry("1000x1000")
    bosspage.mainloop()
    

def quitKey(event):         # quit key is defined here to quit the game, inform the user of this and then go to the restart or quit application window
    messagebox.showinfo("QUIT", "YOU HAVE QUIT THE GAME")
    gameend()

def growSnake():                        # Process to increase snake size by 1, adds a block onto the end of the snake in a different colour to the main head, dependant on direction
    lastElement = len(snake) - 1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(canvas.create_rectangle(0,0, snakeSize,snakeSize, fill="#00FF00"))
    if (direction == "left"):
        canvas.coords(snake[lastElement+1],lastElementPos[0]+snakeSize,lastElementPos[1],lastElementPos[2]+snakeSize,lastElementPos[3])
    elif (direction == "right"):
        canvas.coords(snake[lastElement+1],lastElementPos[0]-snakeSize,lastElementPos[1],lastElementPos[2]-snakeSize,lastElementPos[3])
    elif (direction == "up"):
        canvas.coords(snake[lastElement+1],lastElementPos[0], lastElementPos[1]+snakeSize,lastElementPos[2], lastElementPos[3]+snakeSize)
    else:
        canvas.coords(snake[lastElement+1],lastElementPos[0],lastElementPos[1]-snakeSize,lastElementPos[2], lastElementPos[3]-snakeSize)
    global score                            # makes score readable by every part of the program
    if cheatdoublescore == False:           # if cheat not activated then only increase score by 10 as usual
        score += 10
    elif cheatdoublescore == True:          # if cheat activated then increase score by double the usual amount
        score += 20
   
    txt = "Score: " + str(score)                    # updates the text containing the score
    canvas.itemconfigure(scoreText, text=txt)       # set the location of the text and output it on the canvas that is the game interface
    

def moveFood():                                     # this function moves the food after it is consumed to a point off screen so it cannot be eaten again, it then is moved to a new place
    global food, foodX, foodY                       # by choosing a new random x and y coordinate then moving the food there
    canvas.move(food, (foodX*(-1)), (foodY*(-1)))
    foodX = random.randint(0,width-snakeSize)
    foodY = random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)

def moveFood1():                                    # this function does the same as the previous one just with the second extra food, will only ever be called if the cheat is active
    global food1, foodX1, foodY1
    canvas.move(food1, (foodX1*(-1)), (foodY1*(-1)))
    foodX1 = random.randint(0,width-snakeSize)
    foodY1 = random.randint(0,height-snakeSize)
    canvas.move(food1, foodX1, foodY1)

def overlapping(a, b):                                                  # this function takes two inputs and sees if the positions overlap at any point by  comparing the contents of the variable sent to it
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:     # returns true or false depending on this
        return True
    return False

def setWindowDimensions(w,h):                   # creates a window whose size depends on the size of the screen the user has and gives the window a title
    window = Tk()
    window.title("My Snake Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


width = 550                             # set the original width and height to be used by the program
height = 550
def rungame():                          # the actual game running part of the program, contains key information and creates the snake block
    try:
        mainmenu.destroy()              # when run it terminates the window that it came from which is either the cheatpage or the main menu
    except:
        cheatpage.destroy()
    
    global window, canvas, snake, snakeSize, score, txt, scoreText, direction # make these global so that anyone can access and change them within the program
    window = setWindowDimensions(width, height)                                 # create the window itself
        
    canvas = Canvas(window, bg = "black", width = width, height = height)       # creates the game canvas that contains all the objects that will be used

    snake = []
    snakeSize = 15      # gives the snake a size and creates the snake variable

    snake.append(canvas.create_rectangle(snakeSize,snakeSize, snakeSize * 2, snakeSize * 2, fill="#32CD32" ))   # creates the physical object that is the snake on the canvas and gives it a colour

    score = 0                   # sets the initial score to 0 so it never keeps going
    txt = "Score: " + str(score)    # defines what the text is originally 
    scoreText = canvas.create_text( width/2 , 10 , fill="white" , font="Times 20 italic bold", text=txt)    # creates the text in the window
    canvas.bind("<Left>", leftKey)              # the next 6 canvas.bind(...) statements binds keys to functions so if you press them something will happen when they are pressed
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("p", pauseKey)
    canvas.bind("b", bossKey)
    canvas.bind("q", quitKey)
    canvas.focus_set()
    direction = "right"             # sets the initial direction for the snake to be going

    placeFood()                     # begins running the movement functions and the placing food functions
    moveSnake()
    window.mainloop()               # run the actual loop

def endgame():                      # quitting the application fully displays a message box saying goodbye and ends the windows
    messagebox.showinfo("Thank YOU", "Thank you for playing my game!")
    try:
        mainmenu.destroy()          # tries to end both windows as they are the only two that point here
    except:
        gameendpage.destroy()

def leaders():                          # leaderboard output function, reads from a file and outputs leaders in a messagebox
    file = open("leaderboard.txt", "r")
    lines = file.read()
    messagebox.showinfo("LEADERBOARD", lines)
    file.close()

def returntomenu():             # from the cheatpage return to menu and ends the cheatpage.
    cheatpage.destroy() 
    menu()

def nodiecheat():               # activates the no die cheat where it is impossible to die and starts the game
    global cheatnodie
    cheatnodie = True
    rungame()

def doublescorecheat():         # activates the double score cheat and starts the game
    global cheatdoublescore
    cheatdoublescore = True
    rungame()

def extrafoodcheat():           # activates the extra food cheat and starts the game
    global cheatextrafood
    cheatextrafood = True
    rungame()

def cheats():                   # cheat page, creates a large window of 500px X 500px and runs it with a black background, ends the mainmenu page
    mainmenu.destroy()
    global cheatpage
    cheatpage = Tk()
    cheatpage.title("Cheat page")
    cheatpage.geometry("500x500")
    cheatpage.configure(background = "black")

    nodiepic = PhotoImage(file = "nodiepic.png")        # here imports the image for and creates the cheat button for the NODIE cheat
    nodie = Button(cheatpage, image = nodiepic, width = 330, height = 130, command = lambda: nodiecheat())
    nodie.place(x = 30, y = 30)

    doublescorepic = PhotoImage(file = "doublescorepic.png")    # imports the image for and creates the cheat button for the doublescorecheat
    doublescore = Button(cheatpage, image = doublescorepic, width = 330, height = 130, command = lambda: doublescorecheat())
    doublescore.place(x = 30, y = 170)

    extrafoodpic = PhotoImage(file = "extrafoodpic.png")    # imports the image for and creates the cheat button for the doublescorecheat
    extrafood = Button(cheatpage, image = extrafoodpic, width = 330, height = 130, command = lambda: extrafoodcheat())
    extrafood.place(x = 30, y = 310)
    
    backpic = PhotoImage(file = "backpic.png")      #returns to the main menu
    back = Button(cheatpage, image = backpic, width = 100, height = 410, command = lambda: returntomenu())
    back.place(x = 370, y = 30)

    cheatpage.mainloop()
    
    

def menu():
    try:
        gameendpage.destroy()       #ends the restart game page if it was running as it points back here or continues to run the main code
    except:
        None
        
    global mainmenu, cheatnodie, cheatdoublescore, cheatextrafood

    cheatnodie = False              # initially sets the cheats to be inactive
    cheatdoublescore = False
    cheatextrafood = False
    
    mainmenu = Tk()                     # creates a large window with an image as the background
    mainmenu.title("Snake Game")
    mainmenu.geometry("1000x1000")
    
    background_image = PhotoImage(file = "snakepic.png")
    background_label = Label(mainmenu, image=background_image)
    background_label.place(x=0, y=0)


    startpic = PhotoImage(file = "startpic.png")           #  import the 4 images used for the buttons
    endpic = PhotoImage(file = "endpic.png")
    leaderspic = PhotoImage(file = "leaderspic.png")
    cheatspic = PhotoImage(file = "cheatpic.png")

    start = Button(mainmenu, image = startpic, width = 330, height = 130, command = lambda: rungame())      # start the game
    start.place(x = (185), y = (305))
    end = Button(mainmenu, image = endpic, width = 310, height = 130, command = lambda: endgame())      # quit the application
    end.place(x = (195), y = (445))
    leaderboards = Button(mainmenu, image = leaderspic, width = 340, height = 130, command = lambda: leaders())     # display the leaders
    leaderboards.place(x = (525), y = (305))
    cheatcodes = Button(mainmenu, image = cheatspic, width = 330, height = 130, command = lambda: cheats())     # display cheat page
    cheatcodes.place(x = (530), y = (445))

    mainmenu.title("Snake Game")
    mainmenu.mainloop()         # run the main menu window
    
menu()          # run the main menu function to start the

# thank you and i hope you enjoyed this piece of coursework :)
