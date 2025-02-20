import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import useAnnotationStore from '../../stores/annotationStore';

interface AddBboxDialogProps {
  open: boolean;
  onClose: () => void;
}

const AddBboxDialog: React.FC<AddBboxDialogProps> = ({ open, onClose }) => {
  const { annotations, setAnnotations, pushToHistory } = useAnnotationStore();
  const [selectedClass, setSelectedClass] = useState('default');
  const [availableClasses, setAvailableClasses] = useState<string[]>([]);

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    if (!uniqueClasses.includes('ignore')) {
      uniqueClasses.push('ignore');
    }
    setAvailableClasses(uniqueClasses);
  }, [annotations]);

  const handleAddBbox = () => {
    pushToHistory(); // Push current state to history before adding new bbox
    const newBbox = {
      id: uuidv4(),
      x: window.innerWidth / 2 - 50, // Centered horizontally
      y: window.innerHeight / 2 - 50, // Centered vertically
      width: 100,
      height: 100,
      class: selectedClass,
    };
    setAnnotations([...annotations, newBbox]);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Add Bounding Box</DialogTitle>
      <DialogContent>
        <FormControl fullWidth margin="dense">
          <InputLabel>Class</InputLabel>
          <Select
            value={selectedClass}
            onChange={(e) => setSelectedClass(e.target.value as string)}
            label="Class"
          >
            {availableClasses.map((cls) => (
              <MenuItem key={cls} value={cls}>
                {cls}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleAddBbox} color="primary">
          Add
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddBboxDialog;
