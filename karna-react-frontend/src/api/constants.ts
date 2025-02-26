/**
 * API Route Constants
 * 
 * This file defines constants for all API endpoints used in the frontend.
 * It should be kept in sync with the backend constants.
 */

export const RestEndpoints = {
    // REST API endpoints
    HEALTH: "/health",
    SCREENSHOT: "/api/screenshot",
    ACTIVE_CLIENTS: "/ws/clients",
    GET_IMAGE_DATA: "/api/get_image_data",
    SAVE_BBOXES: "/api/save_bboxes",
};

export const WebSocketEndpoints = {
    // WebSocket endpoints
    COMMAND: "/ws/command",
    STATUS: "/ws/status",
    // Base URL for WebSocket connections
    getBaseUrl: (hostname: string = window.location.hostname, port: number = 8000): string => {
        return `ws://${hostname}:${port}`;
    }
};

// Re-export for easier imports
export const REST = RestEndpoints;
export const WS = WebSocketEndpoints;