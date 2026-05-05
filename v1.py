import tkinter as tk
from random import randint

class Platformer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2D Платформер")
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
        
        self.platforms = [
            (0, 550, 800, 20),
            (350, 450, 150, 20),
            (550, 350, 150, 20),
            (50, 250, 100, 20),
        ]
        
        self.keys_pressed = {}
        
        self.window.bind('<KeyPress>', self.key_press)
        self.window.bind('<KeyRelease>', self.key_release)
        
        self.game_loop()
        
    def key_press(self, event):
        self.keys_pressed[event.keysym] = True
        
    def key_release(self, event):
        self.keys_pressed[event.keysym] = False
        
        self.player_vel_x = 0
        if 'Left' in self.keys_pressed and self.keys_pressed['Left']:
            self.player_vel_x = -self.player_speed
        if 'Right' in self.keys_pressed and self.keys_pressed['Right']:
            self.player_vel_x = self.player_speed
            
        if 'space' in self.keys_pressed and self.keys_pressed['space'] and self.on_ground:
            self.player_vel_y = -self.jump_power
            self.on_ground = False
        if 'Up' in self.keys_pressed and self.keys_pressed['Up'] and self.on_ground:
            self.player_vel_y = -self.jump_power
            self.on_ground = False
            
    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def check_platform_collision(self):
        self.on_ground = False
        for px, py, pw, ph in self.platforms:
            if self.check_collision(
                self.player_x, self.player_y + self.player_vel_y,
                self.player_size, self.player_size,
                px, py, pw, ph
            ):
                if self.player_vel_y > 0:
                    self.player_y = py - self.player_size
                    self.player_vel_y = 0
                    self.on_ground = True
                elif self.player_vel_y < 0: 
                    self.player_y = py + ph
                    self.player_vel_y = 0
                    
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
        
    
    def draw(self):
        self.canvas.delete('all')
        
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='lightblue', outline='')
        
        for px, py, pw, ph in self.platforms:
            self.canvas.create_rectangle(px, py, px+pw, py+ph, fill='green', outline='black', width=2)
        
        self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + self.player_size,
            self.player_y + self.player_size,
            fill='blue', outline='darkblue', width=2
        )
        
    def reset_game(self):
        self.player_x = 100
        self.player_y = 300
        self.player_vel_x = 0
        self.player_vel_y = 0
        
    def game_loop(self):
        
        self.check_platform_collision()
        self.update_player()
        
        self.draw()
        
        self.window.after(30, self.game_loop)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Platformer()
    game.run()