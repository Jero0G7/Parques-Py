import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Parques")

# Fuente personalizada
font = pygame.font.Font('src/fonts/EduSAHand.ttf', 36)

# Renderizado de textos
title = font.render("¡Hola Mundo! Un nuevo juego de", True, (0, 0, 0))
title2 = font.render("parques está por nacer", True, (0, 0, 0))

# Posiciones centradas
title_rect = title.get_rect(center=(300, 280))
title2_rect = title2.get_rect(center=(300, 320))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((225, 225, 225))
    screen.blit(title, title_rect)
    screen.blit(title2, title2_rect)
    pygame.display.flip()
    clock.tick(60)
