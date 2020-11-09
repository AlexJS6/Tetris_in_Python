import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....', #S Shape in tetris
      '......',
      '..00..',
      '.00...',
      '.....'], # the 2 rotations possible
     ['.....', # 0 were block actually exists
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....', # Z shape tetris
      '.....', # ressembles S but in other way
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..', # I Shape tertis
      '..0..', # 4 squares long line 
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....', # square -> so only 1 possible form, same when rotated
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....', # J Shape -> 4 possible rotations
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....', #L shape -> J but other direction -> 4 possible rotations
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....', # T Shape -> 4 possible rotations
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T] # Holds shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

# This class will represent different pieces and will be the main data structure for the game
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 # so when up arrow add 1 to it

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20) ] #creates a list for every row in our grid, 20 rows, 20 sublists and each sublist (2 dimensionnal list) is gonna have 10 colours in it, the (0, 0, 0) is for rgba(black), 10 bcs 10 squares in each row -> 20 rows, '_' because dont need variable name (x)

    for i in range(len(grid)): #len(grid) = 20
        for j in range(len(grid[i])): #now in second list (10)
            if (j, i) in locked_positions: #(if key exists) rows(y) represented by i  and cols(x) by j es: (1, 1): (255, 0, 0) -> position 1, 1 represented by red
                c = locked_positions[(j, i)]
                grid[i][j] = c #look through grid and find corresponding position to locked position and change color in grid to when drawn get accurate grid
    return grid

def convert_shape_format(shape):
    positions = [] #need positions
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y +i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) #move everything up and left

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)] # similar to when created the grid (10 by 20 grid), and the color part is to saw we only add this there if nothing in it! otherwise we can't put it there!
    accepted_pos = [j for sub in accepted_pos for j in sub] #taking items from our 2dimensional list and making a 1d list from it

    formatted = convert_shape_format(shape) #will have a list with bunch of positions in it

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: #check if only asking if valid position when y is greater than -1, because we want it to start fall before grid begins -> ARE we on the grid OR not!??
                return False
    return True


def check_lost(positions): #Check if any of the pos are above the screen
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False 


def get_shape(): #create new shape that will fall down
    return Piece(5, 0, random.choice(shapes)) #x = middle screen (5) -> Class has 3 argument (x , y and shapes)



def draw_text_middle(surface, text, size, color):  
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2)) #final screen display -> This calc is to search middle!


   
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size)) #10 vertical lines and 20 horizontal lines
        for j in range(len(grid[i])): #How many columns in each row
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    
    inc = 0
    for i in range(len(grid) -1, -1, -1): #we start from bottom so when we move the things down we start from bottom so no chance of overwrite other key.
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j ,i)] #whenever we delete a row we need to increment 1
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]: #for every key in our sorted list of locked positions based on y value ex: [(0, 1), (0, 0)] gets [(0, 0), (0, 1)]
            x, y = key #(key is a tuple) so x first value and y second
            if y < ind: #if y is above the current index or row that we removed ex: row 17 deleted -> row over 17 moved down
                newKey = (x, y + inc) #inc sayys how many something needs to be shifted down!
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100 #position of 'Next shape' (changeable)
    format = shape.shape[shape.rotation % len(shape.shape)] #same as before (format -> sublist)

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row): #we do this again bcs don't care of position in grid we care when we should draw something or not (static image)
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0) #similiar to what already done

    surface.blit(label, (sx + 10, sy - 20)) #our position(changeable)



def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f: #w = write
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f: #r = read
        lines = f.readlines()
        score = lines[0].strip()

    return score

def draw_window(surface, grid, score = 0, last_score = 0): #default = 0
    surface.fill((0, 0, 0)) #fill in black

    pygame.font.init() #initialize font
    font = pygame.font.SysFont('comicsans', 60) #Set font and Size(60), (can change font)
    label = font.render('Tetris', 1, (255, 255, 255)) #We render a text ('Tetris) with antialiszing 1 (is obligatory) in white
    
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30)) # Put it in the middle of the screen
    
    #current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100 #position of 'Next shape' (changeable)
    
    surface.blit(label, (sx +20, sy + 180))

    #last score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 220
    
    surface.blit(label, (sx +20, sy + 180))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0) #draw rectangle(rect), 0 at the end to be sure to fill, not just draw a border -> gives correct position to draw

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4) #draws rectangle for play area in red and only border, of size 4

    draw_grid(surface, grid)
    #pygame.display.update()


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/ 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.007

        if fall_time/1000 > fall_speed: #Check values
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN: #Keydown is any key!

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)): #If try to move left in invalid space, - then + so pretend we didnt move
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)): #like above but other way
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1 #changes rotation
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1


        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: #if not above screen
                grid[y][x] = current_piece.color # would look weird without this

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color #locked position is a dictionnary with a position and a color 
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 20 #We declare this here so it cant have a bug when falling making a row and clearing the row, only clearing row when on the ground, and next shape declared. it also increments score


        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, 'YOU LOST!', 80, (255, 255, 255)) #display end message
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN: #Any key makes you launch main() function -> PLAY
                main(win)
    
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game