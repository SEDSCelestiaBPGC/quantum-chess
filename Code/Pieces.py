import pygame
import os
import math

media_path="C:/GitHub/quantum-chess/Media"

# ------------Rooks
#Initalize
brook1 = pygame.image.load(os.path.join(media_path, "BlackRook.png"))
brook1 = pygame.transform.scale(brook1,(50,50))
brook1_rect = brook1.get_rect()
brook1_rect.center = 30,30

brook2 = pygame.image.load(os.path.join(media_path, "BlackRook.png"))
brook2 = pygame.transform.scale(brook2,(50,50))
brook2_rect = brook2.get_rect()
brook2_rect.center = 450,30

wrook1 = pygame.image.load(os.path.join(media_path, "WhiteRook.png"))
wrook1 = pygame.transform.scale(wrook1,(50,50))
wrook1_rect = wrook1.get_rect()
wrook1_rect.center = 450,450

wrook2 = pygame.image.load(os.path.join(media_path, "WhiteRook.png"))
wrook2 = pygame.transform.scale(wrook2,(50,50))
wrook2_rect = wrook2.get_rect()
wrook2_rect.center = 30,450


#Valid Moves
def valid_move_rook (old_pos_name,new_pos_name):
    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        return True
    if old_pos_name[slice(1,2)] == new_pos_name[slice(1,2)]:
        return True
    else:
        return False


# -------------------Bishops


#Initalize
bbishop1 = pygame.image.load(os.path.join(media_path, "BlackBishop.png"))
bbishop1 = pygame.transform.scale(bbishop1,(50,50))
bbishop1_rect = bbishop1.get_rect()
bbishop1_rect.center = 150,30

bbishop2 = pygame.image.load(os.path.join(media_path, "BlackBishop.png"))
bbishop2 = pygame.transform.scale(bbishop2,(50,50))
bbishop2_rect = bbishop2.get_rect()
bbishop2_rect.center = 330,30

wbishop1 = pygame.image.load(os.path.join(media_path, "WhiteBishop.png"))
wbishop1 = pygame.transform.scale(wbishop1,(50,50))
wbishop1_rect = wbishop1.get_rect()
wbishop1_rect.center = 150,450

wbishop2 = pygame.image.load(os.path.join(media_path, "WhiteBishop.png"))
wbishop2 = pygame.transform.scale(wbishop2,(50,50))
wbishop2_rect = wbishop2.get_rect()
wbishop2_rect.center = 330,450

#Valid Moves
def valid_move_bishop (old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    for i in range(-8,9):
        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True



#-----------------Queen

#Initalize
bqueen = pygame.image.load(os.path.join(media_path, "BlackQueen.png"))
bqueen = pygame.transform.scale(bqueen,(50,50))
bqueen_rect = bqueen.get_rect()
bqueen_rect.center = 210,30

wqueen = pygame.image.load(os.path.join(media_path, "WhiteQueen.png"))
wqueen = pygame.transform.scale(wqueen,(50,50))
wqueen_rect = wqueen.get_rect()
wqueen_rect.center = 210,450

#Valid Moves
def valid_move_queen(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        return True
    if old_pos_name[slice(1,2)] == new_pos_name[slice(1,2)]:
        return True

    for i in range(-8,9):
        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True


#-----------------------Knights

#Initalize
bknight1 = pygame.image.load(os.path.join(media_path, "BlackKnight.png"))
bknight1 = pygame.transform.scale(bknight1,(50,50))
bknight1_rect = bknight1.get_rect()
bknight1_rect.center = 90,30

bknight2 = pygame.image.load(os.path.join(media_path, "BlackKnight.png"))
bknight2 = pygame.transform.scale(bknight2,(50,50))
bknight2_rect = bknight2.get_rect()
bknight2_rect.center = 390,30

wknight1 = pygame.image.load(os.path.join(media_path, "WhiteKnight.png"))
wknight1 = pygame.transform.scale(wknight1,(50,50))
wknight1_rect = wknight1.get_rect()
wknight1_rect.center = 90,450

wknight2 = pygame.image.load(os.path.join(media_path, "WhiteKnight.png"))
wknight2 = pygame.transform.scale(wknight2,(50,50))
wknight2_rect = wknight2.get_rect()
wknight2_rect.center = 390,450

#Valid Moves
def valid_move_knight(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if ord(fc_old) == (ord(fc_new) + 2):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 2):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 2):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 2):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) + 2):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) + 2):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) - 2):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) - 2):
            return True

    else:
        return False


# --------------------Kings

#Initalize
bking = pygame.image.load(os.path.join(media_path, "BlackKing.png"))
bking = pygame.transform.scale(bking,(50,50))
bking_rect = bking.get_rect()
bking_rect.center = 270,30

wking = pygame.image.load(os.path.join(media_path, "WhiteKing.png"))
wking = pygame.transform.scale(wking,(50,50))
wking_rect = wking.get_rect()
wking_rect.center = 270,450

#Valid Moves
def valid_move_king(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new)):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new)):
            return True

    if ord(fc_old) == (ord(fc_new)):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) ):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    else:
        return False
