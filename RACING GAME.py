import pygame,sys,math

pygame.init()

size = width, height = 1500, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Racing Cars")

font = pygame.font.Font(None,(50))

carImage = pygame.image.load("car.png")
car = carImage.get_rect()

desaceleradorImage = pygame.image.load("desacelerador.png")
aceleradorImage = pygame.image.load("acelerador.png")
rotated_decelerator = pygame.transform.rotate(desaceleradorImage, 180)
rotated_acceleratorDown = pygame.transform.rotate(aceleradorImage, 270)
rotated_acceleratorUp = pygame.transform.rotate(aceleradorImage, 90)
desacelerador = desaceleradorImage.get_rect()

car.center = 400, 100
speed = 0
inner_walls = [(250, 200), (1250, 200), (1250, 700), (250, 700),(250, 200),(500, 200),(500, 0)]
checkpoints = [(1250,450,250,300),(450,700,300,250),(0,450,250,300)]

obstacle1 = pygame.Rect(900, 100, 80, 50)
obstacle2 = pygame.Rect(500, 800, 80, 60)

clock = pygame.time.Clock()
angle = -90  # Initial rotation angle

inner_wallsRect = (270,220,960,460)
meta = (475,0,400,250)
lap_start_time = 0
lap_time = 0
num_vueltas = 0
best_laps = []
WHITE = (255,255,255)
time_run = False
in_store = False
check_crossed = 3
MAX_SPEED = 3 #5
ACCELERATION = 0.1 #0.2
dinero = 1000

ventaja = False
desventaja = True

def vueltas(tiempo,m_vueltas):
    ordered_laps = []
    m_vueltas.append(tiempo)
    m_vueltas.sort()
    if len(m_vueltas) > 10:
        del m_vueltas[-1]
    return m_vueltas

def draw_store(velocidad,aceleracion,ventaja,desventaja,dinero):
    screen.fill((43, 40, 46))
    button_vel = pygame.Rect(150, height // 2, 350, 100)
    button_acel = pygame.Rect(600, height // 2, 350, 100)
    button_adv = pygame.Rect(1000, height // 2 + 100, 400, 100)
    button_disadv = pygame.Rect(1000, height // 2 - 100, 400, 100)
    pygame.draw.rect(screen, (50, 200, 200), button_vel)
    pygame.draw.rect(screen, (50, 200, 200), button_acel)
    pygame.draw.rect(screen, (50, 200, 200), button_adv)
    pygame.draw.rect(screen, (50, 200, 200), button_disadv)
    
    # Textos
    font_store = pygame.font.Font(None, 36)
    textmoney_store = font.render(f"Money ---> {dinero:.2f} €", True, WHITE)
    textb_vel1 = font_store.render("Increase Speed (1€)", True, (0, 0, 0))
    textb_vel2 = font_store.render(f"Speed --> {velocidad}", True, (WHITE))
    textb_acel1 = font_store.render("Increase Acceleration (5€)", True, (0, 0, 0))
    textb_acel2 = font_store.render(f"Acceleration --> {aceleracion:.1f}", True, (WHITE))
    textb_adv = font_store.render("Buy Accelerators (100€)", True, (0, 0, 0))
    textb_disadv = font_store.render("Remove Decelerators (100€)", True, (0, 0, 0))
    
    textb_vel1_rect = textb_vel1.get_rect(center=button_vel.center)
    textb_vel2_rect = textb_vel1.get_rect(center=(button_vel.centerx + 50, button_vel.centery - 100))
    textb_acel1_rect = textb_acel1.get_rect(center=button_acel.center)
    textb_acel2_rect = textb_acel1.get_rect(center=(button_acel.centerx + 50, button_acel.centery - 100))
    textb_adv_rect = textb_adv.get_rect(center=button_adv.center)
    textb_disadv_rect = textb_disadv.get_rect(center=button_disadv.center)
    
    
    screen.blit(textmoney_store,(200,height/2 - 200))
    screen.blit(textb_vel1, textb_vel1_rect)
    screen.blit(textb_vel2, textb_vel2_rect)
    screen.blit(textb_acel1, textb_acel1_rect)
    screen.blit(textb_acel2, textb_acel2_rect)
    screen.blit(textb_adv, textb_adv_rect)
    screen.blit(textb_disadv, textb_disadv_rect)
    
    # Lógica para detectar clics en el botón
    mouse_pos = pygame.mouse.get_pos()
    click, _, _ = pygame.mouse.get_pressed()
    if button_vel.collidepoint(mouse_pos) and click:
        if dinero >= 1:
            pygame.draw.rect(screen, (20, 80, 80), button_vel)
            velocidad += 1
            dinero -= 1
        else:
            pygame.draw.rect(screen, (80, 20, 20), button_vel)
        screen.blit(textb_vel1, textb_vel1_rect)
        pygame.display.flip()
        pygame.time.wait(200)
    
    if button_acel.collidepoint(mouse_pos) and click:
        if dinero >= 5:
            pygame.draw.rect(screen, (20, 80, 80), button_acel)
            aceleracion += 0.1
            dinero -= 5
        else:
            pygame.draw.rect(screen, (80, 20, 20), button_acel)
        screen.blit(textb_acel1, textb_acel1_rect)
        pygame.display.flip()
        pygame.time.wait(200)
        
    if button_adv.collidepoint(mouse_pos) and click:
        if dinero >= 100 and not ventaja:
            pygame.draw.rect(screen, (20, 80, 80), button_adv)
            ventaja = True
            dinero -= 100
        else:
            pygame.draw.rect(screen, (80, 20, 20), button_adv)
        screen.blit(textb_adv, textb_adv_rect)
        pygame.display.flip()
        pygame.time.wait(200)
    
    if button_disadv.collidepoint(mouse_pos) and click:
        if dinero >= 100 and desventaja:
            pygame.draw.rect(screen, (20, 80, 80), button_disadv)
            desventaja = False
            dinero -= 100
        else:
            pygame.draw.rect(screen, (80, 20, 20), button_disadv)
        screen.blit(textb_disadv, textb_disadv_rect)
        pygame.display.flip()
        pygame.time.wait(200)
        
    return velocidad,aceleracion,ventaja,desventaja,dinero
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    now = pygame.time.get_ticks()
    
    # Calculate movement components based on angle
    radians = math.radians(angle*-1)
    dx = speed * math.sin(radians)
    dy = speed * math.cos(radians)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        speed += ACCELERATION
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        speed -= ACCELERATION
    if keys[pygame.K_r]:
        time_run = False
        speed = 0
        car.center = 400, 100
        lap_time = 0
        lap_start_time = now
        angle = -90
        check_crossed = 3
    if keys[pygame.K_SPACE]:
        speed = abs(speed-1)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        angle += 2 * (speed / 10)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        angle -= 2 * (speed / 10)
    if keys[pygame.K_t]: #TIENDA
        in_store = not in_store
        time_run = False
        speed = 0
        car.center = 400, 100
        lap_time = 0
        lap_start_time = now
        angle = -90
        check_crossed = 3
        pygame.time.wait(200)
    
    if speed < -3:
        speed = -3
    if speed > MAX_SPEED:
        speed = MAX_SPEED
    
    car.x += dx
    car.y -= dy

    if car.left < 0:
        car.left = 0
        speed = max(1, speed - 2)
    if car.right > width:
        car.right = width
        speed = max(1, speed - 2)
    if car.top < 0:
        car.top = 0
        speed = max(1, speed - 2)
    if car.bottom > height:
        car.bottom = height
        speed = max(1, speed - 2)

    if car.colliderect(inner_wallsRect):
        car.center = stored_cr
        speed = max(3, speed - 2)
    else:
        stored_cr = car.center
    
    if car.colliderect(meta) and check_crossed == 3:
        time_run = True
        check_crossed = 0
        lap_start_time = now
        if lap_time/1000 > 0.5:
            num_vueltas += 1
            best_laps = vueltas(lap_time,best_laps)
            dinero += 6000/lap_time
            dinero = round(dinero,2)
    
    if car.colliderect(checkpoints[0]) and check_crossed == 0:
        check_crossed = 1
    
    if car.colliderect(checkpoints[1]) and check_crossed == 1:
        check_crossed = 2
    
    if car.colliderect(checkpoints[2]):
        if check_crossed == 2:
            check_crossed = 3
        elif time_run == False:
            print("DIRECCIÓN CONTRARIA")
            speed = 0
            car.center = 400, 100
            angle = -90
    
    if desventaja and car.colliderect(900,100,desacelerador[2],desacelerador[3]) or car.colliderect(500,800,desacelerador[2],desacelerador[3]):
        speed *= 0.9
        
    if ventaja and car.colliderect(1350,300,desacelerador[2],desacelerador[3]) or car.colliderect(100,350,desacelerador[2],desacelerador[3]):
        speed *= 1.1
        
    if time_run:
        lap_time = now - lap_start_time
    
    rotated_car = pygame.transform.rotate(carImage, angle)
    rotated_rect = rotated_car.get_rect(center=car.center)
    
    screen.fill((43, 40, 46))
    
    # Dibujar el camino
    pygame.draw.lines(screen, (255, 255, 255), False, inner_walls, 5)
    
    for num,lap in enumerate(best_laps):
        text = font.render(f"LAP {num+1} --> {lap/1000:.2f}s", True, WHITE)
        screen.blit(text, (270,250+40*(num)))
    
    textmoney = font.render(f"MONEY -------------> {dinero:.2f} €", True, WHITE)
    texttime = font.render(f"LAP TIME ----------> {lap_time/1000:.2f}s", True, WHITE)
    if len(best_laps) > 0:
        textbl = font.render(f"BEST LAP ---------> {best_laps[0]/1000:.2f}s", True, WHITE)
        textal = font.render(f"BEST 10 LAPS ---> {sum(best_laps)/1000:.2f}s", True, WHITE)
        screen.blit(textbl, (700,350))
        screen.blit(textal, (700,400))
    
    #rozamiento
    speed *= 0.99
    
    if desventaja:
        screen.blit(rotated_decelerator, (900, 100))
        screen.blit(desaceleradorImage, (500, 800))
        
    if ventaja:
        screen.blit(rotated_acceleratorDown, (1350, 300))
        screen.blit(rotated_acceleratorUp, (100, 350))
    screen.blit(textmoney,(700,250))
    screen.blit(texttime,(700,300))
    screen.blit(rotated_car, rotated_rect)
    
    if in_store:
        MAX_SPEED,ACCELERATION,ventaja,desventaja,dinero = draw_store(MAX_SPEED,ACCELERATION,ventaja,desventaja,dinero)

    pygame.display.flip()

    clock.tick(60)