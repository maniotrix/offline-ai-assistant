export interface BoundingBox {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  class: string;  // Class name from the proto
  confidence?: number; // New field from proto
}

export interface ImageDataResponse {
  imageUrl: string;
  originalWidth: number;
  originalHeight: number;
  boundingBoxes: BoundingBox[];
}
