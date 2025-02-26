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

// Use the generated protobuf StatusResult interface
export type Status = karna.status.IStatusResult;

// WebSocket Connection Management
export const connectWebSocket = (): void => {
    websocketService.connect();
};

export const disconnectWebSocket = (): void => {
    websocketService.disconnect();
};

// Command Channel APIs
export const executeCommand = async (command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> => {
    return websocketService.sendCommand(command, domain);
};

export const subscribeToCommandResponse = (callback: (response: karna.command.ICommandResult) => void): () => void => {
    return websocketService.onCommandResponse(callback);
};

// Status Channel APIs
export const requestStatus = async (): Promise<void> => {
    return websocketService.requestStatus();
};

export const subscribeToStatus = (callback: (status: Status) => void): () => void => {
    return websocketService.onStatusUpdate(callback);
};

// Error Handling
export const subscribeToErrors = (callback: (error: Error) => void): () => void => {
    return websocketService.onError(callback);
};

// Screenshot API
export const getScreenshot = async (): Promise<string> => {
    const response = await fetch(REST.SCREENSHOT);
    if (!response.ok) {
        throw new Error('Failed to fetch screenshot');
    }
    const data = await response.json();
    return data.screenshot;
};
