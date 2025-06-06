import React, { useEffect, useRef, useState, useMemo } from "react";
import {
  Stage,
  Layer,
  Rect,
  Image,
  Text as KonvaText,
  Group,
  Transformer,
} from "react-konva";
import useVisionDetectStore from "../../../stores/visionDetectStore";
import { BoundingBox } from "../../../types/types";

// ✅ Generate a random color for each class
const generateRandomColor = (): string => {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

const CanvasEditor: React.FC = () => {
  const {
    currentImageId,
    images,
    selectedClasses,
    setAnnotations,
    pushToHistory,
    setSelectedAnnotationId,
  } = useVisionDetectStore();

  const currentImage = currentImageId ? images[currentImageId] : null;
  const annotations = currentImage?.annotations || [];
  const selectedAnnotationId = currentImage?.selectedAnnotationId;

  const stageRef = useRef<any>(null);
  const transformerRef = useRef<any>(null);
  
  // Use state for the image element
  const [backgroundImage, setBackgroundImage] = useState<HTMLImageElement | null>(null);
  
  // Process the image data when currentImage changes
  useEffect(() => {
    if (!currentImage?.croppedImage) {
      setBackgroundImage(null);
      return;
    }
    
    // Convert binary data to base64 string for Konva Image
    const uint8Array = new Uint8Array(currentImage.croppedImage);
    const blob = new Blob([uint8Array], { type: 'image/png' });
    
    // Use FileReader to get base64
    const reader = new FileReader();
    reader.onload = () => {
      // Create an image element from the base64 data
      const img = new window.Image();
      img.crossOrigin = "Anonymous";
      img.onload = () => {
        setBackgroundImage(img);
      };
      img.src = reader.result as string;
    };
    reader.readAsDataURL(blob);
    
    // In this case, the effect is only concerned with processing the image data (croppedImage), 
    // so it makes sense to only depend on that specific property rather than the entire object.
  }, [currentImage?.croppedImage]);

  // Use useRef instead of useState to maintain a persistent object that doesn't trigger re-renders
  const classColorsRef = useRef<{ [key: string]: string }>({});

  // Update class colors when annotations change
  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    
    uniqueClasses.forEach((cls) => {
      if (!classColorsRef.current[cls]) {
        classColorsRef.current[cls] = generateRandomColor();
      }
    });
  }, [annotations]);

  useEffect(() => {
    if (transformerRef.current) {
      const selectedNode = stageRef.current?.findOne(`#rect-${selectedAnnotationId}`);

      if (selectedNode && selectedClasses.size > 0) {
        transformerRef.current.nodes([selectedNode]);
        transformerRef.current.getLayer().batchDraw();
      } else {
        transformerRef.current.nodes([]);
      }
    }
  }, [selectedAnnotationId, annotations, selectedClasses]);

  const handleDragEnd = (e: any, bbox: BoundingBox) => {
    const node = e.target;
    const updatedAnnotations = annotations.map((ann) =>
      ann.id === bbox.id
        ? {
            ...ann,
            x: Math.round(node.x()),
            y: Math.round(node.y()),
          }
        : ann
    );

    if (currentImageId) {
      pushToHistory(currentImageId);
      setAnnotations(currentImageId, updatedAnnotations);
    }
  };

  const handleTransformEnd = (e: any, bbox: BoundingBox) => {
    const node = e.target;
    const scaleX = node.scaleX();
    const scaleY = node.scaleY();

    node.scaleX(1);
    node.scaleY(1);

    const updatedAnnotations = annotations.map((ann) =>
      ann.id === bbox.id
        ? {
            ...ann,
            x: Math.round(node.x()),
            y: Math.round(node.y()),
            width: Math.round(Math.max(5, node.width() * scaleX)),
            height: Math.round(Math.max(5, node.height() * scaleY)),
          }
        : ann
    );

    if (currentImageId) {
      pushToHistory(currentImageId);
      setAnnotations(currentImageId, updatedAnnotations);
    }
  };

  const handleSelect = (id: string) => {
    if (currentImageId) {
      setSelectedAnnotationId(currentImageId, id);
    }
  };

  if (!backgroundImage || !currentImage) return null;

  return (
    <Stage
      width={currentImage.croppedWidth || 800}
      height={currentImage.croppedHeight || 600}
      ref={stageRef}
    >
      <Layer>
        <Image image={backgroundImage} />
        {annotations
          .filter((bbox) => selectedClasses.has(bbox.class))
          .map((bbox) => (
            <Group key={bbox.id}>
              <Rect
                id={`rect-${bbox.id}`}
                x={bbox.x}
                y={bbox.y}
                width={bbox.width}
                height={bbox.height}
                stroke={classColorsRef.current[bbox.class] || "#00ff00"}
                strokeWidth={2}
                draggable
                onClick={() => handleSelect(bbox.id)}
                onTap={() => handleSelect(bbox.id)}
                onDragEnd={(e) => handleDragEnd(e, bbox)}
                onTransformEnd={(e) => handleTransformEnd(e, bbox)}
              />
              <KonvaText
                x={bbox.x}
                y={bbox.y - 20}
                text={bbox.class}
                fontSize={12}
                fill={classColorsRef.current[bbox.class] || "#00ff00"}
              />
            </Group>
          ))}
        <Transformer
          ref={transformerRef}
          boundBoxFunc={(oldBox, newBox) => {
            // Limit resize
            newBox.width = Math.max(5, newBox.width);
            newBox.height = Math.max(5, newBox.height);
            return newBox;
          }}
        />
      </Layer>
    </Stage>
  );
};

export default CanvasEditor;
