import pgzrun, sys
from pgzero.builtins import Actor, keyboard, Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Jogo de plataforma"
GRAVITY = 1
JUMP_STRENGHT = -20
GROUND_LEVEL = HEIGHT - 50
game_mode = "menu"
start_game = Rect(300, 250, 200, 80) #Botão inicial
menu_button = Rect(600, 50, 100, 50) #Volta para o início
exit_game = Rect(350, 400, 100, 40) #Sair do jogo
music_button = Rect(200, 50, 100, 50) #Botão de habilitar/desabilitar os sons

plataforms = [
    Rect(50, 50, 150, 450),
    Rect(50, 300, 350, 200),
    Rect(50, 400, 500, 100),
]

musica_liberada = True
music.play("musica_fase")

class Player(Actor):
    def __init__(self):
        super().__init__('idle_right_1', pos = (100, GROUND_LEVEL))
        self.vx = 0
        self.vy = 0
        self.is_jumping = False
        self.facing_right = True
        self.anim_timer = 0
        self.frame_index = 1
        self.state = "idle" #pode ser "idle", "jump", "run
    
    def update(self):
        if keyboard.left:
            self.vx = -4
            self.facing_right = False
            self.state = "run"
        elif keyboard.right:
            self.vx = 4
            self.facing_right = True
            self.state = "run"
        else:
            self.vx = 0
            self.state = "idle"
        
        if keyboard.up and not self.is_jumping:
            self.vy = JUMP_STRENGHT
            self.is_jumping = True
            self.state = "jump"
            if musica_liberada: sounds.pulo.play()
        
        self.vy += GRAVITY

        self.x += self.vx
        for plat in plataforms:
            if self.colliderect(plat):
                if self.vx > 0:
                    self.right = plat.left
                else:
                    self.left = plat.right
                self.vx = 0

        self.y += self.vy
        for plat in plataforms:
            if self.colliderect(plat):
                if self.vy > 0:
                    self.bottom = plat.top
                    self.is_jumping = False
                else:
                    self.top = plat.bottom
                self.vy = 0
        if self.bottom >= GROUND_LEVEL:
            self.bottom = GROUND_LEVEL
            self.vy = 0
            self.is_jumping = False

        self.animate()

    def animate(self):
        if self.is_jumping:
            prefix = "jump_right" if self.facing_right else "jump_left"
            max_frames = 4
            speed = 10
        elif self.state == "run":
            prefix = "run_right_8_frames" if self.facing_right else "run_left_8_frames"
            max_frames = 8
            speed = 10
        else:
            prefix = "idle_right" if self.facing_right else "idle_left"
            max_frames = 4
            speed = 10
        
        self.anim_timer += 1
        if self.anim_timer >= speed:
            self.anim_timer = 0
            self.frame_index += 1
            if self.frame_index > max_frames:
                self.frame_index = 1
            self.image = f"{prefix}_{self.frame_index}"

class Snake(Actor):
    def __init__(self, ciclo, pos):
        super().__init__('cobra_right_1', pos = pos)
        self.vx = 2
        self.facing_right = True
        self.anim_timer = 0
        self.frame_index = 1
        self.ciclo = ciclo
        self.ini_pos = pos[0] - ciclo // 2
        self.end_pos = pos[0] + ciclo // 2
    
    def update(self):
        if self.pos[0] > self.end_pos:
            self.vx = -2
            self.facing_right = False
        if self.pos[0] < self.ini_pos:
            self.vx = 2
            self.facing_right = True
        self.x += self.vx
        for plat in plataforms:
            if self.colliderect(plat):
                if self.vx > 0:
                    self.right = plat.left
                else:
                    self.left = plat.right
                self.vx *= (-1)
        self.animate()
    
    def animate(self):
        prefix = "cobra_right" if self.facing_right else "cobra_left"
        max_frames = 3
        speed = 10
        self.anim_timer += 1
        if self.anim_timer >= speed:
            self.anim_timer = 0
            self.frame_index += 1
            if self.frame_index > max_frames:
                self.frame_index = 1
            self.image = f"{prefix}_{self.frame_index}"

hero = Player()
cobra1 = Snake(200, (700, 530))
cobra2 = Snake(20, (440, 380))

def update():
    global game_mode
    if game_mode == "game":
        hero.update()
        cobra1.update()
        cobra2.update()
        if hero.colliderect(cobra1) or hero.colliderect(cobra2):
            game_mode = "menu"
            hero.pos = (100, GROUND_LEVEL)
            cobra1.pos = (700, 530)


def draw():
    if game_mode == "game":
        screen.clear()
        screen.fill((50, 50, 50))
        screen.draw.filled_rect(Rect((0, GROUND_LEVEL + 30), (WIDTH, 50)), (20, 20, 20))
        for plat in plataforms: screen.draw.filled_rect(plat, (100, 200, 100))
        hero.draw()
        cobra1.draw()
        cobra2.draw()
        screen.draw.filled_rect(menu_button, "green")
        screen.draw.text("Voltar", center = menu_button.center, fontsize = 25, color = "white")
    if game_mode == "menu":
        screen.clear()
        screen.fill((50, 50, 50))
        screen.draw.text("Jogo de Plataforma", center = (400, 150), fontsize = 80, color = "yellow")
        screen.draw.filled_rect(start_game, "green")
        screen.draw.text("Jogar", center = start_game.center, fontsize = 40, color = "white")
        screen.draw.filled_rect(exit_game, "green")
        screen.draw.text("Sair", center = exit_game.center, fontsize = 20, color = "white")
        screen.draw.filled_rect(music_button, "green")
        screen.draw.text("Som", center = music_button.center, fontsize = 25, color = "white")
        
def on_mouse_down(pos):
    global game_mode, musica_liberada
    if game_mode == "menu" and start_game.collidepoint(pos): game_mode = "game"
    if game_mode == "game" and menu_button.collidepoint(pos): game_mode = "menu"
    if game_mode == "menu" and exit_game.collidepoint(pos): sys.exit()
    if game_mode == "menu" and music_button.collidepoint(pos):
        musica_liberada = not musica_liberada
        if musica_liberada:
            music.play("musica_fase")
        else:
            music.stop()

pgzrun.go()