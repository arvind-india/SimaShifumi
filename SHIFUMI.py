import pygame
import time
import sys
import re
import os
import serial
import ConfigParser
from random import randint
from colorama import init, Fore
from pygame.locals import *

init(autoreset=True)
pygame.init()
 
LARGEUR = 1280
HAUTEUR = 720

COORD_X_BG = (LARGEUR/16)*3
LARGEUR_B = LARGEUR/8
COORD_X_BD = LARGEUR - (COORD_X_BG + LARGEUR_B)
COORD_Y_B = (HAUTEUR/4)*3
HAUTEUR_B = 50

IMAGE_X = 512
IMAGE_Y = 512

BLANC = (225,225,225)
ROUGE = (240, 0, 0)
ROUGE_B = (255, 135, 135)
NOIR = (0, 0, 0)
VIOLET = (184, 65, 217)
VERT = (0, 217, 0)
VERT_B = (143, 255, 143)
BLEU = (106, 145, 209)
ORANGE = (244, 134, 66)
SIMA = (57, 107, 107)

CONFIG = 'config.cfg'
SIGNES = 'codes.txt'

gameDisplay = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption('SimaProject: SHIFUMI')
clock = pygame.time.Clock()

PIERRE_P = pygame.image.load('data/1_p.png').convert_alpha()
PIERRE_P = pygame.transform.scale(PIERRE_P, (IMAGE_X, IMAGE_Y))
PIERRE_IA = pygame.image.load('data/1_ia.png').convert_alpha()
PIERRE_IA = pygame.transform.scale(PIERRE_IA, (IMAGE_X, IMAGE_Y))
FEUILLE_P = pygame.image.load('data/2_p.png').convert_alpha()
FEUILLE_P = pygame.transform.scale(FEUILLE_P, (IMAGE_X, IMAGE_Y))
FEUILLE_IA = pygame.image.load('data/2_ia.png').convert_alpha()
FEUILLE_IA = pygame.transform.scale(FEUILLE_IA, (IMAGE_X, IMAGE_Y))
CISEAUX_P = pygame.image.load('data/3_p.png').convert_alpha()
CISEAUX_P = pygame.transform.scale(CISEAUX_P, (IMAGE_X, IMAGE_Y))
CISEAUX_IA = pygame.image.load('data/3_ia.png').convert_alpha()
CISEAUX_IA = pygame.transform.scale(CISEAUX_IA, (IMAGE_X, IMAGE_Y))

INTRO_IMAGE = pygame.image.load('data/intro.png').convert_alpha()
INTRO_IMAGE = pygame.transform.scale(INTRO_IMAGE, (LARGEUR, HAUTEUR))

ICON = pygame.image.load('data/icon.png')
BANNER = pygame.image.load('data/banner.png').convert_alpha()

pygame.display.set_icon(ICON)

def GetConfig(cfg):
    try:
        config = ConfigParser.ConfigParser()
        config.read(cfg)

        port = config.get('SHIFUMI', 'port')
        baud = config.get('SHIFUMI','baud')
        score_lim = config.getint('SHIFUMI','score_limit')
        return (port, baud, score_lim)
    except:
        Quit()

def GetPort(port, baud):
    try:
        serial_arduino = serial.Serial(port, baud, rtscts=True, dsrdtr=True, timeout=10)
        return (1, serial_arduino)
    except IOError:
        return (0, 0)

def GetCode(file):
    txt = []
    db = open(file, 'r')
    with db as inputfile:
        for line in inputfile:
            txt.append(line.strip().split(';'))
        code = [item[0] for item in txt]
        sign = [item[1] for item in txt]
    db.close()
    return (code, sign)

def GetArduinoCode(arduino, code, sign):
    code = arduino.readline()
    data_ser = re.findall('\d+', code)
    if not data_ser or data_ser[0] == 0:
        return "0"
    else:
        if data_ser[0] in code:
            idx = code.index(data_ser[0])
            return sign[idx]
        else:
            return "error"

def text_objects(text, font):
    textSurface = font.render(text, True, BLANC)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("data/VeraBd.ttf",35)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def conditions(sign_p, sign_ia):
    if sign_ia == 1:
        gameDisplay.blit(PIERRE_IA, [LARGEUR-IMAGE_X, HAUTEUR-IMAGE_Y])
    elif sign_ia == 2:
        gameDisplay.blit(FEUILLE_IA, [LARGEUR-IMAGE_X, HAUTEUR-IMAGE_Y])
    elif sign_ia == 3:
        gameDisplay.blit(CISEAUX_IA, [LARGEUR-IMAGE_X, HAUTEUR-IMAGE_Y])

    if sign_p == "1":
        sign_p = 1
        gameDisplay.blit(PIERRE_P, [0, HAUTEUR-IMAGE_Y])
        if sign_ia == 1:
            return "tie"
        elif sign_ia == 2:
            return "ia"
        elif sign_ia == 3:
            return "p"
    elif sign_p == "2":
        sign_p = 2
        gameDisplay.blit(FEUILLE_P, [0, HAUTEUR-IMAGE_Y])
        if sign_ia == 1:
            return "p"
        elif sign_ia == 2:
            return "tie"
        elif sign_ia == 3:
            return "ia"
    elif sign_p == "3":
        sign_p = 3
        gameDisplay.blit(CISEAUX_P, [0, HAUTEUR-IMAGE_Y])
        if sign_ia == 1:
            return "ia"
        elif sign_ia == 2:
            return "p"
        elif sign_ia == 3:
            return "tie"


def game_quit():
    print("[MUSIC]\tBattle: https://soundcloud.com/ruari1/8bit-battle-music")
    print("[MUSIC]\tDefeat: https://www.youtube.com/watch?v=QuNhTLVgV2Y")
    print("[MUSIC]\tVictory: https://www.youtube.com/watch?v=YZPPTJzXw2s")
    pygame.quit()
    quit()

def game_startup():
    start = True
    print ("[GAME]\tStartup sequence - Press space to continue...")
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_intro()

        gameDisplay.fill(SIMA)
        gameDisplay.blit(INTRO_IMAGE, [0,0])
        pygame.display.update()
        clock.tick(15)

def game_intro():
    pygame.mixer.music.stop()
    intro = True
    print ("[GAME]\tMain menu")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_quit()
                
        gameDisplay.fill(SIMA)
        largeText = pygame.font.Font('data/VeraBd.ttf',115)
        TextSurf, TextRect = text_objects("SHIFUMI", largeText)
        TextRect.center = ((LARGEUR/2),(HAUTEUR/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play",COORD_X_BG,COORD_Y_B,LARGEUR_B,HAUTEUR_B,VERT,VERT_B,game_loop)
        button("Quit",COORD_X_BD,COORD_Y_B,LARGEUR_B,HAUTEUR_B,ROUGE,ROUGE_B,game_quit)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    pygame.mixer.music.stop()
    print ("[GAME]\tGame loop")
    port, baud, score_limit = GetConfig(CONFIG)
    com, arduino = GetPort(port, baud)
    code, sign = GetCode(SIGNES) 

    if com != 1:
        print("[ERROR]\tNo serial communication. [P] for Rock, [F] for Paper, [C] for scissors !")   
    
    pygame.mixer.music.load('data/battle.mp3')
    pygame.mixer.music.play(-1)
    print ("[MUSIC]\tPlay battle theme...")
    
    score_p = 0
    score_ia = 0

    gameDisplay.fill(SIMA)
    largeText = pygame.font.Font('data/VeraBd.ttf',120)
    TextSurf, TextRect = text_objects("Ready ?", largeText)
    TextRect.center = ((LARGEUR/2),(HAUTEUR/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.delay(2000)
    gameDisplay.fill(SIMA)
    TextSurf, TextRect = text_objects("3", largeText)
    TextRect.center = ((LARGEUR/2),(HAUTEUR/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.delay(1000)
    gameDisplay.fill(SIMA)
    TextSurf, TextRect = text_objects("2", largeText)
    TextRect.center = ((LARGEUR/2),(HAUTEUR/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.delay(1000)
    gameDisplay.fill(SIMA)
    TextSurf, TextRect = text_objects("1", largeText)
    TextRect.center = ((LARGEUR/2),(HAUTEUR/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.delay(1000)
    
    GameExit = False   
    while not GameExit:
        gameDisplay.fill(SIMA)
        sign_p = randint(1,3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                sign_p = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                sign_p = 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                sign_p = 3
        if com != 1:
            sign_p = str(sign_p)
        else:
            sign_p = GetArduinoCode(arduino, code, sign)
        sign_ia = randint(1,3)
        point = conditions(sign_p, sign_ia)
        if point == "ia":
            score_ia +=1
            print ("[ROUND]\tComputer")
        elif point == "p":
            score_p += 1
            print ("[ROUND]\tPlayer")
        elif point == "tie":
            print ("[ROUND]\tTie")

        if score_p == score_limit:
            print ("[GAME]\tPlayer wins")
            game_outro("p")
        elif score_ia == score_limit:
            print ("[GAME]\tComputer wins")
            game_outro("ia")

        largeText = pygame.font.Font('data/VeraBd.ttf',80)
        smallText = pygame.font.SysFont("data/VeraBd.ttf",80)
        
        gameDisplay.blit(BANNER, [(LARGEUR/2)-400, HAUTEUR-200])

        ScorepSurf, ScorepRect = text_objects(str(score_p), smallText)
        ScorepRect.center = ((LARGEUR/4),(HAUTEUR/5))
        gameDisplay.blit(ScorepSurf, ScorepRect)

        ScoreiaSurf, ScoreiaRect = text_objects(str(score_ia), smallText)
        ScoreiaRect.center = (((LARGEUR/4)*3),(HAUTEUR/5))
        gameDisplay.blit(ScoreiaSurf, ScoreiaRect)

        pygame.display.update()
        pygame.time.delay(3000)
        clock.tick(60)

def game_outro(winner):
    outro = True
    print ("[GAME]\tScore screen")
    if winner == "p":
        pygame.mixer.music.load('data/victory.mp3')
        pygame.mixer.music.play(-1)
        print ("[MUSIC]\tPlay victory theme...")
    elif winner == "ia":
        pygame.mixer.music.load('data/defeat.mp3')
        pygame.mixer.music.play(-1)
        print ("[MUSIC]\tPlay defeat theme...")
    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_quit()
                
        gameDisplay.fill(SIMA)
        largeText = pygame.font.Font('data/VeraBd.ttf',115)
        semilargeText = pygame.font.Font('data/VeraBd.ttf',80)
        if winner == "ia":
            text = "YOU LOSE."
        elif winner == "p":
            text = "YOU WIN!"
        outroSurf, outroRect = text_objects(text, largeText)
        outroRect.center = ((LARGEUR/2),(HAUTEUR/2))
        gameDisplay.blit(outroSurf, outroRect)
        gameDisplay.blit(BANNER, [(LARGEUR/2)-400, 0])

        button("Play again",COORD_X_BG,COORD_Y_B,LARGEUR_B,HAUTEUR_B,VERT,VERT_B,game_loop)
        button("Quit",COORD_X_BD,COORD_Y_B,LARGEUR_B,HAUTEUR_B,ROUGE,ROUGE_B,game_quit)

        pygame.display.update()
        clock.tick(15)


game_startup()
game_quit()