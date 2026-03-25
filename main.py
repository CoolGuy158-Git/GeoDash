import pygame as pg

pg.init()
userfile = input("Enter FileName: ") # Just leave blank for default
if userfile == "":
    userfile = 'file.gdl'
elif not userfile.endswith(".gdl"):
    print("Must have the .gdl extension")
    exit()

with open(userfile, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("song"):
            parts = line.split("=")
            if len(parts) == 2:
                song = parts[1].strip().strip("'\"")
                break
    print("Song: ", song)
pg.mixer.init()
pg.mixer.music.load(song)
pg.mixer.music.play()

player_size = 100
window = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
running = True
finished = False
attempts = 0

player = pg.transform.scale(pg.image.load("./player.png"), (player_size, player_size))
block = pg.transform.scale(pg.image.load("./stuff/block.png"), (player_size, player_size))
block2 = pg.transform.scale(pg.image.load("./stuff/block2.png"), (player_size, player_size))
spike = pg.transform.scale(pg.image.load("./stuff/spike.png"), (player_size, player_size))
top = pg.transform.scale(pg.image.load("./stuff/top.png"), (player_size, player_size))

x = 0
velocity = 6
player_y = 470
block_y = 470
top_y = 461
velocity_y = 0

def playerjump():
    global velocity_y, grounded
    if grounded and not finished:
        velocity_y = -20
def reset_game():
    global attempts
    attempts += 1
    global player_y, velocity_y, x
    player_y = 470
    velocity_y = 0
    x = 0
    pg.mixer.music.stop()
    pg.mixer.music.play()
def draw_hitboxes(player_rect, block_rects, top_rects, spike_rects):
    pg.draw.rect(pg.display.get_surface(), (255, 0, 0), player_rect, 2)
    for rect in block_rects:
        pg.draw.rect(pg.display.get_surface(), (0, 255, 0), rect, 2)
    for rect in top_rects:
        pg.draw.rect(pg.display.get_surface(), (0, 0, 255), rect, 2)
    for rect in spike_rects:
        pg.draw.rect(pg.display.get_surface(), (255, 255, 0), rect, 2)

show_hitboxes = False

while running:
    clock.tick(60)
    pg.display.set_caption(str(round(clock.get_fps())))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                playerjump()
            if event.key == pg.K_r:
                reset_game()
            if event.key == pg.K_h:
                show_hitboxes = True

    velocity_y += 0.8
    player_y += velocity_y
    grounded = False

    if player_y >= 470:
        player_y = 470
        velocity_y = 0
        grounded = True

    window.fill((135, 206, 250))

    window.blit(pg.transform.scale(block, (2000, 60)), (-280, 555))
    window.blit(player, (0, int(player_y)))
    player_rect = player.get_rect(topleft=(0, int(player_y)))
    all_block_rects = []
    all_top_rects = []
    all_spike_rects = []
    current_x = x
    for line in lines:
        line = line.strip()

        if line == '':
            current_x += player_size

        elif line in ['block', 'block2']:
            img = block if line == 'block' else block2
            block_rect = img.get_rect(topleft=(current_x, block_y))
            block_width = block_rect.width
            window.blit(pg.transform.scale(img, (player_size, player_size)), (current_x, block_y))
            top_rect = pg.Rect(current_x +8, top_y, block_width-5, 10)
            all_block_rects.append(block_rect)
            all_top_rects.append(top_rect)
            if player_rect.colliderect(top_rect):
                grounded = True
                velocity_y = 0
                player_y = top_y - player_size

            elif player_rect.colliderect(block_rect):
                if velocity_y > 0 and player_rect.bottom - velocity_y <= block_rect.top:
                    player_y = block_rect.top - player_size
                    velocity_y = 0
                    grounded = True

                else:
                    reset_game()
            current_x += player_size

        elif line == 'spike':
            spike_width = 30
            spike_height = 50
            spike_rect = pg.Rect(current_x + (player_size - spike_width) // 2,  block_y + (player_size - spike_height) // 2,  spike_width,spike_height)
            window.blit(pg.transform.scale(spike, (player_size, player_size)), (current_x, block_y))
            all_spike_rects.append(spike_rect)
            if player_rect.colliderect(spike_rect):
                reset_game()
            current_x += player_size
        elif line == 'end':
            finish_rect = pg.Rect(current_x, 0, player_size, 600)
            if show_hitboxes:
                window.blit(pg.Surface((player_size, 600)), (current_x, 0))
            if player_rect.colliderect(finish_rect):
                finished = True
                font = pg.font.SysFont("Impact", 50)
                text = font.render("Level Completed", True, (255, 255, 255))
                font = pg.font.SysFont("Arial", 45)
                texta = font.render('Attempts: '+ str(attempts), True, (255, 255, 255))
                window.blit(text, (250, 200))
                window.blit(texta, (255, 250))
                velocity = 0
            current_x += player_size
    x -= velocity
    if show_hitboxes:
        draw_hitboxes(player_rect, all_block_rects, all_top_rects, all_spike_rects)
    pg.display.flip()


pg.quit()
