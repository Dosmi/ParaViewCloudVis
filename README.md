# ParaViewCloudVis

This documentation summarises the scripts in ParaViewCloudVis/automation_scripts
For a brief overview of ParaView, please see ParaViewCloudVis/documentation/ParaView-UserGuide-Summary.pdf
For the Visualisation Pipeline overview, please see ParaViewCloudVis/documentation/pipeline_documentation.pdf

Automation scripts:
cloudvis_crossect.py
cloudvis_pipeline_automation.py
cloudvis_pipeline_functions.py
cloudvis_statefile_automation.py

They share a set of flags to help generalise. Those flags are reviewed below. 
Note, that when using these scripts, there are two ways:
1) set these flags as command-line arguments, like so: 
... pvbatch cloudvis_pipeline_automation.py --srtx=1 --oformat=".png"

2) set default values inside the script (names of the default values are CAPITALISED below, ...
... for example default of --sli is written in variable SAVE_LOCAL_ILLUMINATION_IMAGE etc.

optional arguments:
  -h, --help                                           show this help message and exit
  --sli [SAVE_LOCAL_ILLUMINATION_IMAGE]                Save Local Illumination rendered image (1=yes, 0=no)
  --srtx [SAVE_RAY_TRACED_IMAGE]                       Save Ray-Traced/Path-Traced rendered image (1=yes, 0=no)
  --sanim [SAVE_ANIMATION]                             Save Animation (1=yes, 0=no)
  --oformat [ANIMATION_FORMAT]                         Output format for video (".png", ".avi", ".mp4", 
                                                           note, that avi and mp4 might not work for ARCHER2 or ARC3/4)
  --name OUTPUT_NAMES                                  Set image Name for all outputs (images and animation).
                                                           Output type (li, rtx, anim) will be appended to this
                                                           name.
  --data DATA_PATH                                     Path to Data
  --tf TRANSFER_FUNCTION_PATH TRANSFER_FUNCTION_TITLE  Path to Transfer Function file .json, and the transfer
                                                           function name
  --camoffset CAMERA_OFFSET[3]                         Camera offset (as fracional percentage) from center,
                                                           given as a list of 3 elements ...
														   example: [1.275, 1, 3]
  --numframes [NUM_FRAMES]                             Number of frames in animation
  --anim_frame_start [ANIMATION_FRAME_START]           Frame Start Number in animation output
  --anim_frame_end [ANIMATION_FRAME_END]               Frame End Number in animation output
  --fps [FPS]                                          Frames per second in animation output
  --crossect [APPLY_CROSS_SECTION]                     Apply Cross Section (0=no, 1=yes)
  --crossect_plane [CROSS_SECTION_PLANE]               Choose the cross-section plane: 0 = X-axis-left-side,
                                                           1 = X-axis-right-side, 2 = Y-axis-left-side, 3 =
                                                           Y-axis-right-side, 4 = Z-axis-left-side, 5 = Z-axis-
                                                           right-side.
  --crossect_percent [CROSS_SECTION_PERCENTAGE]        Choose the plane cutting percentage in chosen
                                                           axis/plane (see argument 'crossect_plane')
  --image_output_width [IMAGE_OUTPUT_WIDTH]            Image/Video output width
  --image_output_height [IMAGE_OUTPUT_HEIGHT]          Image/Video output height
  --video_output_width [VIDEO_OUTPUT_WIDTH]            Image/Video output width
  --video_output_height [VIDEO_OUTPUT_HEIGHT]          Image/Video output height
  --num_orbits [NUM_ORBITS]                            Number of orbits (spins) arount the object
  --anim_time_start [ANIMATION_TIME_START]             Animation time start (if higher than 1.0, it will pick
                                                           next timestep of time-dependent data)
  --anim_time_end [ANIMATION_TIME_END]                 Animation time end (if higher than 1.0, it will pick
                                                           next timestep of time-dependent data)
  --light_rotation [LIGHT_ROTATION]                    Degrees to rotate light in an orbit
  --camera_rotation [CAMERA_ROTATION]                  Degrees to rotate light in an orbit
  --light_above [LIGHT_ABOVE]                          Have the light above the data (1=yes, 0=no)
  --light_radius [LIGHT_RADIUS]                        Light disk radius. 0.0 is point-light and anything
                                                           >0.0 is area light
  --light_intensity [LIGHT_INTENSITY]                  Light intensity (brightness), typically [0.0, 1.0]
  --samples_per_pixel [SAMPLES_PER_PIXEL]              Option for Path-tracing: number of samples for each
                                                           pixel in image
  --progressive_passes [PROGRESSIVE_PASSES]            Option for Path-tracing: more passes, less noisy the
                                                           final picture (if denoising is enabed, it will be
                                                           blurry with less passes)
  --rtx_denoise [DENOISE_PATH_TRACING]                 Option for Path-tracing: post-processing denoising of rendered image
                                                           (1=yes, 0=no)
  --main_variable [MAIN_VARIABLE]                      Main variable of dataset to visualise
                                                           (given as string, from netcdf variable name)
  --current_time [CURRENT_TIME]                        Degrees to rotate light in an orbit
  --normlightdirvec [NORMALISE_LIGHT_DIRECTION]        Set light direction vector to be length 1
                                                           (1=yes, 0=no)
  --animrtx [RAY_TRACED_ANIMATION]                     Save animation using ray/path tracing
