#!/usr/bin/env python3
"""
FitCafe Image Generator v2 - Using PIL with gradients and better design
Creates professional placeholder images until Nano Banana 2 is available
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

# Create assets directory
os.makedirs("assets", exist_ok=True)

# Color palette
COLORS = {
    "primary": "#C05621",      # Dark orange
    "secondary": "#DD6B20",    # Orange
    "accent": "#ED8936",       # Light orange
    "light": "#FBD38D",        # Light yellow
    "cream": "#FFF5F0",        # Cream background
    "white": "#FFFFFF",
    "text_dark": "#2D3748",
    "text_light": "#FFFFFF",
}

def create_gradient_image(width, height, color1, color2, angle=45):
    """Create gradient background"""
    base = Image.new('RGB', (width, height), color=color1)
    top = Image.new('RGB', (width, height), color=color2)
    mask = Image.new('L', (width, height))
    
    for x in range(width):
        alpha = int(255 * (x / width))
        for y in range(height):
            mask.putpixel((x, y), alpha)
    
    base.paste(top, mask=mask)
    return base

def add_text_with_shadow(draw, position, text, font, fill="#FFFFFF", shadow_offset=3):
    """Add text with shadow effect"""
    x, y = position
    # Shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, fill="#000000", font=font)
    # Main text
    draw.text((x, y), text, fill=fill, font=font)

def create_product_image(filename):
    """Create hero product image"""
    width, height = 800, 1200
    
    # Gradient background (cream to light orange)
    img = create_gradient_image(width, height, COLORS["cream"], COLORS["light"])
    draw = ImageDraw.Draw(img)
    
    # Draw coffee pouch shape (simplified)
    pouch_x = width // 2
    pouch_y = height // 2
    pouch_width = 300
    pouch_height = 450
    
    # Pouch body
    draw.rectangle([
        pouch_x - pouch_width//2,
        pouch_y - pouch_height//2,
        pouch_x + pouch_width//2,
        pouch_y + pouch_height//2
    ], fill=COLORS["primary"], outline=COLORS["secondary"], width=3)
    
    # Pouch top (sealed edge)
    draw.rectangle([
        pouch_x - pouch_width//2 - 10,
        pouch_y - pouch_height//2 - 30,
        pouch_x + pouch_width//2 + 10,
        pouch_y - pouch_height//2 + 20
    ], fill=COLORS["secondary"])
    
    # Add text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Brand name
    add_text_with_shadow(draw, (pouch_x - 100, pouch_y - 100), "FitCafe", font_large)
    
    # Tagline
    add_text_with_shadow(draw, (pouch_x - 140, pouch_y + 50), "Wellness Coffee", font_medium)
    
    # Save
    filepath = os.path.join("assets", filename)
    img.save(filepath)
    print(f"✅ Created: {filepath}")

def create_lifestyle_image(filename, text_lines, color_scheme="orange"):
    """Create lifestyle placeholder image"""
    width, height = 800, 1200
    
    # Choose colors
    if color_scheme == "orange":
        bg1, bg2 = COLORS["cream"], COLORS["accent"]
    elif color_scheme == "yellow":
        bg1, bg2 = COLORS["light"], COLORS["secondary"]
    else:
        bg1, bg2 = COLORS["cream"], COLORS["primary"]
    
    # Gradient background
    img = create_gradient_image(width, height, bg1, bg2)
    draw = ImageDraw.Draw(img)
    
    # Add decorative circles
    for i in range(5):
        x = 100 + i * 150
        y = 200 + (i % 2) * 100
        radius = 50 + (i % 3) * 20
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                    fill=COLORS["white"], outline=COLORS["primary"], width=2)
    
    # Add text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font_large = ImageFont.load_default()
    
    # Center text
    total_height = len(text_lines) * 80
    start_y = (height - total_height) // 2
    
    for i, line in enumerate(text_lines):
        text_x = (width - draw.textbbox((0, 0), line, font=font_large)[2]) // 2
        text_y = start_y + i * 80
        add_text_with_shadow(draw, (text_x, text_y), line, font_large)
    
    # Save
    filepath = os.path.join("assets", filename)
    img.save(filepath)
    print(f"✅ Created: {filepath}")

def create_badge_image(filename):
    """Create guarantee badge"""
    width, height = 400, 400
    
    # Circular badge
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle
    draw.ellipse([20, 20, 380, 380], fill=COLORS["primary"], outline=COLORS["light"], width=5)
    
    # Inner circle
    draw.ellipse([50, 50, 350, 350], fill=COLORS["light"], outline=COLORS["primary"], width=3)
    
    # Add text
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_regular = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
    
    # Text lines
    draw.text((200, 120), "180-DAY", fill=COLORS["text_dark"], font=font_bold, anchor="mm")
    draw.text((200, 200), "MONEY BACK", fill=COLORS["text_dark"], font=font_bold, anchor="mm")
    draw.text((200, 280), "GUARANTEE", fill=COLORS["text_dark"], font=font_bold, anchor="mm")
    
    # Save
    filepath = os.path.join("assets", filename)
    img.save(filepath)
    print(f"✅ Created: {filepath}")

# Main execution
print("=" * 60)
print("FitCafe Image Generator v2")
print("=" * 60)

# Product image
create_product_image("hero-product-real.jpg")

# Lifestyle images
create_lifestyle_image("morning-ritual.jpg", ["Morning", "Ritual"], "orange")
create_lifestyle_image("ingredients-visual.jpg", ["Natural", "Ingredients"], "yellow")
create_lifestyle_image("work-from-home.jpg", ["Work From", "Home"], "orange")
create_lifestyle_image("about-story.jpg", ["Our", "Story"], "orange")
create_lifestyle_image("testimonials-collage.jpg", ["Customer", "Stories"], "orange")
create_lifestyle_image("optin-flatlay.jpg", ["Free", "Morning", "Reset Guide"], "yellow")
create_lifestyle_image("cta-hero.jpg", ["Try FitCafe", "Risk-Free"], "orange")
create_lifestyle_image("benefits-lifestyle.jpg", ["Wellness", "Benefits"], "orange")

# Badge
create_badge_image("guarantee-badge.png")

print("\n" + "=" * 60)
print("✅ All images created successfully!")
print("=" * 60)
