from typing import Any
import uuid
from PIL import Image

def export_bounding_boxes(model, image_path : str, results : Any):
    """
    Convert YOLO results into the specified JSON format with automatically extracted image dimensions.

    Parameters:
        model (YOLO): YOLO model.
        image_path (str): Path to the image.
        results (list): YOLO detection results.

    Returns:
        dict: JSON-like dictionary containing bounding boxes.
    """
    # Open the image to get its dimensions
    with Image.open(image_path) as img:
        original_width, original_height = img.size

    bounding_boxes = []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes in (x_min, y_min, x_max, y_max)
        labels = result.boxes.cls.cpu().numpy()  # Class labels (index)
        confidences = result.boxes.conf.cpu().numpy()  # Confidence scores

        for box, label, conf in zip(boxes, labels, confidences):
            x_min, y_min, x_max, y_max = box
            width = x_max - x_min
            height = y_max - y_min
            bounding_boxes.append({
                "id": str(uuid.uuid4()),  # Unique ID for each bounding box
                "x": int(x_min),
                "y": int(y_min),
                "width": int(width),
                "height": int(height),
                "class": model.names[int(label)], # type: ignore
                "confidence": float(conf)
            })

    return {
        "imagePath": image_path,
        "originalWidth": original_width,
        "originalHeight": original_height,
        "boundingBoxes": bounding_boxes
    }