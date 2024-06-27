import random
import pygame
import pygame.mixer

pygame.init()

scr_info = pygame.display.Info()
width = scr_info.current_w
height = scr_info.current_h

scr = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("ChickenRun")

white = (255, 255, 255)
back = (255, 255, 255)

global score, car_speed, neg_speed

score = 0

spawns_x_left = [465, 1050]
spawns_x_right = [750, 1350]
spawns_y_left = [-200]
spawns_y_right = [600]
car_speed = [4,5,6,7]
neg_speed = [-4,-5,-6,-7]


class GameSprite():
    def __init__(self, filename, x, y, speed, w, h):
        super().__init__()
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h

    def reset(self):
        scr.blit(self.image, (self.rect.x, self.rect.y))

    def hide(self):
        self.rect.x = -2000
        self.rect.y = -2000


class Hero(GameSprite):
    def __init__(self, filename, x, y, speed, w, h):
        GameSprite.__init__(self, filename, x, y, speed, w, h)
        self.counter = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x < (width - 70):
            if not self.check(self.rect.x + self.speed, self.rect.y):
                self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            if not self.check(self.rect.x - self.speed, self.rect.y):
                self.rect.x -= self.speed
        if keys[pygame.K_s] and self.rect.y < (height - 120):
            if not self.check(self.rect.x, self.rect.y + self.speed):
                self.rect.y += self.speed
        if keys[pygame.K_w] and self.rect.y > 0:
            if not self.check(self.rect.x, self.rect.y - self.speed):
                self.rect.y -= self.speed

    def check(self, x, y):
        tmp_area = pygame.Rect(x, y, self.w, self.h)
        touch = []
        for thing in touchable:
            touch.append(thing.rect.colliderect(tmp_area))
        return True in touch

    def animation1(self, kind):
            if self.counter > 48:
                self.counter = 0
            self.counter += 1
            if kind == 'go_right':
                if 0 <= self.counter < 24:
                    self.image = self.image = pygame.transform.scale(pygame.image.load('pictures/chicken_right.png'), (self.w, self.h))
                else:
                    self.image = self.image = pygame.transform.scale(pygame.image.load('pictures/chicken_idle.png'), (self.w, self.h))

    def animation2(self, kind):
        if self.counter > 48:
            self.counter = 0
        self.counter += 1
        if kind == 'go_right':
            if 0 <= self.counter < 24:
                self.image = pygame.transform.scale(pygame.image.load('pictures/chigga_right.png'), (self.w, self.h))
            else:
                self.image = pygame.transform.scale(pygame.image.load('pictures/chigga_idle.png'), (self.w, self.h))

    def animation3(self, kind):
            if self.counter > 48:
                self.counter = 0
            self.counter += 1
            if kind == 'go_right':
                if 0 <= self.counter < 24:
                    self.image = pygame.transform.scale(pygame.image.load('pictures/white_chicken_right.png'), (self.w, self.h))
                else:
                    self.image = pygame.transform.scale(pygame.image.load('pictures/white_chicken_idle.png'), (self.w, self.h))

    def animation4(self, kind):
            if self.counter > 48:
                self.counter = 0
            self.counter += 1
            if kind == 'go_right':
                if 0 <= self.counter < 24:
                    self.image = pygame.transform.scale(pygame.image.load('pictures/yellow_chicken_right.png'), (self.w, self.h))
                else:
                    self.image = pygame.transform.scale(pygame.image.load('pictures/yellow_chicken_idle.png'), (self.w, self.h))

    def reset_coor(self):
        self.rect.x = 75
        self.rect.y = (height / 2) - 38

class Cars(GameSprite):
    def __init__(self, filename, x, y, speed, w, h):
        GameSprite.__init__(self, filename, x, y, speed, w, h)
        self.initial_speed = speed

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > height or self.rect.y < -self.h + (-100):
            self.reset_position()

    def reset_position(self):
        while True:
            if self.initial_speed > 0: 
                self.rect.y = -self.h
            else:  
                self.rect.y = height
            self.rect.x = random.choice(spawns_x_left + spawns_x_right)
            if not self.check_collision():
                break

    def check_collision(self):
        for car in carss:
            if car != self and self.rect.colliderect(car.rect):
                return True
        return False

class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color


    def color(self, new_color):
        self.fill_color = new_color


    def fill(self):
        pygame.draw.rect(scr,self.fill_color,self.rect)

class Label(Area):
    def set_text(self, Text, fsize = 12, text_color = (0, 0, 0)):
        self.image = pygame.font.SysFont("bahnschrift", fsize).render(Text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        scr.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

carss = []
touchable = []

def new_level():
    global score
    chicken.reset_coor()
    for car in carss:
        car.reset_position()

    for car in carss:
        if car.initial_speed > 0:
            car.speed += 1
        else:
            car.speed -= 1
    score = score + 1


def create_car(filename, x, y, speed):
    new_car = Cars(filename, x, y, speed, 116, 192)
    while new_car.check_collision():
        new_car.reset_position()
    carss.append(new_car)

for i in range(2):
    create_car("pictures/car_down.png", random.choice(spawns_x_left), random.choice(spawns_y_left), random.choice(car_speed))
for i in range(2):
    create_car("pictures/car_up.png", random.choice(spawns_x_right), random.choice(spawns_y_right), random.choice(neg_speed))

time_text = Label((width / 2) - 175,(height / 2) - 200, 50 ,50 , back)
time_text.set_text("2x Монети", 60, (0, 0, 0))


chicken = Hero("pictures/chicken_idle.png", 75, (height / 2) - 38, 5, 72, 78)
finish = GameSprite("pictures/coin.png", width - 200, 425, 0, 80, 90)
bg_game = GameSprite("pictures/bg_game.png", 0, 0, 0, width, height)
bg_menu = GameSprite("pictures/bg_menu.png", 0, 0, 0, width, height)
play_button = GameSprite("pictures/Play_button.png", (width / 2) - 300, (height / 2) - 200, 0, 600, 250)
exit_button = GameSprite("pictures/exit_button.png", (width / 2) - 300, (height / 2) + 100, 0, 600, 250)
again_button = GameSprite("pictures/again_button.png", 505, 300, 0, 530, 200)# це тоже?(напевно)
shop_button = GameSprite("pictures/shop_button.png", 100, 5, 0, 240, 100) #Для логіки поділити на 2 останні 2 числа?(напевно)
buy_button = GameSprite("pictures/buy_button.png", (width / 2) - 120, (height - 100), 0, 240, 100)#Ну і це тоді тоже?
skin0 = GameSprite("pictures/chicken_idle.png", (width / 2) - 108, (height / 2) - 117, 0, 216, 234)
skin1 = GameSprite("pictures/chigga_idle.png", (width / 2) - 108, (height / 2) - 117, 0, 216, 234)
skin2 = GameSprite("pictures/white_chicken_idle.png", (width / 2) - 108, (height / 2) - 117, 0, 216, 234)
skin3 = GameSprite("pictures/yellow_chicken_idle.png", (width / 2) - 108, (height / 2) - 117, 0, 216, 234)
arrow_right = GameSprite("pictures/arrow_right.png", ((width / 2) + 150), ((height / 2) - 25), 0, 100, 100)
arrow_left = GameSprite("pictures/arrow_left.png", ((width / 2) - 250), ((height / 2) - 25), 0, 100, 100)
arrow_back = GameSprite("pictures/arrow_left.png", 100, 50, 0, 200, 200)

skins = [skin0, skin1, skin2, skin3]
skinnum = 0

screen = "menu"

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if screen == "menu":
        for car in carss:
            car.reset_position()
        bg_menu.reset()
        play_button.reset()
        exit_button.reset()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    mouserect = pygame.Rect(x, y, 1, 1)
                    if play_button.rect.colliderect(mouserect):
                        screen = "game"
                    if exit_button.rect.colliderect(mouserect):
                        game = False
    
    mouse_pos = pygame.mouse.get_pos()
    print(mouse_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        screen = "menu"
    if keys[pygame.K_d]:
        if skinnum == 1: 
            chicken.animation2("go_right")
        elif skinnum == 2:
            chicken.animation3("go_right")
        elif skinnum == 3:
            chicken.animation4("go_right")
        else:
            chicken.animation1("go_right")



    if screen == "game":
        bg_game.reset()
        chicken.reset()
        chicken.move()
        shop_button.reset()
        finish.reset()
        for car in carss:
            car.reset()
            car.move()
        if chicken.rect.colliderect(finish):
            new_level()
        for car in carss:
            if chicken.rect.colliderect(car.rect):
                screen = "fail"
            if car.rect.x == 465 and car.initial_speed < 0: #in neg_speed:
                car.reset_position()
            if car.rect.x == 1050 and car.initial_speed < 0: #in neg_speed:
                car.reset_position()
            if car.rect.x == 750 and car.initial_speed > 0: #in car_speed:
                car.reset_position()
            if car.rect.x == 1350 and car.speed > 0: #in car_speed:
                car.reset_position()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                mouserect = pygame.Rect(x, y, 1, 1)
                if shop_button.rect.colliderect(mouserect):
                    screen = "shop"



    if screen == "fail":
        chicken.reset_coor()
        bg_game.reset()
        again_button.reset()
        exit_button.reset()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    mouserect = pygame.Rect(x, y, 1, 1)
                    if again_button.rect.colliderect(mouserect):
                        screen = "game"
                    if exit_button.rect.colliderect(mouserect):
                        game = False



    if screen == "shop":
        scr.fill(white)
        chicken.reset_coor()
        skin0.reset()
        arrow_left.reset()
        arrow_right.reset()
        arrow_back.reset()
        if skinnum == 1 or skinnum == 2 or skinnum == 3:
            buy_button.reset()
            time_text.draw(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                mouserect = pygame.Rect(x, y, 1, 1)
                if arrow_right.rect.colliderect(mouserect):
                    skin0 = skins[skinnum + 1]
                    skinnum += 1
                    
                elif arrow_left.rect.colliderect(mouserect):
                    skin0 = skins[skinnum - 1]
                    skinnum -= 1
                
                elif arrow_back.rect.colliderect(mouserect):
                    screen = "game"

                if skinnum == 1 and score >= 2 and buy_button.rect.colliderect(mouserect):
                    buy_button.hide()
                    score -= 2
                    chicken = Hero("pictures/chigga_idle.png", 50, 50, 5, 72, 78)
                if skinnum == 2 and score >= 2 and buy_button.rect.colliderect(mouserect)  :
                    buy_button.hide()
                    score -= 2
                    chicken = Hero("pictures/white_chicken_idle.png", 50, 50, 5, 72, 78)
                if skinnum == 3 and score >= 2 and buy_button.rect.colliderect(mouserect)  :
                    buy_button.hide()
                    score -= 2
                    chicken = Hero("pictures/yellow_chicken_idle.png", 50, 50, 5, 72, 78)
                    


    clock.tick(60)
    pygame.display.update()

pygame.quit()