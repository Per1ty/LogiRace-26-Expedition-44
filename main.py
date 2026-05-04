import pygame
import json
import math
from random import randint
import PyButton


def main(game):
    pygame.init()
    pygame.mixer.init()

    #Sounds
    click = pygame.mixer.Sound("Click.mp3")
    step = pygame.mixer.Sound("Walk.mp3")
    step_channel = pygame.mixer.Channel(1)

    info = pygame.display.Info()
    SX, SY = info.current_w, info.current_h
    font = pygame.font.SysFont('comicsans', 30)

    # Save
    if game == 'continue':
        try:
            with open("Save.json", "r") as f:
                data = json.load(f)
        except:
            game = 'new'

    if game == 'new':
        data = {"Player_x": 2600, "Player_y": 1650}
        with open("Save.json", "w") as f:
            json.dump(data, f)

    Player = {
        'Player_x': data['Player_x'],
        'Player_y': data['Player_y'],
        'Player_O2': 100,
        'Player_Hungry': 1000,
        'Player_Thirsty': 1000,
        'Player_Speed': 3
    }

    current_sprite = 0
    animation_speed = 0.10
    is_moving = False
    smooth_camera_x = (SX // 2) - Player['Player_x']
    smooth_camera_y = (SY // 2) - Player['Player_y']
    camera_speed = 0.08

    params_anim_progress = 0.0
    anim_speed = 0.08
    ParametersSwitch = -1

    Screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Expedition 44')
    clock = pygame.time.Clock()
    running = True

    # Animtion sprites
    Walk_Sprites = [
        pygame.image.load('Animation_Left2.png').convert_alpha(),
        pygame.image.load('Animation_Left.png').convert_alpha(),
        pygame.image.load('Animation_Left2.png').convert_alpha(),
        pygame.image.load('Animation_Right2.png').convert_alpha(),
        pygame.image.load('Animation_Right.png').convert_alpha(),
        pygame.image.load('Animation_Right2.png').convert_alpha(),
    ]

    # Spawning world
    CRATER_CENTER_X, CRATER_CENTER_Y = 4000, 2000
    CRATER_RADIUS = 1650

    ground = pygame.transform.scale(pygame.image.load('MarsGround.png').convert(), (8000, 4000))
    rocket = pygame.transform.scale(pygame.image.load('Rocket.png').convert_alpha(), (1200, 1600))
    cave = pygame.transform.scale(pygame.image.load('Cave.png').convert_alpha(), (1200, 1600))
    Factory = pygame.transform.scale(pygame.image.load('Factory.png').convert_alpha(), (1200, 1600))
    Colony = pygame.transform.scale(pygame.image.load('Colony.png').convert_alpha(), (3000, 2500))

    tablet = pygame.transform.scale(pygame.image.load('Screen.png').convert_alpha(), (1260, 700))
    tablet_rect = tablet.get_rect(centerx=1280 / 2, centery=720 / 2)
    Player_idle = pygame.image.load('Animation_Idle.png').convert_alpha()

    # Hitboxes
    obstacles = [
        pygame.Rect(1000, 800, 1200, 1600),  # Rocket
        pygame.Rect(3400, 300, 1200, 600),  # Cave
        pygame.Rect(5500, 1200, 1200, 1600),  # Factory
        pygame.Rect(2900, 1800, 350, 550),  # Colony
    ]

    ParametersBtn = PyButton.PyBtn(1035, 220, 200, 50, text='Параметри', color=(120, 120, 120), screen=Screen,
                                   text_color=(40, 40, 40), bound=5)

    while running:
        keys = pygame.key.get_pressed()
        new_x, new_y = Player['Player_x'], Player['Player_y']

        # Movement
        moving_now = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= Player['Player_Speed']
            moving_now = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += Player['Player_Speed']
            moving_now = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= Player['Player_Speed']
            moving_now = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += Player['Player_Speed']
            moving_now = True

        is_moving = moving_now

        player_rect_x = pygame.Rect(new_x - 25, Player['Player_y'] - 25, 50, 50)
        can_move_x = True
        for wall in obstacles:
            if player_rect_x.colliderect(wall):
                can_move_x = False
                break
        if can_move_x:
            Player['Player_x'] = new_x

        player_rect_y = pygame.Rect(Player['Player_x'] - 25, new_y - 25, 50, 50)
        can_move_y = True
        for wall in obstacles:
            if player_rect_y.colliderect(wall):
                can_move_y = False
                break
        if can_move_y:
            Player['Player_y'] = new_y

        # Round Hitboxes
        dx_c = Player['Player_x'] - CRATER_CENTER_X
        dy_c = Player['Player_y'] - CRATER_CENTER_Y
        dist = math.sqrt(dx_c ** 2 + dy_c ** 2)
        if dist > CRATER_RADIUS:
            angle_c = math.atan2(dy_c, dx_c)
            Player['Player_x'] = CRATER_CENTER_X + CRATER_RADIUS * math.cos(angle_c)
            Player['Player_y'] = CRATER_CENTER_Y + CRATER_RADIUS * math.sin(angle_c)

        # Animation
        if is_moving:
            current_sprite += animation_speed
            if current_sprite >= len(Walk_Sprites): current_sprite = 0
            if not step_channel.get_busy(): step_channel.play(step)
        else:
            current_sprite = 0
            step_channel.stop()

        # Camera
        target_camera_x = (1280 // 2) - Player['Player_x']
        target_camera_y = (720 // 2) - Player['Player_y']
        smooth_camera_x += (target_camera_x - smooth_camera_x) * camera_speed
        smooth_camera_y += (target_camera_y - smooth_camera_y) * camera_speed
        camera_x, camera_y = smooth_camera_x, smooth_camera_y

        # World
        Screen.fill((0, 0, 0))
        Screen.blit(ground, (camera_x, camera_y))
        Screen.blit(rocket, (1400 + camera_x, 800 + camera_y))
        Screen.blit(cave, (3400 + camera_x, -300 + camera_y))
        Screen.blit(Factory, (5300 + camera_x, 1000 + camera_y))
        Screen.blit(Colony, (2500 + camera_x, 800 + camera_y))

        # Rotation
        active_sprite = Walk_Sprites[int(current_sprite)] if is_moving else Player_idle
        mouse_x, mouse_y = pygame.mouse.get_pos()
        p_center = (Player['Player_x'] + camera_x, Player['Player_y'] + camera_y)
        dx, dy = mouse_x - p_center[0], mouse_y - p_center[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rotated_img = pygame.transform.rotate(active_sprite, angle)
        rect = rotated_img.get_rect(center=p_center)
        Screen.blit(rotated_img, rect)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    click.play()
            if ParametersBtn.action(event):
                ParametersSwitch *= -1

        # Tablet
        Screen.blit(tablet, tablet_rect)

        # Parameters animatuion
        if ParametersSwitch == 1:
            params_anim_progress = min(1.0, params_anim_progress + anim_speed)
        else:
            params_anim_progress = max(0.0, params_anim_progress - anim_speed)

        if params_anim_progress > 0:
            smooth_val = 1 - pow((1 - params_anim_progress), 3)
            anim_h = 300 * smooth_val
            pygame.draw.rect(Screen, (120, 120, 120), (1035, 220, 200, anim_h))
            pygame.draw.rect(Screen, (80, 80, 80), (1035, 220, 200, anim_h), 5)
            if params_anim_progress > 0.9:
                text_o2 = font.render(f"O2: {Player['Player_O2']}%", True, (40, 40, 40))
                Screen.blit(text_o2, (1045, 230))

        # Radar
        radar_center = (150, 580)
        pygame.draw.circle(Screen, (0, 130, 0), radar_center, 100)
        for i in range(20, 120, 20):
            pygame.draw.circle(Screen, (0, 160, 0), radar_center, i, 5)

        rx = radar_center[0] + (Player['Player_x'] - CRATER_CENTER_X) / (CRATER_RADIUS / 100)
        ry = radar_center[1] + (Player['Player_y'] - CRATER_CENTER_Y) / (CRATER_RADIUS / 100)
        pygame.draw.circle(Screen, (0, 255, 0), (int(rx), int(ry)), 4)

        coord_text = font.render(f'x: {int(Player["Player_x"])}, y: {int(Player["Player_y"])}', True, (40, 40, 40))
        Screen.blit(coord_text, (50, 50))
        ParametersBtn.draw()
        for wall in obstacles:
            debug_rect = wall.copy()
            debug_rect.x += camera_x
            debug_rect.y += camera_y
            pygame.draw.rect(Screen, (255, 0, 0), debug_rect, 2)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    with open('Save.json', 'w') as f:
        json.dump({"Player_x": int(Player['Player_x']), "Player_y": int(Player['Player_y'])}, f)