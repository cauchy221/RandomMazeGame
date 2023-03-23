import random
from random import randint
import pygame
import time
from queue import LifoQueue

# const
WIDTH = 600  # width of window
HEIGHT = 600 # hight of window
LENGTH = 40  # length of block
COLOR_WORDS = (109, 104, 117)
DIFICULTY = 0.2

# init
pygame.init()
pygame.display.set_caption("Maze Game")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

# count walls
def count_ones(vector):
    count = 0
    for row in vector:
        count += row.count(1)
    return count

# change to path
def change_numbers_to_zero(vector, n):
    # flatten the 2-d vector
    flat_vector = [num for row in vector for num in row]
    selected_indices = random.sample(range(len(flat_vector)), n)  # select n random indices
    
    # loop through the 2-d vector and change the selected elements to 0
    for i, row in enumerate(vector):
        for j, _ in enumerate(row):
            index = i * len(row) + j
            if index in selected_indices:
                vector[i][j] = 0
    return vector

# generate maze
def generate_maze(m, n, dif=0.6):  # m rows, n cols
    ROWS, COLS = m, n
    start = (0,0)
    end = (m-1, n-1)
      
    # Array with only walls
    maze = list(list(1 for _ in range(COLS)) 
                       for _ in range(ROWS))
      
    # Auxiliary matrices to avoid cycles
    seen = list(list(False for _ in range(COLS)) 
                           for _ in range(ROWS))
    previous = list(list((-1, -1) for _ in range(COLS)) for _ in range(ROWS))
  
    S = LifoQueue()
    S.put(start) 
    while not S.empty():
        x, y = S.get()
        seen[x][y] = True

        if (x + 1 < ROWS) and maze[x + 1][y] == 0 and previous[x][y] != (x + 1,  y):
            continue
        if (0 < x) and maze[x-1][y] == 0 and previous[x][y] != (x-1,  y):
            continue
        if (y + 1 < COLS) and maze[x][y + 1] == 0 and previous[x][y] != (x, y + 1):
            continue
        if (y > 0) and maze[x][y-1] == 0 and previous[x][y] != (x, y-1):
            continue
  
        # Mark as walkable position
        maze[x][y] = 0
  
        # Array to shuffle neighbours before insertion
        to_stack = []
        # If adj position is valid and was not seen yet
        if (x + 1 < ROWS) and seen[x + 1][y] == False:
            seen[x + 1][y] = True
            to_stack.append((x + 1,  y))
            previous[x + 1][y] = (x, y)         
        if (0 < x) and seen[x-1][y] == False:
            seen[x-1][y] = True
            to_stack.append((x-1,  y))
            previous[x-1][y] = (x, y)
        if (y + 1 < COLS) and seen[x][y + 1] == False:
            seen[x][y + 1] = True
            to_stack.append((x, y + 1))
            previous[x][y + 1] = (x, y)
        if (y > 0) and seen[x][y-1] == False:
            seen[x][y-1] = True
            to_stack.append((x, y-1))
            previous[x][y-1] = (x, y)
          
        # Indicates if Pf is a neighbour position
        pf_flag = False
        while len(to_stack):
            neighbour = to_stack.pop(randint(0, len(to_stack)-1))
            if neighbour == end:
                pf_flag = True
            else:
                S.put(neighbour)
        if pf_flag:
            S.put(end)

    # randomly change some walls to path (to increase the dificulty)
    nums_wall = count_ones(maze)
    nums_new_path = int(nums_wall * dif)
    maze = change_numbers_to_zero(maze, nums_new_path)
                  
    # Mark the initial position
    x0, y0 = start
    xf, yf = end
    maze[x0][y0] = 3
    maze[xf][yf] = 2
      
    # Return maze formed by the traversed path
    return maze

# render the maze
def renderMaze(maze, length):
    x = 0
    y = 0
    for row in maze:
        for block in row:
        # 0 represents movable cell
            if block == 0:
                pygame.draw.rect(gameDisplay, (255, 205, 178), (x, y, length, length))
        # 1 represents wall
            elif block == 1:
                pygame.draw.rect(gameDisplay, (229, 152, 155) ,(x, y, length, length))
        # 2 represents destination
            elif block == 2:
                pygame.draw.rect(gameDisplay, (255, 183, 0), (x, y, length, length))
        # 3 represents starting cell
            elif block == 3:
                pygame.draw.rect(gameDisplay, (120, 150, 100), (x, y, length, length))
            x = x+length
        y = y+length
        x = 0

# show text when reach the exit
def displayText(text):
    renderFont = pygame.font.Font('freesansbold.ttf', 40)
    textsc = renderFont.render(text, True, COLOR_WORDS)
    surface, rect = textsc, textsc.get_rect()
    rect.center = ((WIDTH/2),(HEIGHT/2))
    gameDisplay.blit(surface, rect)
    pygame.display.update()
    #delay
    time.sleep(1)


maze = generate_maze(WIDTH//LENGTH, HEIGHT//LENGTH, dif=DIFICULTY)
win = False
exit = False
row, col = 0, 0
gameDisplay.fill((255,255,255))
while win == False:
    renderMaze(maze, LENGTH)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                block = maze[row+1][col]
                if block == 0:
                    maze[row][col] = 0
                    maze[row+1][col] = 3
                    row += 1
                elif block == 2:
                    maze[row][col] = 0
                    maze[row+1][col] = 2
                    row += 1
                    win = True
            if event.key == pygame.K_UP:
                block = maze[row-1][col]
                if block == 0:
                    maze[row][col] = 0
                    maze[row-1][col] = 3
                    row -= 1
                elif block == 2:
                    maze[row][col] = 0
                    maze[row-1][col] = 2
                    row -= 1
                    win = True
            if event.key == pygame.K_LEFT:
                block = maze[row][col-1]
                if block == 0:
                    maze[row][col] = 0
                    maze[row][col-1] = 3
                    col -= 1
                elif block == 2:
                    maze[row][col] = 0
                    maze[row][col-1] = 2
                    col -= 1
                    win = True
            if event.key == pygame.K_RIGHT:
                block = maze[row][col+1]
                if block == 0:
                    maze[row][col] = 0
                    maze[row][col+1] = 3
                    col += 1
                elif block == 2:
                    maze[row][col] = 0
                    maze[row][col+1] = 2
                    col += 1
                    win = True
    if exit:
        break
    pygame.display.update()
    if win:
        renderMaze(maze, LENGTH)
        displayText("Great You Solved it!")
        pygame.quit()
pygame.quit()