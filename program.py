import pygame
import pymunk.pygame_util
from pymunk import Vec2d
import math, random

WHITE = pygame.color.THECOLORS["white"]
RED = pygame.color.THECOLORS["red"]
GREEN = pygame.color.THECOLORS["green"]
BLUE = pygame.color.THECOLORS["blue"]


class Bot:
    def __init__(self, shape, body, color):
        self.shape = shape
        self.body = body
        self.shape.color = color
        self.force_angle = random.uniform(-math.pi, math.pi)
        self.force_modulo = 0

    def apply_force(self):
        self.force_modulo = random.uniform(0, 1000)
        self.force_angle = self.force_angle + random.uniform(-0.3, 0.3)
        force_vector = Vec2d(self.force_modulo, 0)
        force_vector.rotate(self.force_angle)
        self.body.force = force_vector


def collision(arbiter, space, data):
    if arbiter.is_first_contact and len(arbiter.shapes) == 2:
        shape_1 = arbiter.shapes[0]
        shape_2 = arbiter.shapes[1]
        if (shape_1.color == RED and shape_2.color == GREEN):
            shape_2.color = shape_1.color
        elif (shape_1.color == GREEN and shape_2.color == BLUE):
            shape_2.color = shape_1.color
        elif (shape_1.color == BLUE and shape_2.color == RED):
            shape_2.color = shape_1.color


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
draw_options = pymunk.pygame_util.DrawOptions(screen)
clock = pygame.time.Clock()
running = True

space = pymunk.Space()  # Create a Space which contain the simulation
# space.gravity = 0, -10  # Set its gravity
space.damping = 0.95
collision_handler = space.add_collision_handler(1, 1)
collision_handler.post_solve = collision

# walls
static_body = space.static_body
static_lines = [pymunk.Segment(static_body, (50, 50), (50, 950), 1),
                pymunk.Segment(static_body, (50, 950), (950, 950), 1),
                pymunk.Segment(static_body, (950, 950), (950, 50), 1),
                pymunk.Segment(static_body, (950, 50), (50, 50), 1)]
for line in static_lines:
    line.elasticity = 0.90
    line.friction = 0.5
space.add(static_lines)

bots = []
for i in range(100):
    body = pymunk.Body(1, 100)
    body.position = (random.randint(100, 900), random.randint(100, 900))

    shape = pymunk.Circle(body, 10)
    shape.collision_type = 1
    shape.friction = random.uniform(0.1, 0.9)
    shape.elasticity = random.uniform(0.1, 0.9)
    space.add(body, shape)
    color = random.choice([RED, GREEN, BLUE])
    bots.append(Bot(shape, body, color))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    for bot in bots:
        bot.apply_force()

    space.step(0.01)  # Step the simulation one step forward
    screen.fill(WHITE)

    # space.debug_draw(draw_options)

    for bot in bots:
        bot_position = Vec2d(bot.body.position.x, 1000 - bot.body.position.y)
        engine_vector = Vec2d(-bot.force_modulo / 30, 0)
        engine_vector.rotate(-bot.force_angle)
        pygame.draw.lines(screen, bot.shape.color, False, [bot_position, bot_position + engine_vector], 2)
        pygame.draw.circle(screen, bot.shape.color, bot_position.int_tuple, 10, 0)

    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
