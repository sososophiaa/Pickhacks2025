import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)

# Load images (replace with actual image paths if available)
earth_img = pygame.image.load("earth.png")  # Placeholder, needs an image
earth_img = pygame.transform.scale(earth_img, (200, 200))

# Game loop
while running:
    screen.fill(DARK_GRAY)  # Spaceship interior

    # Window showing Earth
    pygame.draw.rect(screen, LIGHT_GRAY, (900, 100, 250, 250))  # Window frame
    screen.blit(earth_img, (925, 125))  # Earth image

    # Bookshelf
    pygame.draw.rect(screen, BROWN, (50, 100, 100, 500))

    # Chair
    pygame.draw.rect(screen, LIGHT_GRAY, (500, 450, 150, 100))  # Seat
    pygame.draw.rect(screen, LIGHT_GRAY, (500, 400, 150, 50))  # Backrest

    # Coffee Table
    pygame.draw.rect(screen, BROWN, (550, 550, 100, 50))

    # Snake Plant
    pygame.draw.rect(screen, BROWN, (1100, 600, 40, 60))  # Pot
    pygame.draw.polygon(screen, GREEN, [(1120, 600), (1110, 540), (1130, 500)])  # Leaves

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
