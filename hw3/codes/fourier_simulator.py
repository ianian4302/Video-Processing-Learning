import cv2
import numpy as np

video_path = 'homeworks/hw3/my_videos/'
# Set video signal of a sin pattern:  
# sin(fx_vid * 2 * pi * (x + vx_vid * t) + fy_vid * 2 * pi * (y + vy_vid * t)) # 
fx_vid = 5 # Cycles per mm along horizontal direction
fy_vid = 5 # Cycles per mm along vertical direction
vx_vid = 0.5 # Speed along horizontal direction mm/sec
vy_vid = 0.5 # Speed along vertical direction in mm/sec
Tb = 0 # Beginning of the time
dt = 1 # delta time in seconds
Te = 30 # End of the time in seconds

# Physical Length of the image plane
h_mm = 15
w_mm = 15

# Set video dimension
pix_per_mm = 10 # Resolution
intv = 10 # Interval for downsampling the frequency and spatial temporal variables

# Compute image size of the video
h_vid = int(h_mm * pix_per_mm) # Height in pixels
w_vid = int(w_mm * pix_per_mm) # Width in pixels

# Build time sequence with the interval (Tb, Te, dt) 
t_vid_vec = []
t = Tb
while t < Te:
    t_vid_vec.append(t)
    t += dt

# Build frequency sequence: fr_seq
# Arrange variables from temporal to spatial for the convenience of later viz.
fr_seq = []
for t in t_vid_vec:
    for r in range(h_vid):
        fy = r
        for c in range(w_vid):
            fx = c
            if r % intv == 0 and c % intv == 0: # Down sample frequencies for reducing the computing
                ft = t
                fr_seq.append([fx, fy, ft])

# Build spatial-temporal and input signal sequence: st_seq, phi_st_seq
# Arrange variables from temporal to spatial for the convenience of later viz.
st_seq = []
phi_st_seq = []
for t in t_vid_vec:
    for r in range(h_vid):
        y = r / h_vid # Normalize to 0 - 1
        for c in range(w_vid):
            x = c / w_vid # Normalize to 0 - 1
            if r % intv == 0 and c % intv == 0: # Down sample frequencies for reducing the computing
                st_seq.append([x, y, t / (Te - Tb)])
                # Compute input signal value as the brightness according to the specified sin pattern
                dx = (vx_vid * t) * pix_per_mm / w_vid 
                dy = (vy_vid * t) * pix_per_mm / w_vid
                b = np.sin(fx_vid * 2 * np.pi * (x + dx) + fy_vid * 2 * np.pi * (y + dy)) # Should located in (-1, 1)
                phi_st_seq.append(b) 


# Get frequency response by computing fourier transform on the input signals
phi_fr_seq = []
for f in fr_seq:
    fx, fy, ft = f[0], f[1], f[2]
    phi_fr_real = 0
    phi_fr_img = 0
    for st, phi_st in zip(st_seq, phi_st_seq):
        angle = 0 # Intialization
        # TODO: Caculate the required angle:
        # 1. Inner product of the spatial-temporal and frequency variables
        # 2. Multiply constant term -2 pi 
        # 3. Accumulate the angle
        angle = -2 * np.pi * (fx * st[0] + fy * st[1] + ft * st[2])
        cos_term = np.cos(angle)
        sin_term = np.sin(angle)
        phi_fr_real += phi_st * cos_term - 0 * sin_term
        phi_fr_img += phi_st * sin_term + 0 * cos_term
   
    # Normalization 
    phi_fr_real /= len(st_seq)
    phi_fr_img /= len(st_seq)
    print('fx:', fx, 'fy:', fy, 'ft:', ft, 'phi fr real:', phi_fr_real, 'phi fr img:', phi_fr_img)
    phi_fr_seq.append([phi_fr_real, phi_fr_img])

# Viz for Spatial Temporal Signals
fps = len(t_vid_vec)
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
Vst = cv2.VideoWriter(video_path + 'spatial_temporal.mp4', fourcc, fps, (w_vid, h_vid))
Ist = np.zeros([h_vid, w_vid, 3], dtype = np.uint8)

F_viz = 0
for st, phi_st in zip(st_seq, phi_st_seq):
    # Recover pixel index and frame index 
    x, y, t = st[0], st[1], st[2]
    r = round(y * h_vid)
    c = round(x * w_vid)
    F_phi_st = int(t * (Te - Tb) / dt)

    # Dump to video if current frame is filled.
    if (F_phi_st > F_viz):
        Vst.write(Ist)  
        F_viz += 1

    # Normalization
    phi_st_viz = (phi_st + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

    # Draw response with thickness as the specified interval
    Ist[r:r+intv, c:c+intv, :] = int(phi_st_viz * 255) # Mapping to integer

Vst.release()
     
# Viz for Frequency Response 
Vfr = cv2.VideoWriter(video_path + 'frequency_response.mp4', fourcc, fps, (w_vid, h_vid))
Ifr = np.zeros([h_vid, w_vid, 3], dtype = np.uint8)

# Viz the magnitude
fr_mag_seq = [np.sqrt(phi_fr[0] * phi_fr[0] + phi_fr[1] * phi_fr[1]) for phi_fr in phi_fr_seq]
min_mag, max_mag = min(fr_mag_seq), max(fr_mag_seq)

F_viz = 0
for f, fr_mag in zip(fr_seq, fr_mag_seq):
    fx, fy, ft = f[0], f[1], f[2]
    r = round(fx)
    c = round(fy)
    F_phi_fr = round(ft / dt)
    if (F_phi_fr > F_viz):
        Vfr.write(Ifr)
        F_viz += 1

    # Normalization
    if max_mag != min_mag:
        fr_mag_viz = (fr_mag - min_mag) / (max_mag - min_mag) # Mapping the value from (min_mag, max_mag) to (0, 1)
    else:
        fr_mag_viz = 0

    # Draw response with thickness as the specified interval
    Ifr[r:r+intv, c:c+intv, :] = int(fr_mag_viz * 255) # Mapping to integer

Vfr.release()
