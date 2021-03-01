import pygame

def draw_text(surface, message, font_size, center_position, color=(0, 0, 255)):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = center_position
    surface.blit(text, text_rect)


def create_button(width, height, message, selected=False):
    surf = pygame.Surface((width, height))
    if selected:
        surf.fill((0, 120, 255))
    else:
        surf.fill((120, 120, 120))
    pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 1)
    draw_text(surf, message, height // 3, surf.get_rect().center, (0, 0, 0))
    return surf
