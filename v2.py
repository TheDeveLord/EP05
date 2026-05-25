import tkinter as tk
from random import randint

class Platformer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2D платформер")
        self.window.resizable(False, False)
        
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg='lightblue')
        self.canvas.pack()
        
        self.player_size = 30
        self.player_x = 100
        self.player_y = 300
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.player_speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False
        self.game_over = False

        self.collectibles = []
        for _ in range(10):
            x = randint(50, 750)
            y = randint(50, 500)
            self.collectibles.append({'x': x, 'y': y, 'collected': False})
        self.score = 0
        
        self.platforms = [
            (0, 550, 800, 30),
            (200, 450, 200, 20),
            (500, 350, 200, 20),
            (400, 250, 50, 20),
            (700, 200, 50, 20),
            (100, 250, 200, 20),
        ]
        
        self.keys_pressed = {}
        self.window.bind('<KeyPress>', self.key_press)
        self.window.bind('<KeyRelease>', self.key_release)
        self.window.focus_set()
        
        self.game_loop()
    
    def key_press(self, event):
        self.keys_pressed[event.keysym] = True
    
    def key_release(self, event):
        if event.keysym in self.keys_pressed:
            self.keys_pressed[event.keysym] = False
    
    def handle_input(self):
        if self.game_over == False:
            self.player_vel_x = 0
            if self.keys_pressed.get('Left', False):
                self.player_vel_x = -self.player_speed
            if self.keys_pressed.get('Right', False):
                self.player_vel_x = self.player_speed
        
            if (self.keys_pressed.get('Up', False) or self.keys_pressed.get('space', False)) and self.on_ground:
                self.player_vel_y -= self.jump_power
                self.on_ground = False

        if self.game_over and (self.keys_pressed.get('R', False) or self.keys_pressed.get('r', False)):
            self.reset_game()
    
    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def check_platform_collision(self):
        self.on_ground = False
        
        for px, py, pw, ph in self.platforms:
            if (self.player_vel_y > 0 and
                self.player_y + self.player_size <= py + self.player_vel_y and
                self.player_y + self.player_size + self.player_vel_y >= py and
                self.player_x + self.player_size > px and
                self.player_x < px + pw):
                
                self.player_y = py - self.player_size
                self.player_vel_y = -1
                self.on_ground = True
                break
            
            if (self.player_vel_y < 0 and
                self.player_y >= py + ph + self.player_vel_y and
                self.player_y + self.player_vel_y <= py + ph and
                self.player_x + self.player_size > px and
                self.player_x < px + pw):
                
                self.player_y = py + ph
                self.player_vel_y = 0
                break
            
            if self.check_collision(
                self.player_x + self.player_vel_x, self.player_y,
                self.player_size, self.player_size,
                px, py, pw, ph
            ):
                self.player_vel_x = 0
    
    def update_player(self):
        if not self.on_ground:
            self.player_vel_y += self.gravity
        
        self.player_x += self.player_vel_x
        self.player_y += self.player_vel_y
        
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > self.width - self.player_size:
            self.player_x = self.width - self.player_size
        
        if self.player_y > self.height:
            self.player_x = 100
            self.player_y = 300
            self.player_vel_y = 0

    def update_collectibles(self):
        for item in self.collectibles:
            if not item['collected']:
                if self.check_collision(
                    self.player_x, self.player_y,
                    self.player_size, self.player_size,
                    item['x'], item['y'], 20, 20
                ):
                    item['collected'] = True
                    self.score += 10
                    if self.score >= 100: self.game_over = True
    
    def draw(self):
        self.canvas.delete('all')
        
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='lightblue', outline='')
        
        for px, py, pw, ph in self.platforms:
            self.canvas.create_rectangle(px, py, px+pw, py+ph, fill='green', outline='black', width=2)
        
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + self.player_size,
            self.player_y + self.player_size,
            fill='blue', outline='darkblue', width=2
        )
        
        for px, py, pw, ph in self.platforms:
            self.canvas.create_rectangle(px, py, px+pw, py+ph, fill='green', outline='black', width=2)

        self.canvas.coords(
            self.player,
            self.player_x, self.player_y,
            self.player_x + self.player_size,
            self.player_y + self.player_size
        )
        for item in self.collectibles:
            if not item['collected']:
                self.canvas.create_oval(
                    item['x'], item['y'],
                    item['x'] + 20, item['y'] + 20,
                    fill='gold', outline='orange', width=2
                )
        
        self.canvas.create_text(70, 20, text=f"Счет: {self.score}", font=('Arial', 16), fill='black')
        self.canvas.create_text(400, 20, text="< > движение | Пробел/^ прыжок", 
                               fill='black', font=('Arial', 12), tags="info")
        
        if self.game_over:
            self.canvas.create_rectangle(200, 200, 600, 300, fill='gray', outline='black', width=3)
            self.canvas.create_text(400, 230, text="ИГРА ОКОНЧЕНА", font=('Arial', 24, 'bold'), fill='red')
            self.canvas.create_text(400, 260, text=f"Финальный счет: {self.score}", font=('Arial', 18), fill='white')
            self.canvas.create_text(400, 290, text="Нажмите R для перезапуска", font=('Arial', 14), fill='yellow')
    
    def reset_game(self):
        self.player_x = 100
        self.player_y = 300
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.score = 0
        self.game_over = False
        
        for item in self.collectibles:
            item['collected'] = False
            item['x'] = randint(50, 750)
            item['y'] = randint(50, 500)

    def game_loop(self):
        self.handle_input()
        self.check_platform_collision()
        self.update_player()
        self.draw()
        self.update_collectibles()
        self.window.after(30, self.game_loop)

if __name__ == "__main__":
    game = Platformer()
    game.window.mainloop()
