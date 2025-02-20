import { BoundingBox } from '../../types/types';

/**
 * Adjusts bounding box coordinates based on the current zoom level.
 * Useful for ensuring pixel-level accuracy when sending data to the backend.
 */
export const adjustBoundingBoxCoordinates = (bbox: BoundingBox, zoomLevel: number): BoundingBox => {
  return {
    ...bbox,
    x: bbox.x / zoomLevel,
    y: bbox.y / zoomLevel,
    width: bbox.width / zoomLevel,
    height: bbox.height / zoomLevel,
  };
};
