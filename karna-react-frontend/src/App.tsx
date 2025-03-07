import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Homepage from "./components/Home/Homepage";
import BboxEditor from "./components/Editor/BboxEditor";
import { websocketService } from "./api/websocket";

const App: React.FC = () => {
  useEffect(() => {
    // Initialize WebSocket connection with the new approach
    websocketService.connect();

    // Cleanup on unmount
    return () => {
      websocketService.disconnect();
    };
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/editor" element={<BboxEditor />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
