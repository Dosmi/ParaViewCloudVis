# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10


# DEFAULT ARGUMENTS ALL SET HERE:
# OS-RELATED
FOLDER = "/"

# SAVING
SAVE_LOCAL_ILLUMINATION_IMAGE = 1
SAVE_RAY_TRACED_IMAGE = 0
SAVE_ANIMATION = 0
OUTPUT_NAMES = "rendered"
OUTPUT_PATH = "/work/e710/shared"

# DATA:
DATA_PATH = "/work/e710/shared/hl3_98.nc"
TRANSFER_FUNCTION_PATH = "/work/e710/shared/hl_Cloud_white_realistic_tf.json"
TRANSFER_FUNCTION_TITLE = "WhiteCloud"

# CAMERA SETTINGS:
CAMERA_OFFSET = [1.275, 1.0, 3.0]

# ANIMATION SETTINGS:
NUM_FRAMES = 200
ANIMATION_FRAME_START = 0
ANIMATION_FRAME_END = 20
FPS = 24

# OUTPUT SETTINGS:
IMAGE_OUTPUT_WIDTH = 1920
IMAGE_OUTPUT_HEIGHT = 1024

VIDEO_OUTPUT_WIDTH = 1920
VIDEO_OUTPUT_HEIGHT = 1024

NUM_ORBITS = 1
ANIMATION_TIME_START = 0.0
ANIMATION_TIME_END = 1.0

# RAY-TRACING OPTIONS
LIGHT_ROTATION = 90.0



# Set-up named command-line arguments:
import argparse, sys, os

parser=argparse.ArgumentParser()

parser.add_argument("--sli",        help="Save Local Illumination rendered image",
                    nargs='?',      default=SAVE_LOCAL_ILLUMINATION_IMAGE, const=SAVE_LOCAL_ILLUMINATION_IMAGE)
parser.add_argument("--srtx",       help="Save Ray-Traced/Path-Traced rendered image",
                    nargs='?',      default=SAVE_RAY_TRACED_IMAGE, const=SAVE_RAY_TRACED_IMAGE)
parser.add_argument("--sanim",      help="Save Animation",
                    nargs='?',      default=SAVE_ANIMATION, const=SAVE_ANIMATION)
parser.add_argument("--name",       help="Set image Name for all outputs (images and animation). Output type (li, rtx, anim) will be appended to this name.",
                    nargs=1, type=str, default=OUTPUT_NAMES)
parser.add_argument("--data",       help="Path to Data",
                    nargs=1, type=str, default=DATA_PATH )
parser.add_argument("--tf",       help="Path to Transfer Function file .json, and the transfer function name",
                    nargs=2, type=str, default=[TRANSFER_FUNCTION_PATH, TRANSFER_FUNCTION_TITLE])
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
                    nargs='?',      default=VIDEO_OUTPUT_HEIGHT, const=VIDEO_OUTPUT_HEIGHT, type=int)

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


args=parser.parse_args()

print(f"Args: {args}\nCommand Line: {sys.argv}\nsrtx: {args.srtx}")
print(f"Dict format: {vars(args)}")

parsed_path = os.path.normpath(args.data).split(os.sep)

file_name       = parsed_path[-1]
formatted_path  = OUTPUT_PATH# FOLDER.join(parsed_path[:-1])
print("FILENAME:", file_name, "FORMATTED:", formatted_path)

print(args.tf[0], args.tf[1])



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

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# STEP 1.	Load in data placeholder
# create a new 'NetCDF Reader'
# hl3_98nc = NetCDFReader(registrationName='hl3_98.nc', FileName=['C:\\Users\\Dom\\AppData\\Roaming\\MobaXterm\\home\\hl3_98.nc'])
# hl3_98nc = NetCDFReader(registrationName=file_name, FileName=[formatted_path])
hl3_98nc = NetCDFReader(registrationName=file_name, FileName=[args.data])
# MODIFIED - to work for arbitrary data:
hl3_98nc.Dimensions = hl3_98nc.GetProperty("DimensionInfo")[0] # '(xp, yp, zp)'


# STEP 2.	Turn off Spherical Coordinates
# Properties modified on hl3_98nc
hl3_98nc.SphericalCoordinates = 0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
hl3_98ncDisplay = Show(hl3_98nc, renderView1, 'UniformGridRepresentation')

######################################### Display Default Values Explained ##########################################

# Display.ScaleFactor = 0.6280000000000001           This gets automatically computed for you from the reader
#                                                            ... and corresponds to the Bounding Volume Size/100
# Display.GaussianRadius = 0.031400000000000004      This is ScaleFactor/20
# ScalarOpacityUnitDistance = DataResolution / Bounding Box Dimensions = Voxel Dimension,
# Then,ScalarOpacityUnitDistance = Voxel Dimension * 1.732 (sqrt of 3)
# Display.ScalarOpacityUnitDistance = 0.0849799064386218

# # this can be used as INITIAL CAMERA POSITION!
# hl3_98ncDisplay.SliceFunction.Origin = [3.14, 3.1154687500000002, 3.1154687500000002]

######################################### Display Default Values Explained ##########################################

# reset view to fit data
renderView1.ResetCamera(False)

#### CAMERA CONTROLS:

# Compute the camera position from specified user input:
# (NOTE: hl3_98ncDisplay.SliceFunction.Origin tells us the center of the bounding volume ...
#  ...   and the user might want to offset it slightly if data is off-center, hence the 'camoffset')
campos = [hl3_98ncDisplay.SliceFunction.Origin[0]*args.camoffset[0], # default offset in x = 1.275
          hl3_98ncDisplay.SliceFunction.Origin[1]*args.camoffset[1], # default offset in y = 1
          hl3_98ncDisplay.SliceFunction.Origin[2]*args.camoffset[2]] # default offset in z = 3
# camera focus = look at point (like gluLookAt in OpenGL)
camfocus = [hl3_98ncDisplay.SliceFunction.Origin[0]*args.camoffset[0], # default offset in x = 1.275
            hl3_98ncDisplay.SliceFunction.Origin[1],
            hl3_98ncDisplay.SliceFunction.Origin[2]]
#            x  , y  , z
camviewup = [1.0, 0.0, 0.0]

cam = GetActiveCamera()
# rv1 = GetRenderView()
# STEP 3.	Set Camera View Up
cam.SetViewUp(camviewup[0], camviewup[1], camviewup[2])
# STEP 4.	Set Camera Position and Focal Point 	X coordinate to 4
# + STEP 5. Set Camera Position (Zoom)
# cam.SetPosition(cam.GetPosition()[0]*1.275, cam.GetPosition()[1], cam.GetPosition()[2]*0.4)
cam.SetPosition(campos[0], campos[1], campos[2]) # 3
# cam.SetFocalPoint(cam.GetFocalPoint()[0]*1.275, cam.GetFocalPoint()[1], cam.GetFocalPoint()[2])
# only vary it in the x direction here ... keep focus data centered, just lift up.down (assuming up direction 1, 0, 0)
cam.SetFocalPoint(camfocus[0], camfocus[1], camfocus[2])


# STEP 6.	Set Camera Center of Rotation to be same as focus
renderView1.CenterOfRotation = camfocus

### ...

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()


# STEP 7.	Add Light n degrees rotated from camera:
# Create a new 'Light'
light1 = AddLight(view=renderView1)

# toggle 3D widget visibility (only when running from the GUI)
# Show3DWidgets(proxy=light1)
# Hide3DWidgets(proxy=light1)
# HideInteractiveWidgets(proxy=light1)


# camera-centre distance:
camera_centre_distance = math.dist((cam.GetPosition()[1], cam.GetPosition()[2]),
                                   (cam.GetFocalPoint()[1], cam.GetFocalPoint()[2]))

light_y_pos = y_light(camera_centre_distance, args.light_rotation, campos[1], campos[2], camfocus)
light_z_pos = z_light(camera_centre_distance, args.light_rotation, campos[1], campos[2], camfocus)

#update the light
light1.Position = [campos[0], light_y_pos, light_z_pos]
# light1.FocalPoint = list(camfocus) #[4.0, 3.115468740463257, 3.115468740463257]
light1.FocalPoint = [campos[0],
                     light_y_pos+(camfocus[0]-light_y_pos)/camera_centre_distance,
                     light_z_pos+(camfocus[1]-light_z_pos)/camera_centre_distance]




# Properties modified on light1
light1.Radius = 2.0

LoadPalette(paletteName='BlackBackground')

# find settings proxy
generalSettings = GetSettingsProxy('GeneralSettings')

# Properties modified on generalSettings
# generalSettings.AutoApplyInfo = 0 NOTE: disabled, was causing ERROR:
# ... AttributeError: Attribute AutoApplyInfo does not exist.
#  This class does not allow addition of new attributes to avoid mistakes due to typos.
#  Use add_attribute() if you really want to add this attribute.
generalSettings.EnableStreaming = 1

# find settings proxy
renderViewInteractionSettings = GetSettingsProxy('RenderViewInteractionSettings')

# find settings proxy
renderViewSettings = GetSettingsProxy('RenderViewSettings')

# find settings proxy
representedArrayListSettings = GetSettingsProxy('RepresentedArrayListSettings')

# find settings proxy
colorPalette = GetSettingsProxy('ColorPalette')

# Properties modified on renderView1
renderView1.EnableRayTracing = 1

# Properties modified on renderView1
renderView1.SamplesPerPixel = 30

# Properties modified on renderView1
renderView1.ProgressivePasses = 10

# Properties modified on renderView1
renderView1.BackEnd = 'OSPRay pathtracer'

# Properties modified on renderView1
# set pathtracing background to be black
# (best contrast for clouds)
renderView1.EnvironmentalBG = [0.0, 0.0, 0.0]

# Disable ray tracing for now, as we just set up the default parameters, ...
# ... but will not save to image unless user specifies to do so
renderView1.EnableRayTracing = 0

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.StartTime = args.anim_time_start #0.0

# Properties modified on animationScene1
animationScene1.EndTime = args.anim_time_end

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# Properties modified on animationScene1
animationScene1.NumberOfFrames = args.numframes #180


# Programmatically compute the orbit camera points that ParaView will interpolate between
# NOTE: by default, 7 is enough for an orbit (as ParaView pvpython generates 7 points itself)
OrbitPoints = []

for i in range(0,7):
    OrbitPoints.append(cam.GetPosition()[0])
    OrbitPoints.append(y_light(camera_centre_distance, -i*360.0/7.0, cam.GetPosition()[1], cam.GetPosition()[2], cam.GetFocalPoint()))
    OrbitPoints.append(z_light(camera_centre_distance, -i*360.0/7.0, cam.GetPosition()[1], cam.GetPosition()[2], cam.GetFocalPoint()))


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

# set scalar coloring
ColorBy(hl3_98ncDisplay, ('POINTS', 'hl'))

# rescale color and/or opacity maps used to include current data range
hl3_98ncDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
hl3_98ncDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'hl'
hlLUT = GetColorTransferFunction('hl')
hlLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941,
                   0.03771344944834709, 0.865003, 0.865003, 0.865003,
                   0.07542689889669418, 0.705882, 0.0156863, 0.14902]
hlLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'hl'
hlPWF = GetOpacityTransferFunction('hl')
hlPWF.Points = [0.0, 0.0,
                0.5, 0.0,
                0.07542689889669418, 1.0,
                0.5, 0.0]
hlPWF.ScalarRangeInitialized = 1

# if an external transfer function is specified, apply it here:

ImportPresets(filename=args.tf[0])

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
hlLUT.ApplyPreset(args.tf[1], True)
# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
# hlLUT.ApplyPreset(args.tf[1], True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
hlPWF.ApplyPreset(args.tf[1], True)



# change representation type
hl3_98ncDisplay.SetRepresentationType('Volume')

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(args.image_output_width, args.image_output_height)

# current camera placement for renderView1
renderView1.CameraPosition   = list(cam.GetPosition())#[4.0, 3.115468740463257, 9.776123778010504]
renderView1.CameraFocalPoint = list(cam.GetFocalPoint()) #[4.0, 3.115468740463257, 3.115468740463257]
renderView1.CameraViewUp = camviewup
renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737

#######################################################################################################################
####################################################### OPTIONS #######################################################

# ############################ Option 1: Saving default VTK Volume Local-Illumination image ##########################

if args.sli:
    # save screenshot
    # SaveScreenshot('C:/Users/Dom/Documents/1-PhD-Year/2022-06-to-09-Summer/OngoingVisualisations/2022-09-01-Automation/0904auto-test.png', renderView1, ImageResolution=[args.image_output_width, args.image_output_height])
    SaveScreenshot(formatted_path+FOLDER+args.name+"_sli.png", renderView1, ImageResolution=[args.image_output_width, args.image_output_height])

else:
    print("didn't save screenshot")







######################################## Option 2: Saving Ray-traced Volume image ####################################
if args.srtx:
    # hide color bar/color legend
    hl3_98ncDisplay.SetScalarBarVisibility(renderView1, False)

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
    # SaveScreenshot('C:/Users/Dom/Documents/1-PhD-Year/2022-06-to-09-Summer/OngoingVisualisations/2022-09-01-Automation/auto-rtx-test.png', renderView1, ImageResolution=[args.image_output_width, args.image_output_height])
    SaveScreenshot(formatted_path+FOLDER+args.name+"_srtx.png", renderView1, ImageResolution=[args.image_output_width, args.image_output_height])

    # Properties modified on renderView1
    renderView1.EnableRayTracing = 0

else:
    print("didn't save RTX image")




############################################### Option 3: Saving animation ############################################
# get light
lightproxy = GetLight(0, renderView1)
Hide3DWidgets(proxy=lightproxy)

# Show()
# lightproxy.Enable = 0

# update the view to ensure updated data information
# renderView1.Update()

# remove light added to the view
# RemoveLight(light=lightproxy)
# Show()
# light1.Enable = 1


if args.sanim:
    print("saving animation ...")
    # toggle 3D widget visibility (only when running from the GUI)
    # Hide3DWidgets(proxy=light1)

    # toggle 3D widget visibility (only when running from the GUI)
    # Show3DWidgets(proxy=light1)

    # toggle 3D widget visibility (only when running from the GUI)
    # Hide3DWidgets(proxy=light1)

    print("1made it here")

    # layout/tab size in pixels
    layout1.SetSize(args.video_output_width, args.video_output_height)
    print("2made it here")
    # current camera placement for renderView1
    renderView1.CameraPosition = campos #[4.0, 3.115468740463257, 9.776123778010504]
    renderView1.CameraFocalPoint = camfocus #[4.0, 3.115468740463257, 3.115468740463257]
    renderView1.CameraViewUp = camviewup#[1.0, 0.0, 0.0]
    renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737
    print("3made it here")
    # save animation
    # SaveAnimation('C:/Users/Dom/Documents/1-PhD-Year/2022-06-to-09-Summer/OngoingVisualisations/2022-09-01-Automation/auto-animation-test.avi', renderView1, ImageResolution=[1280, 720],
    #               FrameRate=24.0,
    #               FrameWindow=[0, 179])
    SaveAnimation(formatted_path+FOLDER+args.name+"_sanim.avi", renderView1, ImageResolution=[args.video_output_width, args.video_output_height],
        FrameRate=args.fps, #24,
        FrameWindow=[args.anim_frame_start, args.anim_frame_end-1]) #[0, 179])
    print("4made it here")
    animationScene1.GoToNext()

    animationScene1.GoToPrevious()

else:
    print("didn't save animation")

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