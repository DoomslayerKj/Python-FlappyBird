import pygame,sys,os,random,time

pygame.init()
pygame.mixer.pre_init(frequency=44100,size= 16, channels=2,buffer=320)

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos+576,900))

def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop  = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom  = (700,random_pipe_pos - 290))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe= pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False


        if bird_rect.top<= - 100 or bird_rect.bottom >= 900:
            return False

    return True

def rotate_bird(bird):    #can scale and rotate
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird= bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)   ),True,(255,255,255))
        score_rect = score_surface.get_rect(center=(288,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)
        
def update_score(score,high_score):
    if score > high_score:
        high_score=score
    return high_score


#screen , base canvas               x and y
screen = pygame.display.set_mode((576,1024) )
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("FlappyBirdy.ttf",80)

high_file =  open("high.txt","w+") 

#Game Variables
gravity = 0.32
bird_movement = 0
game_active= True
score = 0
high_score = 0

bg_surface = pygame.image.load('Assets/sprites/background-day.png').convert() #converts img to easy processing
bg_surface=pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('Assets/sprites/base.png').convert()
print(floor_surface)
floor_surface=pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#Animating The Bird(importing assets)
bird_downflap = pygame.transform.scale2x(pygame.image.load('Assets/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Assets/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100,512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

# bird_surface=pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100,512))

#Pipes Data , Assests Import Of Pipes
pipe_surface = pygame.image.load('Assets/sprites/pipe-green.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE =pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('Assets/sprites/message.png').convert_alpha())
game_over_surface_rect=game_over_surface.get_rect(center = (288,512))

#SOUNDS
flap_sound = pygame.mixer.Sound('Assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('Assets/audio/hit.wav')
score_sound=pygame.mixer.Sound('Assets/audio/point.wav')
score_sound_countdown = 100

  


while True:
    for event in pygame.event.get():  #checks for all events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if (event.key == pygame.K_SPACE ) and game_active == True:
                bird_movement=0
                bird_movement-=12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()            #when game over
                bird_rect.center=(100,512)
                bird_movement=0
                score = 0
                pygame.time.delay(3)

                #TESTINGmouse functonality
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.type==  pygame.MOUSEBUTTONDOWN) and game_active == True:
                bird_movement=0
                bird_movement-=12
                flap_sound.play()

            if event.type==  pygame.MOUSEBUTTONDOWN and game_active == False:
                game_active = True
                pipe_list.clear()            #when game over
                bird_rect.center=(100,512)
                bird_movement=0
                score = 0
                pygame.time.delay(3)




        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type ==BIRDFLAP:
            if bird_index >=2:
                bird_index=0
            else:
                bird_index+=1

            bird_surface,bird_rect=bird_animation()


    #go up = decrease Y, X is same
    screen.blit(bg_surface,(0,0))


    if game_active == True:
        #Bird
        bird_movement += gravity * (1.45)
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active=check_collision(pipe_list)

        #Pipe
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #Displaying Score
        score += 0.01

        score_display('main_game')
        score_sound_countdown -=1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown=100
    else:
        score_display('game_over')
        high_score = update_score(score, high_score)
        screen.blit(game_over_surface,game_over_surface_rect)

    #Floor
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos <=-576:
        floor_x_pos=0



        
    pygame.display.update()
    clock.tick(90)