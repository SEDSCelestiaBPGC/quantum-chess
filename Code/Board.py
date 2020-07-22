import pygame

light_square=(255,255,204)
dark_square=(26,4,0)
white=(255,255,255)
black=(0,0,0)
grey=(169,169,169)

def make_board():
    pygame.init()
    board_width=480
    margin=30
    board_height=board_width
    board = pygame.display.set_mode((board_width+margin, board_height+margin))
    board.fill(white)
    cols=[light_square, dark_square]
    sq_dim=board_width/8

    for i in range(0,8):
        for j in range(0,8):
            sq_col=cols[(i+j)%2]
            pygame.draw.rect(board, sq_col, ((i*sq_dim), (j*sq_dim), sq_dim, sq_dim))
  
    label_font=pygame.font.SysFont("calibri", 18)

    for i in range(0,8):
        #pygame.draw.line(board, grey, (board_width, (i+1)*sq_dim), (board_width+margin, (i+1)*sq_dim), 2)
        #pygame.draw.line(board, grey, ((i+1)*sq_dim, board_height), ((i+1)*sq_dim, board_height+margin), 2)    
        col_text=label_font.render(chr(ord('A')+i), True, black)
        row_text=label_font.render(str(8-i), True, black)
        board.blit(col_text, ((i*sq_dim)+22, board_height+8))
        board.blit(row_text, ((board_width+10), (i*sq_dim)+22))


    pygame.draw.lines(board, black, True, [(0,0), (board_width, 0), (board_width, board_height), (0, board_height)], 2)

    pygame.display.flip()

    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

make_board()

