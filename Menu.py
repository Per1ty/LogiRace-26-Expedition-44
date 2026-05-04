import pygame
import PyButton
import json
import main



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Expedition44_Music.mp3')
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound('Click.mp3')
info = pygame.display.Info()
SX, SY = info.current_w, info.current_h
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Expedition 44')
clock = pygame.time.Clock()
Background = pygame.image.load('Bg.png').convert()
Background = pygame.transform.scale(Background, (1600,900))

Logika = pygame.image.load('Logika.png').convert_alpha()
Logika = pygame.transform.scale(Logika, (300,200))
running = True
scalex = SX/1920
scaley = SY/1080
scale = (scalex + scaley) / 2

#Buttons
QuitBtn = PyButton.PyBtn(1330*scalex,360*scaley,250*scalex,90*scaley, text = 'Вийти',color = (200,100,100),screen=screen,bound = 5,text_size = int(30*scale))
NewGameBtn = PyButton.PyBtn(x=550*scalex,
                            y=360*scaley,
                            width=250*scalex,
                            height=90*scaley,
                            text = 'Нова Гра',
                            color = (80,80,80),
                            screen=screen,
                            bound = 5,
                            text_size = int(35*scale),
                            text_color=(40,40,40))
ContinueBtn = PyButton.PyBtn(x=810*scalex,
                             y=360*scaley,
                             width=250*scalex,
                             height=90*scaley,
                             text = 'Продовжити',
                             color = (80,80,80),
                             screen=screen,
                             bound = 5,
                             text_size = int(35*scale),
                             text_color=(40,40,40))
SettingsBtn = PyButton.PyBtn(x=1070*scalex,
                             y=360*scaley,
                             width=250*scalex,
                             height=90*scaley,
                             text = 'Налаштування',
                             color = (80,80,80),
                             screen=screen,
                             bound = 5,
                             text_size = int(35*scale),
                             text_color=(40,40,40))
maingame = False
while running:
    screen.fill((30,30,30))
    screen.blit(Background,(0,0))
    screen.blit(Logika,(50,50))
    QuitBtn.draw()
    NewGameBtn.draw()
    ContinueBtn.draw()
    SettingsBtn.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if QuitBtn.action(event):
            running = False
        if NewGameBtn.action(event):
            running = False
            maingame = True
            type = 'new'
        if ContinueBtn.action(event):
            running = False
            maingame = True
            type = 'continue'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                click_sound.play()

    pygame.display.update()
    clock.tick(60)
if maingame:
    if type == 'new':

        main.main('new')
    elif type == 'continue':
        main.main('continue')