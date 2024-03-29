import cv2
import numpy as np
from sinusoidal_pattern_generator import *
from fourier_transformer import *
from camera import *

video_path = 'homeworks/hw4/my_videos/'
fx_vid = 0.5 # Cycles per mm along horizontal direction
fy_vid = 0.0 # Cycles per mm along vertical direction
vx_vid = 0.2 # Speed along horizontal direction mm/sec
vy_vid = 0.2 # Speed along vertical direction in mm/sec
Tb = 0 # Beginning of the time
dt = 1 # delta time in seconds
Te = 30 # End of the time in seconds
fps = (Te - Tb) / dt

# Physical Length of the image plane
h_mm = 10
w_mm = 10
h_pix = 100
w_pix = 100
intv = 5 # Interval for downsampling the frequency and spatial temporal variables

pattern_generator = SinusoidalPatternGenerator(w_mm, h_mm, w_pix, h_pix, Tb, Te)
phi_st_seq = pattern_generator.generate_moving_sinusoidals(fx_vid, fy_vid, fps, vx_vid, vy_vid, intv)

# Viz for Spatial Temporal Signals
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
Vst = cv2.VideoWriter(video_path + 'spatial_temporal.mp4', fourcc, fps, (w_pix, h_pix))
Ist = np.zeros([h_pix, w_pix, 3], dtype = np.uint8)

F_viz = 0
for phi_st in phi_st_seq:
    # Recover pixel index and frame index 
    b, x, y, t = phi_st[0], phi_st[1], phi_st[2], phi_st[3]

    r = round(y)
    c = round(x)
    F_phi_st = int(t)

    # Dump to video if current frame is filled.
    if (F_phi_st > F_viz):
        Vst.write(Ist)  
        F_viz += 1

    # Normalization
    phi_st_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

    # Draw response with thickness as the specified interval
    Ist[r:r+intv, c:c+intv, :] = int(phi_st_viz * 255) # Mapping to integer

Vst.release()


# Viz for viewer image
fourcc=cv2.VideoWriter_fourcc(*'mp4v')

Vv = cv2.VideoWriter(video_path + 'viewing.mp4', fourcc, fps, (w_pix, h_pix))
Iv = np.zeros([h_pix, w_pix, 3], dtype = np.uint8)
fov = 60
viewer = Camera(fov, w_pix, h_pix, fps) #Treat a viewer with camera
d_mm = 15 # The viewing distance
F_viz = 0
for phi_st in phi_st_seq:
    b, x, y, t = phi_st[0], phi_st[1], phi_st[2], phi_st[3]
    x_mm = x * w_mm / w_pix
    y_mm = y * h_mm / h_pix

    c, r = x, y #Initialize
    # TODO: update (c, r) for viewer image using Camera.project_to_image_position 
    # Notice: the viewer image center should align to the screen center.
    c, r = viewer.project_to_image_position([x_mm-5, y_mm-5, d_mm])
    
    F_phi_st = int(t)
    if (F_phi_st > F_viz):
        Vv.write(Iv)
        F_viz += 1

    # Normalization
    phi_st_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

    # Draw response with thickness as the specified interval
    if r > 0 and r < h_pix - intv and c > 0 and c < w_pix - intv:
        Iv[r:r+intv, c:c+intv, :] = int(phi_st_viz * 255) # Mapping to integer
Vv.release()


# Build frequency sequence: fr_seq
# Arrange variables from temporal to spatial for the convenience of later viz.
ft_seq = [t / (Te - Tb) for t in range(Tb, Te)]
fy_seq = [r / h_pix for r in range(h_pix) if r % intv == 0]
fx_seq = [c / w_pix for c in range(w_pix) if c % intv == 0]

fr_xformer = FourierTransformer(ft_seq, fx_seq, fy_seq)

# Online compute fourier transform
# phi_fr_seq = fr_xformer.transform(phi_st_seq)


#You can use the following code snippet to dump phi_fr_seq to file
# with open('response.fq', 'w') as file:
#     # Write each float number to the file
#     for phi_fr in phi_fr_seq:
#         for idx in range(len(phi_fr)):
#             file.write(f'{phi_fr[idx]} ')


# Read cached frequency response file
phi_fr_seq = []
with open('hw4/codes/response.fq', 'r') as file:
    content = file.read()
    vals = content.split()
    while len(vals) > 0:
        phi_fr_seq.append([float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]), float(vals[4])])
        vals = vals[5:]


# Viz for Frequency Response 
Vfr = cv2.VideoWriter(video_path + 'frequency_response.mp4', fourcc, fps, (w_pix, h_pix))
fr_xformer.prepare_image(h_pix, w_pix)

# Viz the magnitude
fr_mag_seq, min_mag, max_mag = fr_xformer.compute_response_magnitudes(phi_fr_seq)
F_viz = 0
for mag, phi_fr in zip(fr_mag_seq, phi_fr_seq):
    fx, fy, ft = phi_fr[2], phi_fr[3], phi_fr[4]
    r = round(fy * h_pix)
    c = round(fx * w_pix)
    F_phi_fr = round(ft * (Te - Tb))
    if (F_phi_fr > F_viz):
        Vfr.write(fr_xformer.output_image())
        F_viz += 1
    fr_xformer.draw_response_to_image(r, c, mag, min_mag, max_mag, intv)
Vfr.release()

# Shift the frequency signal
dx = 0.02
dy = 0.02
for idx, phi_fr in enumerate(phi_fr_seq):
    fx, fy, ft = phi_fr[2], phi_fr[3], phi_fr[4]
    fx += dx
    fy += dy
    phi_fr_seq[idx][2] = fx
    phi_fr_seq[idx][3] = fy
        

# Uncomment the following code snippet for bonus experiments 
# Remove response on certain frequency region
'''
x_clip = 5
for idx, phi_fr in enumerate(phi_fr_seq):
    fx, fy, ft = phi_fr[2], phi_fr[3], phi_fr[4]
    if fx  > x_clip / w_pix:
        phi_fr_seq[idx][0] = phi_fr_seq[idx][1] = 0
'''


# Reconstruct spatial temporal signal via inverse fourier transform
st_seq = [[phi_st[1], phi_st[2], phi_st[3]] for phi_st in phi_st_seq]

# TODO: Replace phi_st_seq with FourierTransformer.inverse_transform to reconstruct the spatial temporal signal
phi_st_seq = fr_xformer.inverse_transform(phi_fr_seq, st_seq)

fourcc=cv2.VideoWriter_fourcc(*'mp4v')
Vrec = cv2.VideoWriter(video_path + 'reconstruction.mp4', fourcc, fps, (w_pix, h_pix))
Irec = np.zeros([h_pix, w_pix, 3], dtype = np.uint8)

F_viz = 0
for phi_st in phi_st_seq:
    # Recover pixel index and frame index 
    b, x, y, t = phi_st[0], phi_st[1], phi_st[2], phi_st[3]

    r = round(y)
    c = round(x)
    F_phi_st = int(t)

    # Dump to video if current frame is filled.
    if (F_phi_st > F_viz):
        Vrec.write(Irec)  
        F_viz += 1

    # Normalization
    phi_st_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

    # Draw response with thickness as the specified interval
    Irec[r:r+intv, c:c+intv, :] = int(phi_st_viz * 255) # Mapping to integer

Vrec.release()
