import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import CanvasEditor from "./components/CanvasEditor/CanvasEditor";
import ClassSelector from "./components/ClassSelector/ClassSelector";
import Header from "./components/Header/Header";
import Homepage from "./components/home/Homepage";
import { fetchAnnotations } from "./api/api";
import useAnnotationStore from "./stores/annotationStore";
import { Box } from "@mui/material";

const EditorLayout = ({ imageUrl, onCancel }: { imageUrl: string | null, onCancel: () => void }) => (
  <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
    <Header imageUrl={imageUrl} onCancel={onCancel} />
    <Box sx={{ display: "flex", flexGrow: 1, marginTop: "64px" }}>
      <ClassSelector />
      <CanvasEditor />
    </Box>
  </Box>
);

const App: React.FC = () => {
  const { setAnnotations } = useAnnotationStore();
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    const loadAnnotations = async () => {
      try {
        const data = await fetchAnnotations();
        setAnnotations(data.boundingBoxes);
        setImageUrl(data.imageUrl);
      } catch (error) {
        console.error("Error fetching annotations:", error);
      }
    };
    loadAnnotations();
  }, [setAnnotations]);

  const handleCancel = () => {
    console.log("Cancel button clicked");
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/editor" element={<EditorLayout imageUrl={imageUrl} onCancel={handleCancel} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
