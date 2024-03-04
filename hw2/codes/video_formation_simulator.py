import cv2
from rotated_rainbow import * 
from human_visual_system import *
from color_converter import *
from camera import *
from display import *

video_path = 'homeworks/hw2/my_videos/'
# Generate lights from a rotated rainbow
scene = RotatedRainbow()
color_converter = ColorConverter()
elapsed_time_ms = 0 # in milli seconds
delta_time_ms_light = 10 # in milli seconds 

# Video simulation
fov = 60 # vertical fov in degrees
frames_per_second = 30 # 
image_width, image_height = 200, 150 # in pixels
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
Vd = cv2.VideoWriter(video_path +'display.mp4', fourcc, frames_per_second, (image_width, image_height))
camera = Camera(fov, image_width, image_height, frames_per_second)
display = Display(image_width, image_height)

# Start video capture loop, use human visual system as camera absorption function
frame = 0
delta_time_ms_frame = 1000 / frames_per_second

# Illustrate the raster scanning processing by snapshoting the image on line rate
# Calculate the observation counter duration by setting it as the line interval divided by the number of rasters per line (i.e., the image width).
elapsed_time_ms_observ = 0
Tl = camera.get_line_interval()
delta_time_ms_observ = Tl / image_width
frame_observ = 0

# Constant for millisecond to second conversion
ms2sec = 0.001
while frame < 3:
    lights = scene.generate_lights(elapsed_time_ms * ms2sec)
    elapsed_time_ms += delta_time_ms_light

    camera.expose(lights) 

    if elapsed_time_ms >= frame * delta_time_ms_frame:
        print('Start scanning for frame:', frame)
        elapsed_time_ms_observ = 0
        frame_observ = 0
        scan_idx_prev = 0
        camera.restart_scanning_frame()
        while not camera.frame_completed():
            camera.raster_scan(delta_time_ms_observ)

            # Display the scanning image.
            # If the observation timing precedes the completion of the frame, intermediate scanning results become visible.
            if (elapsed_time_ms_observ >= frame_observ * (0.1 * Tl)):
                #I_dist = camera.output_attenuation_image()
                I_dist = camera.output_attenuation_image_scanned(scan_idx_prev,
                                                                 camera.get_raster_index())
                gc = camera.get_gamma()

                # Update latest scanned segment only for quick viz. freshing
                for idx in range(scan_idx_prev, camera.get_raster_index()):
                    y = int(idx / image_width)
                    x = idx - y * image_width
                    r, g, b = I_dist[y, x, :]
                    display_color = [r, g, b]
                    # TODO: Record brightness after correction (already done it on hw1)
                    vc = camera.get_output_voltage(x)
                    vd = display.gamma_correct(vc, display.gd)
                    bd = display.output_brightness(vd)
        
                    rd, gd, bd = display_color[0], display_color[1], display_color[2]
                    display.write_buffer([x, y], rd, gd, bd)

                print('Observe scanned lines:', camera.scanned_lines, 'r_idx:', camera.get_raster_index())
                Id = display.output_buffer()
                Vd.write(Id)
                frame_observ += 1
                scan_idx_prev = camera.get_raster_index()

            elapsed_time_ms_observ += delta_time_ms_observ

        # Clear the display buffer to prevent the retention of content from the previous frame.
        display.clear_buffer() 
        frame += 1

    print('Elapsed time in ms:', elapsed_time_ms)

Vd.release()
