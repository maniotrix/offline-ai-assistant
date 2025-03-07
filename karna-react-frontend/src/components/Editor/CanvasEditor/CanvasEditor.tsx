import React, { useEffect, useRef, useState } from "react";
import {
  Stage,
  Layer,
  Rect,
  Image,
  Text as KonvaText,
  Group,
  Transformer,
} from "react-konva";
import useAnnotationStore from "../../../stores/annotationStore";
import { BoundingBox, ImageDataResponse } from "../../../types/types";
import { fetchAnnotations } from "../../../api/api";

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
    annotations,
    setAnnotations,
    pushToHistory,
    selectedAnnotationId,
    setSelectedAnnotationId,
    selectedClasses,
    isSidebarOpen,
  } = useAnnotationStore();

  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const stageRef = useRef<any>(null);
  const transformerRef = useRef<any>(null);
  const backgroundImage = useImage(imageUrl);

  useEffect(() => {
    const loadAnnotations = async () => {
      try {
        const data: ImageDataResponse = await fetchAnnotations();
        setAnnotations(data.boundingBoxes);
        setImageUrl(data.imageUrl);
      } catch (error) {
        console.error("Error fetching annotations:", error);
      }
    };
    loadAnnotations();
  }, [setAnnotations]);

  // ✅ Store a unique random color for each class
  const [classColors, setClassColors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];

    const newClassColors: { [key: string]: string } = {};
    uniqueClasses.forEach((cls) => {
      if (!classColors[cls]) {
        newClassColors[cls] = generateRandomColor();
      } else {
        newClassColors[cls] = classColors[cls];
      }
    });

    setClassColors(newClassColors);
  }, [annotations]);

useEffect(() => {
  if (transformerRef.current) {
    const selectedNode = stageRef.current?.findOne(`#rect-${selectedAnnotationId}`);

    // ✅ Hide Transformer when no classes are selected
    if (selectedNode && selectedClasses.size > 0) {
      transformerRef.current.nodes([selectedNode]);
      transformerRef.current.getLayer().batchDraw();
    } else {
      transformerRef.current.nodes([]); // ✅ Hide transformer when no checkboxes are selected
    }
  }
}, [selectedAnnotationId, annotations, selectedClasses]);

// ✅ Track when dragging starts to store history once
const handleDragStart = () => {
  pushToHistory(); // ✅ Store previous state ONCE when dragging starts
};

  // ✅ Handle dragging a bounding box
  const handleDragMove = (e: any, bboxId: string) => {
    const node = e.target;
    const nodeAttrs = node.attrs;
    const { x, y } = nodeAttrs;

    const updatedAnnotations = annotations.map((box) =>
      box.id === bboxId ? { ...box, x: x, y: y } : box
    );
    setAnnotations(updatedAnnotations);
  };

  // ✅ Handle resizing of a bounding box (Fixed issue with shifting)
  const handleTransformEnd = () => {
    if (!transformerRef.current) return;

    pushToHistory(); // ✅ Store previous state before modifying

    const node = transformerRef.current.nodes()[0]; // Get the selected node
    if (!node) return;

    const bboxId = node.id().replace("rect-", ""); // Extract ID
    const nodeAttrs = node.attrs;
    const { x, y } = nodeAttrs;
    console.log("node0", { x, y });
    const newScaleX = node.scaleX();
    const newScaleY = node.scaleY();
    console.log("node1", node);

    // Find the existing bbox
    const bboxIndex = annotations.findIndex((box) => box.id === bboxId);
    if (bboxIndex === -1) return;

    // Get the original bbox and apply scaling adjustments
    const originalBBox = annotations[bboxIndex];
    const newWidth = originalBBox.width * newScaleX;
    const newHeight = originalBBox.height * newScaleY;

    // Reset scale to prevent unwanted stretching
    node.scaleX(1);
    node.scaleY(1);
    console.log("node2", node);

    const updatedAnnotations = [...annotations];
    updatedAnnotations[bboxIndex] = {
      ...originalBBox,
      width: newWidth,
      height: newHeight,
      x:x,
      y:y
    };

    setAnnotations(updatedAnnotations);
  };

  return (
    <div
      style={{
        marginLeft: isSidebarOpen ? 240 : 0,
        transition: "margin 0.3s ease",
      }}
    >
      <Stage
        width={window.innerWidth - (isSidebarOpen ? 240 : 0)}
        height={window.innerHeight}
        ref={stageRef}
      >
        <Layer>
          {backgroundImage && (
            <Image
              image={backgroundImage}
              x={0}
              y={0}
            />
          )}

          {/* Render Bounding Boxes Only If Classes Are Selected */}
          {annotations
            .filter(
              (bbox) =>
                selectedClasses.size > 0 && selectedClasses.has(bbox.class)
            )
            .map((bbox) => {
              const bboxColor = classColors[bbox.class] || "blue";

              return (
                <Rect
                    key={bbox.id}
                    id={`rect-${bbox.id}`}
                    x={bbox.x}
                    y={bbox.y}
                    draggable
                    onClick={() => setSelectedAnnotationId(bbox.id)}
                    onDragStart={handleDragStart} // ✅ Store history before dragging
                    onDragMove={(e) => handleDragMove(e, bbox.id)}
                    onDragEnd={(e) => handleDragMove(e, bbox.id)} // ✅ Unique ID for Transformer attachment
                    width={bbox.width}
                    height={bbox.height}
                    fill={
                      bbox.id === selectedAnnotationId
                        ? `${bboxColor}50`
                        : "transparent"
                    } // ✅ Translucent Fill on Selection
                    stroke={bboxColor} // Assign unique color
                    strokeWidth={1}
                  />
              );
            })}

          {/* ✅ Transformer should be rendered inside the Layer and attached correctly */}
          <Transformer
            ref={transformerRef}
            onTransformEnd={handleTransformEnd}
          />
        </Layer>
        {/* Add Layer for Text */}
        <Layer>
          {annotations
            .filter(
              (bbox) =>
                selectedClasses.size > 0 && selectedClasses.has(bbox.class)
            )
            .map((bbox) => (
              <KonvaText
                key={`text-${bbox.id}`}
                x={bbox.x}
                y={bbox.y - 20} // Position text above the bounding box
                text={`${bbox.class} (x: ${Math.round(
                  bbox.x
                )}, y: ${Math.round(bbox.y)}, w: ${Math.round(
                  bbox.width
                )}, h: ${Math.round(bbox.height)})`}
                fontSize={16}
                fill={classColors[bbox.class] || "black"}
              />
            ))}
        </Layer>
      </Stage>
    </div>
  );
};

export default CanvasEditor;
