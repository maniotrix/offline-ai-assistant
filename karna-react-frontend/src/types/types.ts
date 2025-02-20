export interface BoundingBox {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  class: string;  // New field from API
}

export interface ImageDataResponse {
  imageUrl: string;
  originalWidth: number;
  originalHeight: number;
  boundingBoxes: BoundingBox[];
}
