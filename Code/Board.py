import pygame

light_square=(255,255,204)
dark_square=(26,4,0)

def make_board():
    pygame.init()
    board_width=480
    board_height=board_width
    board = pygame.display.set_mode((board_width, board_height))
    cols=[light_square, dark_square]
    sq_dim=board_width/8

    for i in range(0,8):
        for j in range(0,8):
            sq_col=cols[(i+j)%2]
            pygame.draw.rect(board, sq_col, ((i*sq_dim), (j*sq_dim), sq_dim, sq_dim))

    pygame.display.flip()

    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

make_board()

