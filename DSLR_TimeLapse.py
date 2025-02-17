# Jose Marquez Doblas
# Canon EOS 1200D TimeLapse

# import gphoto2 as gp
import os
import time
import cv2
import pyrealsense2 as rs
import numpy as np
# Configuration
N_PHOTOS = 9999
LAPSE = 1
CAMERA_DELAY = 0
IMG_PATH = "/home/iiitb/Pictures/"
VID_PATH = "/home/iiitb/Pictures/video.avi"


def configured_camera():
 
    config = rs.config()
        
    config.enable_stream(rs.stream.depth, 1280 , 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920 , 1080, rs.format.bgr8, 30)

    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    sensor = profile.get_device().query_sensors()[0]
    sensor.set_option(rs.option.hdr_enabled, 1)

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    # depth_sensor = profile.get_device().first_depth_sensor()
    # depth_scale = depth_sensor.get_depth_scale()
    # print("Depth Scale is: " , depth_scale)

    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    # align_to = rs.stream.color
    # align = rs.align(align_to)
    # return pipeline,align
    return pipeline

def take_photos():
    pipeline= configured_camera()
    ctr=0
    hdr = rs.hdr_merge() # needs to be declared once
    for ctr in range(N_PHOTOS):
        frames = pipeline.wait_for_frames()
        frames = hdr.process(frames).as_frameset()
        color_frame=frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        aligned_depth_frame=depth_frame
        # Align the depth frame to color frame
        # aligned_frames = align.process(frames)

        # Get aligned frames
        # aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        # color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        # if not aligned_depth_frame or not color_frame:
        #     continue
        # depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics


        target = os.path.join(IMG_PATH,str(ctr))
        print('Copying image to', target)
        cv2.imwrite(IMG_PATH+str(ctr)+'_rgb.png', np.asanyarray(color_frame.get_data())) 
        cv2.imwrite(IMG_PATH+str(ctr)+'_depth.png', np.asanyarray(aligned_depth_frame.get_data()))
        time.sleep(lapse_time())

    pipeline.stop()

def create_video():

    images = [img for img in os.listdir(IMG_PATH) if img.endswith("_rgb.png")]
    
    frame = cv2.imread(os.path.join(IMG_PATH, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(VID_PATH, 0, 5, (width, height))

    print("Creating the video")
    for image in images:
        video.write(cv2.imread(os.path.join(IMG_PATH, image)))

    cv2.destroyAllWindows()
    video.release()
    print("Video Created")


# Calculate the time between photos taking into account the camera delay
def lapse_time():
    time = 0
    if LAPSE > CAMERA_DELAY:
        time = LAPSE - CAMERA_DELAY

    return time


if __name__ == "__main__":
    # take_photos()
    create_video()