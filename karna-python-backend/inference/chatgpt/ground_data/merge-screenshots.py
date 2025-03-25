from PIL import Image, ImageDraw

import os

# Directory with screenshots in current directory
directory = os.path.dirname(os.path.abspath(__file__))

# Collect all PNG/JPG images in the directory, sorted alphabetically
image_files = sorted([f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

images = [Image.open(os.path.join(directory, f)) for f in image_files]

separator_height = 10  # Separator height in pixels
separator_color = (200, 200, 200)  # Light gray

if images:
    # Calculate maximum width and total height including separators
    width = max(im.width for im in images)
    total_height = sum(im.height for im in images) + separator_height * (len(images) - 1)
    
    combined = Image.new('RGB', (width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(combined)
    
    y_offset = 0
    for i, im in enumerate(images):
        combined.paste(im, (0, y_offset))
        y_offset += im.height
        
        # Add separator if not the last image
        if i < len(images) - 1:
            draw.rectangle([(0, y_offset), (width, y_offset + separator_height)], fill=separator_color)
            y_offset += separator_height
    
    output_path = os.path.join(directory, 'combined_screenshots_with_separator.png')
    combined.save(output_path)
    print("Combined image saved at:", output_path)
else:
    print("No images found")