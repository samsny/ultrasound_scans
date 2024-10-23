# Code to stitch together ultrasound images and extract distances from the image

### Initial steps:
1. Create a Fork of the repository
2. Clone repository
3. Install dependencies by running:
    
```rb
conda env create -f environment.yml
```

4. Activate environment by running
```rb
conda activate ultrasound_scan_env
```
  
For windows Visual Studio Code, activate environment from Command Palette (Ctrl+Shift+P), type and select Python: Select Interpreter, and then select ultrasound_scan_env from drop down list. 
       
### Stitch together images:

Place data in folder labeled "data". Within data folder, there should be subfolders corresponding to each subject. The name of subfolders is not important. Example folder structure: 
```
data/
├── S01/
│   ├── video_1.mp4
│   ├── video_2.mp4
│   ├── ...
│   └── video_n.mp4
├── S02/
│   ├── video_1.mp4
│   ├── video_2.mp4
│   ├── ...
│   └── video_n.mp4
```
Once data folder is set up, run ```stitch_image.py```. It may take a few minutes to stitch together each image. The code extracts 10 frames per second, and stitches together the frames into a single image. 

### Extract distances within images:

Check that stitched images appear within each subject folder with "stitched_image.jpg" appended to end of file name. Run ```extract_contact_distance.py```. When image appears on screen, select two points of interest and then click "Esc". After all images are looped through, images will appear in a random order and will be saved with subject folder label and file name in csv file along with corresponding distance. Rename csv file at end of code if needed.
