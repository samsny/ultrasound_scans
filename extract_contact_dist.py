import cv2
import numpy as np
from pathlib import Path
import csv
import os
import glob 
import random 

# define a function to display the coordinates of the points clicked on the image
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(f'({x},{y})')
        cPoints.append([x,y])
        # put coordinates as text on the image
        cv2.putText(img, f'({x},{y})',(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # draw point on the image
        cv2.circle(img, (x,y), 3, (0,255,255), -1)

    return cPoints

outputdir = 'output\\'
all_jpg_files = glob.glob(os.path.join(outputdir, '**', '*.jpg'), recursive=True)
# filter the list to include only files with "stitched_image" in the name
stitched_image_files = [file for file in all_jpg_files if 'stitched_image' in os.path.basename(file)]
results = []

random.shuffle(stitched_image_files) # Loop through this in random order 
for filename in stitched_image_files: 
    if os.path.isfile(filename):
        if filename.endswith(".jpg"):
            cPoints = []
            image = str(filename)
            fileName = Path(image)
            # read input image
            img = cv2.imread(image)
            # create a window
            cv2.namedWindow('Point Coordinates')
            # bind the callback function to window
            cv2.setMouseCallback('Point Coordinates', click_event)
            # display the image
            while True:
                cv2.imshow('Point Coordinates',img)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
         
            contactDistCoord = np.sqrt((cPoints[0][0]-cPoints[1][0])**2+(cPoints[0][1]-cPoints[1][1])**2)*0.0109
            # android contact distance scaling
            # contactDistCoord = np.sqrt((cPoints[0][0]-cPoints[1][0])**2+(cPoints[0][1]-cPoints[1][1])**2)*0.0103

            file_label = str(os.path.basename(os.path.dirname(fileName))+'_'+fileName.name)
            results.append([file_label,contactDistCoord])
            # close image        
            cv2.destroyAllWindows()

# save labeled image distances to csv file
with open(outputdir+'labeled_images.csv', 'w', newline='') as myfile: 
    write = csv.writer(myfile)
    write.writerows(results)
