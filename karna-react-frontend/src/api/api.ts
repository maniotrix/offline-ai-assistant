import { BoundingBox, ImageDataResponse } from '../types/types';
import { websocketService } from './websocket';
import { karna } from '../generated/messages';
import { REST } from './constants';
import useVisionDetectStore from '../stores/visionDetectStore';

// REST APIs for non-real-time operations
export const fetchAnnotations = async (): Promise<ImageDataResponse> => {
    const response = await fetch(REST.GET_IMAGE_DATA);
    if (!response.ok) {
        throw new Error('Failed to fetch image data');
    }
    return response.json();
};

export const saveAnnotations = async (): Promise<any> => {
    // Get the current state from the vision detect store
    const store = useVisionDetectStore.getState();
    
    // Create a VisionDetectResultsList proto message with all images and their annotations
    const resultsList: karna.vision.IVisionDetectResultsList = {
        results: [],
        projectUuid: '',
        commandUuid: ''
    };
    
    // Get project and command UUIDs from the first image (they should be the same for all images)
    const firstImage = Object.values(store.images)[0];
    if (firstImage) {
        resultsList.projectUuid = firstImage.projectUuid || '';
        resultsList.commandUuid = firstImage.commandUuid || '';
    }
    
    // Add all images from the store to the results list
    Object.values(store.images).forEach(image => {
        // Convert BoundingBox[] to IUiIconBoundingBox[]
        const mergedUiIconBboxes = image.annotations.map(ann => ({
            id: ann.id,
            x: ann.x,
            y: ann.y,
            width: ann.width,
            height: ann.height,
            className: ann.class,
            confidence: ann.confidence
        }));
        
        // Create a result model for each image
        const resultModel: karna.vision.IVisionDetectResultModel = {
            eventId: image.eventId,
            projectUuid: image.projectUuid,
            commandUuid: image.commandUuid,
            timestamp: image.timestamp,
            description: image.description,
            originalImagePath: image.originalImagePath,
            originalWidth: image.originalWidth,
            originalHeight: image.originalHeight,
            isCropped: image.isCropped,
            mergedUiIconBboxes: mergedUiIconBboxes,
            croppedImage: image.croppedImage,
            croppedWidth: image.croppedWidth,
            croppedHeight: image.croppedHeight
        };
        
        resultsList.results!.push(resultModel);
    });
    
    // Send the updated results via WebSocket
    try {
        await websocketService.updateVisionDetectResults(resultsList);
        return { success: true };
    } catch (error) {
        console.error('Failed to save annotations via WebSocket:', error);
        throw new Error('Failed to save annotations');
    }
};

// Use the generated protobuf StatusResult interface
export type Status = karna.status.IStatusResult;

// WebSocket connection management
export const connectWebSocket = (): void => {
    websocketService.connect();
};

export const disconnectWebSocket = (): void => {
    websocketService.disconnect();
};

// Command execution via WebSocket
export const executeCommand = async (command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> => {
    return websocketService.sendCommand(command, domain);
};

// Status request via WebSocket
export const requestStatus = async (): Promise<void> => {
    return websocketService.requestStatus();
};

// Screenshot request via WebSocket
export const getScreenshot = async (): Promise<string> => {
    const response = await fetch(REST.SCREENSHOT);
    if (!response.ok) {
        throw new Error('Failed to get screenshot');
    }
    const blob = await response.blob();
    return URL.createObjectURL(blob);
};
