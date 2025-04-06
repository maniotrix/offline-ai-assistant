from PIL import Image, ImageDraw

import os

      
def merge_images(image_files, output_dir, output_filename):
    images = []
    for image_file in image_files:
        images.append(Image.open(image_file))


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
        
        output_path = os.path.join(output_dir, output_filename)
        combined.save(output_path)
        print("Combined image saved at:", output_path)
    else:
        print("No images found")
    pass

def merge_all_screenshots_in_dir():
    # Directory with screenshots 
    screenshots_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ground_data/screenshots')
    raw_screenshots_directory = os.path.join(screenshots_directory, 'raw')

    # Collect all PNG/JPG images in the directory, sorted alphabetically
    image_files = sorted([f for f in os.listdir(raw_screenshots_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    images = [os.path.join(raw_screenshots_directory, f) for f in image_files]

    merge_images(images, screenshots_directory, 'combined_screenshots_with_separator.png')
    
def merge_selected_screenshots_in_dir():
    # Directory with screenshots 
    screenshots_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ground_data/screenshots')
    raw_screenshots_directory = os.path.join(screenshots_directory, 'raw')

    # Collect all PNG/JPG images in the directory, sorted alphabetically
    image_file_names = [
        'annotated_screenshot_20250327_165159_546611.png',
        'annotated_screenshot_20250327_165201_486128.png',
        'annotated_screenshot_20250327_165220_545152.png',
        'annotated_screenshot_20250327_165331_494499.png',
        'annotated_screenshot_20250327_165336_540238.png',
        ]
    images = [os.path.join(raw_screenshots_directory, f) for f in image_file_names]

    merge_images(images, screenshots_directory, 'combined_screenshots_with_separator.png')
    
if __name__ == "__main__":
    merge_all_screenshots_in_dir()
    # merge_selected_screenshots_in_dir()
