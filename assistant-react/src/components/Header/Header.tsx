import React from "react";
import { AppBar, Toolbar, Typography, IconButton, Box } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import useAnnotationStore from "../../stores/annotationStore";
import ToolbarButtons from "../Toolbar/Toolbar"; // Import Toolbar buttons

interface HeaderProps {
  imageUrl: string | null;
  onCancel: () => void;
}

const Header: React.FC<HeaderProps> = ({ imageUrl, onCancel }) => {
  const { toggleSidebar } = useAnnotationStore();

  return (
    <AppBar position="fixed" sx={{ zIndex: 1200, backgroundColor: "#1976d2" }}>
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        {/* Left Side: Sidebar Toggle & Title */}
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <IconButton edge="start" color="inherit" onClick={toggleSidebar} sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6">YOLO Bounding Box Editor</Typography>
        </Box>

        {/* Right Side: Save & Cancel Buttons */}
        <ToolbarButtons imageUrl={imageUrl} onCancel={onCancel} />
      </Toolbar>
    </AppBar>
  );
};

export default Header;
