# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10
import sys

# DEFAULT ARGUMENTS ALL SET HERE:
# OS-RELATED
FOLDER = "/"

# SAVING OPTIONS:
# set to save locally uniform rendered image (by default VTK renderer)
SAVE_LOCAL_ILLUMINATION_IMAGE = 1
# set to save ray-traced image (note the default is OSPRay pathtracer)
SAVE_RAY_TRACED_IMAGE = 1
# set to save animation, and specify the format:
SAVE_ANIMATION = 1
ANIMATION_FORMAT = ".png"
# set name of individual images/frames output
# NOTE: if rendering video, frame numbers will be automatically appended to this
OUTPUT_NAMES = "frame"
# set output directory for images/video
OUTPUT_PATH = "/work/e710/shared/PVCLOUDVIS_OUTPUTS/"

# DATA:
# specify where to load data from; this can be both individual files, ...
# ... or time-dependent array of files.
# EXAMPLE: single file:  DATA_PATH = ["/work/e710/shared/hl3_98.nc"]
#          multiple:     ['gridded/grids_1092.nc', 'gridded/grids_1958.nc', ...]
DATA_PATH = "/work/e710/shared/ParaViewCloudVis/state_files/test_state.pvsm"

# CAMERA SETTINGS:
# NOTE:by default, ParaView puts the camera to point to the ...
# ... center of the bounding box of the data.
# ... but in specific cases, we might want to move camera slightly up ...
# ... or zoom out.
# EXAMPLE: [1.25, 1.0, 3.4] will move camera 1.25 in x axis and zoom out 3.4 times
# (this is assuming x axis is up, which might differ dataset-to-dataset)
CAMERA_OFFSET = [1.25, 1.0, 3.4]

# ANIMATION SETTINGS:
# Total number of frames, ...
# ... irregardless of how long the video will be ...
# ... which is determined by framerate (FPS)
NUM_FRAMES = 840
# frame start/finish can do a segment of the full video ...
# ... useful when rendering as .png's as an array job
ANIMATION_FRAME_START = 0
ANIMATION_FRAME_END = 2
FPS = 24

# OUTPUT SETTINGS:
# Output sizes can be different for Image and Video:
IMAGE_OUTPUT_WIDTH = 1920
IMAGE_OUTPUT_HEIGHT = 1080

VIDEO_OUTPUT_WIDTH = 1920
VIDEO_OUTPUT_HEIGHT = 1080

# Settings below relate to video only:
# Set number of times camera orbits around the data (full 360 rotation)
NUM_ORBITS = 2
# Animation time start/end is distinct from frame start/end ...
# ... as this is used for time-dependent data animations only.
# Each time slice of data will be an integer value from 0, 1, ... to n ...
# ... and it will automatically load the next timestep after hitting that number
# For example, in range [0,7], it will have timestep 0 at times [0, 0.99] ...
# ... and as soon as the animation time reaches 1.0, it will load timestep 1
# NOTE: if the dataset is not time-dependent, best to leave start/end range to ...
# ... [0, 1], however, values greater than 1 will keep the only timestep loaded
ANIMATION_TIME_START = 0.0
ANIMATION_TIME_END = 7.0

# RAY-TRACING OPTIONS
# Set light rotation offset from camera position in a circular orbits
# (see Desmos graph for example)
LIGHT_ROTATION = 90.0
CAMERA_ROTATION = 80.0
LIGHT_ABOVE = 1
# set light radius - 0.0 is a point light, anything >0 is an area light:
# ... in ray tracing, area light is dealt with differently,
# ... as we then need to integrate the lighting contributions from ...
# ... multiple points within the area
LIGHT_RADIUS = 0.0
LIGHT_INTENSITY = 0.6
# set how many rays to cast per pixel (higher - better quality)
SAMPLES_PER_PIXEL = 30
# set how many passes for image improvement (higher - less noise)
PROGRESSIVE_PASSES = 100
# set whether the final image should undergo denoising offered by ParaView
DENOISE_PATH_TRACING = 1

# set the main variable name to be inspected
MAIN_VARIABLE = 'hl'#'hgliq'

# must be in range [ANIMATION_TIME_START, ANIMATION_TIME_END] ...
# NOTE: since video animation willl start from ANIMATION_TIME_START, ...
# ... this CURRENT_TIME parameter is only relevant ...
# ... if we want to first save an image from a specific timestep:
CURRENT_TIME = 1.0

# when doing local illumination rendering (default in VTK), ...
# ... the light direction (light focus point) might be shown as a white line.
# ... by normalising the light direction, we can shorten that white line ...
# ... to be out of the sight of the renderview:
NORMALISE_LIGHT_DIRECTION = 1

# set whether the animation individual frames should be ray-traced
RAY_TRACED_ANIMATION = 0



# Set-up named command-line arguments:
import argparse, sys, os

parser=argparse.ArgumentParser()

parser.add_argument("--sli",        help="Save Local Illumination rendered image",
                    nargs='?',      default=SAVE_LOCAL_ILLUMINATION_IMAGE, const=SAVE_LOCAL_ILLUMINATION_IMAGE)
parser.add_argument("--srtx",       help="Save Ray-Traced/Path-Traced rendered image",
                    nargs='?',      default=SAVE_RAY_TRACED_IMAGE, const=SAVE_RAY_TRACED_IMAGE)
parser.add_argument("--sanim",      help="Save Animation",
                    nargs='?',      default=SAVE_ANIMATION, const=SAVE_ANIMATION)
parser.add_argument("--oformat",    help="Output format for video",
                    nargs='?',      default=ANIMATION_FORMAT, const=ANIMATION_FORMAT)
parser.add_argument("--name",       help="Set image Name for all outputs (images and animation). Output type (li, rtx, anim) will be appended to this name.",
                    type=str, default=OUTPUT_NAMES)
parser.add_argument("--data",       help="Path to Data",
                    nargs=1, type=str, default=DATA_PATH )
parser.add_argument("--camoffset",  help="Camera offset (as fracional percentage) from center, default (1.275, 1, 3)",
                    nargs=3, type=float, default=CAMERA_OFFSET)

parser.add_argument("--numframes",  help="Number of frames in animation",
                    nargs='?',      default=NUM_FRAMES, const=NUM_FRAMES, type=int)
parser.add_argument("--anim_frame_start",  help="Frame Start Number in animation output",
                    nargs='?',      default=ANIMATION_FRAME_START, const=ANIMATION_FRAME_START, type=int)
parser.add_argument("--anim_frame_end",  help="Frame End Number in animation output",
                    nargs='?',      default=ANIMATION_FRAME_END, const=ANIMATION_FRAME_END, type=int)
parser.add_argument("--fps",  help="Frames per second in animation output",
                    nargs='?',      default=FPS, const=FPS, type=int)

parser.add_argument("--image_output_width",  help="Image/Video output width",
                    nargs='?',      default=IMAGE_OUTPUT_WIDTH, const=IMAGE_OUTPUT_WIDTH, type=int)
parser.add_argument("--image_output_height",  help="Image/Video output height",
                    nargs='?',      default=IMAGE_OUTPUT_HEIGHT, const=IMAGE_OUTPUT_HEIGHT, type=int)

parser.add_argument("--video_output_width",  help="Image/Video output width",
                    nargs='?',      default=VIDEO_OUTPUT_WIDTH, const=VIDEO_OUTPUT_WIDTH, type=int)
parser.add_argument("--video_output_height",  help="Image/Video output height",
                    nargs='?',      default=VIDEO_OUTPUT_HEIGHT, const=VIDEO_OUTPUT_HEIGHT, type=int)

parser.add_argument("--num_orbits",  help="Number of orbits (spins) arount the object",
                    nargs='?',      default=NUM_ORBITS, const=NUM_ORBITS, type=int)

parser.add_argument("--anim_time_start",  help="Animation time start (if higher than 1.0, it will pick next timestep of time-dependent data) ",
                    nargs='?',      default=ANIMATION_TIME_START, const=ANIMATION_TIME_START, type=float)

parser.add_argument("--anim_time_end",  help="Animation time end (if higher than 1.0, it will pick next timestep of time-dependent data) ",
                    nargs='?',      default=ANIMATION_TIME_END, const=ANIMATION_TIME_END, type=float)

parser.add_argument("--light_rotation",  help="Degrees to rotate light in an orbit",
                    nargs='?',      default=LIGHT_ROTATION, const=LIGHT_ROTATION, type=float)
parser.add_argument("--camera_rotation",  help="Degrees to rotate light in an orbit",
                    nargs='?',      default=CAMERA_ROTATION, const=CAMERA_ROTATION, type=float)
parser.add_argument("--light_above",     help="Have the light above the data (1=yes, 0=no)",
                    nargs='?',      default=LIGHT_ABOVE, const=LIGHT_ABOVE)

parser.add_argument("--light_radius",  help="Light disk radius. 0.0 is point-light and anything >0.0 is area light",
                    nargs='?',      default=LIGHT_RADIUS, const=LIGHT_RADIUS, type=float)
parser.add_argument("--light_intensity",  help="Light intensity (brightness), typically [0.0, 1.0]",
                    nargs='?',      default=LIGHT_INTENSITY, const=LIGHT_INTENSITY, type=float)

parser.add_argument("--samples_per_pixel",  help="Option for Path-tracing: number of samples for each pixel in image",
                    nargs='?',      default=SAMPLES_PER_PIXEL, const=SAMPLES_PER_PIXEL, type=int)

parser.add_argument("--progressive_passes",  help="Option for Path-tracing: more passes, less noisy the final picture (if denoising is enabed, it will be blurry with less passes)",
                    nargs='?',      default=PROGRESSIVE_PASSES, const=PROGRESSIVE_PASSES, type=int)

parser.add_argument("--rtx_denoise",  help="Option for Path-tracing: more passes, less noisy the final picture (if denoising is enabed, it will be blurry with less passes)",
                    nargs='?',      default=DENOISE_PATH_TRACING, const=DENOISE_PATH_TRACING, type=int)

parser.add_argument("--main_variable",  help="Main variable of dataset to visualise",
                    nargs='?',      default=MAIN_VARIABLE, const=MAIN_VARIABLE, type=str)

parser.add_argument("--current_time",  help="Degrees to rotate light in an orbit",
                    nargs='?',      default=CURRENT_TIME, const=CURRENT_TIME, type=float)

parser.add_argument("--normlightdirvec",      help="Save Animation",
                    nargs='?',      default=NORMALISE_LIGHT_DIRECTION, const=NORMALISE_LIGHT_DIRECTION)

parser.add_argument("--animrtx",        help="Save animation using ray/path tracing",
                    nargs='?',      default=RAY_TRACED_ANIMATION, const=RAY_TRACED_ANIMATION)


args=parser.parse_args()

print(f"Args: {args}\nCommand Line: {sys.argv}\nsrtx: {args.srtx}")
print(f"Dict format: {vars(args)}")

formatted_path  = OUTPUT_PATH

############################## HELPER FUNCTIONS ################################

#### import the simple module from the paraview
from paraview.simple import *
import math

def getAbsoluteRotation(x, y):
    if x >= 0:
        return math.acos(y) * 180.0 / math.pi
    else:
        return math.asin(y) * 180.0 / math.pi + 270.0

def y_light(d_dst, l_deg, y_cam, z_cam, f_p):
    return d_dst * math.sin(
        l_deg * math.pi / 180.0 + getAbsoluteRotation((y_cam - f_p[1]) / d_dst, (z_cam - f_p[2]) / d_dst) * math.pi / 180.0) + f_p[1]

def z_light(d_dst, l_deg, y_cam, z_cam, f_p):
    return d_dst*math.cos(l_deg*math.pi/180.0+getAbsoluteRotation((y_cam-f_p[1])/d_dst, (z_cam-f_p[2])/d_dst)*math.pi/180.0)+f_p[2]

############################ END OF HELPER FUNCTIONS ###########################

################################ LOADING DATA IN ###############################
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# STEP 1.	Load in data placeholder
# create a new 'NetCDF Reader'
# input_data = NetCDFReader(registrationName="grids_*", FileName=args.data)
# load
LoadState(args.data)
# MODIFIED - to work for arbitrary data:
# input_data = GetActiveDataSource()
# input_data.Dimensions = input_data.GetProperty("DimensionInfo")[0] # '(xp, yp, zp)'


# STEP 2.	Turn off Spherical Coordinates
# Properties modified on input_data
# input_data.SphericalCoordinates = 0

############################ END OF LOADING DATA IN ############################

# get active view
# renderView1 = GetActiveViewOrCreate('RenderView')
# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
# set active view
SetActiveView(renderView1)

currentdataname = list(GetSources().keys())[0][0]
print(currentdataname)

currentdata = FindSource(currentdataname)
SetActiveSource(currentdata)


# show data in view
main_display = Show(currentdata) #input_data, renderView1, 'UniformGridRepresentation')

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.AnimationTime = args.current_time

######################################### Display Default Values Explained ##########################################

# Display.ScaleFactor = 0.6280000000000001           This gets automatically computed for you from the reader
#                                                            ... and corresponds to the Bounding Volume Size/100
# Display.GaussianRadius = 0.031400000000000004      This is ScaleFactor/20
# ScalarOpacityUnitDistance = DataResolution / Bounding Box Dimensions = Voxel Dimension,
# Then,ScalarOpacityUnitDistance = Voxel Dimension * 1.732 (sqrt of 3)
# Display.ScalarOpacityUnitDistance = 0.0849799064386218

# # this can be used as INITIAL CAMERA POSITION!
# main_display.SliceFunction.Origin = [3.14, 3.1154687500000002, 3.1154687500000002]

######################################### Display Default Values Explained ##########################################

################################ CAMERA SETUP ##################################

# reset view to fit data
renderView1.ResetCamera(False)

# Compute the camera position from specified user input:
# (NOTE: main_display.SliceFunction.Origin tells us the center of the bounding volume ...
#  ...   and the user might want to offset it slightly if data is off-center, hence the 'camoffset')
# NOTE: THIS IS ALL ASSUMING x = up
campos = [main_display.SliceFunction.Origin[0]*args.camoffset[0], # default offset in x = 1.275
          main_display.SliceFunction.Origin[1]*args.camoffset[1], # default offset in y = 1
          main_display.SliceFunction.Origin[2]*args.camoffset[2]] # default offset in z = 3
# camera focus = look at point (like gluLookAt in OpenGL)
camfocus = [main_display.SliceFunction.Origin[0]*args.camoffset[0], # default offset in x = 1.275
            main_display.SliceFunction.Origin[1],
            main_display.SliceFunction.Origin[2]]
#            x  , y  , z
camviewup = [1.0, 0.0, 0.0]

cam = GetActiveCamera()
# rv1 = GetRenderView()
# STEP 3.	Set Camera View Up
cam.SetViewUp(camviewup[0], camviewup[1], camviewup[2])
# STEP 4.	Set Camera Position and Focal Point
# + STEP 5. Set Camera Position (Zoom)
cam.SetPosition(campos[0], campos[1], campos[2])
# only vary it in the x direction here ...
# ... keep focus data centered, just lift up.down (assuming up direction 1, 0, 0)
cam.SetFocalPoint(camfocus[0], camfocus[1], camfocus[2])


# STEP 6.	Set Camera Center of Rotation to be same as focus
renderView1.CenterOfRotation = camfocus

### ...

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

############################# END OF CAMERA SETUP ##############################

################################ LIGHT SETUP ###################################
# camera-centre distance:
camera_centre_distance = math.dist((cam.GetPosition()[1], cam.GetPosition()[2]),
                                   (cam.GetFocalPoint()[1], cam.GetFocalPoint()[2]))

# if the user requested camera rotation around the orbit circle path, ...
# ... compute it here (this will offset the camera from the default origin ...
# ... following an orbit path)
camera_y_pos = y_light(camera_centre_distance, args.camera_rotation, campos[1], campos[2], camfocus)
camera_z_pos = z_light(camera_centre_distance, args.camera_rotation, campos[1], campos[2], camfocus)

campos[1] = camera_y_pos
campos[2] = camera_z_pos
cam.SetPosition(campos[0], campos[1], campos[2])
############################ END OF LIGHT SETTINGS #############################

############################ RAY-TRACING SETTINGS ##############################
# Change background colour for ray-tracing here:
LoadPalette(paletteName='BlackBackground')

# find settings proxy
generalSettings = GetSettingsProxy('GeneralSettings')

# Properties modified on generalSettings
# generalSettings.AutoApplyInfo = 0 NOTE: disabled, was causing ERROR:
# ... AttributeError: Attribute AutoApplyInfo does not exist.
#  This class does not allow addition of new attributes to avoid mistakes due to typos.
#  Use add_attribute() if you really want to add this attribute.

# enable streaming for pathtracing progressive_passes support:
generalSettings.EnableStreaming = 1

# find settings proxies
renderViewInteractionSettings = GetSettingsProxy('RenderViewInteractionSettings')
renderViewSettings = GetSettingsProxy('RenderViewSettings')
representedArrayListSettings = GetSettingsProxy('RepresentedArrayListSettings')
colorPalette = GetSettingsProxy('ColorPalette')

# Properties modified on renderView1
renderView1.EnableRayTracing = 1

# Properties modified on renderView1
renderView1.SamplesPerPixel = args.samples_per_pixel #30

# Properties modified on renderView1
renderView1.ProgressivePasses = args.progressive_passes #1000#10

# Controlling denoising:
renderView1.Denoise = args.rtx_denoise #0

# By default, choose the OSPRay pathtracer
renderView1.BackEnd = 'OSPRay pathtracer'

# Properties modified on renderView1
# set pathtracing background to be black
# (best contrast for clouds)
renderView1.EnvironmentalBG = [0.0, 0.0, 0.0]

# Disable ray tracing for now, as we just set up the default parameters, ...
# ... but will not save to image unless user specifies to do so
renderView1.EnableRayTracing = 0
########################## END OF RAY-TRACING SETTINGS #########################



############################## ANIMATION SETTINGS ##############################
# get animation scene
animationScene1 = GetAnimationScene()

# Set start/end times of animation explicitly
animationScene1.StartTime = args.anim_time_start #0.0
animationScene1.EndTime = args.anim_time_end

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# Properties modified on animationScene1
animationScene1.NumberOfFrames = args.numframes #180

########################## COMPUTING CAMERA PATH/ORBIT #########################
# Programmatically compute the orbit camera points that ParaView will interpolate between
# NOTE: by default, 7 is enough for an orbit (as ParaView pvpython generates 7 points itself)
OrbitPoints = []

for i in range(0,7):
    OrbitPoints.append(cam.GetPosition()[0])
    OrbitPoints.append(y_light(camera_centre_distance, -i*360.0/7.0,
                cam.GetPosition()[1], cam.GetPosition()[2], cam.GetFocalPoint()))
    OrbitPoints.append(z_light(camera_centre_distance, -i*360.0/7.0,
                cam.GetPosition()[1], cam.GetPosition()[2], cam.GetFocalPoint()))


# get camera animation track for the view
cameraAnimationCue1 = GetCameraTrack(view=renderView1)

# create keyframes for this animation track
keyframes_list = []

for i in range(0, args.num_orbits):
    # create a key frame
    keyFrame1 = CameraKeyFrame()
    # keyFrame1.KeyTime = args.anim_time_start + args.anim_time_end/args.num_orbits * i
    # NOTE: time for orbits actually goes from 0.0 to 1.0, even though actual time steps might got from 0.0 to 7.0 etc.
    keyFrame1.KeyTime = args.anim_time_start + 1.0/args.num_orbits * i
    keyFrame1.Position = campos #[4.0, 3.115468740463257, 9.776123778010504]
    keyFrame1.FocalPoint = camfocus #[4.0, 3.115468740463257, 3.115468740463257]
    keyFrame1.ViewUp = camviewup #[1.0, 0.0, 0.0]
    keyFrame1.ParallelScale = cam.GetParallelScale() # 5.41035041419737
    keyFrame1.PositionPathPoints = OrbitPoints
    keyFrame1.FocalPathPoints = camfocus #[4.0, 3.11547, 3.11547]
    keyFrame1.ClosedPositionPath = 1

    keyframes_list.append(keyFrame1)

    # create a key frame
    keyFrame2 = CameraKeyFrame()
    # keyFrame2.KeyTime = args.anim_time_start + args.anim_time_end/args.num_orbits * (i+1)
    keyFrame2.KeyTime = args.anim_time_start + 1.0/args.num_orbits * (i+1)
    keyFrame2.Position = campos #[4.0, 3.115468740463257, 9.776123778010504]
    keyFrame2.FocalPoint = camfocus #[4.0, 3.115468740463257, 3.115468740463257]
    keyFrame2.ViewUp = camviewup #[1.0, 0.0, 0.0]
    keyFrame2.ParallelScale = cam.GetParallelScale() # 5.41035041419737

    keyframes_list.append(keyFrame2)

    print("orbit:", i, "start: ", keyFrame1.KeyTime, " end ", keyFrame2.KeyTime)



# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = keyframes_list #[keyFrame1, keyFrame2, keyFrame3, keyFrame4]

####################### END OF COMPUTING CAMERA PATH/ORBIT #####################

############################# END OF ANIMATION SETUP ###########################






layout1 = GetLayout()

#######################################################################################################################
####################################################### OPTIONS #######################################################

# ############################ Option 1: Saving default VTK Volume Local-Illumination image ##########################

if args.sli:
    # save screenshot
    # SaveScreenshot('C:/Users/Dom/Documents/1-PhD-Year/2022-06-to-09-Summer/OngoingVisualisations/2022-09-01-Automation/0904auto-test.png', renderView1, ImageResolution=[args.image_output_width, args.image_output_height])
    SaveScreenshot(formatted_path+FOLDER+args.name+"_sli.png", renderView1,
                  ImageResolution=[args.image_output_width, args.image_output_height])

else:
    print("Not saving screenshot")







######################################## Option 2: Saving Ray-traced Volume image ####################################
if args.srtx:
    # hide color bar/color legend
    main_display.SetScalarBarVisibility(renderView1, False)

    # Properties modified on renderView1
    renderView1.OrientationAxesVisibility = 0

    # Properties modified on renderView1
    renderView1.EnableRayTracing = 1

    # layout/tab size in pixels
    layout1.SetSize(args.image_output_width, args.image_output_height)

    # current camera placement for renderView1
    renderView1.CameraPosition = campos #[4.0, 3.115468740463257, 9.776123778010504]
    renderView1.CameraFocalPoint = camfocus #[4.0, 3.115468740463257, 3.115468740463257]
    renderView1.CameraViewUp = camviewup #[1.0, 0.0, 0.0]
    renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737

    # save screenshot
    SaveScreenshot(formatted_path+FOLDER+args.name+"_srtx.png", renderView1,
        ImageResolution=[args.image_output_width, args.image_output_height])

    # Properties modified on renderView1
    renderView1.EnableRayTracing = 0

else:
    print("Not saving Ray-traced image")




############################################### Option 3: Saving animation ############################################

if args.sanim:
    print("Saving animation ...")
    # toggle 3D widget visibility (only when running from the GUI)
    # Hide3DWidgets(proxy=light1)

    # toggle 3D widget visibility (only when running from the GUI)
    # Show3DWidgets(proxy=light1)

    # toggle 3D widget visibility (only when running from the GUI)
    # Hide3DWidgets(proxy=light1)
    if args.animrtx:
        renderView1.EnableRayTracing = 1
        print("Ray-Tracing - Enabled")

    # hide color bar/color legend
    main_display.SetScalarBarVisibility(renderView1, False)
    print("Scalar Bar Legend Visibility - Disabled")
    # Properties modified on renderView1
    renderView1.OrientationAxesVisibility = 0
    print("Orientation Axes Visibility - Disabled")



    # layout/tab size in pixels
    layout1.SetSize(args.video_output_width, args.video_output_height)
    print("Output Video Size - ", args.video_output_width, args.video_output_height)
    # current camera placement for renderView1
    renderView1.CameraPosition = campos #[4.0, 3.115468740463257, 9.776123778010504]
    renderView1.CameraFocalPoint = camfocus #[4.0, 3.115468740463257, 3.115468740463257]
    renderView1.CameraViewUp = camviewup#[1.0, 0.0, 0.0]
    renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737
    print("Starting Rendering to path:", formatted_path+FOLDER, "...")
    # save animation
    if ANIMATION_FORMAT == ".png":
        SaveAnimation(formatted_path+FOLDER+args.name+"_sanim.png", renderView1,
                      ImageResolution=[args.video_output_width, args.video_output_height],
                      # FrameRate=args.fps, #24,
                      CompressionLevel='0',
                      FrameWindow=[args.anim_frame_start, args.anim_frame_end-1])
    else:
        SaveAnimation(formatted_path+FOLDER+args.name+"_sanim"+ANIMATION_FORMAT,
        renderView1, ImageResolution=[args.video_output_width, args.video_output_height],
        FrameRate=args.fps, #24,
        CompressionLevel='0',
        FrameWindow=[args.anim_frame_start, args.anim_frame_end-1] )

    print("Animation Rendering Finished.")

    animationScene1.GoToNext()
    animationScene1.GoToPrevious()
    renderView1.EnableRayTracing = 0

else:
    print("Not rendering video/animation")

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(args.image_output_width, args.image_output_height)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = campos #[4.0, 3.11547, 9.77612]
renderView1.CameraFocalPoint = camfocus #[4.0, 3.11547, 3.11547]
renderView1.CameraViewUp = camviewup #[1.0, 0.0, 0.0]
renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
