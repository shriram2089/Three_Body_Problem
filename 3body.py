import pygame
import math

pygame.init()
dt=0.01

def gravitational_force(m1, m2, r):
    G = 6.674e-11
    if r==0: return 0
    return  (G * m1 * m2) / (r**2)

def collide(m1,m2,v1,v2):
    v_new=(m1*v1+m2*v2)/(m1+m2)
    
    
def force_direction(x1, y1, x2, y2, force_magnitude):
    
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    if distance==0:
      collide()
      return 0
     
    force_x = force_magnitude * (x2 - x1) / distance
    force_y = force_magnitude * (y2 - y1) / distance
    return force_x, force_y
def com(x1, x2, x3, y1, y2, y3, m1, m2, m3):
    x_com = (x1*m1 + x2*m2 + x3*m3) / (m1 + m2 + m3)
    y_com = (y1*m1 + y2*m2 + y3*m3) / (m1 + m2 + m3)
    return x_com, y_com

def v_com(vx1,vx2,vx3,vy1,vy2,vy3,m1,m2,m3):
    v_x= (vx1*m1 + vx2*m2 + vx3*m3) / (m1 + m2 + m3)
    v_y= (vy1*m1 + vy2*m2 + vy3*m3) / (m1 + m2 + m3)
    return v_x,v_y

def potential(x1,x2,x3,y1,y2,y3,m1,m2,m3):
    G = 6.674e-11
    p1=G*m1*m2/math.sqrt((x2-x1)**2 + (y2-y1)**2)
    p2=G*m3*m2/math.sqrt((x2-x3)**2 + (y2-y3)**2)
    p3=G*m3*m1/math.sqrt((x3-x1)**2 + (y3-y1)**2)
    return p1+p2+p3
WIDTH, HEIGHT = 800, 600

DOT1_RADIUS = 5
MASS1 = 1e12
DOT2_RADIUS = 3
MASS2 = 1e9
DOT3_RADIUS = 4
MASS3 = 1e9
COM_RADIUS = 1

speed_x1, speed_y1 = 0, 0
speed_x2, speed_y2 = 0, 1
speed_x3, speed_y3 = 0, 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triple Body Gravitational Movement")
pygame.font.init()
font = pygame.font.SysFont(None, 36)

x1, y1 = WIDTH//2 , HEIGHT//2 + 60
x2, y2 = WIDTH//2 - 40, HEIGHT//2
x3, y3 = WIDTH//2 + 30, HEIGHT//2

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))


    #initial com
    x_com,y_com = com(x1,x2,x3,y1,y2,y3,MASS1,MASS2,MASS3)
    com_text_str = f"CoM: ({x_com:.2f}, {y_com:.2f})"
    com_text_surface = font.render(com_text_str, True, (255, 255, 255))  


    # Compute the forces based on current positions
    f12 = gravitational_force(MASS1, MASS2, math.sqrt((x2-x1)**2 + (y2-y1)**2))
    f23 = gravitational_force(MASS2, MASS3, math.sqrt((x3-x2)**2 + (y3-y2)**2))
    f31 = gravitational_force(MASS1, MASS3, math.sqrt((x1-x3)**2 + (y1-y3)**2))

    fx12, fy12 = force_direction(x1, y1, x2, y2, f12)
    fx23, fy23 = force_direction(x2, y2, x3, y3, f23)
    fx31, fy31 = force_direction(x3, y3, x1, y1, f31)

    speed_x1 += 0.5 * (fx12 - fx31) / MASS1 * dt
    speed_y1 += 0.5 * (fy12 - fy31) / MASS1 * dt
    speed_x2 += 0.5 * (-fx12 + fx23) / MASS2 * dt
    speed_y2 += 0.5 * (-fy12 + fy23) / MASS2 * dt
    speed_x3 += 0.5 * (-fx23 + fx31) / MASS3 * dt
    speed_y3 += 0.5 * (-fy23 + fy31) / MASS3 * dt

    # Update positions using half-updated velocities
    x1 += speed_x1 * dt
    y1 += speed_y1 * dt
    x2 += speed_x2 * dt
    y2 += speed_y2 * dt
    x3 += speed_x3 * dt
    y3 += speed_y3 * dt

    # Compute new forces based on updated positions
    f12 = gravitational_force(MASS1, MASS2, math.sqrt((x2-x1)**2 + (y2-y1)**2))
    f23 = gravitational_force(MASS2, MASS3, math.sqrt((x3-x2)**2 + (y3-y2)**2))
    f31 = gravitational_force(MASS1, MASS3, math.sqrt((x1-x3)**2 + (y1-y3)**2))

    fx12, fy12 = force_direction(x1, y1, x2, y2, f12)
    fx23, fy23 = force_direction(x2, y2, x3, y3, f23)
    fx31, fy31 = force_direction(x3, y3, x1, y1, f31)

    # Finish updating velocities with new forces
    speed_x1 += 0.5 * (fx12 - fx31) / MASS1 * dt
    speed_y1 += 0.5 * (fy12 - fy31) / MASS1 * dt
    speed_x2 += 0.5 * (-fx12 + fx23) / MASS2 * dt
    speed_y2 += 0.5 * (-fy12 + fy23) / MASS2 * dt
    speed_x3 += 0.5 * (-fx23 + fx31) / MASS3 * dt
    speed_y3 += 0.5 * (-fy23 + fy31) / MASS3 * dt


    # Remaining code for rendering and displaying remains unchanged

    speed1 = math.sqrt(speed_x1**2 + speed_y1**2)
    speed2 = math.sqrt(speed_x2**2 + speed_y2**2)
    speed3 = math.sqrt(speed_x3**2 + speed_y3**2)

    # Render the speeds to surfaces
    speed_text1 = font.render(f"Speed 1: {speed1:.2f}", True, (255, 255, 255))
    speed_text2 = font.render(f"Speed 2: {speed2:.2f}", True, (255, 255, 255))
    speed_text3 = font.render(f"Speed 3: {speed3:.2f}", True, (255, 255, 255))

    v_x,v_y=v_com(speed_x1,speed_x2,speed_x3,speed_y1,speed_y2,speed_y3,MASS1,MASS2,MASS3)
    energy=0.5*(MASS1+MASS2+MASS3)*(v_x**2 + v_y**2)
    energy2 = ((0.5*MASS1*speed1**2)+(0.5*MASS2*speed2**2)+(0.5*MASS3*speed3**2)) - potential(x1,x2,x3,y1,y2,y3,MASS1,MASS2,MASS3)
    vcom_text_str = f"CoM energy: {energy:.20f}"
    vcom_text_str2 = f"Total energy: {energy2:.20f}"
    vcom_text_surface2 = font.render(vcom_text_str2, True, (255, 255, 255))
    vcom_text_surface = font.render(vcom_text_str, True, (255, 255, 255))


    # Display the speeds on the screen
    screen.blit(speed_text1, (10, 10))
    screen.blit(speed_text2, (10, 50))
    screen.blit(speed_text3, (10, 90))
    #screen.blit(vcom_text_surface, (10, 500))
    screen.blit(vcom_text_surface2, (10, 400))
    screen.blit(com_text_surface, (WIDTH - com_text_surface.get_width() - 10, 130))
    pygame.draw.circle(screen, (0, 255, 0), (int(x1), int(y1)), DOT1_RADIUS)
    pygame.draw.circle(screen, (0, 0, 255), (int(x2), int(y2)), DOT2_RADIUS)
    pygame.draw.circle(screen, (255, 0, 0), (int(x3), int(y3)), DOT3_RADIUS)
    pygame.display.flip()
    clock.tick(1000000000)

pygame.quit()