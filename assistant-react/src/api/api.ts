import { BoundingBox, ImageDataResponse } from '../types/types';

/**
 * Fetch bounding boxes and image URL from the Flask backend.
 */
export const fetchAnnotations = async (): Promise<ImageDataResponse> => {
  const response = await fetch('/api/get_image_data');
  if (!response.ok) {
    throw new Error('Failed to fetch image data');
  }
  return response.json();
};

/**
 * Save bounding boxes to the backend.
 */
export const saveAnnotations = async (imageUrl: string, annotations: BoundingBox[]): Promise<any> => {
  const response = await fetch('/api/save_bboxes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      imageUrl,  // Ensure image URL is sent
      boundingBoxes: annotations
    })
  });

  if (!response.ok) {
    throw new Error('Failed to save annotations');
  }
  return response.json();
};
