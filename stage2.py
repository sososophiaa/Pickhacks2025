import random
import pygame

# Initialize Pygame
pygame.init()

# Load the lander image once before the game loop
earth_image = pygame.image.load("earth.png")  # Load
earth_image = pygame.transform.scale(earth_image, (400, 400))  # Resize if needed

def stage2_play(screen, font, pygame, stars, current_screen):
    
    screen.fill("black")  # Fill with black
    

    # Generate stars (x, y, initial brightness)
    for i in range(len(stars)):
        x, y, brightness = stars[i]
        brightness += random.randint(-5, 5)  # Slight flickering effect
        brightness = max(100, min(255, brightness))  # Keep brightness in range
        stars[i] = (x, y, brightness)  # Update star with new brightness
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 2)

    
    # Blit the earth in the center of the screen
    earth_x = (screen.get_width() - earth_image.get_width()) // 2
    earth_y = (screen.get_height() - earth_image.get_height()) // 2
    screen.blit(earth_image, (earth_x, earth_y))
    
    # Draw the right arrow (pointing right) as a button
    right_arrow_rect = pygame.draw.polygon(screen, (0, 255, 0), [
        (screen.get_width() - 50, screen.get_height() // 2),  # Tip of the arrow
        (screen.get_width() - 100, screen.get_height() // 2 - 50),  # Top corner
        (screen.get_width() - 100, screen.get_height() // 2 + 50)  # Bottom corner
    ])
    
    # Event handling for mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position

            # Check if right arrow is clicked
            if right_arrow_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "stage3"  # Change screen to the next screen
                print("Right Arrow Clicked! Moving to next screen.")
