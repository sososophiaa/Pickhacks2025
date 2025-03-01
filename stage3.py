import pygame

pygame.init()

table_image = pygame.image.load("tablephoto.webp")  # Load lander
table_image = pygame.transform.scale(table_image, (400, 400))