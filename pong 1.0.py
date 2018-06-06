from livewires import games, color, math
games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pong(games.Sprite):
    image = games.load_image('ball.bmp')
    speed = 3
    
    def __init__(self, x = 320 ,y = 240 ):
        super(Pong, self).__init__(image = Pong.image,
                                   x = x, y = y, dx = Pong.speed, dy = Pong.speed)
        self.comp_score = games.Text(value = 0, size = 35, color = color.green,
                                top = 240, left = 200, is_collideable = False)
        games.screen.add(self.comp_score)
        
        self.player_score = games.Text(value = 0, size = 35, color = color.green,
                                top = 240, right = games.screen.width - 200, is_collideable = False)
        games.screen.add(self.player_score)
    def update(self):
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
            
        if self.top > games.screen.height:
            self.player_score.value += 1
            self.bottom = games.screen.height/2
            
        if self.bottom <= 0:
            self.comp_score.value += 1
            self.top = games.screen.height/2
            
        if (self.player_score.value or self.comp_score.value) == 7:
            self.destroy()
            if self.player_score.value < self.comp_score.value:
                game_over = games.Message(value = 'Player 1 wins!',
                                          size = 40, color = color.blue,
                                          x = 420, y = 100, lifetime = 250,
                                          after_death = games.screen.quit)
            elif self.comp_score.value < self.player_score.value:
                game_over = games.Message(value = 'Computer wins!',
                                          size = 40, color = color.blue,
                                          x = 420, y = 100, lifetime = 250,
                                          after_death = games.screen.quit)
            games.screen.add(game_over)
    def hit_back(self):
        self.dy = -self.dy
       
class Paddle_handler(games.Sprite):
    def update(self):
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width - 0.5:
            self.right = games.screen.width - 0.5
        self.collision()

    def collision(self):
        for ball in self.overlapping_sprites:
            ball.hit_back()
            
class Paddle(Paddle_handler):
    image = games.load_image('paddle.bmp')

    def __init__(self):
        super(Paddle, self).__init__(image = Paddle.image,
                                     x = 240,
                                     bottom = games.screen.height)
    def update(self):
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 4
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 4
        super(Paddle, self).update()

class Computer(Paddle_handler):
    image = games.load_image('paddle.bmp')
    def __init__(self):
        super(Computer, self).__init__(image = Computer.image, x = 320,
                                       top = 0)
        self.ball = Pong()
        games.screen.add(self.ball)
        
    def update(self):
        super(Computer, self).update()
        if self.x < self.ball.x and self.ball.dy < 0:
            self.x += 2.6
        if self.x > self.ball.x and self.ball.dy < 0:
            self.x -= 2.6
        
def main():
    court = games.load_image('background.jpg', transparent = False)
    games.screen.background = court

    player = Paddle()
    games.screen.add(player)

    computer = Computer()
    games.screen.add(computer)

    games.mouse.is_visible = False
    games.screen.event_grab = False
    games.screen.mainloop()

main()

    
            
        
            
        
