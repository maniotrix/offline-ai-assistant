import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import useVisionDetectStore from '../../../stores/visionDetectStore';

interface AddBboxDialogProps {
  open: boolean;
  onClose: () => void;
}

const AddBboxDialog: React.FC<AddBboxDialogProps> = ({ open, onClose }) => {
  const { currentImageId, images, setAnnotations, pushToHistory } = useVisionDetectStore();
  const [selectedClass, setSelectedClass] = useState('default');
  const [availableClasses, setAvailableClasses] = useState<string[]>([]);

  const currentImage = currentImageId ? images[currentImageId] : null;
  const annotations = currentImage?.annotations || [];

  /**
   * Adds mandatory class names to the list of classes if they don't already exist
   * @param classes - The current list of class names
   * @returns The updated list with mandatory class names included
   */
  const addMandatoryClasses = (classes: string[]): string[] => {
    const mandatoryClasses = [
      'ignore', 
      'button', 
      'field', 
      'heading', 
      'iframe', 
      'image', 
      'label', 
      'link', 
      'text'
    ];
    
    const updatedClasses = [...classes];
    
    mandatoryClasses.forEach(className => {
      if (!updatedClasses.includes(className)) {
        updatedClasses.push(className);
      }
    });
    
    return updatedClasses;
  };

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    const classesWithMandatory = addMandatoryClasses(uniqueClasses);
    setAvailableClasses(classesWithMandatory);
  }, [annotations]);

  const handleAddBbox = () => {
    if (!currentImageId || !currentImage) return;

    pushToHistory(currentImageId);
    const newBbox = {
      id: uuidv4(),
      x: (currentImage.croppedWidth || 800) / 2 - 50,
      y: (currentImage.croppedHeight || 600) / 2 - 50,
      width: 100,
      height: 100,
      class: selectedClass,
    };
    setAnnotations(currentImageId, [...annotations, newBbox]);
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
