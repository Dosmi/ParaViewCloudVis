# Simpler Script just for cross-sections ...
# ... as Local-Illumination image output
# (If a video/rtx output is needed, use the other ...
#  ... 'cloudvis_pipeline_automation.py' script ...
#  ... as it also has the cross-section filter)

# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10


# DEFAULT ARGUMENTS ALL SET HERE:
# OS-RELATED
FOLDER = "/"

# SAVING OPTIONS:
# set to save locally uniform rendered image (by default VTK renderer)
SAVE_LOCAL_ILLUMINATION_IMAGE = 1
# set name of individual images output
OUTPUT_NAMES = "cloudvis_crossect"
# set output directory for images/video
OUTPUT_PATH = "/work/e710/shared/PVCLOUDVIS_OUTPUTS/"

# DATA:
# specify where to load data from; this can be both individual files, ...
# ... or time-dependent array of files.
# EXAMPLE: single file:  DATA_PATH = ["/work/e710/shared/hl3_98.nc"]
#          multiple:     ['gridded/grids_1092.nc', 'gridded/grids_1958.nc', ...]
DATA_PATH = ['/work/e710/shared/gridded_extracted/grids_1092-only_hgliq_xtime.nc', # timestep 1 [0] 0.0-1.0
             '/work/e710/shared/gridded_extracted/grids_1958-only_hgliq_xtime.nc', # timestep 2 [1] 1.0-2.0
             '/work/e710/shared/gridded_extracted/grids_2780-only_hgliq_xtime.nc', # timestep 3 [2] 2.0-3.0
             '/work/e710/shared/gridded_extracted/grids_3665-only_hgliq_xtime.nc', # timestep 4 [3] 3.0-4.0
             '/work/e710/shared/gridded_extracted/grids_4483-only_hgliq_xtime.nc', # timestep 5 [4] 4.0-5.0
             '/work/e710/shared/gridded_extracted/grids_5220-only_hgliq_xtime.nc', # timestep 6 [5] 5.0-6.0
             '/work/e710/shared/gridded_extracted/grids_5937-only_hgliq_xtime.nc'] # timestep 7 [6] 6.0-7.0
# specify file location of the transfer function .json file
TRANSFER_FUNCTION_PATH = "/work/e710/shared/ParaViewCloudVis/transfer_functions/hl_Cloud_white_realistic_tf.json"
# specify the title of the transfer function ...
# ... (this can be find inside the .json file, as the "Name" : "...")
TRANSFER_FUNCTION_TITLE = "WhiteCloud"


# CAMERA SETTINGS:
# NOTE:by default, ParaView puts the camera to point to the ...
# ... center of the bounding box of the data.
# ... but in specific cases, we might want to move camera slightly up ...
# ... or zoom out.
# EXAMPLE: [1.25, 1.0, 3.4] will move camera 1.25 in x axis and zoom out 3.4 times
# (this is assuming x axis is up, which might differ dataset-to-dataset)
CAMERA_OFFSET = [1.25, 1.0, 3.4]

# OUTPUT SETTINGS:
# Output sizes can be different for Image and Video:
IMAGE_OUTPUT_WIDTH = 1920
IMAGE_OUTPUT_HEIGHT = 1080

CAMERA_ROTATION = 80.0


# allow to set up cross-section filter (volume-slice on plane)
APPLY_CROSS_SECTION = 1
#                                 XL XR   YL YR   ZL ZR
# Choose a cross-section plane - [0,  1,  2,  3,  4,  5]
CROSS_SECTION_PLANE = 3
CROSS_SECTION_PERCENTAGE = 50

# set the main variable name to be inspected
MAIN_VARIABLE = 'hgliq'

# must be in range [ANIMATION_TIME_START, ANIMATION_TIME_END] ...
# NOTE: since video animation willl start from ANIMATION_TIME_START, ...
# ... this CURRENT_TIME parameter is only relevant ...
# ... if we want to first save an image from a specific timestep:
CURRENT_TIME = 5.0










# Set-up named command-line arguments:
import argparse, sys, os

parser=argparse.ArgumentParser()

parser.add_argument("--sli",        help="Save Local Illumination rendered image",
                    nargs='?',      default=SAVE_LOCAL_ILLUMINATION_IMAGE, const=SAVE_LOCAL_ILLUMINATION_IMAGE)
parser.add_argument("--name",       help="Set image Name for all outputs (images and animation). Output type (li, rtx, anim) will be appended to this name.",
                    type=str, default=OUTPUT_NAMES)
parser.add_argument("--data",       help="Path to Data",
                    nargs=1, type=str, default=DATA_PATH )

parser.add_argument("--tf",       help="Path to Transfer Function file .json, and the transfer function name",
                    nargs=2, type=str, default=[TRANSFER_FUNCTION_PATH, TRANSFER_FUNCTION_TITLE])
parser.add_argument("--camoffset",  help="Camera offset (as fracional percentage) from center, default (1.275, 1, 3)",
                    nargs=3, type=float, default=CAMERA_OFFSET)


parser.add_argument("--crossect",      help="Apply Cross Section (0=no, 1=yes)",
                    nargs='?',      default=APPLY_CROSS_SECTION, const=APPLY_CROSS_SECTION, type=int)
                    #                                 XL XR   YL YR   ZL ZR
                    # Choose a cross-section plane - [0,  1,  2,  3,  4,  5]
parser.add_argument("--crossect_plane",      help="Choose the cross-section plane:\n"+
                                                  "0 = X-axis-left-side,\n"+
                                                  "1 = X-axis-right-side,\n"+
                                                  "2 = Y-axis-left-side,\n"+
                                                  "3 = Y-axis-right-side,\n"+
                                                  "4 = Z-axis-left-side,\n"+
                                                  "5 = Z-axis-right-side.",
                    nargs='?',      default=CROSS_SECTION_PLANE, const=CROSS_SECTION_PLANE, type=int)

parser.add_argument("--crossect_percent",  help="Choose the plane cutting percentage in chosen axis/plane (see argument 'crossect_plane')",
                    nargs='?',      default=CROSS_SECTION_PERCENTAGE, const=CROSS_SECTION_PERCENTAGE, type=float)


parser.add_argument("--image_output_width",  help="Image/Video output width",
                    nargs='?',      default=IMAGE_OUTPUT_WIDTH, const=IMAGE_OUTPUT_WIDTH, type=int)
parser.add_argument("--image_output_height",  help="Image/Video output height",
                    nargs='?',      default=IMAGE_OUTPUT_HEIGHT, const=IMAGE_OUTPUT_HEIGHT, type=int)


parser.add_argument("--camera_rotation",  help="Degrees to rotate light in an orbit",
                    nargs='?',      default=CAMERA_ROTATION, const=CAMERA_ROTATION, type=float)


parser.add_argument("--main_variable",  help="Main variable of dataset to visualise",
                    nargs='?',      default=MAIN_VARIABLE, const=MAIN_VARIABLE, type=str)

parser.add_argument("--current_time",  help="Degrees to rotate light in an orbit",
                    nargs='?',      default=CURRENT_TIME, const=CURRENT_TIME, type=float)



args=parser.parse_args()

print(f"Args: {args}\nCommand Line: {sys.argv}\n")
print(f"Dict format: {vars(args)}")
print(args.tf[0], args.tf[1])

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

def y_orbit_offset_position(d_dst, l_deg, y_cam, z_cam, f_p):
    return d_dst * math.sin(
        l_deg * math.pi / 180.0 + getAbsoluteRotation((y_cam - f_p[1]) / d_dst, (z_cam - f_p[2]) / d_dst) * math.pi / 180.0) + f_p[1]

def z_orbit_offset_position(d_dst, l_deg, y_cam, z_cam, f_p):
    return d_dst*math.cos(l_deg*math.pi/180.0+getAbsoluteRotation((y_cam-f_p[1])/d_dst, (z_cam-f_p[2])/d_dst)*math.pi/180.0)+f_p[2]

############################ END OF HELPER FUNCTIONS ###########################
















################################ LOADING DATA IN ###############################
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# STEP 1.	Load in data placeholder
# create a new 'NetCDF Reader'
input_data = NetCDFReader(registrationName="input_datasource", FileName=args.data)
# MODIFIED - to work for arbitrary data:
input_data.Dimensions = input_data.GetProperty("DimensionInfo")[0] # '(xp, yp, zp)'


# STEP 2.	Turn off Spherical Coordinates
# Properties modified on input_data
input_data.SphericalCoordinates = 0

############################ END OF LOADING DATA IN ############################

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
main_display = Show(input_data, renderView1, 'UniformGridRepresentation')

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

### Compute camera orbital offset

# camera-centre distance:
camera_centre_distance = math.dist((cam.GetPosition()[1], cam.GetPosition()[2]),
                                   (cam.GetFocalPoint()[1], cam.GetFocalPoint()[2]))

# if the user requested camera rotation around the orbit circle path, ...
# ... compute it here (this will offset the camera from the default origin ...
# ... following an orbit path)
camera_y_pos = y_orbit_offset_position(camera_centre_distance, args.camera_rotation, campos[1], campos[2], camfocus)
camera_z_pos = z_orbit_offset_position(camera_centre_distance, args.camera_rotation, campos[1], campos[2], camfocus)

campos[1] = camera_y_pos
campos[2] = camera_z_pos
cam.SetPosition(campos[0], campos[1], campos[2])

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

############################# END OF CAMERA SETUP ##############################
























############################ COLOURING SETTINGS ################################
# set scalar coloring
ColorBy(main_display, ('POINTS', args.main_variable))

# rescale color and/or opacity maps used to include current data range
main_display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
main_display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for args.main_variable
hlLUT = GetColorTransferFunction(args.main_variable)
hlLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941,
                   0.03771344944834709, 0.865003, 0.865003, 0.865003,
                   0.07542689889669418, 0.705882, 0.0156863, 0.14902]
hlLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for args.main_variable
hlPWF = GetOpacityTransferFunction(args.main_variable)
hlPWF.Points = [0.0, 0.0,
                0.5, 0.0,
                0.07542689889669418, 1.0,
                0.5, 0.0]
hlPWF.ScalarRangeInitialized = 1

# if an external transfer function is specified, apply it here:

ImportPresets(filename=args.tf[0])

# Apply a COLOUR LOOK-UP TABLE using its name.
# NOTE this may not work as expected when presets have duplicate names.
hlLUT.ApplyPreset(args.tf[1], True)

# Apply TRANSPARENCIES using its name.
# NOTE this may not work as expected when presets have duplicate names.
hlPWF.ApplyPreset(args.tf[1], True)

############################ END OF COLOURING SETTINGS #########################

# change representation type
main_display.SetRepresentationType('Volume')

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(args.image_output_width, args.image_output_height)

# current camera placement for renderView1
renderView1.CameraPosition   = list(cam.GetPosition())#[4.0, 3.115468740463257, 9.776123778010504]
renderView1.CameraFocalPoint = list(cam.GetFocalPoint()) #[4.0, 3.115468740463257, 3.115468740463257]
renderView1.CameraViewUp = camviewup
renderView1.CameraParallelScale = cam.GetParallelScale() #5.41035041419737




############################# Cross-section Filter #############################

if args.crossect == 1:
    # There is a ParaView filter which already does this called 'Clip' ...
    # ... but it is horribly inefficient, as it converts the data ...
    # ... from what might be Structured Uniform Grid (Image) to Unstructured Grid ...
    # ... and volume rendering runs much slower for unstructured data.
    # Therefore, we use the ExtractSubset filter here to manually ....
    # ... compute the cross-section plane, and keep the date in the Image format

    # create a new 'Extract Subset'
    extractSubset1 = ExtractSubset(registrationName='CrossSectionVolume1', Input=input_data)
    # extractSubset1.VOI[args.crossect_plane] = [0, 128, 0, 127, 0, 127]

    index1 = args.crossect_plane
    index2 = ((index1+1)%2) + index1 - (index1%2)

    split_on_value = math.floor((extractSubset1.VOI[index1] + extractSubset1.VOI[index2]) * args.crossect_percent/100.0)

    # Properties modified on extractSubset1
    extractSubset1.VOI[index1] = split_on_value

    # show data in view
    extractSubset1Display = Show(extractSubset1, renderView1, 'UniformGridRepresentation')

    # change representation type
    extractSubset1Display.SetRepresentationType('Volume')

    # get color transfer function/color map for args.main_variable
    hlLUT = GetColorTransferFunction(args.main_variable)
    hlLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941,
                       0.03771344944834709, 0.865003, 0.865003, 0.865003,
                       0.07542689889669418, 0.705882, 0.0156863, 0.14902]
    hlLUT.ScalarRangeInitialized = 1.0

    # get opacity transfer function/opacity map for args.main_variable
    hlPWF = GetOpacityTransferFunction(args.main_variable)
    hlPWF.Points = [0.0, 0.0,
                    0.5, 0.0,
                    0.07542689889669418, 1.0,
                    0.5, 0.0]
    hlPWF.ScalarRangeInitialized = 1

    # if an external transfer function is specified, apply it here:

    ImportPresets(filename=args.tf[0])

    # Apply a COLOUR LOOK-UP TABLE using its name.
    # NOTE this may not work as expected when presets have duplicate names.
    hlLUT.ApplyPreset(args.tf[1], True)

    # Apply TRANSPARENCIES using its name.
    # NOTE this may not work as expected when presets have duplicate names.
    hlPWF.ApplyPreset(args.tf[1], True)

    # hide data in view
    Hide(input_data, renderView1)



    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    extractSubset1Display = Show(extractSubset1, renderView1, 'UniformGridRepresentation')















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
