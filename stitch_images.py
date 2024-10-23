import cv2
import numpy as np
from datetime import timedelta
import os
from pathlib import Path


def stitchTogether(data_path):
    print('Stitching Image')

    stitchedImage = str(data_path) + '_stitched_image.jpg'
    
    # check if the stitched image already exists
    if Path(stitchedImage).exists():
        print(f"{stitchedImage} already exists. Continuing...")
    else: 
        imgs = []
        c = 0 
        data_path = Path(data_path)
        pathlist = data_path.glob('**/*.jpg')
        for path in pathlist:
            image_path = str(path)
            imgs.append(cv2.imread(image_path))
            imgs[c]=cv2.resize(imgs[c],(0,0),fx=0.6,fy=0.6)
            
            imgs[c] = imgs[c][65:394, 225:539] #TABLET
            #imgs[c] = imgs[c][60:320, 216:546] #PHONE 

            c = c + 1
            
        stitchy=cv2.Stitcher.create(mode =1) # set mode to 1 for scan of image
        (dummy,output)=stitchy.stitch(imgs)

        # save Image
        cv2.imwrite(stitchedImage,output)   

    
def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def main(video_file, img_output_path):
    filename,_ = os.path.splitext(img_output_path)
    filename += "-opencv"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        print('Extracting Frames')
        os.makedirs(filename)
        # read the video file    
        cap = cv2.VideoCapture(video_file)
        # get the FPS of the video
        fps = cap.get(cv2.CAP_PROP_FPS)
        # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
        SAVING_FRAMES_PER_SECOND = 10
        # i.e if video of duration 30 seconds, saves 10 frame per second = 300 frames saved in total
        saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
        # get the list of duration spots to save
        saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
        # start the loop
        count = 0
        while True:
            is_read, frame = cap.read()
            if not is_read:
                # break out of the loop if there are no frames to read
                break
            # get the duration by dividing the frame count by the FPS
            frame_duration = count / fps
            try:
                # get the earliest duration to save
                closest_duration = saving_frames_durations[1] # Skip first frame where screen is black
            except IndexError:
                # the list is empty, all duration frames were saved
                break
            if frame_duration >= closest_duration:
                # if closest duration is less than or equals the frame duration, 
                # then save the frame
                frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
                cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
                # drop the duration spot from the list, since this duration spot is already saved
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # increment the frame count
            count += 1
    
    return filename

if __name__ == "__main__":
    # data should be organized into subfolders with subjects and videos within each subject folder
    rootdir = 'data\\'
    outputdir = 'output\\'
    for subdir, dirs, files in os.walk(rootdir):
        for subject in dirs: 
            sub = subject
            subject_path = os.path.join(subdir, subject)
            for subdir2, _, subject_files in os.walk(subject_path):
                for file in subject_files:
                    scan_video_path = os.path.join(subdir,sub,file)
                    print('current file path',scan_video_path)
                    output_path = os.path.join(outputdir,sub,file)
                    output_file_path = main(scan_video_path, output_path)
                    stitchTogether(output_file_path)
      