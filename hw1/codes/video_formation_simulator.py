import cv2
from rotated_rainbow import * 
from human_visual_system import *
from color_converter import *
from camera import *
from display import *

# Generate lights from a rotated rainbow
scene = RotatedRainbow()
hvs = HumanVisualSystem()
color_converter = ColorConverter()
time_ms = 0 # in milli seconds
delta_time_ms_light = 10 # in milli seconds 

# Video simulation
fov = 60 # vertical fov in degrees
fps = 30 # frames_per_second
image_width, image_height = 800, 600 # in pixels
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
Vc = cv2.VideoWriter('camera.mp4', fourcc, fps, (image_width, image_height))
Vy = cv2.VideoWriter('luminance.mp4', fourcc, fps, (image_width, image_height))
Vuv = cv2.VideoWriter('chrominance.mp4', fourcc, fps, (image_width, image_height))
Vd = cv2.VideoWriter('display.mp4', fourcc, fps, (image_width, image_height))
Vd_ori = cv2.VideoWriter('display_without_correction.mp4', fourcc, fps, (image_width, image_height))
camera = Camera(fov, image_width, image_height)
display = Display(image_width, image_height)
Iy = np.zeros([image_height, image_width, 3], dtype=np.uint8) # Luminance image
Iuv = np.zeros([image_height, image_width, 3], dtype=np.uint8) # Chrominance image
Id_ori = np.zeros([image_height, image_width, 3], dtype=np.uint8) # Display color image without correction

# Start video capture loop, use human visual system as camera absorption function
frame = 0
ms2sec = 0.001
delta_time_ms_frame = 1000 / fps
while frame < 300:
    lights = scene.generate_lights(time_ms * ms2sec)
    time_ms += delta_time_ms_light

    for light in lights: 
        r = g = b = 0 # Initialize r, g, b to zeros
        y = u = v = 0 # Initialize y, u, v to zeros

	# TODO: Get receptor responses
        r = hvs.red_cone_response(light)
        g = hvs.green_cone_response(light)
        b = hvs.blue_cone_response(light)
	# TODO: Get luminance and chrominance
        y, u, v = color_converter.rgb_to_yuv(r, g, b)
        
	# Capture lights in camera
        x = camera.project_to_image_position(light.X)
        camera.write_image(x, r, g, b)

	# TODO: Simulate attenuation and gamma corrected color on the display
        vc = camera.get_output_voltage(x)
        vd = display.gamma_correct(vc, display.gd)
        bd = display.output_brightness(vd)
        
        display_color = [r, g, b]
        display_color_ori = [r, g, b]
            
        rd, gd, bd = display_color[0], display_color[1], display_color[2]
        display.write_buffer(x, rd, gd, bd)

        # Viz. luminance and chrominance into images
        if (x[1] >= 0 and x[1] < image_height and x[0] >= 0 and x[0] < image_width):
            Iy[x[1], x[0], :] = [int(y * 255), int(y * 255), int(y * 255)]
            Iuv[x[1], x[0], 1:] = [int(u * 255), int(v * 255)]
            rd, gd, bd = display_color_ori[0], display_color_ori[1], display_color_ori[2]
            Id_ori[x[1], x[0], :] = [int(bd * 255), int(gd * 255), int(rd * 255)]

    if time_ms >= frame * delta_time_ms_frame:
        print('write image to video, frame:', frame)
        Ic = camera.output_image()
        Id = display.output_buffer()
        Vc.write(Ic)
        Vy.write(Iy)
        Vuv.write(Iuv)  
        Vd.write(Id)
        Vd_ori.write(Id_ori)
        frame += 1

    print('Elapsed time in ms:', time_ms)

Vc.release()
Vy.release()
Vuv.release()
Vd.release()
Vd_ori.release()
