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
            imageUrl,
            boundingBoxes: annotations
        })
    });

    if (!response.ok) {
        throw new Error('Failed to save annotations');
    }
    return response.json();
};

// Match the Status interface from websocket.ts
export interface Status {
    vision: string;
    language: string;
    command: string;
}

// Using WebSocket for real-time command execution
export const executeCommand = async (command: string): Promise<any> => {
    return websocketService.sendCommand(command);
};

// Using WebSocket for status updates
export const getStatus = async (): Promise<Status> => {
    try {
        await websocketService.requestStatus();
        // The actual status will be received through the status update subscription
        return { vision: '', language: '', command: '' };
    } catch (error) {
        throw new Error('Failed to fetch status');
    }
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
