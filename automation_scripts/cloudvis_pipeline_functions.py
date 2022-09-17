# Importable Function Definitions for the Cloud Visualisation Pipeline
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









def setup_light(camera_rotation=0, light_rotation=90,
                light_from_above=0, normalise_light_direction=0,
                light_radius=0.0, light_intensity=0.6):
    ################################ LIGHT SETUP ###################################
    # STEP 7.	Add Light n degrees rotated from camera (or above the data):
    # Create a new 'Light'
    light1 = AddLight(view=renderView1)

    # toggle 3D widget visibility (only when running from the GUI)
    # Show3DWidgets(proxy=light1)
    # Hide3DWidgets(proxy=light1)
    # HideInteractiveWidgets(proxy=light1)


    # camera-centre distance:
    camera_centre_distance = math.dist((cam.GetPosition()[1], cam.GetPosition()[2]),
                                       (cam.GetFocalPoint()[1], cam.GetFocalPoint()[2]))

    # if the user requested camera rotation around the orbit circle path, ...
    # ... compute it here (this will offset the camera from the default origin ...
    # ... following an orbit path)
    camera_y_pos = y_light(camera_centre_distance, locals()["camera_rotation"], campos[1], campos[2], camfocus)
    camera_z_pos = z_light(camera_centre_distance, locals()["camera_rotation"], campos[1], campos[2], camfocus)

    campos[1] = camera_y_pos
    campos[2] = camera_z_pos
    cam.SetPosition(campos[0], campos[1], campos[2])

    # by default, assuming light position is above the camera:
    light_x_pos = main_display.SliceFunction.Origin[0]+camera_centre_distance
    light_y_pos = main_display.SliceFunction.Origin[1]
    light_z_pos = main_display.SliceFunction.Origin[2]

    if locals()["light_above"]:
        light1.Position = [light_x_pos, light_y_pos, light_z_pos]
        if locals()["normalise_light_direction"]:
            light1.FocalPoint = [light_x_pos-1.0, light_y_pos, light_z_pos]
        else:
            light1.FocalPoint = list(camfocus)

    else:
        light_y_pos = y_light(camera_centre_distance, locals()["light_rotation"], campos[1], campos[2], camfocus)
        light_z_pos = z_light(camera_centre_distance, locals()["light_rotation"], campos[1], campos[2], camfocus)

        # update the light
        # will be on the same height as camera, just by 'args.light_rotation' offset ...
        # on a circular plane.
        light1.Position = [campos[0], light_y_pos, light_z_pos]

        if locals()["normalise_light_direction"]:
            light1.FocalPoint = [campos[0],
                                 light_y_pos+(camfocus[0]-light_y_pos)/camera_centre_distance,
                                 light_z_pos+(camfocus[1]-light_z_pos)/camera_centre_distance]
        else:
            light1.FocalPoint = list(camfocus)



    # Properties modified on light1
    light1.Radius = locals()["light_radius"]

    # Light intensity:
    light1.Intensity = locals()["light_intensity"] # 0.6 gives good results

    ############################ END OF LIGHT SETTINGS #############################











def setup_rtx(  colour_palette='BlackBackground', backend="OSPRay pathtracer",
                samples_per_pixel=30, progressive_passes=10, denoise=1,
                environmental_background=[0.0, 0.0, 0.0],
                enable_rtx=0):
    ############################ RAY-TRACING SETTINGS ##############################

    # Change background colour for ray-tracing here:
    LoadPalette(paletteName=locals()["colour_palette"])

    # find settings proxy
    generalSettings = GetSettingsProxy('GeneralSettings')
    # enable streaming for pathtracing progressive passes support:
    generalSettings.EnableStreaming = 1

    # find settings proxies
    renderViewInteractionSettings = GetSettingsProxy('RenderViewInteractionSettings')
    renderViewSettings = GetSettingsProxy('RenderViewSettings')
    representedArrayListSettings = GetSettingsProxy('RepresentedArrayListSettings')
    colorPalette = GetSettingsProxy('ColorPalette')

    # Properties modified on renderView1
    renderView1.EnableRayTracing = 1

    # Properties modified on renderView1
    renderView1.SamplesPerPixel = locals()["samples_per_pixel"] #30

    # Properties modified on renderView1
    renderView1.ProgressivePasses = locals()["progressive_passes"] #10

    # Controlling denoising:
    renderView1.Denoise = locals()["denoise"] #1

    # By default, choose the OSPRay pathtracer
    renderView1.BackEnd = locals()["backend"] #'OSPRay pathtracer'

    # Properties modified on renderView1
    # set pathtracing background to be black
    # (best contrast for clouds)
    renderView1.EnvironmentalBG = locals()["environmental_background"] #[0.0, 0.0, 0.0]

    # Disable ray tracing for now, as we just set up the default parameters, ...
    # ... but will not save to image unless user specifies to do so
    renderView1.EnableRayTracing = locals()["enable_rtx"] #0
    ########################## END OF RAY-TRACING SETTINGS #########################





















def animation_setup(anim_time_start=0.0, anim_time_end=1.0,
                    num_frames=180, num_orbits=1):
    ############################## ANIMATION SETTINGS ##############################
    # get animation scene
    animationScene1 = GetAnimationScene()

    # Set start/end times of animation explicitly
    animationScene1.StartTime = locals()["anim_time_start"] #0.0
    animationScene1.EndTime = locals()["anim_time_end"] #1.0

    # get the time-keeper
    timeKeeper1 = GetTimeKeeper()

    # Properties modified on animationScene1
    animationScene1.NumberOfFrames = locals()["num_frames"] #180

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

    for i in range(0, locals()["num_orbits"]):
        # create a key frame
        keyFrame1 = CameraKeyFrame()
        # keyFrame1.KeyTime = args.anim_time_start + args.anim_time_end/args.num_orbits * i
        # NOTE: time for orbits actually goes from 0.0 to 1.0, even though actual time steps might got from 0.0 to 7.0 etc.
        keyFrame1.KeyTime = args.anim_time_start + 1.0/locals()["num_orbits"] * i
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
        keyFrame2.KeyTime = args.anim_time_start + 1.0/locals()["num_orbits"] * (i+1)
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















def crossect_setup(crossect_plane=1, crossect_percent=50.0):
        # There is a ParaView filter which already does this called 'Clip' ...
        # ... but it is horribly inefficient, as it converts the data ...
        # ... from what might be Structured Uniform Grid (Image) to Unstructured Grid ...
        # ... and volume rendering runs much slower for unstructured data.
        # Therefore, we use the ExtractSubset filter here to manually ....
        # ... compute the cross-section plane, and keep the date in the Image format

        # create a new 'Extract Subset'
        extractSubset1 = ExtractSubset(registrationName='CrossSectionVolume1', Input=input_data)
        # extractSubset1.VOI[args.crossect_plane] = [0, 128, 0, 127, 0, 127]

        index1 = locals()["crossect_plane"]
        index2 = ((index1+1)%2) + index1 - (index1%2)

        split_on_value = math.floor((extractSubset1.VOI[index1] + extractSubset1.VOI[index2]) * locals()["crossect_percent"]/100.0)

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

        # If there is a custom transfer function ...
        # ... need to separately set it outside this function, like following:
        # ImportPresets(filename=args.tf[0])
        #
        # # Apply a COLOUR LOOK-UP TABLE using its name.
        # # NOTE this may not work as expected when presets have duplicate names.
        # hlLUT.ApplyPreset(args.tf[1], True)
        #
        # # Apply TRANSPARENCIES using its name.
        # # NOTE this may not work as expected when presets have duplicate names.
        # hlPWF.ApplyPreset(args.tf[1], True)
        #
        # # hide data in view
        # Hide(input_data, renderView1)



        # get active view
        renderView1 = GetActiveViewOrCreate('RenderView')

        # show data in view
        extractSubset1Display = Show(extractSubset1, renderView1, 'UniformGridRepresentation')
