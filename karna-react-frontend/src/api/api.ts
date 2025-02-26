import { BoundingBox, ImageDataResponse } from '../types/types';
import { websocketService } from './websocket';
import { karna } from '../generated/messages';
import { REST } from './constants';

// REST APIs for non-real-time operations
export const fetchAnnotations = async (): Promise<ImageDataResponse> => {
    const response = await fetch(REST.GET_IMAGE_DATA);
    if (!response.ok) {
        throw new Error('Failed to fetch image data');
    }
    return response.json();
};

export const saveAnnotations = async (imageUrl: string, annotations: BoundingBox[]): Promise<any> => {
    const response = await fetch(REST.SAVE_BBOXES, {
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

// Use the generated protobuf Status interface
export type Status = karna.IStatus;

// Using WebSocket for real-time command execution
export const executeCommand = async (command: string, domain: string = 'default'): Promise<karna.ICommandResult> => {
    return websocketService.sendCommand(command, domain);
};

// Using WebSocket for status updates
export const getStatus = async (): Promise<Status> => {
    await websocketService.requestStatus();
    // The actual status will be received through the status update subscription
    return { vision: '', language: '', command: '' };
};

export const subscribeToStatus = (callback: (status: Status) => void): () => void => {
    return websocketService.onStatusUpdate(callback);
};

export const subscribeToCommandResponse = (callback: (response: karna.ICommandResult) => void): () => void => {
    return websocketService.onCommandResponse(callback);
};

export const subscribeToErrors = (callback: (error: Error) => void): () => void => {
    return websocketService.onError(callback);
};

export const getScreenshot = async (): Promise<string> => {
    const response = await fetch(REST.SCREENSHOT);
    if (!response.ok) {
        throw new Error('Failed to fetch screenshot');
    }
    const data = await response.json();
    return data.screenshot;
};
