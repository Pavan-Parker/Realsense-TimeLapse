# Jose Marquez Doblas
# Canon EOS 1200D TimeLapse

# import gphoto2 as gp
import os
import time
import cv2
import pyrealsense2 as rs
# Configuration
N_PHOTOS = 10
LAPSE = 1
CAMERA_DELAY = 0  # Canon EOS 1200D delay
IMG_PATH = "~/Pictures/"
VID_PATH = "~/Pictures/video.avi"


def configured_camera():
    # # Getting the camera
    # context = gp.Context()
    # cam = gp.Camera()
    # cam.init(context)

    # print(cam.get_summary(context))
    # return cam
        # Create a pipeline
##########
    config = rs.config()
    config.enable_stream(rs.stream.infrared,1, 848, 480, rs.format.y8, 60)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)

    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    sensor = profile.get_device().query_sensors()[0]
    sensor.set_option(rs.option.hdr_enabled, 1)
##########
    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: " , depth_scale)

    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)
    return pipeline,align
def take_photos():
    pipeline,align = configured_camera()
    ctr=0
    for ctr in range(N_PHOTOS):

        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue
        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics


        target = os.path.join(IMG_PATH,ctr)
        print('Copying image to', target)
        cv2.imwrite(color_img_path, color_img) 
cv2.imwrite(depth_img_path), depth_img)
        camera_file = gp.check_result(gp.gp_camera_file_get(cam,
                                      file_path.folder,
                                      file_path.name,
                                      gp.GP_FILE_TYPE_NORMAL))

        gp.check_result(gp.gp_file_save(camera_file, target))
        time.sleep(lapse_time())

    gp.check_result(gp.gp_camera_exit(cam))


def create_video():
    images = [img for img in os.listdir(IMG_PATH) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(IMG_PATH, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(VID_PATH, 0, 24, (width, height))

    print "Creating the video"
    for image in images:
        video.write(cv2.imread(os.path.join(IMG_PATH, image)))

    cv2.destroyAllWindows()
    video.release()
    print "Video Created"


# Calculate the time between photos taking into account the camera delay
def lapse_time():
    time = 0
    if LAPSE > CAMERA_DELAY:
        time = LAPSE - CAMERA_DELAY

    return time


if __name__ == "__main__":
    take_photos()
    create_video()