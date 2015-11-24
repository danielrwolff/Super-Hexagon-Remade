#Daniel
#17/01/2014
#SuperHexagonV1.py

import pygame, math, random
pygame.init()
screen = pygame.display.set_mode([1200,800])
pygame.display.set_caption("Super Hexagon")

#Set up variables
page = 'main'                                                                               #Defines which page of the menu you are on.              
hexSize = 50                                                                                #Defines the size of the Hexagon.
timeCount = 0                                                                               #Keeps track of the survival time of the player. Reset after death.
activeMenuOption = 2                                                                        #Keeps track of what option of the menu is highlighted.
tutorialStage = 0                                                                           #Keeps track of what section of the tutorial you are on.

bgMainColour = [[255,40,40],[100,100,100],False]                                            #Holds the main background colours in a list, and the switch bool that determines whether or not the colours have switches positions. [mainColour, contrastColour, switch] . 
bgColourDrawMain = [255,40,40]                                                              #Variable allows the switching of colours in the background. This variable represents the section thats colour is the main colour.
bgColourDrawContrast = [255,65,65]                                                          #The contrasting colour of the main colour. (The main value + 25).
objColour = [255,120,0]                                                                     #Defines the obstacles' colour.
textBoxColour = [0,0,0]                                                                     #Defines the colour of the HUD boxes that contain text.

pulseLen = 0                                                                                #Represents the distance the object is in the pulse (the range).
pulseInc = 0.8                                                                              #Defines the speed in which the game pulses.
obstaclePushBack = 0                                                                        #Allows animation of obstacles moving off the screen upon death.

rotPos = 0                                                                                  #Defines the rotation position for all objects (not including the player).
rotSpeed = 0.5                                                                              #Define rotSpeed through a function.
rotInput = 0
playerRotChange = 0

origin = [screen.get_width()/2,screen.get_height()/2]                                       #Defines the origin for the game. (Center of screen).
playerInfo = [[0,0],[0,0],[0,0],60,2,30,10]                                                 #Defines player info.
obstacles = []                                                                              #Defines the obstacle info (for each obstacle).
removeObstacles = []                                                                        #When an obstacle needs to be removed, it gets appended to here and removed later.
highscoreList = [0,0,0,0]                                                                   #Keeps track of the highscore for each level.

#Set up transitions and animations
timeHUDorigin = [screen.get_width(),0]                                                      #Sets the origin for the timeHUD during gameplay.
gradeHUDorigin = [0,0]                                                                      #Sets the origin for the gradeHUD during gameplay.
scoreHUDorigin = [-800,screen.get_height()/2 - 150]                                         #Sets the origin for the scoreHUD after gameplay.
score2HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1]]                #Sets the origin for the second scoreHUD after gameplay.
score3HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1] + 150]          #Sets the origin for the third scoreHUD after gameplay.

#Set up fonts
fontLoc = (pygame.font.match_font('impact'))                                                #Holds the font used for all text within the game. (Finds the font location and uses the font).
font40 = pygame.font.Font(fontLoc,40)                                                       #Used for rendering text in a size 40 font.
font80 = pygame.font.Font(fontLoc,80)                                                       #Used for rendering text in a size 80 font.
font100 = pygame.font.Font(fontLoc,100)                                                     #Used for rendering text in a size 100 font.
fontTitle = pygame.font.Font(fontLoc,150)                                                   #Used for rendering titles in a size 150 font.
tutorialFont = pygame.font.Font(fontLoc,20)                                                 #Used for rendering small text in a size 20 font.

#Set up text                                                                                #These variables are used to render text in a certain font.
textTime = font40.render('Time',True,(255,255,255))                                         #Rendering 'Time' in size 40 font.
textGameOver = font100.render('GAME OVER',True,(255,255,255))                               #Rendering 'GAME OVER' in size 100 font.
textGrade1 = font40.render('Grade: ',True,(255,255,255))                                    #Rendering 'Grade: ' in size 40 font.

textEscLevel = font40.render('ESC - Level Selection',True,(255,255,255))                    #Rendering 'ESC - Level Selection' in size 40 font.
textEscMain = font40.render('ESC - Main Menu',True,(255,255,255))                           #Rendering 'ESC - Main Menu' in size 40 font.
textExit = font40.render('ESC - Exit Game',True,(255,255,255))                              #Rendering 'ESC - Exit Game' in size 40 font.
textEntertoPlay = font40.render('ENTER - Play Level',True,(255,255,255))                    #Rendering 'ENTER - Play Level' in size 40 font.

textSuper = fontTitle.render('SUPER',True,(255,255,255))                                    #Rendering 'SUPER' in size 150 font.
textHexagon = fontTitle.render('HEXAGON',True,(255,255,255))                                #Rendering 'HEXAGON' in size 150 font.
textPlay = font40.render('PLAY',True,(255,255,255))                                         #Rendering 'PLAY' in size 40 font.
textTutorial = font40.render('TUTORIAL',True,(255,255,255))                                 #Rendering 'TUTORIAL' in size 40 font.
textOptions = font40.render('OPTIONS',True,(255,255,255))                                   #Rendering 'OPTIONS' in size 40 font.
textCredits = font40.render('CREDITS',True,(255,255,255))                                   #Rendering 'CREDITS' in size 40 font.

textCreditInfo = [font40.render('Super Hexagon remake by Daniel',True,(255,255,255)),         #Holds a list of renderings for rendering the text in the 'credits' page. 
               font40.render('Music supplied by MonsterCatMedia',True,(255,255,255)),               #This text will be blitted to the screen later in a FOR loop.
               font40.render('Songs:' ,True,(255,255,255)),
               font40.render('Main Menu: PIXL - Sugar Rush',True,(255,120,0)),
               font40.render('Beginner level: Pegboard Nerds - Rocktronik',True,(255,120,0)),
               font40.render('Intermediate level: Rogue - Dynamite',True,(255,120,0)),
               font40.render('Expert level: Favright - Green Storm',True,(255,120,0)),
               font40.render('Ridiculous level: Favright - Iceladen',True,(255,120,0))]
               
textLevelNames = [fontTitle.render('BEGINNER',True,(255,255,255)), fontTitle.render('INTERMEDIATE',True,(255,255,255)),     #Holds a list of renderings for rendering the text in the 'levelSelect' page.
                  fontTitle.render('EXPERT',True,(255,255,255)), fontTitle.render('RIDICULOUS',True,(255,255,255))]         #This text will be blitted to the screen later in a FOR loop.

textHighscore1 = font40.render('Best',True,(255,255,255))                                   #Rendering 'Best' in size 40 font.

tutorialText = [tutorialFont.render('Welcome to the Super Hexagon tutorial! To continue on with the tutorial, press ENTER.',True,(255,255,255)),                                        #Holds a list of renderings for rendering the text in the 'tutorial' page.
                tutorialFont.render('You are a triangle rotating around a hexagon (like the one you see below). Your goal is to survive as long as possible.',True,(255,255,255)),      #This text will be blitted to the screen later in a FOR loop.
                tutorialFont.render('To survive, rotate around the hexagon to dodge obstacles.',True,(255,255,255)),
                tutorialFont.render('You can do this by pressing the left and right arrow keys, pressing A and D, or clicking the left and right mouse buttons.',True,(255,255,255)),
                tutorialFont.render('Obstacles will appear from the edge of the screen, moving closer to the hexagon.',True,(255,255,255)),
                tutorialFont.render('They can come from 6 directions, shown by the background sections.',True,(255,255,255)),
                tutorialFont.render('Here comes an obstacle now. Try moving the triangle out of the way to avoid the obstacle.',True,(255,255,255)),
                tutorialFont.render('These types of obstacles will come towards you in intricate patterns. It\'s up to you to find a path through them!',True,(255,255,255)),
                tutorialFont.render('Don\'t be afraid to push up against their sides, though, as only colliding directly into the obstacle will kill you.',True,(255,255,255)),
                tutorialFont.render('During gameplay, you will see the two HUD boxes above. The one on the right shows your current time.',True,(255,255,255)),
                tutorialFont.render('The one on the left shows you your current grade.',True,(255,255,255)),
                tutorialFont.render('Your grade shows you how well you have done in the level. E is the worst, and A++ is the best.',True,(255,255,255)),
                tutorialFont.render('Every 15 seconds, your grade will go up. However, you must last 100 seconds to get A++.',True,(255,255,255)),
                tutorialFont.render('Upon death, a screen will pop up displaying your final time, your final grade, and the highscore.',True,(255,255,255)),
                tutorialFont.render('To replay the level, you can press both mouse buttons down at the same time, or press SPACE or ENTER.',True,(255,255,255)),
                tutorialFont.render('At any time while playing a level, you can press ESCAPE to return to the level selection menu.',True,(255,255,255)),
                tutorialFont.render('WARNING: This game can make you very dizzy, confused, frustrated, and addicted. Good luck!',True,(255,255,255)),
                tutorialFont.render('Press ESCAPE to return to the Main Menu.',True,(255,255,255))]

#Set up functions
def pointRotate (rotChange, lineLen) :                                                      # rotPos = int (0 - 360) ; lineLen = int ; origin = [int, int] ; rotSpeed = int
    'Rotates a point around an origin.'
    point = [0,0]
    
    point[0] = (math.sin(math.radians(rotPos + rotChange))) * (lineLen) + (origin[0])       #Rotation equations. The sin/cos of the rotation position plus the rotation change, multiplied by the line length and added to the origin point.
    point[1] = (math.cos(math.radians(rotPos + rotChange))) * (lineLen) + (origin[1])

    return point                                                                            #Returns the newly rotated point.

def collisionCheck(point1, point2, point3, point4) :                                        #Where points 1-4 are lists: [int,int] . point1 and point2 are the player, and point3 and point4 are the obstacles.
    'Detects if a collision occurs between the character and an obstacle.'
    x = float(0)                                                                            #Defining variables.
    y = float(0)
    
    x1 = float(point1[0]) ; y1 = float(point1[1])                                           #Points for the first line     
    x2 = float(point2[0]) ; y2 = float(point2[1])
    
    x3 = float(point3[0]) ; y3 = float(point3[1])                                           #Points for the second line              
    x4 = float(point4[0]) ; y4 = float(point4[1])

    try:                                                                                    #Allows exception for vertical and horizontal lines.
        m1 = (y2 - y1) / (x2 - x1)                                                          #Try these equations for the slope for the first line. 
        m2 = (y4 - y3) / (x4 - x3)                                                          #Try these equations for the slope for the second line.
    except:
        m1 = x1 ; m2 = x2                                                                   #If you can't do the equations above, do this instead.

    if m1 == m2 :                                               
        if ((m2 * x3) - y3) == ((m1 * x1) - y1) :                                           #If the slopes are parallel and have the same y-intercept, they intersect.
            return True
        else:
            return False                                                                    #If slopes are the same, and don't have the same y-intercept, they don't intersect.
    
    x = (((m2 * x3) - y3) - ((m1 * x1) - y1)) / (m1 - m2)                                   #x value of intersection equation.
    y = m1 * x + ((m1 * x1) - y1)                                                           #y value of intersection equation.

    x = x * -1 ; y = y * -1                                                                 #Changes x and y to the correct integers. (Equation outputs opposite integers).

    if (x >= min(x1,x2) and x <= max(x1,x2) and                                             #Checks to see if the intersection actually occurs between the 2 lines, and not the 2 infinite lines.
        x >= min(x3, x4) and x <= max(x3, x4) and
        y >= min(y1, y2) and y <= max(y1, y2) and
        y >= min(y3, y4) and y <= max(y3, y4)):
        return True                                                                         
    return False


def background () :
    'Draws the background animations.'
    global bgColourDrawContrast
    lineLen = screen.get_width()                                                            #Linelength is the width of the screen, so the ends of the lines are always off screen.
    
    pointA1 = pointRotate(0,lineLen)                                                        #Calling the rotation function to find the points of the 3 polygons (not including the origin).
    pointA2 = pointRotate(60,lineLen)
    pointB1 = pointRotate(120,lineLen)
    pointB2 = pointRotate(180,lineLen)
    pointC1 = pointRotate(240,lineLen)
    pointC2 = pointRotate(300,lineLen)

    pygame.draw.polygon(screen,(bgColourDrawContrast),[pointA1, pointA2, origin])           #Drawing of the newly rotated polygons.
    pygame.draw.polygon(screen,(bgColourDrawContrast),[pointB1, pointB2, origin])
    pygame.draw.polygon(screen,(bgColourDrawContrast),[pointC1, pointC2, origin])
    
def drawHexagon (size) :
    'Draws the outline and inside of the hexagon.'
    for lineLen in [size,size-5] :                                                          #For loop draws the larger outline first, and then the fill hexagon on top. I used a For loop to save space.
        point1 = pointRotate(0,lineLen + pulseLen)                                          #'lineLen + pulseLen' - The line length plus the pulse length. Allows the shape to get the pulsing effect.
        point2 = pointRotate(60,lineLen + pulseLen)                                         
        point3 = pointRotate(120,lineLen + pulseLen)
        point4 = pointRotate(180,lineLen + pulseLen)
        point5 = pointRotate(-120,lineLen + pulseLen)
        point6 = pointRotate(-60,lineLen + pulseLen)

        if lineLen == size :                                                                #If the size of the hexagon is 50 (the larger one/outline), the colour of it is the same as the objColour.
            hexColour = objColour
        else:                                                                               #Else, the size must be 45, so the colour is the same as the background colour.
            hexColour = bgMainColour[0]
            
        pygame.draw.polygon(screen,(hexColour),[point1,point2,point3,point4,point5,point6]) #Draws the hexagons.

def pulse(maximum) :                                                                        #maximum = Maximum height of pulse.
    'Returns ascending and descending values within a maximum to create a wave.'
    global pulseLen, pulseInc
    pulseLen = pulseLen + pulseInc
    if pulseLen >= maximum :                                                                #Once at maximum or minimum value in the range, the increment is set to its opposite integer to have the pulse go in the opposite direction. 
        pulseLen = maximum                                                                  #This makes sure that the pulseLen stays within the range. 
        pulseInc = pulseInc * -1
    elif pulseLen <= 0 :
        pulseLen = 0                                                                        #This also makes sure that the pulseLen stays within the range.
        pulseInc = pulseInc * -1

def fade(start,stop,inc) :                                                                  #start = Starting position ; stop = Ending position ; inc = Increments
    'Allows the transition between 2 values. (Mostly used for animation).'
    if start == stop :                                                                      #If the fade is complete (start == stop), set the pos as start and return the finishing pos.
        pos = start                                                                         
        return pos

    if inc > 0 :                                                                            #Makes sure that if the increment is adding, start is less than stop. 
        if start < stop :
            pos = start + inc                                                               
        else:                                                                               #If the increment is adding when start is greater than stop, just the pos = start to avoid leaving the targetted range.
            pos = start
    elif inc < 0 :                                                                          #Makes sure that if the increment is subtracting, start is greater than stop.
        if start > stop :
            pos = start + inc                                                                   
        else:                                                                               #If the increment is subtracting when start is lower than stop, just the pos = start to avoid leaving the targetted range.
            pos = start
            
    return pos                                                                              #pos = Position in fade

def colourManagement(page,timeCount) :
    'Updates the colour switch and the colour change for the game.'
    global bgMainColour, bgColourDrawMain, bgColourDrawContrast, objColour, activeMenuOption        #Recieving global variables of bgMainColour, bgColourDrawMain, bgColourDrawContrast, and objColour for editting.
                                                                                                    #Recieving activeMenuOption for use as well.
    if page in ['main','tutorial'] :                                                                #IF statement sorts the colour settings into groups of pages. (These pages get this colour, those get that, etc.)
        bgMainColour = [[100,100,100],[90,90,90],bgMainColour[2]]                                       #If the page is the main menu or the tutorial, the background colour is gray and the object colour is orange.
        objColour = [255,120,0]
        
    elif page == 'level1' or (page == 'levelSelect' and activeMenuOption == 0) :                        #If the page is on the beginner level, or in the first option of levelSelect, the background is orange-yellow, and the obstacles are yellow.
        bgMainColour = [[190,65,0],[150,15,0],bgMainColour[2]]
        objColour = [255,120,0]
        
    elif page == 'level2' or (page == 'levelSelect' and activeMenuOption == 1) :                        #If the page is on the intermediate level, or in the second option of levelSelect, the background is blue, and the obstacles are white-blue.
        bgMainColour = [[30,0,190],[80,50,240],bgMainColour[2]]
        objColour = [150,150,255]
        
    elif page == 'level3' or (page == 'levelSelect' and activeMenuOption == 2) :                        #If the page is on the expert level, or in the third option of levelSelect, the background is white-red, and the obstacles are red.
        bgMainColour = [[255,200,200],[255,150,150],bgMainColour[2]]
        objColour = [255,25,25]
        
    elif page == 'level4' or (page == 'levelSelect' and activeMenuOption == 3) :                        #If the page is on the ridiculous level, or in the last option of levelSelect, the background is black, and the obstacles are white.
        bgMainColour = [[0,0,0],[0,0,0],True]
        objColour = [255,255,255]

    if timeCount % 100 == 0 and page != 'levelSelect' :                                             #This controls the flashing of the background. Every second when the page is not 'levelSelect', the background will switch colours.
        if bgMainColour[2] == True :                                                                    #If colourSwitch is True, make it False. (Switches colours).
            bgMainColour[2] = False
        else :                                                                                          #If colourSwitch is False, make it True. (Switches colours).
            bgMainColour[2] = True

        
    if bgMainColour[2] == True :                                                                    #If colour switch is True, assign the bgColours to the other colours.
        bgColourDrawMain = bgMainColour[1]                                                              #bgMainColour holds both of the background colours, as well as the switchColours boolean.
        bgColourDrawContrast = bgMainColour[0]
        
    else:                                                                                           #If colour switch is False, assign the bgColours to their original colours.
        bgColourDrawMain = bgMainColour[0]
        bgColourDrawContrast = bgMainColour[1]

            
      
def playerManagement(rotInput) :
    'Updates the position of the player based upon the rotPos and the rotInput'
    global playerInfo                                                                       #Gets the data from the player's character. (point1, point2, point3, lineLen, speed, playerRotChange).

    ''' playerInfo = [point1,point2,point3,lineLen,speed,degrees,size]
        lineLen: Equal to the lineLen of the points closest to
            the hexagon.
        speed: Defines the speed in which the player object can
            move.
        degrees: Defines the position of the character in degrees
            around the hexagon.
        size: Defines the distance of the furthest point of the triangle
            from the other points. (Default is 10).
    '''


    playerInfo[5] = playerInfo[5] + (rotInput * playerInfo[4])                              #Translates the rotInput into the addition and subtraction of the playerRotSpeed (playerInfo[4]).

    if playerInfo[5] >= 360 :                                                               #Sets the playerRotChange (playerInfo[5]) to 0 if the value becomes 360 or higher, and set it to 360 if it becomes 0 or lower.
        playerInfo[5] = 0
    elif playerInfo[5] <= 0 :
        playerInfo[5] = 360
        
    playerPoint1 = pointRotate(5 + playerInfo[5], playerInfo[3] + pulseLen)                                             #Sets the points for the player. The '5', '0', and '-5' represent the degree difference between the points.
    playerPoint2 = pointRotate(0 + playerInfo[5], (playerInfo[3] + pulseLen) + playerInfo[6])                           #The degree difference creates 3 points with 5 units between them. The addition of 10 to the lineLen creates...
    playerPoint3 = pointRotate(-5 + playerInfo[5], playerInfo[3] + pulseLen)                                            #... the point of the triangle, pushing it out farther than the other points.

    playerInfo = [playerPoint1,playerPoint2,playerPoint3,playerInfo[3],playerInfo[4],playerInfo[5],playerInfo[6]]       #Places the newly updated information back in the playerInfo list. 
    
    pygame.draw.polygon(screen,(objColour),[playerPoint1,playerPoint2,playerPoint3])                                    #Draws the triangle.

def obstacleManagement (obstaclePushBack) :                                                                             #obstaclePushBack = The distance added on to the obstacle lineLen to give it the animation of exitting the screen upon player death.
    'Manages the obstacles throughout the game.'                                                                        
    global playerInfo,page,obstacles,removeObstacles,tutorialStage, tutorialCollision, timeCount                        #Gets the data from the player's character. (point1, point2, point3, lineLen, speed, playerRotChange).
                                                                                                                        #Also gets the page, obstacles and removeObstacles list, the tutorialStage and tutorialCollision for editting.
                                                                                                                        #Gets the timeCount variable for use in the playSoundEffect function.

    ''' obstacles = [point1,point2,point3,point4,lineLen,slot,speed,size]
        lineLen: Equal to the lineLen of the farthest point
            to the center (point3 or point4).
        slot: One of the 6 sections of the background that
            the object follows. Value ranges from 0 - 5 .
        speed: The speed in which the obstacle moves towards
            the center.
        size: The size (or thickness) of the obstacle.
    '''
    
    for i in range(len(obstacles)) :                                                                                    #Sorts through all the obstacles and updates their position and checks for collisions.
        if obstacles[i-1][4] - obstacles[i-1][7] <= 20 :                                                                #Checks to see if the points closts to the origin are past the snap zone (20 pixels from the origin).
            obstacles[i-1][0] = pointRotate(obstacles[i-1][5] * 60 + 60, 20 + obstaclePushBack)                         #If they are past the snap zone, they snap to a lineLen of 20. 
            obstacles[i-1][1] = pointRotate(obstacles[i-1][5] * 60, 20 + obstaclePushBack)                              #This prevents the obstacles from passing through the origin and out the other side of the hexagon.
        else:
            obstacles[i-1][0] = pointRotate(obstacles[i-1][5] * 60 + 60, (obstacles[i-1][4] - obstacles[i-1][7]) + pulseLen + obstaclePushBack)    #If they aren't past the snap zone, they move like normal. 
            obstacles[i-1][1] = pointRotate(obstacles[i-1][5] * 60, (obstacles[i-1][4] - obstacles[i-1][7]) + pulseLen + obstaclePushBack)         #The " * 60 + 60 " helps align the obstacles to the background sections. The obstaclePushBack is for obstacle animation upon player death.
            
        obstacles[i-1][2] = pointRotate(obstacles[i-1][5] * 60, obstacles[i-1][4] + pulseLen + obstaclePushBack)                                   #Deals with the points furthest from the origin. 
        obstacles[i-1][3] = pointRotate(obstacles[i-1][5] * 60 + 60, obstacles[i-1][4] + pulseLen + obstaclePushBack)
            
        '''Collisions'''

        if obstacles[i-1][4] >= playerInfo[3] and obstacles[i-1][4] - obstacles[i-1][7] <= playerInfo[3] + 25 :                 #If the obstacles are within collision range, it calls the collision function to check for collisions.                             

            leftCollision = collisionCheck(playerInfo[0],playerInfo[1],obstacles[i-1][0],obstacles[i-1][1])
            rightCollision = collisionCheck(playerInfo[2],playerInfo[1],obstacles[i-1][0],obstacles[i-1][1])

            
            if leftCollision == True and rightCollision == True :                                                               #If collision is True for both sides, gameover.
                if page == 'level1' :                                                                                           #This IF statement sends the player back to the correct gameover screen.
                    page = 'gameover1'
                    playSoundEffect('death',timeCount)
                elif page == 'level2' :
                    page = 'gameover2'
                    playSoundEffect('death',timeCount)
                elif page == 'level3' :
                    page = 'gameover3'
                    playSoundEffect('death',timeCount)
                elif page == 'level4' :
                    page = 'gameover4'
                    playSoundEffect('death',timeCount)
                elif page == 'tutorial':                                                                                        #This ELIF deals with collision in the Tutorial mode.
                    if tutorialStage == 7 :                                                                                     #If a collision is detected in stage 7, go back to stage 6. (Stage 6 sends the obstacle again).
                        tutorialStage = 6
                    for i in range(0,len(obstacles)) :                                                                          #This will removed the obstacle on the collision by appending all of the obstacles to the removeObstacles list.
                        removeObstacles.append(obstacles[i])
                    
            elif leftCollision == True and rightCollision == False :                                                            #If collision is True for one side and not the other, position the character beside the obstacle...
                playerInfo[5] = obstacles[i-1][5] * 60 - 5                                                                      #...This allows for the obstacle to get pushed out of the way if only part of it hits an obstacle...
            elif leftCollision == False and rightCollision == True :                                                            #...The "*60 + 60 + 5" position the character in the correct position. The optional + 60 decides which side of the obstacle...                                                       
                playerInfo[5] = obstacles[i-1][5] * 60 + 60 + 5                                                                #...the character will be positioned on, and the +- 5 is used to align one side of the character with the obstacle (so that...
                                                                                                                                #...the center of the character isn't on top of the side of the obstacle.

             
            if obstacles[i-1][4] >= playerInfo[3] >= obstacles[i-1][4] - obstacles[i-1][7] :
                if ((rotInput == 1) and ((obstacles[i-1][5] * 60 + 60) >= (playerInfo[5] + 5) >= (obstacles[i-1][5] * 60))) :       #This IF statement checks for a collision with the side of an obstacle only. (Not the front of the obstacle, like the code above).                           
                    playerInfo[5] = obstacles[i-1][5] * 60 - 10
                    
                elif ((rotInput == -1) and ((obstacles[i-1][5] * 60 + 60) >= (playerInfo[5] - 5) >= (obstacles[i-1][5] * 60))):                                         
                    playerInfo[5] = obstacles[i-1][5] * 60 + 60 + 10
            
        '''Drawing'''

        pygame.draw.polygon(screen,(objColour),[obstacles[i-1][0],obstacles[i-1][1],obstacles[i-1][2],obstacles[i-1][3]])       #Draws the obstacle.
##        pygame.draw.line(screen,(0,255,0),obstacles[i-1][1],obstacles[i-1][2])
##        pygame.draw.line(screen,(0,255,0),obstacles[i-1][0],obstacles[i-1][3])
##        pygame.draw.line(screen,(0,255,0),playerInfo[0],playerInfo[1])
##        pygame.draw.line(screen,(0,255,0),playerInfo[2],playerInfo[1])
        
        '''Moving and Removing'''                                                                                               
            
        if obstacles[i-1][4] < 30 or obstaclePushBack >= screen.get_width() or page in ['main','levelSelect'] :                 #If obstacle has reached hexagon, or been pushed back off the screen, or if the page is not a page with obstacles.                                                                                                                    
            removeObstacles.append(obstacles[i-1])                                                                              #(Credits not needed, as the only page that leads to it is the 'main' page, which takes care of obstacles for it.                                                  
        else:                                                                                                                   #Appends an obstacle to the removal list if it needs to be removed. It is then removed below.
            obstacles[i-1][4] = obstacles[i-1][4] - obstacles[i-1][6]                                                           #If the obstacle doesn't need to be removed, its position is updated.

    for i in range(len(removeObstacles)) :                                                                                      #This FOR loop checks the removeObstacles list and removes the values in that list from the obstacles list.
        remove = removeObstacles[i-1]
        obstacles.remove(remove)
    removeObstacles = []                                                                                                        #Resets the removeObstacles list.
        
    
def timeManagement(timeCount) :
    'Keeps track of time during gameplay.'
    sec = timeCount / 100 ; sec = int(sec)                                                                                      #timeCount / 100 is equal to one second. 'sec' also needs to be an integer.
    if sec < 10 :                                                                                                               #If sec is less than 10, add a zero on the front (for visual effect. 05 looks better than just a 5).
        sec = ("0" + str(sec))

    millisec = timeCount - (int(sec) * 100)                                                                                     #timeCount - the amount of seconds * 100 is equal to the amount of milliseconds. 
    if millisec < 10 :                                                                                                          #If millisec is less than 10, add a zero on the front (for visual effect. 05 looks better than just a 5).
        millisec = ("0" + str(millisec))

    return sec, millisec                                                                                                        #Returns the sec and millisec variables.

def gradeChooser(timeCount) :
    'Chooses the grade that matches the time the player survived.'
    if timeCount >= 10000 :                                                                                                     #If the time is greater than 100 seconds, the grade is A++
        return 'A++'
    elif timeCount >= 6000 :                                                                                                    #If the time is greater than 60 seconds, the grade is A
        return 'A'
    elif timeCount >= 4500 :                                                                                                    #If the time is greater than 45 seconds, the grade is B
        return 'B'
    elif timeCount >= 3000 :                                                                                                    #If the time is greater than 30 seconds, the grade is C
        return 'C'
    elif timeCount >= 1500 :                                                                                                    #If the time is greater than 15 seconds, the grade is D
        return 'D'
    else:                                                                                                                       #If the time is lesser than 15 seconds, the grade is E
        return 'E'

def progressBar(timeCount,pos) :
    'Manages the grade progress bar in-game.'
    if timeCount >= 10000 :                                                                                                     #If the time is greater than 100 seconds, keep the bar full.
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200,20])
    elif timeCount >= 6000 :                                                                                                    #If the time is greater than 60 seconds, (timeCount - the most recent grade time) / the amount of time to get to the next grade...
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200 - (((timeCount - 6000)/4000)*200),20])                           #... gives you the percentage that the bar should be full. Multiply this by 200 pixels, and you get the amount of pixels the bar should be...
    elif timeCount >= 4500 :                                                                                                    #... Since the bar is descending, and not ascending, subtract the value of the equation above from 200... 
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200 - (((timeCount - 4500)/1500)*200),20])                           #... This strategy was used for each grade margin in this IF statement.
    elif timeCount >= 3000 :
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200 - (((timeCount - 3000)/1500)*200),20])
    elif timeCount >= 1500 :
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200 - (((timeCount - 1500)/1500)*200),20])
    else:
        pygame.draw.rect(screen,(50,255,50),[pos[0],pos[1],200 - (((timeCount)/1500)*200),20])                                  #For grade E, there is no need to subtract the last grade time, as it is 0.

def tutorialManagement() :
    'Manages the tutorial.'
    global tutorialStage, tutorialText, tutorialFont, obstacles, removeObstacles                                                #Receiving the tutorialStage, tutorialText, tutorialFont, obstacles, and removeobstacles for use and editting. 

    for i in range(0,len(tutorialText) + 1) :                                                                                   #For each item in tutorialText (the +1 is to accommodate for the use of a tutorialStage to emit an obstacle...
                                                                                                                                #...and not blit text.
        if i <= 6 and tutorialStage == i :                                                                                      #Checks to see if the tutorialStage matches 'i', and 'i' is less than or equal to 6 (before the obstacle).
            screen.blit(tutorialText[i],[100,120])                                                                              #If the tutorialStage is less than or equal to 6, it will blit the correct line of text to the screen.
            
        elif i == 7 and tutorialStage == 7 :                                                                                    #If tutorialStage and 'i' are equal to 7, emit an obstacle.
            for i in range(0,5) :                                                                                               #The FOR loop emits 5 obstacles to make 5/6's of a hexagon.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width(),(i - 2) % 6,2,60])                     #Appends the obstacles to the list. (i - 2 aligns the obstacle in a way that forces the player to move to avoid the obstacle).
            tutorialStage = 8                                                                                                   #Sets the tutorialStage to 8 to allow for the blitting of text.
            
        elif i >= 8 and tutorialStage == i :                                                                                    #Checks to see if the tutorialStage matches 'i', and 'i' is greater than or equal to 8 (after the obstacle).
            screen.blit(tutorialText[i-1],[100,120])                                                                            #If the tutorialStage is greater than or equal to 8, it will blit the correct line of text to the screen.
                                                                                                                                # (i - 1) is to accommodate for the skipping of a tutorialStage to emit an obstacle.

def highscoreManagement(timeCount,page) :
    'Manages the highscores.'
    global highscoreList,textHighscore1,activeMenuOption                                            #Receiving of the highscoreList, textHighscore1, and the activeMenuOptions for editting and use.
    
    if page in ['gameover1','level1'] :                                                             #If page is equal to the beginner level or the beginner gameover screen...
        if timeCount > highscoreList[0] :                                                               #If the timeCount is greater than the original highscore for that level...
            highscoreList[0] = timeCount                                                                #... The highscore is equal to the current timeCount.
        sec,millisec = timeManagement(highscoreList[0])                                                 #Receiving of sec and millisec variables from the timeManagement function for the highscore for the level.
        
    elif page in ['gameover2','level2'] :                                                           #If page is equal to the intermediate level or the intermediate gameover screen.
        if timeCount > highscoreList[1] :                                                               #If the timeCount is greater than the original highscore for that level...
            highscoreList[1] = timeCount                                                                #... The highscore is equal to the current timeCount.
        sec,millisec = timeManagement(highscoreList[1])                                                 #Receiving of sec and millisec variables from the timeManagement function for the highscore for the level.
            
    elif page in ['gameover3','level3'] :                                                           #If page is equal to the expert level or the expert gameover screen...
        if timeCount > highscoreList[2] :                                                               #If the timeCount is greater than the original highscore for that level...
            highscoreList[2] = timeCount                                                                #... The highscore is equal to the current timeCount.
        sec,millisec = timeManagement(highscoreList[2])                                                 #Receiving of sec and millisec variables from the timeManagement function for the highscore for the level.
            
    elif page in ['gameover4','level4'] :                                                           #If page is equal to the ridiculous level or the ridiculous gameover screen...
        if timeCount > highscoreList[3] :                                                               #If the timeCount is greater than the original highscore for that level...
            highscoreList[3] = timeCount                                                                #... The highscore is equal to the current timeCount.
        sec,millisec = timeManagement(highscoreList[3])                                                 #Receiving of sec and millisec variables from the timeManagement function for the highscore for the level.

    elif page == 'levelSelect' :                                                                    #If page is equal to the levelSelect page...
        for i in range(0,4) :                                                                           #FOR loop checks for each of the possible activeMenuOptions
            if i == activeMenuOption :                                                                  #For the correct activeMenuOption, receive the sec and millisec variables from the timeManagement function...
                sec,millisec = timeManagement(highscoreList[i])                                         #...for the highscore matching the highlighted level in the menu

    return (font40.render((str(sec) + ':' + str(millisec)),True,(255,255,255)))                     #Returns the rendered sec and millisec variables.

def musicManagement(page,playMusic) :
    'Manages the music within the game.'
    if playMusic == False or pygame.mixer.music.get_busy() == True :                                #If the player chose for playMusic to be False, or if there is a song already playing, return None.
        return

    if page in ['main','levelSelect','tutorial','options','credits'] :                              #If the page is equal to the main menu, levelSelect, tutorial, options, or credits...
        pygame.mixer.music.load('songs/sugarrush(tutmenu).mp3')                                         #Play the song: Sugar Rush      
        pygame.mixer.music.play(-1)                                                                     #(-1) plays the song infinitely.

    elif page == 'level1' :                                                                         #If the page is equal to level1...
        pygame.mixer.music.load('songs/rocktronik(level1).mp3')                                         #Play the song: Rocktronik
        pygame.mixer.music.play(-1)                                                                     #(-1) plays the song infinitely.
        
    elif page == 'level2' :                                                                         #If the page is equal to level1...
        pygame.mixer.music.load('songs/dynamite(level2).mp3')                                           #Play the song: Dynamite
        pygame.mixer.music.play(-1)                                                                     #(-1) plays the song infinitely.

    elif page == 'level3' :                                                                         #If the page is equal to level1...
        pygame.mixer.music.load('songs/greenstorm(level3).mp3')                                         #Play the song: Greenstorm
        pygame.mixer.music.play(-1)                                                                     #(-1) plays the song infinitely.

    elif page == 'level4' :                                                                         #If the page is equal to level1...
        pygame.mixer.music.load('songs/iceladen(level4).mp3')                                           #Play the song: Iceladen
        pygame.mixer.music.play(-1)                                                                     #(-1) plays the song infinitely.

def playSoundEffect(sound,timeCount) :                                                              #sound = a string that defines which sound is needed to be played.
    'Manages the sound effects within the game.'
    
    if sound == 'death' :                                                                           #If sound is equal to 'death' ...
        if timeCount >= 10000 :                                                                         #If the time is greater than 100 seconds...
            playSound = pygame.mixer.Sound('sounds/wonderful.wav')                                          #... Play the sound 'wonderful'.
            playSound.play()

        else:                                                                                           #If the time is less than 100 seconds...
            playSound = pygame.mixer.Sound('sounds/gameover.wav')                                           #... Play the sound 'gameover'.
            playSound.play()

        playSound = pygame.mixer.Sound('sounds/die.wav')                                                #Play the sound 'die' regardless of the time.
        playSound.play()
        
    elif sound == 'begin' :                                                                         #If sound is equal to 'begin' ...
        playSound = pygame.mixer.Sound('sounds/begin.wav')                                              #... Play the sound 'begin'.
        playSound.play()

        playSound = pygame.mixer.Sound('sounds/start.wav')                                              #... Play the sound 'start'.
        playSound.play()
        
    elif sound == 'superhexagon' :                                                                  #If sound is equal to 'superhexagon' ...
        playSound = pygame.mixer.Sound('sounds/superhexagon.wav')                                       #... Play the sound 'superhexagon'.
        playSound.play()


#Set up music
playMusic = True                                                                                    #Default music setting is on.
pygame.mixer.music.set_volume(0.8)                                                                  #Sets the volume of the music to 0.8 (about 80%).
playSoundEffect('superhexagon',timeCount)                                                           #Calls the playSoundEffect to play the 'superhexagon' sound effect.

##########################################################################
#                       Level building functions.                        #
##########################################################################

def levelManagement(page,timeCount,rotSpeed) :
    'Manages the levels within the game.'
    randLevelPiece = None                                                                           #Sets the randLevelPiece variable to None so that it doesn't need to check the large IF statement below when no obstacles are needed.
    if page == 'level1' :                                                                           #If page is equal to the beginner level...
        speed = 3                                                                                       #Set the speed and player rotation speed to 3.
        playerInfo[4] = 3            
        if len(obstacles) > 0 :                                                                         #If there are obstacles in the obstacles list...
            if obstacles[(len(obstacles) - 1)][4] <= screen.get_width() - 350 :                             #If the last emitted obstacle in the obstacle lists distance from the origin is greater than the width of the screen - 350 (-350 to create a space between obstacle patterns)...
                randLevelPiece = random.randrange(0,8)                                                          #Choose a random level piece between 0 and 8 (0-8 are easy obstacles).
        else:
            randLevelPiece = random.randrange(0,8)                                                      #If there are no obstacles yet, choose a random level piece between 0 and 8 (0-8 are easy obstacles).

        if timeCount % 3000 == 0 :                                                                      #Every 30 seconds, switch the direction of the rotSpeed. This will cause the whole level to spin in the opposite direction.
            rotSpeed = rotSpeed * -1

    elif page == 'level2' :                                                                         #If page is equal to the intermediate level...
        speed = 4                                                                                       #Set the speed and player rotation speed to 4.
        playerInfo[4] = 4
        if len(obstacles) > 0 :                                                                         #If there are obstacles in the obstacles list...
            if obstacles[(len(obstacles) - 1)][4] <= screen.get_width() - 350 :                             #If the last emitted obstacle in the obstacle lists distance from the origin is greater than the width of the screen - 350 (-350 to create a space between obstacle patterns)...
                randLevelPiece = random.randrange(0,8)                                                          #Choose a random level piece between 0 and 8 (0-8 are easy obstacles).
        else:
            randLevelPiece = random.randrange(0,8)                                                      #If there are no obstacles yet, choose a random level piece between 0 and 8 (0-8 are easy obstacles).

        if timeCount % 2000 == 0 :                                                                      #Every 20 seconds, switch the direction of the rotSpeed. This will cause the whole level to spin in the opposite direction.
            rotSpeed = rotSpeed * -1
            
    elif page == 'level3' :                                                                         #If page is equal to the expert level...
        speed = 5                                                                                       #Set the speed and player rotation speed to 5.
        playerInfo[4] = 5
        if len(obstacles) > 0 :                                                                         #If there are obstacles in the obstacles list...
            if obstacles[(len(obstacles) - 1)][4] <= screen.get_width() - 250 :                             #If the last emitted obstacle in the obstacle lists distance from the origin is greater than the width of the screen - 250 (-250 to create a tight space between obstacle patterns)...
                randLevelPiece = random.randrange(0,16)                                                          #Choose a random level piece between 0 and 16 (0-16 are easy - hard obstacles).
        else:
            randLevelPiece = random.randrange(0,16)                                                      #If there are no obstacles yet, choose a random level piece between 0 and 16 (0-16 are easy - hard obstacles).

        if timeCount % 1500 == 0 :                                                                      #Every 15 seconds, switch the direction of the rotSpeed. This will cause the whole level to spin in the opposite direction.
            rotSpeed = rotSpeed * -1

    elif page == 'level4' :                                                                         #If page is equal to the ridiculous level...
        speed = 6                                                                                       #Set the speed and player rotation speed to 6.
        playerInfo[4] = 6
        if len(obstacles) > 0 :                                                                         #If there are obstacles in the obstacles list...
            if obstacles[(len(obstacles) - 1)][4] <= screen.get_width() - 250 :                             #If the last emitted obstacle in the obstacle lists distance from the origin is greater than the width of the screen - 250 (-250 to create a tight space between obstacle patterns)...
                randLevelPiece = random.randrange(0,18)                                                          #Choose a random level piece between 0 and 18 (0-18 are easy - ridiculous obstacles).
        else:
            randLevelPiece = random.randrange(0,18)                                                      #If there are no obstacles yet, choose a random level piece between 0 and 18 (0-18 are easy - ridiculous obstacles).

        if timeCount % 1000 == 0 :                                                                      #Every 10 seconds, switch the direction of the rotSpeed. This will cause the whole level to spin in the opposite direction.
            rotSpeed = rotSpeed * -1

    elif page == 'tutorial' :                                                                       #If page is equal to tutorial...
        rotSpeed = 3                                                                                    #Set the speed and player rotation speed to 3.
        playerInfo[4] = 3

    if randLevelPiece != None :                                                                     #If an obstacle hasn't been choosen, don't bother checking the IF statement below.

        randomizer = random.randint(0,6)                                                            #The randomizer variable adds a random element to all of the obstacles below. It will randomly choose the direction each pattern will be facing.
                                                                                                    #The random number (0-5) will be added to the slot number when appending obstacles to the obstacle list. 
        if randLevelPiece == 0 :                                                                        #This IF statement checks to see which randLevelPiece was chosen, and then calls the function that will emit the obstacle pattern.
            levelPieceSingleSpiral(speed,randomizer)

        elif randLevelPiece == 1 :
            levelPieceSingleSpiralReverse(speed,randomizer)

        elif randLevelPiece == 2 :
           levelPieceJaggedHexagon(speed,randomizer)
            
        elif randLevelPiece == 3 :
            levelPieceBackandForthShort(speed,randomizer)
            
        elif randLevelPiece == 4 :
            levelPiece3Hexagon(speed,randomizer)
            
        elif randLevelPiece == 5 :
            levelPiece3Split(speed,randomizer)
            
        elif randLevelPiece == 6 :
            levelPiece3SplitHexagon(speed,randomizer)
            
        elif randLevelPiece == 7 :
            levelPieceBackandForthWide(speed,randomizer)
            
        elif randLevelPiece == 8 :
            levelPieceDoubleSpiral(speed,randomizer)
            
        elif randLevelPiece == 9 :
            levelPieceDoubleSpiralReverse(speed,randomizer)

        elif randLevelPiece == 10 :
            levelPiece3SplitQuick(speed,randomizer)
            
        elif randLevelPiece == 11 :
            levelPieceTwoThirdHexagon(speed,randomizer)

        elif randLevelPiece == 12 :
            levelPieceHexagonQuick(speed,randomizer)

        elif randLevelPiece == 13 :
            levelPieceHexagonQuickReverse(speed,randomizer)

        elif randLevelPiece == 14 :
            levelPieceHalfHexagon(speed,randomizer)

        elif randLevelPiece == 15 :
            levelPieceHalfHexagonReverse(speed,randomizer)

        elif randLevelPiece == 16 :
            levelPieceRandom10(speed)

        elif randLevelPiece == 17 :
            levelPieceRandom10Double(speed)
            
    return rotSpeed                                                                                                                         #Returning the updated rotSpeed

def levelPieceDoubleSpiral(speed,randomizer) :
    'Creates obstacles that force the player to go in a spiral.'
    for i in range(0,10) :                                                                                                              #Emits 20 obstacles, 2 at a time, opposite from eachother in a rotating pattern.
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(i + randomizer) % 6,speed,60])                 #(i * 60) positions obstacles right after another, with no space in between.
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(i - 3 + randomizer) % 6,speed,60])             #((i + randomizer) % 6) positions obstacles in the slot beside the last one. (The "-3" creates obstacles across from eachother). 

def levelPieceSingleSpiral(speed,randomizer) :
    'Creates obstacles that force the player to go in a spiral.'
    for i in range(0,10) :                                                                                                              #Emits 10 obstacles, 1 at a time, in a rotating pattern.
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(i + randomizer) % 6,speed,60])                 #(i * 60) positions obstacles right after another, with no space in between.
                                                                                                                                            #((i + randomizer) % 6) positions obstacles in the slot beside the last one.
def levelPieceDoubleSpiralReverse(speed,randomizer) :
    'Creates obstacles that force the player to go in a spiral.'
    for i in range(0,10) :
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(6 - i + randomizer) % 6,speed,60])             #Same strategy as the regular double spiral, but you subtract the slot from 6 to get the reversing effect.
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(6 - (i - 3 + randomizer)) % 6,speed,60])

def levelPieceSingleSpiralReverse(speed,randomizer) :
    'Creates obstacles that force the player to go in a spiral.'
    for i in range(0,10) :
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 60),(6 - i + randomizer) % 6,speed,60])             #Same strategy as the regular single spiral, but you subtract the slot from 6 to get the reversing effect.

def levelPiece3Hexagon(speed,randomizer) :
    'Creates 3 Hexagon shapes that come down one after another.'
    for i in range(0,3) :                                                                                                               #Emits 3 sets of obstacles.
        for j in range(0,5) :                                                                                                               #In each set, there are 5 singular obstacles placed beside eachother.
            if i / 2 % 1 :                                                                                                                      #This IF splits the 3 sets in half. Half points one way, the other points in the opposite direction. 
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j - 3 + randomizer) % 6,speed,60])            #"j - 3" points the obstacle in the other direction.
            else:
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + randomizer) % 6,speed,60])

def levelPiece3Split(speed,randomizer) :
    'Creates 3 sections of the full hexagon, with spaces in between them. It does this 5 times.'
    for i in range(0,5) :                                                                                                               #Emits 5 sets of obstacles.
        for j in range(0,3) :                                                                                                               #In each set, there are 3 singular obstacles placed with spaces in between them.
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),((j*2 + i) + randomizer) % 6,speed,60])        #The "j*2" places spaces between each singular obstacle.

def levelPiece3SplitQuick(speed,randomizer) :
    'Same as levelPiece3Split, but there it is closer, faster, and there is more.'
    for i in range(0,10) :                                                                                                              #Emits 10 sets of obstacles.
        for j in range(0,3) :                                                                                                               #Same strategy as levelPiece3Split, but the distance between each set of obstacles is shortened to 150.
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 150),((j*2 + i) + randomizer) % 6,speed,60])

def levelPieceBackandForthWide(speed,randomizer) :
    'Forces the player to move back and forth.'
    obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + 700,randomizer,speed,700])                               #Creates one large, solid obstacle.
    for i in range(0,3) :                                                                                                               #Emits 3 sets of obstacles around the large obstacle.
        for j in range(0,5) :                                                                                                               #In each set, there are 4 single obstacles.
            if i / 2 % 1 :                                                                                                                      #Half of the time, the obstacles are placed 2 slots over.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + 2 + randomizer) % 6,speed,60])            #(j + 2) places them over 2 slots.
            else:                                                                                                                               #The other half of the time, the obstacles are placed normally.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + randomizer) % 6,speed,60])                #(j) by itself places them normally.
        
def levelPieceBackandForthShort(speed,randomizer) :
    'Forces the player to choose between 2 paths that force the player to move back and forth.'
    obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + 875,(randomizer) % 6,speed,935])                         #Creates two large, solid obstacles, opposite from eachother.
    obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + 875,(3 + randomizer) % 6,speed,935])                     #The +3 positions this obstacle opposite from the other.
    for i in range(0,3) :                                                                                                               #Emits 3 sets of obstacles between the two larger obstacles.                                                                                                      
        for j in range(0,2) :                                                                                                               #Each set is split into two sections that are opposite from each other.
            for k in range(0,2) :                                                                                                               #Each split set has 2 single obstacles placed adjacent to each other, but one is further than the other.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350) + (k * 175),(j*3 + k + 1 + randomizer) % 6,speed,60])  #(k * 175) makes one obstacle farther than another. "j*3" splits each set into opposite sections...
                                                                                                                                                            #..."+ k" makes one obstacle adjacent from another. "+ 1" is for adjusting the alignment of obstacles.
def levelPiece3SplitHexagon(speed,randomizer) :
    'Combination of the 3 split and the 3 hexagon.'
    for i in range(0,3) :                                                                                                               #Emits 3 sets of obstacles.
        if i / 2 % 1 :                                                                                                                      #Half of these obstacles ...
            for j in range(0,3) :                                                                                                               #...are like the obstacles in levelPiece3Split.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(j*2 + i + randomizer) % 6,speed,60])
        else:                                                                                                                               #The other half are ...
            for j in range(0,5) :                                                                                                               #...like the obstacles in levelPiece3Hexagon.
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + randomizer) % 6,speed,60])
    
def levelPieceJaggedHexagon(speed,randomizer) :
    'Same as 3 Hexagon, but there is 3 sides together, and one with spaces on each side.'
    for i in range(0,3) :                                                                                                               #Emits 3 sets of obstacles.
        if i / 2 % 1 :                                                                                                                      #Half of these obstacles...
            for j in range(0,3) :                                                                                                               #
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + randomizer) % 6,speed,60])
                if j == 1 :
                    obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + 3 + randomizer) % 6,speed,60])
        else:
            for j in range(0,3) :
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + 3 + randomizer) % 6,speed,60])
                if j == 1 :
                    obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 350),(j + randomizer) % 6,speed,60])
        
def levelPieceTwoThirdHexagon(speed,randomizer) :
    'Creates 6 2/3 hexagon pieces, with 2 openings opposite from eachother. Emits these obstacles in a swirling pattern.'
    for i in range(0,6) :
        for j in range(0,6) :
            if j % 3 != 1 :
                obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(j + i + randomizer) % 6,speed,60])

def levelPieceHalfHexagon(speed,randomizer) :
    'Creates 6 2/3 hexagon pieces, with 2 openings opposite from eachother. Emits these obstacles in a swirling pattern.'
    for i in range(0,6) :
        for j in range(0,3) :
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(j + i*2 + randomizer) % 6,speed,60])

def levelPieceHalfHexagonReverse(speed,randomizer) :
    'Creates 6 2/3 hexagon pieces, with 2 openings opposite from eachother. Emits these obstacles in a swirling pattern.'
    for i in range(0,6) :
        for j in range(0,3) :
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(6 - (j + i*2 + randomizer)) % 6,speed,60])

def levelPieceHexagonQuick(speed,randomizer) :
    'Creates 6 Hexagon shapes that come down quickly one after another in a swirling motion.'
    for i in range(0,6) :
        for j in range(0,5) :
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(j + i + randomizer) % 6,speed,60])

def levelPieceHexagonQuickReverse(speed,randomizer) :
    'Creates 6 Hexagon shapes that come down quickly one after another in a swirling motion.'
    for i in range(0,6) :
        for j in range(0,5) :
            obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 250),(6 - (j + i + randomizer)) % 6,speed,60])

def levelPieceRandom10(speed) :
    'Creates 20 random single obstacles.'
    for i in range(0,10) :
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 150),(random.randint(0,6)) % 6,speed,60])

def levelPieceRandom10Double(speed) :
    'Creates 20 random double obstacles.'
    for i in range(0,10) :
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 150),(random.randint(0,3)) % 6,speed,60])
        obstacles.append([(-10,-10),(0,-10),(-10,-20),(0,-20),screen.get_width() + (i * 150),(random.randint(3,6)) % 6,speed,60])
    

#Game loop
while True:

    # ========================== HANDLE EVENTS ========================== #
    done = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                                                   #If the player exits, set the done variable to true and break from the loop.
            done = True                                                                             
            break
        if page == 'main' :                                                                             #If page is equal to the main menu...
            if event.type == pygame.KEYDOWN :                                                               #Check for keys being pressed.
                if event.key == pygame.K_UP or event.key == pygame.K_w :                                        #If the UP key or the W key is pressed, move menu option up.
                    activeMenuOption = activeMenuOption + 1                                                         
                if event.key == pygame.K_DOWN or event.key == pygame.K_s :                                      #If the DOWN key or the S key is pressed, move menu option down.
                    activeMenuOption = activeMenuOption - 1
                    
                if event.key == pygame.K_RETURN :                                                               #If ENTER is pressed, check which menu option is highlighted.
                    timeCount = 0
                    if activeMenuOption == 0 :                                                                      #If menuOption 0 is highlighted, go to the options page.
                        page = 'options' 
                        activeMenuOption = 1                                                                            #Set the menu option to 1 for the options menu.
                    elif activeMenuOption == 1 :                                                                    #If menuOption 1 is highlighted, go to the tutorial page.
                        page = 'tutorial'
                    else :                                                                                          #If menuOption 2 is highlighted, go to the levelSelect page.
                        page = 'levelSelect'
                        activeMenuOption = 0                                                                            #Set the menu option to 0 for the levelSelect menu.
                if event.key == pygame.K_ESCAPE :                                                               #If ESC is pressed, set the done variable to true and break from the loop.
                    done = True
                    break

        elif page == 'levelSelect' :                                                                    #If page is equal to the levelSelect page...
            if event.type == pygame.KEYDOWN :                                                               #Check for keys being pressed.  
                if event.key == pygame.K_ESCAPE :                                                               #If ESC is pressed, page is set to main and the menuOption is set to 2 for the main menu.
                    page = 'main'
                    activeMenuOption = 2
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d :                                     #If the RIGHT key or the D key is pressed, move the menu option up (to the right).
                    activeMenuOption = activeMenuOption + 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a :                                      #If the LEFT key or the A key is pressed, move the menu option down (to the left).
                    activeMenuOption = activeMenuOption - 1
                    
                if event.key == pygame.K_RETURN :                                                               #If ENTER is pressed, check the menu options to see which option was highlighted. 
                    if activeMenuOption == 0 :                                                                      #If menuOption 0 is highlighted, go to the level1 page.
                        page = 'level1'
                        rotSpeed = 1                                                                                    #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 1 :                                                                    #If menuOption 1 is highlighted, go to the level2 page.
                        page = 'level2'
                        rotSpeed = 1.5                                                                                  #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 2 :                                                                    #If menuOption 2 is highlighted, go to the level3 page.
                        page = 'level3'
                        rotSpeed = 2                                                                                    #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 3 :                                                                    #If menuOption 4 is highlighted, go to the level4 page.
                        page = 'level4'
                        rotSpeed = 2.5                                                                                  #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    
            if event.type == pygame.MOUSEBUTTONDOWN :                                                       #Check for mouse buttons being pressed.
                if pygame.mouse.get_pressed() == (1,0,0) :                                                      #If left click, move menu option down (left).
                    activeMenuOption = activeMenuOption - 1
                if pygame.mouse.get_pressed() == (0,0,1) :                                                      #If right click, move menu option up (right).
                    activeMenuOption = activeMenuOption + 1
                if pygame.mouse.get_pressed() == (1,0,1) :                                                      #If double click, check the menu options to see which option was highlighted.
                    if activeMenuOption == 0 :                                                                      #If menuOption 0 is highlighted, go to the level1 page.
                        page = 'level1'
                        rotSpeed = 1                                                                                    #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 1 :                                                                    #If menuOption 1 is highlighted, go to the level2 page.
                        page = 'level2'
                        rotSpeed = 1.5                                                                                  #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 2 :                                                                    #If menuOption 2 is highlighted, go to the level3 page.
                        page = 'level3'
                        rotSpeed = 2                                                                                    #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()
                    elif activeMenuOption == 3 :                                                                    #If menuOption 4 is highlighted, go to the level4 page.
                        page = 'level4'
                        rotSpeed = 2.5                                                                                  #Sets rotation speed and stops the music (so the music function will update the song).
                        timeCount = 0
                        pygame.mixer.music.stop()

        elif page == 'options' :                                                                        #If page is equal to the options page...
            if event.type == pygame.KEYDOWN :                                                               #Check for keys being pressed.
                if event.key == pygame.K_UP or event.key == pygame.K_w :                                        #If the UP key or the W key is pressed, move menu option up.
                    activeMenuOption = activeMenuOption + 1                                                         
                if event.key == pygame.K_DOWN or event.key == pygame.K_s :                                      #If the DOWN key or the S key is pressed, move menu option down.
                    activeMenuOption = activeMenuOption - 1
                    
                if event.key == pygame.K_RETURN :                                                               #If the ENTER key is pressed, check for the highlighted menu options.
                    timeCount = 0                                                                                   #Reset timeCount.
                    if activeMenuOption == 0 :                                                                      #If the menu option is 0, set the page to credits.
                        page = 'credits'
                    else:                                                                                           #If the menu option is 1, toggle the playMusic variable.
                        if playMusic == True :                                                                          #If true, make false. If false, make true.
                            playMusic = False
                            pygame.mixer.music.stop()                                                                       #Stops the music if OFF is chosen.
                        else:
                            playMusic = True
                        
                if event.key == pygame.K_ESCAPE :                                                               #If ESC is pressed, set the page to the main menu and set the menuOption to 2.
                    page = 'main'
                    activeMenuOption = 2
                    
        elif page == 'credits' :                                                                        #If page is equal to the credits page...
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :                                                           #If ESC is pressed, set the page to the options page and set the menuOption to 1.
                    page = 'options' 
                    activeMenuOption = 1
     
        elif page in ['level1','level2','level3','level4','tutorial'] :                                 #If the page is equal to one of the levels (or tutorial)...
                    
            if event.type == pygame.MOUSEBUTTONDOWN :                                                       #If left click, rotate left.
                if pygame.mouse.get_pressed() == (1,0,0) :
                    rotInput = 1
                if pygame.mouse.get_pressed() == (0,0,1) :                                                  #If right click, rotate right.
                    rotInput = -1

            if event.type == pygame.MOUSEBUTTONUP :                                                     #Stop the rotation if a mouse click is released.
                rotInput = 0
            
            if event.type == pygame.KEYDOWN :                                                           #Check for keys being pressed.
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d :                                 #If RIGHT or D key is pressed, rotate right.
                    rotInput = -1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a :                                  #If LEFT or A key is pressed, rotate left.
                    rotInput = 1
                    
                if page == 'tutorial' :                                                                     #If the page is tutorial...
                    if event.key == pygame.K_ESCAPE :                                                           #If ESC is pressed, set the page to the main menu, and the menuOption to 2.
                        page = 'main'
                        activeMenuOption = 2
                        tutorialStage = 0                                                                           #Set tutorialStage to 0 (resets the tutorial).
                    if event.key == pygame.K_RETURN :                                                           #If ENTER is pressed, go to the next tutorialStage.
                        tutorialStage = tutorialStage + 1
                else:                                                                                       #If the page isn't equal to tutorial...
                    if event.key == pygame.K_ESCAPE :                                                           #If ESC is pressed, set the page to levelSelect, and stop the music (to be reset).
                        page = 'levelSelect'                                                                    
                        pygame.mixer.music.stop()
                
            if event.type == pygame.KEYUP :                                                             #If a rotation key is let go, stop the rotation.              
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d :
                    rotInput = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                    rotInput = 0

        elif page in ['gameover1','gameover2','gameover3','gameover4'] :                                #If the page is equal to any of the gameover screens...
            if event.type == pygame.MOUSEBUTTONDOWN :                                                       #Check for mouse clicks.
                if pygame.mouse.get_pressed() == (1,0,1) and obstacles == [] :                                  #If double mouse click and all of the obstacles have been removed from the previous gameplay...
                    if page == 'gameover1' :                                                                        #Check page. If gameover1, send to level1, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 0.5
                        page = 'level1'
                    elif page == 'gameover2' :                                                                      #Check page. If gameover2, send to level2, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 1
                        page = 'level2'
                    elif page == 'gameover3' :                                                                      #Check page. If gameover3, send to level3, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 1.5
                        page = 'level3'
                    elif page == 'gameover4' :                                                                      #Check page. If gameover4, send to level4, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 2
                        page = 'level4'
                        
                    playSoundEffect('begin',timeCount)                                                          #Plays the begin sound effects upon play.
            
            if event.type == pygame.KEYDOWN :                                                               #Check for keys being pressed.
                if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and obstacles == [] :          #If ENTER or SPACE is being pressed, and all the obstacles have been removed...
                    if page == 'gameover1' :                                                                        #Check page. If gameover1, send to level1, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 0.5
                        page = 'level1'
                    elif page == 'gameover2' :                                                                      #Check page. If gameover2, send to level2, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 1
                        page = 'level2'
                    elif page == 'gameover3' :                                                                      #Check page. If gameover3, send to level3, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 1.5
                        page = 'level3'
                    elif page == 'gameover4' :                                                                      #Check page. If gameover4, send to level4, set the rotSpeed, and reset the time.
                        timeCount = 0
                        rotSpeed = 2
                        page = 'level4'
                        
                    playSoundEffect('begin',timeCount)                                                          #Plays the begin sound effects upon play.
                    
                elif event.key == pygame.K_ESCAPE :                                                             #If ESC is pressed, set the page to levelSelect, reset the time, and stop the music (to reset).
                    timeCount = 0
                    page = 'levelSelect'
                    pygame.mixer.music.stop()
                    
    if done == True:
        break
    
    
    
    # ========================== MOVE STUFF ========================== #
    rotPos = rotPos + rotSpeed                                                                          #The rotation position is equal to itself plus the rotation speed. This rotates the bakcground and game.
    if rotPos > 360 :                                                                                       #If the rotPos is greater than 360, set to 0. (Keeps the rotPos consistant).                           
        rotPos = 0
    elif rotPos < 0 :                                                                                       #If the rotPos is lesser than 0, set to 360. (Keeps the rotPos consistant).
        rotPos = 360

    # ========================== COLLISION ========================== #
    

    # ========================== DRAW STUFF ========================== #

    colourManagement(page,timeCount)                                                                    #Calls the colourManagement to manage the colours in-game.
    screen.fill(bgColourDrawMain)                                                                       #Fills the screen with the background colour.
    pygame.mouse.set_visible(False)                                                                     #Makes the mouse invisible while playing.
        
    if page == 'main' :                                                                                 #If the page is equal to the main menu.
        origin = [screen.get_width()/2,screen.get_height() + 50]                                        #Set the page origin.
        rotSpeed = 0.25                                                                                 #Set the rotSpeed.
        background()                                                                                    #Call the background function to manage the background.
        timeCount = timeCount + 1                                                                       #Update the time.

        obstaclePushBack = 0                                                                            #Sets the obstacle pushback to zero because that animation is not needed.
        obstacleManagement(obstaclePushBack)                                                            #Manages the obstacles. (Only needed here to deal with leftover obstacles from the tutorial).

        if pygame.mixer.get_busy() == False :                                                           #If the pygame mixer is not finished playing the intro sound effect, don't start playing the song.
            musicManagement(page,playMusic)

        if activeMenuOption < 0 :                                                                       #Creates a boundary for the activeMenuOptions. If less than 0, set to 2.
            activeMenuOption = 2
        elif activeMenuOption > 2 :                                                                     #If greater than 2, set to 0.
            activeMenuOption = 0

        ## Shapes and Text ##

        for i in range(0,3) :                                                                                                       #FOR loop draws the boxes for the menu options.
            menuOptionsOrigin = [screen.get_width()/2 - 200,(screen.get_height() - 200 - (100 * i))]                                    #Set the origin for the outlining boxes.
            pygame.draw.polygon(screen,(255,255,255),[menuOptionsOrigin,[menuOptionsOrigin[0] - 25,menuOptionsOrigin[1] + 75],          #Draw the shapes (this is the background of the box. (Gives the white outline effect)).
                                                [menuOptionsOrigin[0] + 400,menuOptionsOrigin[1] + 75],
                                                [menuOptionsOrigin[0] + 425,menuOptionsOrigin[1]]])
            
            menuOptionsOrigin = [screen.get_width()/2 - 195,(screen.get_height() - 195 - (100 * i))]                                    #Set the origin for the box fills.
            
            if activeMenuOption == i :                                                                                                  #If the activemMenuOption is equal to the value in the for loop, set the fill to a darker colour.
                textBoxColour = [30,30,30]
            else:                                                                                                                       #If it isn't, keep the colour the same.
                textBoxColour = [50,50,50]
                
            pygame.draw.polygon(screen,(textBoxColour),[menuOptionsOrigin,[menuOptionsOrigin[0] - 22,menuOptionsOrigin[1] + 65],        #Draws the fills for the boxes.
                                                [menuOptionsOrigin[0] + 390,menuOptionsOrigin[1] + 65],
                                                [menuOptionsOrigin[0] + 412,menuOptionsOrigin[1]]])
            
        '''Quit game notification'''
        pygame.draw.polygon(screen,(50,50,50),[[0,screen.get_height()],[400,screen.get_height()],[375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]])      #Draws the polygon.
        
        screen.blit(textExit,[10,(screen.get_height() - 50)])                                                                                                           #Blits the textExit.

        '''Title'''
        screen.blit(textSuper,[screen.get_width()/2 - 325,50])                                                                                                          #Blits the title to the screen.
        screen.blit(textHexagon,[screen.get_width()/2 - 225,200])

        '''Options'''
        screen.blit(textPlay,[menuOptionsOrigin[0] + 155,menuOptionsOrigin[1] + 7])                                                                                     #Blits the menu options.
        screen.blit(textTutorial,[menuOptionsOrigin[0] + 120,menuOptionsOrigin[1] + 107])
        screen.blit(textOptions,[menuOptionsOrigin[0] + 130,menuOptionsOrigin[1] + 207])

    elif page == 'levelSelect' :
        origin = [screen.get_width()/2,screen.get_height()/2]                                       #Set origin for the page.
        
        rotInput = 0                                                                                #Set the rotInput to 0 to stop the player from rotating.                                                                 
        rotSpeed = 0.25                                                                             #Set the rotSpeed.
        playerInfo[5] = 30                                                                          #Set the player rotPos to 30 for visual effect.
        timeCount = timeCount + 1                                                                   #Update the time                                          
        playerInfo[3] = 60 ; playerInfo[6] = 10                                                     #Set the lineLen and size of the player
        
        background()                                                                                #Call the background function to manage the background.
        pulse(20)                                                                                   #Calls the pulse function to create a pulse effect.
        
        obstaclePushBack = 0                                                                        #Sets the obstacle pushback to zero because that animation is not needed.
        obstacleManagement(obstaclePushBack)                                                        #Manages the obstacles. (Only needed here to deal with leftover obstacles from the levels).

        playerManagement(rotInput)                                                                  #Manages the player position.

        drawHexagon(50)                                                                             #Draws the hexagon to the screen.

        musicManagement(page,playMusic)                                                             #Manages music.
        pygame.mixer.music.set_volume(fade(pygame.mixer.music.get_volume(),0.8,0.1))                #Fades volume to full volume
            
        if activeMenuOption < 0 :                                                                   #Creates the boundary for the menu options. 
            activeMenuOption = 0
        elif activeMenuOption > 3 :
            activeMenuOption = 3

        if activeMenuOption == 3 :                                                                  #Changes the colour of the textBoxes for the fourth level display because of the black background.
            textBoxColour = [50,50,50]
        else:
            textBoxColour = [0,0,0]

        '''Level name Display'''
        pygame.draw.polygon(screen,(textBoxColour),[[0,50],[0,250],[screen.get_width()/2,250],[screen.get_width()/2 + 50,300],      #Draws the level name display.
                                                    [screen.get_width(),300],[screen.get_width(),50]])

        for i in range(0,4) :                                                                                                       #FOR loop checks the activeMenuOption to see which level name to blit.
            if activeMenuOption == i :
                screen.blit(textLevelNames[i],[100,60])

        textHighscore2 = highscoreManagement(timeCount,page)                                                                        #recieves the highscore value from the highscoreManagement for blitting.
                
        screen.blit(textHighscore1,[screen.get_width()/2 + 60,240])                                                                 #Blits text to screen.
        screen.blit(textHighscore2,[screen.get_width()/2 + 250,240])

        '''Press ENTER to play'''
        pygame.draw.polygon(screen,(textBoxColour),[[screen.get_width(),screen.get_height()],[screen.get_width() - 400,screen.get_height()],                            #Draws polygon to screen.
                                                    [ screen.get_width() - 375,(screen.get_height() - 50)],[screen.get_width(),(screen.get_height() - 50)]])
        
        screen.blit(textEntertoPlay,[screen.get_width() - 295,(screen.get_height() - 50)])                                                                              #Blits text.
        
        '''Escape to Main Menu'''
        pygame.draw.polygon(screen,(textBoxColour),[[0,screen.get_height()],[400,screen.get_height()],[375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]]) #Draws polygon to screen.
        
        screen.blit(textEscMain,[10,(screen.get_height() - 50)])                                                                                                        #Blits text.

        
    elif page == 'tutorial' :                                                                                           #If page is equal to tutorial...
        origin = [screen.get_width()/2,screen.get_height()/2]                                                               #Set the origin of the page.

        timeCount = timeCount + 1                                                                                           #Update time
        playerInfo[3] = fade(playerInfo[3],60,-15) ; playerInfo[6] = fade(playerInfo[6],10,-2)                              #Fade the player size and lineLen (visual effect).
        
        background()                                                                                #Call the background function to manage the background.
        pulse(15)                                                                                   #Calls the pulse function to create a pulse effect.
        
        obstaclePushBack = 0                                                                        #Sets the obstacle pushback to zero because that animation is not needed.
        obstacleManagement(obstaclePushBack)                                                        #Manages the obstacles.

        playerManagement(rotInput)                                                                  #Manages the player position.

        drawHexagon(50)                                                                             #Draws the hexagon to the screen.

        tutorialManagement()                                                                        #Manages the tutorial text.
        levelManagement(page,timeCount,rotSpeed)                                                    #Manages the tutorial level

        musicManagement(page,playMusic)                                                             #Manages the music.

        '''Escape to Main Menu'''
        pygame.draw.polygon(screen,(textBoxColour),[[0,screen.get_height()],[400,screen.get_height()],                      #Draws polygon.
                                                    [375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]])     
        
        screen.blit(textEscMain,[10,(screen.get_height() - 50)])                                                            #Blits text

        if tutorialStage >= 10 :                                                                                            #If the tutorial stage is greater than or equal to 10...
            
            ''' Time Display Bar'''
            timeHUDorigin = [screen.get_width(),0]                                                                          #Set the origin of the HUD.
            
            pygame.draw.polygon(screen,(textBoxColour),[(timeHUDorigin),(timeHUDorigin[0] - 450, timeHUDorigin[1]), (timeHUDorigin[0] - 425,timeHUDorigin[1] + 50),         #Draw the HUD.
                                                (timeHUDorigin[0] - 275, timeHUDorigin[1] + 50), (timeHUDorigin[0] - 260, timeHUDorigin[1] + 80),
                                                (timeHUDorigin[0],timeHUDorigin[1] + 80)])

            screen.blit(textTime,[timeHUDorigin[0] - 395,0])                                                                                                                #Blit text to HUD.

            sec, millisec = timeManagement(timeCount)                                                                           #Receives the timeManagement of the current time in-game.
            numTime = font80.render(str(sec) + ':' + str(millisec),True,(255,255,255))                                          #Renders the time
            screen.blit(numTime,[timeHUDorigin[0] - 225,-10])                                                                   #Blits the time.

            
            '''Grade Display Bar'''
            gradeHUDorigin = [0,0]                                                                                          #Set the origin of the second part of the HUD.
            
            pygame.draw.polygon(screen,(textBoxColour),[(gradeHUDorigin), [gradeHUDorigin[0] + 400,0], [gradeHUDorigin[0] + 375, 50], [gradeHUDorigin[0] + 150, 50],        #Draw the HUD.
                                                        [gradeHUDorigin[0] + 125, 100], [gradeHUDorigin[0],100]])

            progressBar(timeCount,[gradeHUDorigin[0] + 165,gradeHUDorigin[1] + 15])                                                 #Update the progress bar.
            
            if timeCount <= 10000 :                                                                                                 #If the time is less than 100 seconds, change the size of the font...
                textCurrentGrade = font100.render((gradeChooser(timeCount)),True,(50,255,50))                                       #... to fit the grade  in the text box.
                screen.blit(textCurrentGrade,[40,-10])                                                                              #Blit text.
            else:
                textCurrentGrade = font80.render((gradeChooser(timeCount)),True,(50,255,50))                                        #Else, change the font to a smaller size to fit the "A++" in the text box.
                screen.blit(textCurrentGrade,[10,0])




    elif page == 'options' :                                                                            #If page is equal to options...
        origin = [screen.get_width()/2,screen.get_height() + 50]                                            #Set the origin of the page.
        rotSpeed = 0.25                                                                                     #Set the rotSpeed.
        background()                                                                                        #Call the background.
        timeCount = timeCount + 1                                                                           #Update the time.

        obstaclePushBack = 0                                                                                #Sets the obstacle pushback to zero because that animation is not needed.
        obstacleManagement(obstaclePushBack)                                                                #Manages the obstacles. (Only needed here to deal with leftover obstacles from the levels).

        musicManagement(page,playMusic)                                                                     #Manages music.

        if activeMenuOption < 0 :                                                                           #Creates boundaries for the menu options.
            activeMenuOption = 1
        elif activeMenuOption > 1 :
            activeMenuOption = 0

        ## Shapes and Text ##

        for i in range(0,2) :                                                                                                   #Draws the text boxes for the menu options to the screen.
            menuOptionsOrigin = [screen.get_width()/2 - 200,(screen.get_height() - 300 - (100 * i))]                                #Set origin of outline boxes.
            pygame.draw.polygon(screen,(255,255,255),[menuOptionsOrigin,[menuOptionsOrigin[0] - 25,menuOptionsOrigin[1] + 75],      #Draw outline boxes.
                                                [menuOptionsOrigin[0] + 400,menuOptionsOrigin[1] + 75],
                                                [menuOptionsOrigin[0] + 425,menuOptionsOrigin[1]]])
            
            menuOptionsOrigin = [screen.get_width()/2 - 195,(screen.get_height() - 295 - (100 * i))]                                #Set origin of fill boxes.
            
            if activeMenuOption == i :                                                                                              #Highlights a box if it is the correct menuOption
                textBoxColour = [30,30,30]
            else:
                textBoxColour = [50,50,50]
                
            pygame.draw.polygon(screen,(textBoxColour),[menuOptionsOrigin,[menuOptionsOrigin[0] - 22,menuOptionsOrigin[1] + 65],    #Draws the fill boxes
                                                [menuOptionsOrigin[0] + 390,menuOptionsOrigin[1] + 65],
                                                [menuOptionsOrigin[0] + 412,menuOptionsOrigin[1]]])
            
        '''Escape to Main Menu '''
        pygame.draw.polygon(screen,(50,50,50),[[0,screen.get_height()],[400,screen.get_height()],[375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]])      #Draw polygon.
        
        screen.blit(textEscMain,[10,(screen.get_height() - 50)])                                                                                                        #Blit text.

        '''Options title'''
        screen.blit(textOptions,[screen.get_width()/2 - 75,250])                                                                                                        #Blit text.

        '''Options'''
        if playMusic == True :                                                                                      #Renders the correct text depending on the state of playMusic.
            textToggleMusic = font40.render('MUSIC: On',True,(255,255,255))                                             #If on, render "ON"
        else:
            textToggleMusic = font40.render('MUSIC: Off',True,(255,255,255))                                            #If off, render "OFF"
        
        screen.blit(textToggleMusic,[menuOptionsOrigin[0] + 110,menuOptionsOrigin[1] + 7])                          #Blit text the screen.
        screen.blit(textCredits,[menuOptionsOrigin[0] + 120,menuOptionsOrigin[1] + 107])





    elif page == 'credits' :                                                                            #If page is equal to credits...
        origin = [screen.get_width()/2,screen.get_height() + 50]                                            #Set origin of page.
        rotSpeed = 0.25                                                                                     #Set rotSpeed.
        background()                                                                                        #Call background.
        timeCount = timeCount + 1                                                                           #Update time. 

        musicManagement(page,playMusic)                                                                     #Manage music.

        for i in range(0,len(textCreditInfo)) :                                                         #Loops through the credit text and blits it to the screen.
            screen.blit(textCreditInfo[i],[50,(100 + (75*i))])

        '''Escape to Main Menu'''
        pygame.draw.polygon(screen,(textBoxColour),[[0,screen.get_height()],[400,screen.get_height()],[375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]])     #Draw polygon.
        
        screen.blit(textEscMain,[10,(screen.get_height() - 50)])                                                                                                            #Blit text.

    elif page in ['level1','level2','level3','level4'] :                                                #If page is equal to a level...

        if page == 'level4' :                                                                           #If level4, set the textbox colour to a brighter colour.
            textBoxColour = [50,50,50]
        else:
            textBoxColour = [0,0,0]

        origin = [screen.get_width()/2,screen.get_height()/2]                                           #Set origin.
        rotSpeed = levelManagement(page,timeCount,rotSpeed)                                             #Get rotSpeed from levelManagement.

        timeCount = timeCount + 1                                                                       #Update time
        playerInfo[3] = fade(playerInfo[3],60,-15) ; playerInfo[6] = fade(playerInfo[6],10,-2)          #Create player size and lineLen animation.
        
        background()                                                                                    #Call background.
        pulse(15)                                                                                       #Create pulse.
        
        obstaclePushBack = 0                                                                            #Sets the obstacle pushback to zero because that animation is not needed.
        obstacleManagement(obstaclePushBack)                                                            #Manages the obstacles.

        playerManagement(rotInput)                                                                      #Manges the player.
        
        hexSize = fade(hexSize,50,-10)                                                                  #Animates the size of the hexagon between gameover and the gameplay.
        drawHexagon(hexSize)                                                                            #Draws the hexagon.

        musicManagement(page,playMusic)                                                                 #Manages music.
        pygame.mixer.music.set_volume(fade(pygame.mixer.music.get_volume(),0.8,0.1))                    #Manges the volume. (Fades between gameover and gameplay).

        ## Shapes and Text (HUD) ##

        ''' Time Display Bar'''
        timeHUDorigin = [screen.get_width(),0]                                                          #Sets origin of HUD.
        
        pygame.draw.polygon(screen,(textBoxColour),[(timeHUDorigin),(timeHUDorigin[0] - 450, timeHUDorigin[1]), (timeHUDorigin[0] - 425,timeHUDorigin[1] + 50),     #Draws polygon.
                                            (timeHUDorigin[0] - 275, timeHUDorigin[1] + 50), (timeHUDorigin[0] - 260, timeHUDorigin[1] + 80),
                                            (timeHUDorigin[0],timeHUDorigin[1] + 80)])

        screen.blit(textTime,[timeHUDorigin[0] - 395,0])                                                                                                            #Blits text.

        sec, millisec = timeManagement(timeCount)                                                                                                                   #Retreives timeManagement info
        numTime = font80.render(str(sec) + ':' + str(millisec),True,(255,255,255))                                                                                  #Renders info.
        screen.blit(numTime,[timeHUDorigin[0] - 225,-10])                                                                                                           #Blits info.

        
        '''Grade Display Bar'''
        gradeHUDorigin = [0,0]                                                                                                                                      #Set origin.
        
        pygame.draw.polygon(screen,(textBoxColour),[(gradeHUDorigin), [gradeHUDorigin[0] + 400,0], [gradeHUDorigin[0] + 375, 50], [gradeHUDorigin[0] + 150, 50],    #Draw polygon.
                                                    [gradeHUDorigin[0] + 125, 100], [gradeHUDorigin[0],100]])

        progressBar(timeCount,[gradeHUDorigin[0] + 165,gradeHUDorigin[1] + 15])                                                                                     #Updates progress bar.
        
        if timeCount < 10000 :
            textCurrentGrade = font100.render((gradeChooser(timeCount)),True,(50,255,50))                                                                           #Renders grade.
            screen.blit(textCurrentGrade,[40,-10])
        else:
            textCurrentGrade = font80.render((gradeChooser(timeCount)),True,(50,255,50))                                                                            #Renders 'A++' smaller so it fits in box.
            screen.blit(textCurrentGrade,[10,0])
        
        '''Score Display'''                                                                                     #The following polygons are for animations. These aren't actually visible during gameplay.
        scoreHUDorigin[0] = fade(scoreHUDorigin[0],-800,-50)                                                                                    #Draws polygon and blits GAMEOVER.
        
        pygame.draw.polygon(screen,(textBoxColour),[(scoreHUDorigin), [scoreHUDorigin[0] + (screen.get_width()/2 - 80),scoreHUDorigin[1]],
                                            [scoreHUDorigin[0] + (screen.get_width()/2),scoreHUDorigin[1] + 300],[scoreHUDorigin[0],scoreHUDorigin[1] + 300]])

        screen.blit(textGameOver,[scoreHUDorigin[0] + 40,scoreHUDorigin[1]])
        
        '''Score 2 Display'''                                                                                                                   #Draws polygon and blits the final time.
        score2HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1]]
        
        pygame.draw.polygon(screen,(textBoxColour),[(score2HUDorigin),[score2HUDorigin[0] - screen.get_width()/2, score2HUDorigin[1]],
                                            [score2HUDorigin[0] - screen.get_width()/2 + 20, score2HUDorigin[1] + 75],
                                            [score2HUDorigin[0] - 350,score2HUDorigin[1] + 75],[score2HUDorigin[0] - 341.66,score2HUDorigin[1] + 100],
                                            [score2HUDorigin[0],score2HUDorigin[1] + 100]])
        
        screen.blit(textTime,[score2HUDorigin[0] - screen.get_width()/2 + 40, score2HUDorigin[1] + 13])

        '''Score 3 Display'''                                                                                                                   #Draws polygon and blits the highscores.
        score3HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1] + 200]
        
        pygame.draw.polygon(screen,(textBoxColour),[(score3HUDorigin),[score3HUDorigin[0] - (screen.get_width()/2 - 55), score3HUDorigin[1]],
                                            [score3HUDorigin[0] - screen.get_width()/2 + 75, score3HUDorigin[1] + 75], [score3HUDorigin[0],score3HUDorigin[1] + 75]])

        screen.blit(textHighscore1,[score3HUDorigin[0] - 500,score3HUDorigin[1] + 12])
        screen.blit(highscoreManagement(timeCount,page),[score3HUDorigin[0] - 290,score3HUDorigin[1] + 12])
        

        
        
    elif page in ['gameover1', 'gameover2','gameover3','gameover4'] :                                           #If page is equal to a gameover screen.

        if page == 'gameover4' :                                                                                    
            textBoxColour = [50,50,50]
        else:
            textBoxColour = [0,0,0]
            
        origin = [screen.get_width()/2,screen.get_height()/2]
        rotSpeed = 0.1
        playerInfo[3] = fade(playerInfo[3],340,15) ; playerInfo[6] = fade(playerInfo[6],60,2)
        rotInput = 0
        
        background()
        pulse(15)

        obstaclePushBack = fade(obstaclePushBack,screen.get_width(),50)
        obstacleManagement(obstaclePushBack)

        playerManagement(rotInput)
        
        hexSize = fade(hexSize,230,10)
        drawHexagon(hexSize)

        musicManagement(page,playMusic)
        pygame.mixer.music.set_volume(fade(pygame.mixer.music.get_volume(),0.1,-0.1))

        ## Shapes and Text (HUD) ##

        ''' Time Display Bar'''                                                                                             #Time display and grade display are animated off the screen.
        timeHUDorigin[0] = fade(timeHUDorigin[0],screen.get_width() + 450,50)
        
        pygame.draw.polygon(screen,(textBoxColour),[(timeHUDorigin),(timeHUDorigin[0] - 450, timeHUDorigin[1]), (timeHUDorigin[0] - 425,timeHUDorigin[1] + 50),
                                            (timeHUDorigin[0] - 275, timeHUDorigin[1] + 50), (timeHUDorigin[0] - 260, timeHUDorigin[1] + 80),
                                            (timeHUDorigin[0],timeHUDorigin[1] + 80)])

        screen.blit(textTime,[timeHUDorigin[0] - 395,0])


        '''Grade Display Bar'''
        gradeHUDorigin[0] = fade(gradeHUDorigin[0],-400,-50) 
        
        pygame.draw.polygon(screen,(textBoxColour),[(gradeHUDorigin), [gradeHUDorigin[0] + 400,0], [gradeHUDorigin[0] + 375, 50], [gradeHUDorigin[0] + 150, 50],
                                                    [gradeHUDorigin[0] + 125, 100], [gradeHUDorigin[0],100]])

        progressBar(timeCount,[gradeHUDorigin[0] + 165,gradeHUDorigin[1] + 15])
        
        if timeCount <= 10000 :
            textCurrentGrade = font100.render((gradeChooser(timeCount)),True,(50,255,50))
            screen.blit(textCurrentGrade,[gradeHUDorigin[0] + 40,gradeHUDorigin[1] -10])
        else:
            textCurrentGrade = font80.render((gradeChooser(timeCount)),True,(50,255,50))
            screen.blit(textCurrentGrade,[gradeHUDorigin[0] + 10,gradeHUDorigin[1]])
        
        '''Score Display'''                                                                                                     #The following polyons are visible through the animation of them coming on screen.
        scoreHUDorigin[0] = fade(scoreHUDorigin[0],0,50)
        
        pygame.draw.polygon(screen,(textBoxColour),[(scoreHUDorigin), [scoreHUDorigin[0] + (screen.get_width()/2 - 80),scoreHUDorigin[1]],
                                            [scoreHUDorigin[0] + (screen.get_width()/2),scoreHUDorigin[1] + 300],[scoreHUDorigin[0],scoreHUDorigin[1] + 300]])

        screen.blit(textGameOver,[scoreHUDorigin[0] + 40,scoreHUDorigin[1]])

        screen.blit(textGrade1,[scoreHUDorigin[0] + 150,scoreHUDorigin[1] + 170])
        
        textGrade2 = font100.render((gradeChooser(timeCount)),True,(50,255,50))
        screen.blit(textGrade2,[scoreHUDorigin[0] + 350,scoreHUDorigin[1] + 130])

        '''Score 2 Display'''
        score2HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1]]
        
        pygame.draw.polygon(screen,(textBoxColour),[(score2HUDorigin),[score2HUDorigin[0] - screen.get_width()/2, score2HUDorigin[1]],
                                            [score2HUDorigin[0] - screen.get_width()/2 + 20, score2HUDorigin[1] + 75],
                                            [score2HUDorigin[0] - 350,score2HUDorigin[1] + 75],[score2HUDorigin[0] - 341.66,score2HUDorigin[1] + 100],
                                            [score2HUDorigin[0],score2HUDorigin[1] + 100]])
        
        screen.blit(textTime,[score2HUDorigin[0] - screen.get_width()/2 + 40, score2HUDorigin[1] + 13])

        numTime = font80.render(str(sec) + ':' + str(millisec),True,(255,255,255))
        screen.blit(numTime,[score2HUDorigin[0] - screen.get_width()/2 + 300, score2HUDorigin[1]])

        
        '''Score 3 Display'''
        score3HUDorigin = [screen.get_width() - scoreHUDorigin[0],scoreHUDorigin[1] + 200]
        
        pygame.draw.polygon(screen,(textBoxColour),[(score3HUDorigin),[score3HUDorigin[0] - (screen.get_width()/2 - 55), score3HUDorigin[1]],
                                            [score3HUDorigin[0] - screen.get_width()/2 + 75, score3HUDorigin[1] + 75], [score3HUDorigin[0],score3HUDorigin[1] + 75]])

        screen.blit(textHighscore1,[score3HUDorigin[0] - 500,score3HUDorigin[1] + 12])
        screen.blit(highscoreManagement(timeCount,page),[score3HUDorigin[0] - 290,score3HUDorigin[1] + 12])

        '''Escape to level selection notification'''                                                                        #This polygon and blit appears on screen (no animation). 
        pygame.draw.polygon(screen,(textBoxColour),[[0,screen.get_height()],[400,screen.get_height()],[375,(screen.get_height() - 50)],[0,(screen.get_height() - 50)]])
        
        screen.blit(textEscLevel,[10,(screen.get_height() - 50)])
        


        
    # ========================== PYGAME STUFF ========================== #
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit ()
