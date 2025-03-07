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

const useImage = (url: string | null) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    if (!url) return;
    const img = new window.Image();
    img.src = url;
    img.crossOrigin = "Anonymous";
    img.onload = () => setImage(img);
  }, [url]);

  return image;
};

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

  const imageUrl = currentImage?.croppedImage 
    ? URL.createObjectURL(new Blob([currentImage.croppedImage], { type: 'image/png' })) 
    : null;
  const backgroundImage = useImage(imageUrl);

  const [classColors] = useState<{ [key: string]: string }>({});

  // Generate colors for classes only when annotations change
  const updatedClassColors = useMemo(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    const newClassColors: { [key: string]: string } = { ...classColors };

    uniqueClasses.forEach((cls) => {
      if (!newClassColors[cls]) {
        newClassColors[cls] = generateRandomColor();
      }
    });

    return newClassColors;
  }, [annotations, classColors]);

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
                stroke={updatedClassColors[bbox.class] || "#00ff00"}
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
                fill={updatedClassColors[bbox.class] || "#00ff00"}
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
