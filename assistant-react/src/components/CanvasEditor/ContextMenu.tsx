import React from "react";
import { Menu, MenuItem } from "@mui/material";

interface ContextMenuProps {
  anchorEl: HTMLElement | null;
  onClose: () => void;
  onDelete: () => void;
  onEdit: () => void;
}

const ContextMenu: React.FC<ContextMenuProps> = ({ anchorEl, onClose, onDelete, onEdit }) => {
  const open = Boolean(anchorEl);

  return (
    <Menu
      anchorEl={anchorEl}
      open={open}
      onClose={onClose}
      PaperProps={{
        style: {
          maxHeight: 48 * 4.5,
          width: '20ch',
        },
      }}
    >
      <MenuItem onClick={onEdit}>Edit Label</MenuItem>
      <MenuItem onClick={onDelete}>Delete</MenuItem>
    </Menu>
  );
};

export default ContextMenu;