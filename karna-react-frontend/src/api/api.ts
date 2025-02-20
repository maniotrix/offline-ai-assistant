import { BoundingBox, ImageDataResponse } from '../types/types';
import { websocketService } from './websocket';

// REST APIs for non-real-time operations
export const fetchAnnotations = async (): Promise<ImageDataResponse> => {
  const response = await fetch('/api/get_image_data');
  if (!response.ok) {
    throw new Error('Failed to fetch image data');
  }
  return response.json();
};

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

export interface Status {
  operation: string | null;
  status: string;
  message: string;
  progress: number;
}

// Using WebSocket for real-time command execution
export const executeCommand = async (command: string): Promise<void> => {
  websocketService.sendCommand(command);
};

// Using both REST and WebSocket for status
// REST for initial status, WebSocket for updates
export const getStatus = async (): Promise<Status> => {
  const response = await fetch('/api/status');
  if (!response.ok) {
    throw new Error('Failed to fetch status');
  }
  return response.json();
};

export const subscribeToStatus = (callback: (status: Status) => void) => {
  websocketService.onStatusUpdate(callback);
};

export const getScreenshot = async (): Promise<string> => {
  const response = await fetch('/api/screenshot');
  if (!response.ok) {
    throw new Error('Failed to fetch screenshot');
  }
  const data = await response.json();
  return data.screenshot;
};
