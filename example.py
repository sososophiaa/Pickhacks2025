import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Generate stars (x, y, initial brightness)
num_stars = 100
stars = [(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.randint(100, 255)) for _ in range(num_stars)]

# Mars properties
mars_radius = 120  # Increased Mars size
mars_center = mars_radius  # Center offset for drawing
crater_min_radius = 15  # Larger craters
crater_max_radius = 30
crater_distance_min = 20  # Craters must be at least this far from center
crater_distance_max = 100  # Stay inside Mars

# Create Mars texture
mars_surface = pygame.Surface((mars_radius * 2, mars_radius * 2), pygame.SRCALPHA)
mars_surface.fill((0, 0, 0, 0))  # Transparent background

# Draw the base red-orange planet
pygame.draw.circle(mars_surface, (210, 90, 40), (mars_center, mars_center), mars_radius)  # Mars base color

# Add shading (radial gradient effect)
for i in range(mars_radius, 0, -1):  # From outer edge to center
    color = (max(100, 210 - i * 2), max(40, 90 - i), max(20, 40 - i // 2))  # Darker towards edges
    pygame.draw.circle(mars_surface, color, (mars_center, mars_center), i)

# Place non-overlapping craters
craters = []
max_attempts = 50  # Prevent infinite loops

# Reduced number of craters (5 craters)
for _ in range(5):  # Reduce number of craters
    for _ in range(max_attempts):  # Try multiple times if needed
        angle = random.uniform(0, 2 * math.pi)  # Random angle
        distance = random.uniform(crater_distance_min, crater_distance_max)  # Stay inside Mars

        # Convert to Cartesian (Mars center is at (mars_center, mars_center))
        cx = int(mars_center + distance * math.cos(angle))
        cy = int(mars_center + distance * math.sin(angle))
        radius = random.randint(crater_min_radius, crater_max_radius)

        # Check for overlap
        overlap = any(math.dist((cx, cy), (ox, oy)) < (radius + oradius) for ox, oy, oradius in craters)
        
        if not overlap:  # If no overlap, accept this crater
            craters.append((cx, cy, radius))
            break  # Exit the loop once a valid spot is found

# Draw craters
for cx, cy, radius in craters:
    pygame.draw.circle(mars_surface, (150, 50, 30), (cx, cy), radius)  # Dark brown craters
    pygame.draw.circle(mars_surface, (180, 70, 50), (cx + 5, cy + 5), max(radius - 5, 2))  # Lighter highlight

# Play button properties (triangle button)
button_size = 60  # Triangle size
button_color = (0, 255, 0)  # Green color
border_color = (0, 100, 0)  # Dark green border
button_pos = (screen.get_width() // 2 + 10, screen.get_height() // 2)  # Center of the screen shifted by 10px on the x-axis

# Define the triangle's points
button_points = [
    (button_pos[0], button_pos[1] - button_size),  # Top point
    (button_pos[0] - button_size, button_pos[1] + button_size),  # Bottom left
    (button_pos[0] + button_size, button_pos[1] + button_size)   # Bottom right
]

# Function to rotate the triangle
def rotate_points(points, angle, center):
    rotated_points = []
    for point in points:
        px, py = point
        # Translate point back to origin
        px -= center[0]
        py -= center[1]

        # Rotate the point
        rotated_x = px * math.cos(angle) - py * math.sin(angle)
        rotated_y = px * math.sin(angle) + py * math.cos(angle)

        # Translate back to the center
        rotated_points.append((rotated_x + center[0], rotated_y + center[1]))
    return rotated_points

# Rotate the triangle 90 degrees (pi/2 radians)
rotated_button_points = rotate_points(button_points, math.pi / 2, button_pos)
rotated_border_points = rotate_points(button_points, math.pi / 2, button_pos)

# New screen state
current_screen = "main_menu" # Default to main menu screen

# Font for "Play" text
font = pygame.font.SysFont(None, 48)

# Rocket properties
rocket_pos = pygame.Vector2(-200, screen.get_height() // 2)  # Start off screen (to the left)
rocket_speed = 200  # Speed of the rocket
rocket_image = pygame.image.load("rocket.png").convert_alpha()  # Load PNG with transparency
rocket_image = pygame.transform.scale(rocket_image, (70, 70))  # Resize if needed
rocket_rect = rocket_image.get_rect(center=rocket_pos)

# Flag to control rocket movement
rocket_moving = False

# Rectangle button properties
button_width = 300
button_height = 75
button_margin = 20  # Space between buttons
button_color_left = (0, 200, 255)  # Blue for the left button
button_color_right = (255, 165, 0)  # Orange for the right button
button_pos_left = (screen.get_width() // 2 - 500, screen.get_height() // 2 + 200)  # Left button
button_pos_right = (screen.get_width() // 2 + 200, screen.get_height() // 2 + 200)  # Right button

# Function to draw rectangle buttons
def draw_rectangle_button_with_text(pos, width, height, color, text):
    pygame.draw.rect(screen, color, (pos[0], pos[1], width, height))  # Draw the button
    # Render the text
    text_surface = font.render(text, True, (0, 0, 0))  # Black text
    # Get the rectangle for the text
    text_rect = text_surface.get_rect(center=(pos[0] + width // 2, pos[1] + height // 2))  # Center the text
    screen.blit(text_surface, text_rect)  # Draw the text

# New button click logic
def is_point_in_rect(pt, rect_pos, width, height):
    x, y = pt
    rect_x, rect_y = rect_pos
    return rect_x <= x <= rect_x + width and rect_y <= y <= rect_y + height

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the play button (triangle) is clicked
            mouse_pos = pygame.mouse.get_pos()

            hover_color = (0, 200, 0)
            # Check if the mouse click is within the triangle using a polygon-point-inclusion check
            def is_point_in_triangle(pt, v1, v2, v3):
                x, y = pt
                x1, y1 = v1
                x2, y2 = v2
                x3, y3 = v3
                denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
                a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
                b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
                c = 1 - a - b
                return a >= 0 and b >= 0 and c >= 0

            if is_point_in_triangle(mouse_pos, *rotated_button_points):
                # Start rocket movement when Play is clicked
                rocket_moving = True  # Start moving the rocket
                button_color = hover_color
                border_color = (0, 150, 0)

            # Check if the mouse click is within the rectangle buttons
            if is_point_in_rect(mouse_pos, button_pos_left, button_width, button_height):
                print("Left button clicked!")
            elif is_point_in_rect(mouse_pos, button_pos_right, button_width, button_height):
                print("Right button clicked!")

    # Fill screen with black
    screen.fill("black")

    # Update and draw twinkling stars
    for i in range(len(stars)):
        x, y, brightness = stars[i]
        brightness += random.randint(-5, 5)  # Slight flickering effect
        brightness = max(100, min(255, brightness))  # Keep brightness in range
        stars[i] = (x, y, brightness)  # Update star with new brightness
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 2)  # Draw star

    # Only draw play button on the main menu screen
    if current_screen == "main_menu":
        # Draw Mars (blitted so transparency works)
        screen.blit(mars_surface, (player_pos.x - mars_center, player_pos.y - mars_center))  # Center Mars on player_pos
        
        # Draw the play button (only on the main menu screen)
        pygame.draw.polygon(screen, border_color, rotated_border_points)  # Dark green border
        pygame.draw.polygon(screen, button_color, rotated_button_points)  # Green play button

        # Draw the "Play" text in the center of the button
        text = font.render("Play", True, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=(button_pos[0] - 15, button_pos[1]))  # Position text at the button center
        screen.blit(text, text_rect)

        # Draw the rectangle buttons below Mars
        draw_rectangle_button_with_text(button_pos_left, button_width, button_height, button_color_left, "Instructions")
        draw_rectangle_button_with_text(button_pos_right, button_width, button_height, button_color_right, "Credits")

    elif current_screen == "stage1":
        # Stage 1 content here
        screen.fill((255, 255, 255))  # Example for stage1, fill with white
        text = font.render("Stage 1", True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))

    # Rocket movement logic
    if rocket_moving:
        # Move the rocket toward Mars (adjust position based on the speed and delta time)
        rocket_pos.x += rocket_speed * dt

        # Update rocket rect position
        rocket_rect.center = rocket_pos

        # If the rocket reaches the target position, transition to stage 1
        if rocket_pos.x >= screen.get_width() // 2 - mars_radius:
            rocket_moving = False  # Stop the rocket from moving
            pygame.time.wait(1000)
            current_screen = "stage1"  # Transition to stage 1 screen

    # Draw the rocket if it is moving
    if rocket_moving:
        rotated_rocket = pygame.transform.rotate(rocket_image, 135)  # Rotate counterclockwise
        rotated_rect = rotated_rocket.get_rect(center=rocket_rect.center)  # Adjust position
        screen.blit(rotated_rocket, rotated_rect)

    # Flip display
    pygame.display.flip()

    # Limit FPS to 60, update delta time
    dt = clock.tick(60) / 1000

pygame.quit()
