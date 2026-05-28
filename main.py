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
        
        # Состояния игры
        self.game_state = "menu"
        self.menu_type = "main"
        self.menu_items = ["Играть", "Сложность", "Выход"]
        self.menu_selection = 0
        
        self.difficulty = "normal"
        
        self.player_size = 30
        self.player_x = 100
        self.player_y = 300
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.player_speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False
        self.lives = 3
        self.score = 0
        
        self.platforms = []
        self.enemies = []
        self.collectibles = []
        self.total_coins = 0
        
        self.keys_pressed = {}
        self.window.bind('<KeyPress>', self.key_press)
        self.window.bind('<KeyRelease>', self.key_release)
        self.window.focus_set()
        
        self.game_loop()
    
    def init_game_objects(self):
        self.platforms = [
            (0, 550, 800, 30),
            (200, 450, 200, 20),
            (500, 350, 200, 20),
            (400, 250, 50, 20),
            (700, 200, 50, 20),
            (100, 250, 200, 20),
        ]
        
        if self.difficulty == "hard":
            self.platforms.extend([
                (300, 150, 80, 20),
                (600, 300, 80, 20),
            ])
        
        self.enemies = [
            {'x': 300, 'y': 450-25, 'size': 25, 'speed': 2, 'dir': 1},
            {'x': 550, 'y': 350-25, 'size': 25, 'speed': 1.5, 'dir': -1},
        ]
        
        if self.difficulty == "hard":
            self.enemies.append({'x': 150, 'y': 250-25, 'size': 25, 'speed': 2.5, 'dir': 1})
        elif self.difficulty == "normal":
            self.enemies.append({'x': 400, 'y': 250-25, 'size': 25, 'speed': 1.8, 'dir': 1})
        
        if self.difficulty == "easy":
            self.total_coins = 8
        elif self.difficulty == "normal":
            self.total_coins = 10
        else:
            self.total_coins = 12
        
        self.collectibles = []
        for _ in range(self.total_coins):
            while True:
                x = randint(50, 750)
                y = randint(50, 500)
                on_platform = False
                for px, py, pw, ph in self.platforms:
                    if py - 30 < y < py + ph and px < x < px + pw:
                        on_platform = True
                        break
                if not on_platform:
                    self.collectibles.append({'x': x, 'y': y, 'collected': False})
                    break
    
    def set_difficulty(self, diff):
        self.difficulty = diff
        if diff == "easy":
            self.player_speed = 6
            self.jump_power = 17
            self.lives = 5
            self.gravity = 0.7
        elif diff == "normal":
            self.player_speed = 5
            self.jump_power = 15
            self.lives = 3
            self.gravity = 0.8
        else:
            self.player_speed = 4
            self.jump_power = 14
            self.lives = 1
            self.gravity = 0.9
    
    def start_game(self):
        self.set_difficulty(self.difficulty)
        self.game_state = "playing"
        self.score = 0
        self.player_x = 100
        self.player_y = 300
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.on_ground = False
        self.init_game_objects()
    
    def key_press(self, event):
        if self.game_state == "menu":
            if event.keysym == 'Up':
                self.menu_selection = (self.menu_selection - 1) % len(self.menu_items)
            elif event.keysym == 'Down':
                self.menu_selection = (self.menu_selection + 1) % len(self.menu_items)
            elif event.keysym == 'Return':
                self.handle_menu_selection()
        
        elif self.game_state in ["game_over", "victory"]:
            if event.keysym == 'Escape':
                self.back_to_menu()
            elif event.keysym == 'r' or event.keysym == 'R':
                self.back_to_menu()
        
        elif self.game_state == "playing":
            self.keys_pressed[event.keysym] = True
            if event.keysym == 'Escape':
                self.back_to_menu()
    
    def key_release(self, event):
        if self.game_state == "playing" and event.keysym in self.keys_pressed:
            self.keys_pressed[event.keysym] = False
    
    def handle_menu_selection(self):
        if self.menu_type == "main":
            selected = self.menu_items[self.menu_selection]
            if selected == "Играть":
                self.start_game()
            elif selected == "Сложность":
                self.show_difficulty_menu()
            elif selected == "Выход":
                self.window.quit()
        elif self.menu_type == "difficulty":
            selected = self.menu_items[self.menu_selection]
            if selected == "Легкая":
                self.difficulty = "easy"
                self.back_to_main_menu()
            elif selected == "Нормальная":
                self.difficulty = "normal"
                self.back_to_main_menu()
            elif selected == "Сложная":
                self.difficulty = "hard"
                self.back_to_main_menu()
            elif selected == "Назад":
                self.back_to_main_menu()
    
    def show_difficulty_menu(self):
        self.menu_type = "difficulty"
        self.menu_items = ["Легкая", "Нормальная", "Сложная", "Назад"]
        self.menu_selection = 0
    
    def back_to_main_menu(self):
        self.menu_type = "main"
        self.menu_items = ["Играть", "Сложность", "Выход"]
        self.menu_selection = 0
    
    def back_to_menu(self):
        self.game_state = "menu"
        self.menu_type = "main"
        self.menu_items = ["Играть", "Сложность", "Выход"]
        self.menu_selection = 0
        self.keys_pressed.clear()
    
    def handle_input(self):
        if self.game_state != "playing":
            return
        
        self.player_vel_x = 0
        if self.keys_pressed.get('Left', False):
            self.player_vel_x = -self.player_speed
        if self.keys_pressed.get('Right', False):
            self.player_vel_x = self.player_speed
        
        if (self.keys_pressed.get('Up', False) or self.keys_pressed.get('space', False)) and self.on_ground:
            self.player_vel_y -= self.jump_power
            self.on_ground = False
    
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
                self.player_vel_y = 1
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
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = "game_over"
            else:
                self.player_x = 100
                self.player_y = 300
                self.player_vel_y = 0
    
    def update_enemies(self):
        speed_multiplier = 1.3 if self.difficulty == "hard" else 1.0
        
        for enemy in self.enemies:
            enemy['x'] += enemy['speed'] * enemy['dir'] * speed_multiplier
            
            if enemy['x'] <= 50 or enemy['x'] >= 750 - enemy['size']:
                enemy['dir'] *= -1
            
            if self.check_collision(
                self.player_x, self.player_y, self.player_size, self.player_size,
                enemy['x'], enemy['y'], enemy['size'], enemy['size']
            ):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_state = "game_over"
                else:
                    if self.player_x < enemy['x']:
                        self.player_x -= 50
                    else:
                        self.player_x += 50
                    self.player_vel_y = -10
    
    def update_collectibles(self):
        collected_count = 0
        for item in self.collectibles:
            if not item['collected']:
                if self.check_collision(
                    self.player_x, self.player_y,
                    self.player_size, self.player_size,
                    item['x'], item['y'], 20, 20
                ):
                    item['collected'] = True
                    points = 20 if self.difficulty == "hard" else 15 if self.difficulty == "normal" else 10
                    self.score += points
            else:
                collected_count += 1
        
        if collected_count == self.total_coins:
            self.game_state = "victory"
    
    def draw_menu(self):
        self.canvas.delete('all')
        
        if self.menu_type == "main":
            bg_color = 'green'
        else:
            bg_color = 'teal'
        
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=bg_color, outline='')
        
        self.canvas.create_text(self.width//2, 100, text="2D ПЛАТФОРМЕР", 
                               font=('Arial', 36, 'bold'), fill='white')
        
        y_start = 200
        button_width = 200
        button_height = 50
        
        for i, item in enumerate(self.menu_items):
            button_x1 = self.width//2 - button_width//2
            button_y1 = y_start + i * 70
            button_x2 = button_x1 + button_width
            button_y2 = button_y1 + button_height
            
            if i == self.menu_selection:
                self.canvas.create_rectangle(button_x1, button_y1, button_x2, button_y2, 
                                            fill='black', outline='yellow', width=3)
                text_color = 'yellow'
            else:
                self.canvas.create_rectangle(button_x1, button_y1, button_x2, button_y2, 
                                            fill='black', outline='white', width=2)
                text_color = 'white'
            
            self.canvas.create_text(self.width//2, button_y1 + button_height//2, 
                                   text=item, font=('Arial', 20, 'bold'), fill=text_color)
        
        if self.menu_type == "main":
            diff_text = {"easy": "Легкая", "normal": "Нормальная", "hard": "Сложная"}.get(self.difficulty, "Нормальная")
            self.canvas.create_text(self.width//2, 470, text=f"Текущая сложность: {diff_text}", 
                                   font=('Arial', 14), fill='white')
        
        self.canvas.create_text(self.width//2, 550, text="↑/↓: навигация | Enter: выбор | Esc: выход", 
                               font=('Arial', 12), fill='white')
    
    def draw_game(self):
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
        
        for enemy in self.enemies:
            color = 'darkred' if self.difficulty == "hard" else 'red'
            self.canvas.create_oval(
                enemy['x'], enemy['y'],
                enemy['x'] + enemy['size'], enemy['y'] + enemy['size'],
                fill=color, outline='darkred', width=2
            )
        
        for item in self.collectibles:
            if not item['collected']:
                self.canvas.create_oval(
                    item['x'], item['y'],
                    item['x'] + 20, item['y'] + 20,
                    fill='gold', outline='orange', width=2
                )
        
        collected = sum(1 for item in self.collectibles if item['collected'])
        diff_text = {"easy": "Легкая", "normal": "Нормальная", "hard": "Сложная"}.get(self.difficulty, "Нормальная")
        
        self.canvas.create_text(70, 20, text=f"Счет: {self.score}", font=('Arial', 16), fill='black')
        self.canvas.create_text(70, 45, text=f"Жизни: {self.lives}", font=('Arial', 16), fill='red')
        self.canvas.create_text(70, 70, text=f"Монеты: {collected}/{self.total_coins}", 
                               font=('Arial', 14), fill='gold')
        self.canvas.create_text(70, 95, text=f"Сложность: {diff_text}", 
                               font=('Arial', 12), fill='purple')
        self.canvas.create_text(400, 20, text="← → движение | Пробел/↑ прыжок | Esc меню", 
                               fill='black', font=('Arial', 12))
    
    def draw_game_over(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='lightblue', outline='')
        self.canvas.create_rectangle(200, 200, 600, 320, fill='gray', outline='black', width=3)
        self.canvas.create_text(400, 230, text="ИГРА ОКОНЧЕНА", font=('Arial', 24, 'bold'), fill='red')
        self.canvas.create_text(400, 260, text=f"Финальный счет: {self.score}", font=('Arial', 18), fill='white')
        self.canvas.create_text(400, 290, text="Нажмите Esc для выхода в меню", font=('Arial', 14), fill='yellow')
    
    def draw_victory(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='lightblue', outline='')
        self.canvas.create_rectangle(200, 200, 600, 320, fill='gold', outline='orange', width=3)
        self.canvas.create_text(400, 230, text="ПОБЕДА!", font=('Arial', 24, 'bold'), fill='green')
        self.canvas.create_text(400, 260, text=f"Финальный счет: {self.score}", font=('Arial', 18), fill='darkblue')
        for _ in range(15):
            x = randint(250, 550)
            y = randint(210, 310)
            self.canvas.create_text(x, y, text="★", font=('Arial', 16), fill='yellow')
        self.canvas.create_text(400, 290, text="Нажмите Esc для выхода в меню", font=('Arial', 14), fill='orange')
    
    def game_loop(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.handle_input()
            self.check_platform_collision()
            self.update_player()
            self.update_enemies()
            self.update_collectibles()
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()
        
        self.window.after(30, self.game_loop)

if __name__ == "__main__":
    game = Platformer()
    game.window.mainloop()