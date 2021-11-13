import pygame
import itertools
import random

W_WIDTH = 700
W_HEIGHT = 800


class BouncingBall(pygame.sprite.Sprite):

    def __init__(self, start_pos, start_dir, velocity):
        super().__init__()
        self.pos = pygame.math.Vector2(start_pos)
        self.dir = pygame.math.Vector2(start_dir).normalize()
        self.vel = velocity
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def bounce(self, new_dir):
        self.dir = self.dir.reflect(pygame.math.Vector2(new_dir))

    def update(self):
        self.pos += self.dir * self.vel
        self.rect.center = self.pos.x, self.pos.y

        if self.rect.right >= W_WIDTH:
            self.bounce((-1, 0))
            self.rect.right = W_WIDTH
        if self.rect.left <= 0:
            self.bounce((1, 0))
            self.rect.left = 0
        if self.rect.bottom >= W_HEIGHT:
            self.bounce((0, -1))
            self.rect.bottom = W_HEIGHT
        if self.rect.top <= 0:
            self.bounce((0, 1))
            self.rect.top = 0


pygame.init()
window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption('Bouncing balls')
clock = pygame.time.Clock()

all_balls = pygame.sprite.Group()

num_of_balls = int(input("Type, how many balls: "))
balls = []

for i in range(num_of_balls):
    s_pos_x = random.randint(20, 100) * (i + 1)
    s_pos_y = random.randint(20, 100) * (i + 2)
    s_dir_x = random.randint(1, 10) * (i + 1)
    s_dir_y = random.randint(1, 10) * (i + 2)
    speed = random.randint(7, 12)

    ball = BouncingBall((s_pos_x, s_pos_y), (s_dir_x, s_dir_y), speed)
    balls.append(ball)
    all_balls.add(balls[i])


def bounce_balls(bs):
    v = []
    r = []
    d = []

    for j in range(len(bs)):
        v.append(pygame.math.Vector2(bs[j].rect.center))
        r.append(bs[j].rect.width // 2)

    combs = list(itertools.combinations(range(num_of_balls), 2))
    num_of_combs = len(combs)

    for j in range(num_of_combs):
        d.append(v[combs[j][0]].distance_to(v[combs[j][1]]))

        if d[j] < r[combs[j][0]] + r[combs[j][1]]:
            new_dist = (v[combs[j][0]] + bs[combs[j][0]].dir).distance_to\
                (v[combs[j][1]] + bs[combs[j][1]].dir)
            new_vel = v[combs[j][1]] - v[combs[j][0]]

            if new_dist < d[j] and new_vel.length() > 0:
                bs[combs[j][0]].bounce(new_vel)
                bs[combs[j][1]].bounce(new_vel)


run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_balls.update()

    b_list = all_balls.sprites()
    for i, ball1 in enumerate(b_list):
        for ball2 in b_list[i+1:]:
            bounce_balls(balls)

    window.fill(0)
    pygame.draw.rect(window, (0, 0, 0), (0, 0, W_WIDTH, W_HEIGHT), 1)
    all_balls.draw(window)
    pygame.display.flip()