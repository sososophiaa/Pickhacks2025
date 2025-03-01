import pygame

pygame.init()

table_image = pygame.image.load("tablephoto.webp")  # Load lander
table_image = pygame.transform.scale(table_image, (400, 400))

def stage3_play(screen, font, pygame, *current_screen):
    screen.fill("black")  # Fill with black

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

    # table placement
    table_x = (screen.get_width() - table_image.get_width()) // 2
    table_y = (screen.get_height() - table_image.get_height()) // 2
    table_rect = screen.blit(table_image, (table_x, table_y))

    # Event handling for mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position

            # Check if left arrow is clicked
            if table_rect.collidepoint(mouse_x, mouse_y):
                current_screen = "stage4"  # Change screen to the previous screen
                print("Left Arrow Clicked! Moving to previous screen.")

