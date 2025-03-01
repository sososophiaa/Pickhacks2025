import random
import pygame

# Initialize Pygame
pygame.init()

# Load the lander image once before the game loop
lander_image = pygame.image.load("lander.png")  # Load lander
lander_image = pygame.transform.scale(lander_image, (400, 400))  # Resize if needed

# Load the telescope image once before the game loop
telescope_image = pygame.image.load("telescope.png")  # Load telescope
telescope_image = pygame.transform.scale(telescope_image, (200, 200))  # Resize if needed

def stage1_play(screen, font, pygame, stars, *current_screen):
    screen.fill("black")  # Fill with black

    # Generate stars (x, y, initial brightness)
    for i in range(len(stars)):
        x, y, brightness = stars[i]
        brightness += random.randint(-5, 5)  # Slight flickering effect
        brightness = max(100, min(255, brightness))  # Keep brightness in range
        stars[i] = (x, y, brightness)  # Update star with new brightness
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 2)

    # Mars properties
    mars_radius = 1200  # Increased Mars size
    mars_center = mars_radius  # Center offset for drawing

    # Create Mars texture
    mars_surface = pygame.Surface((mars_radius * 2, mars_radius * 2), pygame.SRCALPHA)
    mars_surface.fill((0, 0, 0, 0))  # Transparent background

    # Draw the base red-orange planet
    pygame.draw.circle(mars_surface, (210, 90, 40), (mars_center, mars_center + 1200), mars_radius)

    # Add shading (radial gradient effect)
    for i in range(mars_radius, 0, -1):
        color = (max(100, 210 - i * 2), max(40, 90 - i), max(20, 40 - i // 2))
        pygame.draw.circle(mars_surface, color, (mars_center, mars_center + 1200), i)

    # Blit Mars at the bottom
    screen.blit(mars_surface, (screen.get_width() // 2 - mars_radius, screen.get_height() // 2 - mars_radius))

    # Blit the lander in the center of the screen
    lander_x = (screen.get_width() - lander_image.get_width()) // 2
    lander_y = (screen.get_height() - lander_image.get_height()) // 2
    rocket_rect = screen.blit(lander_image, (lander_x, lander_y))

    # Blit the telescope slightly to the right of the lander
    telescope_x = (screen.get_width() - telescope_image.get_width()) // 2 + 400
    telescope_y = (screen.get_height() - telescope_image.get_height()) // 2 + 100
    telescope_rect = screen.blit(telescope_image, (telescope_x, telescope_y))

    # Draw the left arrow (pointing left) as a button
    left_arrow_rect = pygame.draw.polygon(screen, (0, 255, 0), [
        (50, screen.get_height() // 2),  # Tip of the arrow
        (100, screen.get_height() // 2 - 50),  # Top corner
        (100, screen.get_height() // 2 + 50)  # Bottom corner
    ])
    
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

            # Check if left arrow is clicked
            if left_arrow_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "main"  # Change screen to the previous screen
                print("Left Arrow Clicked! Moving to previous screen.")

            # Check if right arrow is clicked
            if right_arrow_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "stage4"  # Change screen to the next screen
                print("Right Arrow Clicked! Moving to next screen.")

            # Check if telescope is clicked
            if telescope_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "stage2"  # Change screen to stage 2
                print("Telescope Clicked! Moving to stage 2.")

            # Check if rocket is clicked
            if rocket_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "stage3"  # Change screen to stage 3
                print("Rocket Clicked! Moving to stage 3.")

                