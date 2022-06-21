#!/usr/bin/env python
import pygame
import sys
import random

speed = 10
ball_number = 5
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
fps = 60
exp_time = 120

class Ball(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, type, location):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.random_pos = random.randint(0, screen_height)
        self.status = 0
        if type == 0:
            self.image = pygame.image.load("Image/circle_gray.png")
            self.image = pygame.transform.scale(self.image, (86, 86))
        elif type == 1:
            self.image = pygame.image.load("Image/circle_green.png")
            self.speed_x = 0
            self.speed_y = 8
            self.image = pygame.transform.scale(self.image, (74, 74))
        elif type == 2:
            self.image = pygame.image.load("Image/circle_pink.png")
            self.speed_x = 0
            self.speed_y = 8
            self.image = pygame.transform.scale(self.image, (74, 74))
        elif type == 3:  
            self.image = pygame.image.load("Image/circle_orange.png")  
            self.speed_x = 0
            self.speed_y = 8
            self.image = pygame.transform.scale(self.image, (74, 74))
        # 加载图片并且缩小
        self.rect = self.image.get_rect()
        # 获取图片rect区域
        self.rect.topleft = location
        # 设置位置

def ready(word):
    my_font = pygame.font.SysFont('arial', 80)
    text = my_font.render(word, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect = text.get_rect()
    # 设置显示对象居中
    textRect.center = (screen_width/2, 200)
    screen.blit(text, textRect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                f.close()
                pygame.quit()
                sys.exit()

def control_ball_bar():
    global speed
    global step
    key_pressed_is = pygame.key.get_pressed()
    if key_pressed_is[pygame.K_LEFT] & (player_ball.rect.left > 0):
        player_ball.rect.left -= speed
    if key_pressed_is[pygame.K_RIGHT] & (player_ball.rect.right < screen_width):
        player_ball.rect.left += speed
    if key_pressed_is[pygame.K_UP] & (abs(speed) < 5):
        speed = (speed > 0) * (abs(speed) + 1)
    if key_pressed_is[pygame.K_DOWN] & (abs(speed) > 1):
        speed = (speed > 0) * (abs(speed) - 1)
    if key_pressed_is[pygame.K_SPACE]:
        step -= 5

def draw_balls():
    global score
    global step
    for ball in group_ball:
        if (ball.status == 0) and (ball.rect.top > ball.random_pos):   
            if ball.type == 1:
                ball.speed_x = 0
                ball.speed_y = 8
            elif (ball.type == 2) and (random.randint(0, 9) < 4):
                ball.speed_x = 4 * random.randrange(-1,2,2)
                ball.speed_y = 7
            elif (ball.type == 3) and (random.randint(0, 9) < 9):  
                ball.speed_x = 4 * random.randrange(-1,2,2)
                ball.speed_y = 7
            ball.status = 1
        ball.rect.left += ball.speed_x
        ball.rect.top += ball.speed_y
        if ball.rect.left < 0 or ball.rect.right > screen_width:
            ball.speed_x = - ball.speed_x
        if ball.rect.top < 0 or (ball.rect.bottom > screen_height-30):
            score += 1
            group_ball.remove(ball)
            group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
        # 下落小球 碰撞边界变向
        crash_result = pygame.sprite.collide_mask(player_ball, ball)
        if crash_result:
            print("score:%d" % score)
            show_score()
            group_ball.empty()
            score = 0
            step = 0
            ball_number = 5
            ready("Crash!!Press enter to restart or esc to quit")
            for i in range(ball_number):
                group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
        # 碰撞检测

def init():
    global player_ball
    global group_ball
    global clock
    global add_ball
    global get_score
    global game_end
    global score
    global step
    global f
    pygame.init()
    # 初始化pygame
    pygame.mouse.set_visible(False)
    # shu biao bu ke jian
    score = 0
    step = 0
    fileName = 'data.txt'
    f = open(fileName,'w')
    screen.fill((156, 156, 156))
    # 填充屏幕颜色
    pygame.display.set_caption('Jeu de boule')
    # 设置窗口标题
    location = (screen_width / 2, screen_height * 0.8)
    player_ball = Ball(0, location)
    # 创建玩家的球
    group_ball = pygame.sprite.Group()
    # 向组内添加一个精灵
    for i in range(ball_number):
        group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
    # 创建下落的球组
    clock = pygame.time.Clock()
    # create clock
    add_ball = pygame.USEREVENT + 1
    pygame.time.set_timer(add_ball,5 * 1000)
    # add balls while time pass
    get_score = pygame.USEREVENT + 2
    pygame.time.set_timer(get_score,300)
    # get score while maintain bar in 0.7-0.9
    game_end = pygame.USEREVENT + 3
    pygame.time.set_timer(game_end,exp_time * 1000)

def show_score():
    my_font = pygame.font.SysFont('arial', 50)
    dy = f"score:{score}"
    text = my_font.render(dy, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect = text.get_rect()
    # 设置显示对象居中
    textRect.center = (300, 800)
    screen.blit(text, textRect)
    # 得分显示

def flash():
    screen.fill((156, 156, 156))
    draw_balls()
    draw_bar()
    screen.blit(player_ball.image, player_ball.rect)
    for ball in group_ball:
        screen.blit(ball.image, ball.rect)
        f.write("position(%d,%d)\n"%(ball.rect.left,ball.rect.top))
    f.write("0,0,0,0,0\n")
    show_score()
    pygame.display.flip()
    # 刷新界面显示

def draw_bar():
    global step
    global score
    pygame.draw.rect(screen,(192,192,192),(0,screen_height-30,screen_width,30))
    pygame.draw.rect(screen,(0,0,255),(screen_width*0.5, screen_height-30, step, 30))
    pygame.draw.rect(screen,(0,0,255),(screen_width*0.5-step, screen_height-30, step, 30))
    pygame.draw.rect(screen,(0,0,0),(screen_width*0.7,screen_height-30,5,30))
    pygame.draw.rect(screen,(0,0,0),(screen_width*0.9,screen_height-30,5,30))
    pygame.draw.rect(screen,(0,0,0),(screen_width*0.1,screen_height-30,5,30))
    pygame.draw.rect(screen,(0,0,0),(screen_width*0.3,screen_height-30,5,30))
    if (step < screen_width*0.5):
        step += 1
    # bar
    # full_result = (step == screen_width*0.5)
    # if full_result:
    #     screen.fill((156, 156, 156))
    #     print("score:%d" % score)
    #     show_score()
    #     group_ball.empty()
    #     score = 0
    #     step = 0
    #     ball_number = 5
    #     ready("Full!!Press enter to restart or esc to quit")
    #     for i in range(ball_number):
    #         group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
    # test bar 

if __name__ == '__main__':   
    init()
    ready("Are You Ready? Press enter to begin")
    # ready function
    while True:
        clock.tick(fps)
        # 游戏主循环
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f.close()
                pygame.quit()
                sys.exit()
            if (event.type == add_ball) and (ball_number <= 8):
                ball_number += 1
                group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
            # add balls while time pass
            if event.type == get_score:
                if (step > screen_width*0.2)and (step < screen_width*0.4):
                    score += 1
                # add score while time pass and bar is in 0.7-0.9
            if event.type == game_end:
                print("score:%d" % score)
                show_score()
                group_ball.empty()
                score = 0
                step = 0
                ball_number = 5
                ready("Time's up! Press enter to restart")
                for i in range(ball_number):
                    group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
        control_ball_bar()
        # 移动玩家小球
        flash()
        # flash
