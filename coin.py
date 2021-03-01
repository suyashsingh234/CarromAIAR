from pygame import Vector2
from pygame import Rect
import pygame


class Coin:
    def __init__(self, radius, mass, position: Vector2, container: Rect):
        self.radius = radius
        self.mass = mass
        self.position = position
        self.container = container
        self.velocity = Vector2(0.0, 0.0)

    def update(self, dt, deceleration):
        self.position += self.velocity * dt

        if self.position.x + self.radius > self.container.right:
            self.position.x -= 2 * (self.position.x + self.radius - self.container.right)
            self.velocity.x = -self.velocity.x
        elif self.position.x - self.radius < self.container.left:
            self.position.x += 2 * (self.container.left - self.position.x + self.radius)
            self.velocity.x = -self.velocity.x

        if self.position.y + self.radius > self.container.bottom:
            self.position.y -= 2 * (self.position.y + self.radius - self.container.bottom)
            self.velocity.y = -self.velocity.y
        elif self.position.y - self.radius < self.container.top:
            self.position.y += 2 * (self.container.top - self.position.y + self.radius)
            self.velocity.y = -self.velocity.y

        if self.velocity.length() <= deceleration * dt:
            self.velocity = Vector2()
        else:
            self.velocity -= self.velocity.normalize() * deceleration * dt

    def check_collision(self, other):
        if self.position.distance_to(other.position) > self.radius + other.radius:
            return False

        if (self.velocity - other.velocity) * (self.position - other.position) > 0:
            return False

        return True

    def resultant_collision_velocity(self, other, e):
        if Vector2.length(self.position - other.position) == 0:
            return self.velocity
        return self.velocity - ((1 + e) * other.mass / (self.mass + other.mass)) * \
            Vector2.dot(self.velocity - other.velocity, self.position - other.position) / \
            Vector2.length_squared(self.position - other.position) * (self.position - other.position)

    def collide(self, other, e):
       self.velocity, other.velocity = self.resultant_collision_velocity(other, e), \
            other.resultant_collision_velocity(self, e)

    def check_moving(self):
        return self.velocity.length() > 0

    def draw(self, win):
        raise NotImplementedError("draw function not implemented")


class CarromMen(Coin):
    def __init__(self, player, radius, mass, position: Vector2, container: Rect):
        assert player in (0, 1)
        self.player = player
        self.color = (255, 255, 255) if player == 0 else (0, 0, 0)
        Coin.__init__(self, radius, mass, position, container)

    def reset(self):
        self.position = Vector2(self.container.center)
        self.velocity = Vector2()

    def get_player(self):
        return self.player

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))


class Queen(Coin):
    def __init__(self, radius, mass, position: Vector2, container: Rect):
        Coin.__init__(self, radius, mass, position, container)
        self.color = (255, 0, 0)

    def reset(self):
        self.position = Vector2(self.container.center)
        self.velocity = Vector2()

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))


class Striker(Coin):
    def __init__(self, radius, mass, container: Rect):
        Coin.__init__(self, radius, mass, Vector2(), container)

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (int(self.position.x), int(self.position.y)), int(self.radius))
