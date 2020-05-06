# This Python file uses the following encoding: utf-8
import pygame
import pygame.freetype
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
import random

pygame.init()
win = pygame.display.set_mode((800, 600))


BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

pygame.display.set_caption("Goblin Game")

walkRight = [pygame.image.load(os.path.join('img','R1.png')), pygame.image.load(os.path.join('img','R2.png')), pygame.image.load(os.path.join('img','R3.png')),pygame.image.load(os.path.join('img','R4.png')), pygame.image.load(os.path.join('img','R5.png'))
, pygame.image.load(os.path.join('img','R6.png')), pygame.image.load(os.path.join('img','R7.png')),pygame.image.load(os.path.join('img','R8.png')),pygame.image.load(os.path.join('img','R9.png'))]
walkLeft = [pygame.image.load(os.path.join('img','L1.png')), pygame.image.load(os.path.join('img','L2.png')), pygame.image.load(os.path.join('img','L3.png')),pygame.image.load(os.path.join('img','L4.png')), pygame.image.load(os.path.join('img','L5.png')),pygame.image.load(os.path.join('img','L6.png')), pygame.image.load(os.path.join('img','L7.png')), pygame.image.load(os.path.join('img','L8.png')), pygame.image.load(os.path.join('img','L9.png'))]
bg = pygame.image.load(os.path.join('img','bg.jpg'))
char = pygame.image.load(os.path.join('img','standing.png'))
goblin_bg = pygame.image.load(os.path.join('img','goblin.jpg'))



clock = pygame.time.Clock()

music = pygame.mixer.music.load(os.path.join('img','music.mp3'))
pygame.mixer.music.play(-1)



score = 0

bullets = []

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        global win
        self.isJump = False
        self.jumpCount = 10
        self.x = random.randint(10,450)
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 300)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (400 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 7 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        
        

class enemy(object):
    walkRight = [pygame.image.load(os.path.join('img','R1E.png')),pygame.image.load(os.path.join('img','R2E.png')), pygame.image.load(os.path.join('img','R3E.png')), pygame.image.load(os.path.join('img','R4E.png')), pygame.image.load(os.path.join('img','R5E.png')), pygame.image.load(os.path.join('img','R6E.png')),pygame.image.load(os.path.join('img','R7E.png')), pygame.image.load(os.path.join('img','R8E.png')), pygame.image.load(os.path.join('img','R9E.png')),pygame.image.load(os.path.join('img','R10E.png')), pygame.image.load(os.path.join('img','R11E.png'))]
    walkLeft = [pygame.image.load(os.path.join('img','L1E.png')),pygame.image.load(os.path.join('img','L2E.png')),pygame.image.load(os.path.join('img','L3E.png')), pygame.image.load(os.path.join('img','L4E.png')), pygame.image.load(os.path.join('img','L5E.png')), pygame.image.load(os.path.join('img','L6E.png')), pygame.image.load(os.path.join('img','L7E.png')),pygame.image.load(os.path.join('img','L8E.png')), pygame.image.load(os.path.join('img','L9E.png')),pygame.image.load(os.path.join('img','L10E.png')), pygame.image.load(os.path.join('img','L11E.png'))]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


def main():
    
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(win)

        if game_state == GameState.NEWGAME:
            game_state = play_level(win)

        if game_state == GameState.DASHBOARD:
            game_state = dashboard(win)

        if game_state == GameState.NAMEBLANK:
            game_state = nameblank(win)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

def redrawGameWindow():
    global win, score, bullets
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (650, 10))
    man.draw(win)
    goblin.draw(win)
    goblin2.draw(win)
    goblin3.draw(win)
    goblin4.draw(win)
         
    for bullet in bullets:
        
        bullet.draw(win)
    
    pygame.display.flip()

text_dashboard = ''

def dashboard(win):
    global text_dashboard

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=(0,128,0),
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        win.fill((0,128,0))
        
        high_score = get_high_score()

        current_score = score

        text_1 = font.render('Best Score: ' + str(high_score), 1, RED)
        win.blit(text_1, (400 - (text_1.get_width()/2),200))

        text_2 = font.render(str(text_dashboard)+"'s Score: "+ str(score), 1, (0,0,0))
        win.blit(text_2, (400 - (text_2.get_width()/2),300))

        if current_score > high_score:
            save_high_score(current_score)
        else:
            pass

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(win)

        pygame.display.flip()



def nameblank(win):
    global clock, text_dashboard

    return_btn = UIElement(
        center_position=(400, 350),
        font_size=20,
        bg_rgb=(0,128,0),
        text_rgb=WHITE,
        text="Confirm",
        action=GameState.DASHBOARD,
    )
    
    gogo = True
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(300, 280, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = (255,255,255)
    color = color_inactive
    active = False
    done = False

    while not done:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text_dashboard)   
                        
                    elif event.key == pygame.K_BACKSPACE:
                        text_dashboard = text_dashboard[:-1]
                    else:
                        text_dashboard += event.unicode

        win.fill((0,128,0))
        
        font1 = pygame.font.SysFont('comicsans', 50)
        text_1 = font1.render(' Type your name.', 1, WHITE)
        win.blit(text_1, (400 - (text_1.get_width()/2),200))
            
        # Render the current text.
        txt_surface = font.render(text_dashboard, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(win, color, input_box, 2)

        
        clock.tick(30)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(win)
        

        pygame.display.flip()


def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try: 
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")         
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
 
    return high_score

def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")

def button_1(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action(win)         
    else:
        pygame.draw.rect(win, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def title_screen(win):
    global button_1
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]


    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        win.blit(goblin_bg, (0,0))
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('GOBLIN GAME', 1, (255,0,0))
        win.blit(text, (400 - (text.get_width()/2),200))

        button_1("How?",150,450,100,50,GREEN,RED,play_level)
        

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(win)

        pygame.display.flip()

font = pygame.font.SysFont('comicsans', 30, True)
man = player(random.randint(10,450), 410, 64,64)
goblin = enemy(10, 410, 64, 64, 750)
goblin2 = enemy(random.randint(10,400), 410, 64, 64, 750)
goblin3 = enemy(random.randint(300,700), 410, 64, 64, 750)
goblin4 = enemy(random.randint(10,500), 410, 64, 64, 750)


def play_level(win):
    global font, man, goblin, goblin2, goblin3, goblin4, bullets, score ,gogo
    
    shootLoop = 0
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=(0,128,0),
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    return_btn1 = UIElement(
        center_position=(600, 570),
        font_size=50,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="SCORE BOARD",
        action=GameState.NAMEBLANK,
    )
    print("hello")
    goblin.visible = True
    goblin2.visible = True
    goblin3.visible = True
    goblin4.visible = True
    goblin = enemy(10, 410, 64, 64, 750)
    goblin2 = enemy(random.randint(10,400), 410, 64, 64, 750)
    goblin3 = enemy(random.randint(300,700), 410, 64, 64, 750)
    goblin4 = enemy(random.randint(10,500), 410, 64, 64, 750)
    score = 0
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        win.fill((0,128,0))

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(win)

        clock.tick(27)

        if goblin.visible == True:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    man.hit()
                    score -= 5

        if goblin2.visible == True:
            if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                    man.hit()
                    score -= 5

        if goblin3.visible == True:
            if man.hitbox[1] < goblin3.hitbox[1] + goblin3.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin3.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin3.hitbox[0] and man.hitbox[0] < goblin3.hitbox[0] + goblin3.hitbox[2]:
                    man.hit()
                    score -= 5

        if goblin4.visible == True:
            if man.hitbox[1] < goblin4.hitbox[1] + goblin4.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin4.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin4.hitbox[0] and man.hitbox[0] < goblin4.hitbox[0] + goblin4.hitbox[2]:
                    man.hit()
                    score -= 5

        if goblin.visible == False and goblin2.visible == False and goblin3.visible == False and goblin4.visible == False:
            ui_action1 = return_btn1.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action1 is not None:
                return ui_action1
            return_btn1.draw(win)
            

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
            
        for bullet in bullets:
            if goblin.visible == True:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                        
                        goblin.hit()

                        score += 1
                        bullets.pop(bullets.index(bullet))

            if goblin2.visible == True:
                if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
                    if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                        
                        goblin2.hit()

                        score += 1
                        bullets.pop(bullets.index(bullet))

            if goblin3.visible == True:
                if bullet.y - bullet.radius < goblin3.hitbox[1] + goblin3.hitbox[3] and bullet.y + bullet.radius > goblin3.hitbox[1]:
                    if bullet.x + bullet.radius > goblin3.hitbox[0] and bullet.x - bullet.radius < goblin3.hitbox[0] + goblin3.hitbox[2]:
                        
                        goblin3.hit()

                        score += 1
                        bullets.pop(bullets.index(bullet))

            if goblin4.visible == True:
                if bullet.y - bullet.radius < goblin4.hitbox[1] + goblin4.hitbox[3] and bullet.y + bullet.radius > goblin4.hitbox[1]:
                    if bullet.x + bullet.radius > goblin4.hitbox[0] and bullet.x - bullet.radius < goblin4.hitbox[0] + goblin4.hitbox[2]:
                        
                        goblin4.hit()

                        score += 1
                        bullets.pop(bullets.index(bullet))

            
                    
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop == 0:
                
            if man.left:
                facing = -1
            else:
                facing = 1
                    
            if len(bullets) < 2:
                bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 10, (0,0,0), facing))

            shootLoop = 1
        
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
                
        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
        else: 
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
                    
        redrawGameWindow()

            
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    DASHBOARD = 2
    NAMEBLANK = 3


if __name__ == "__main__":
    main()


