import sys
from Maze import *
from show import *
from Algorithm import *

pygame.init()
size = width, height = 700, 600
screen = pygame.display.set_mode(size)

RectButtonFont = pygame.font.Font("OpenSans-Regular.ttf", 16)
CirButtonFont = pygame.font.Font("OpenSans-Regular.ttf", 40)

colors = {
    "black": (15, 15, 35),              # 🎇 BACKGROUND – Midnight navy (dark, clean)
    "white": (230, 230, 230),           # 🟫 AREA KOSONG – Soft white
    "blue": (0, 122, 255),              # 🟦 START – iOS-style blue (vibrant)
    "red": (255, 59, 48),               # 🟥 TARGET – Apple-style red
    "gray": (40, 40, 40),               # ⬛ WALL – Dark gray for elegance
    "green": (52, 199, 89),             # 🟩 DIJELAJAHI – Apple-style green
    "purple": (175, 82, 222),           # 🟣 Q-LEARNING – Soft violet
    "p_yellow": (255, 214, 10),         # 🟨 PATH – Strong yellow (Golden)
    "yellow": (255, 150, 0),            # 🟡 TOMBOL KLIK – Rich amber
    "frontier": (255, 149, 204)         # 🟣 FRONTIER – pink modern style
}

# board and algorithm parameter
TRAIN = 10
PADDING = 32
RADIUS = 40
board_height = height - 4*PADDING
board_width = width - 4*PADDING
v_cells = 30
h_cells = 30
cell_size = int(min(board_height/(v_cells), 
                    board_width/(h_cells)))
board_origin = (PADDING, PADDING)

# Rectangular buttons for main controls
start_button = RectButton(
    left=PADDING, top=height-2*PADDING,
    width=3*PADDING, height=1.5*PADDING,
    text="Search Start", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

draw_button = RectButton(
    left=4.5*PADDING, top=height-2*PADDING,
    width=3*PADDING, height=1.5*PADDING,
    text="Draw Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

erase_button = RectButton(
    left=8*PADDING, top=height-2*PADDING,
    width=3*PADDING, height=1.5*PADDING,
    text="Erase Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

maze_button = RectButton(
    left=11.5*PADDING, top=height-2*PADDING,
    width=3*PADDING, height=1.5*PADDING,
    text="Maze", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

reset_button = RectButton(
    left=15*PADDING, top=height-2*PADDING,
    width=3*PADDING, height=1.5*PADDING,
    text="Reset", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

# Calculate the x-position for algorithm buttons (right of the maze)
maze_right_edge = PADDING + h_cells * cell_size
algo_button_x = maze_right_edge + 2*PADDING
algo_button_width = 100
algo_button_height = 50

# Rectangular buttons for algorithm selection
dijkstra_button = RectButton(
    left=algo_button_x, top=PADDING,
    width=algo_button_width, height=algo_button_height,
    text="Dijkstra", textcolor=colors["white"],
    rectcolor=colors["yellow"],  # Default to yellow as in the second image
    screen=screen, font=RectButtonFont)

SEARCH = False
DRAW = False
ERASE = False
RESET = False
ALGO = "Dijkstra"  # Default to Dijkstra to match the yellow button
board = Board(v_cells, h_cells, board_origin[0], board_origin[1], cell_size, screen, colors)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(colors["black"])

    if not SEARCH:
        # draw board and store cells (pygame rect object) for drawing and erasing wall
        cells = board.draw_board()
        
        # call game board buttons
        start_button()
        draw_button()
        erase_button()
        maze_button()
        reset_button()

        # call algorithm buttons
        dijkstra_button()
        # if Reset button is pressed, change color back to white and set flag to False
        if RESET == True:
            time.sleep(0.05)
            reset_button.color_change(colors["white"])
            reset_button()
            RESET = False

        # mouse event
        left, _, right = pygame.mouse.get_pressed()

        # if left clicked, get mouse position and take corresponding action
        if left == 1:
            mouse = pygame.mouse.get_pos()

            # Board modified selections
            # button for start search
            if start_button.rect.collidepoint(mouse):
                if SEARCH == False:
                    SEARCH = True
                    DRAW = False
                    ERASE = False
                    
                    draw_button.color_change(colors["white"])
                    erase_button.color_change(colors["white"])
                    start_button.color_change(colors["yellow"])
                    
                    start_button()
                    draw_button()
                    erase_button()
                    time.sleep(0.1)
            # button for drawing wall
            elif draw_button.rect.collidepoint(mouse):
                if DRAW == False:
                    DRAW = True
                    ERASE = False
                    draw_button.color_change(colors["yellow"])
                    erase_button.color_change(colors["white"])
                else:
                    DRAW = False
                    draw_button.color_change(colors["white"])   

                time.sleep(0.1)                
            # button for erasing wall
            elif erase_button.rect.collidepoint(mouse):
                if ERASE == False:
                    ERASE = True
                    DRAW = False
                    erase_button.color_change(colors["yellow"])
                    draw_button.color_change(colors["white"])
                else:
                    ERASE = False
                    erase_button.color_change(colors["white"])    

                time.sleep(0.1)
            # button for reset board
            elif reset_button.rect.collidepoint(mouse):
                DRAW = False
                ERASE = False
                RESET = True
                
                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                reset_button.color_change(colors["yellow"])
                reset_button()
                
                board.reset()
                time.sleep(0.1)   
            # button for automated generate maze
            elif maze_button.rect.collidepoint(mouse):
                if board.wall:
                    print("Please Reset the Board")
                    time.sleep(0.1)   
                    continue

                if not board.start:
                    print("Please Select Start")
                    time.sleep(0.1)   
                    continue
                elif board.target:
                    print("Please Do Not Set Target")
                    time.sleep(0.1)   
                    continue
                
                DRAW = False
                ERASE = False
                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                maze_button.color_change(colors["yellow"])
                maze_button()

                maze_creator = Maze(board)
                maze_creator.initialize()
                maze_creator.generate()

                maze_button.color_change(colors["white"])
                maze_button()
                time.sleep(0.1)

            # Algorithm selections
            # button for dijkstra
            if dijkstra_button.rect.collidepoint(mouse):
                ALGO = "Dijkstra"
                dijkstra_button.color_change(colors["yellow"])
                time.sleep(0.1)

            # drawing or erasing wall by checking corresponding flag and position of mouse
            else:
                for i in range(v_cells):
                    for j in range(h_cells):
                        cell = cells[i][j]
                        if (i,j) != board.start or (i,j) != board.target:
                            if DRAW and cell.collidepoint(mouse):
                                board.wall.add((i,j))
                            elif ERASE and cell.collidepoint(mouse) and (i,j) in board.wall:
                                board.wall.remove((i,j))

        # right clicked, defining start and target point
        elif right == 1:
            mouse = pygame.mouse.get_pos()

            for i in range(v_cells):
                for j in range(h_cells):
                    cell = cells[i][j]
                    if cell.collidepoint(mouse):
                        # if it's not wall and start has not been created, create start
                        if (i,j) not in board.wall and board.start is None:
                            board.start = (i,j)
                        # if it's not wall and start, and target has not been created, create target
                        elif (i,j) not in board.wall and (i,j) != board.start and board.target is None:
                            board.target = (i,j)
                        # if it's start and target has not been created, chancel start
                        elif (i,j) == board.start and board.target is None:
                            board.start = None
                        # if it's target, chancel target
                        elif (i,j) == board.target:
                            board.target = None
            time.sleep(0.1)

        pygame.display.flip()

    # search start
    else:
        # if start or target have not been specified, game will not start
        if board.start is None or board.target is None:
            print("Please choose position of start and target")
            SEARCH = False
            start_button.color_change(colors["white"])
            continue  

        # elif algorithm is not selected, game will not start
        elif ALGO is None:
            print("Please select algorithm")
            SEARCH = False
            start_button.color_change(colors["white"])
            continue

        if board.visited or board.path:
            board.clear_visited()

        # run chosen algorithm
        if ALGO == "Dijkstra":
            algorithm = Dijkstra(board)
            algorithm.initialize()
            algorithm.solver()
        

        # if find shortest path, draw the path. if not, show "No Solution Found"
        if algorithm.find == True:
            algorithm.output()
        else:
            print("No Solution Found!")

        # set SEARCH flag to False to restart the game
        SEARCH = False
        start_button.color_change(colors["white"])