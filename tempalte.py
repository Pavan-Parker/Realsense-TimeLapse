
####################################
    # Create a pipeline
    pipeline = rs.pipeline()

    #Create a config and configure the pipeline to stream
    #  different resolutions of color and depth streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, src_size[0],  src_size[1], rs.format.z16, 30)
    config.enable_stream(rs.stream.color,  src_size[0],  src_size[1], rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: " , depth_scale)

    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    try:
        while(True):
            start=time.time()
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

            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            poses, inference_time = engine.DetectPosesInImage(color_image)
            for pose in poses:    
                draw_pose(color_image,pose,src_size,(0,0, src_size[0]+1, src_size[1]),depth_image,depth_intrin)
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
            end=time.time()
            #print(end-start)
            timestamps.append(end-start)
            if(len(timestamps)>45):
                del timestamps[0]
    finally:
        pipeline.stop()
###################################