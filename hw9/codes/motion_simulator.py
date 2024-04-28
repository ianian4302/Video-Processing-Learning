import cv2
from camera import *
from motion_generator import *

image_path = 'hw9/my_images/'
# Specify the planar object
# W: object plane width (in meter)
# H: object plane height (in meter)
# D: object plane distance (in meter)
# intv_x: sampling interval along x direction 
# intv_y: sampling interval along y direction
W = 6 # In meter
H = 4 # In meter
D = 2 # In meter
intv_x = 0.5 # In meter
intv_y = 0.5 # In meter
# P_seq: object points
# P: the 3D object point
# Px: x coordinate of the 3D object point
# Py: y coordinate of the 3D object point
# Pz: z coordinate of the 3D object point
# sx: sampling index along x direction
# sy: sampling index along y direction
# nx: number of samples along x direction
# ny: number of samples along y direction
P_seq = []
Px = 0
Py = 0
sx = 0 
sy = 0
nx = int(W / intv_x)
ny = int(H / intv_y)
for sx in range(nx):
    for sy in range(ny):
        Px = sx * intv_x - 0.5 * W 
        Py = sy * intv_y - 0.5 * H
        Pz = D
        P_seq.append([Px, Py, Pz])

# Project object point P to imaged point p
# p_seq: imaged point sequence
# p: the image point
# w_img: image width
# h_img: image height
p_seq = []
fov = 60
w_img = 600
h_img = 400
camera = Camera(fov, w_img, h_img)
for P in P_seq:
    # Projection
    p = camera.project_to_image_position(P)
    p_seq.append(p)

# Generate rotation and translation matrix
# theta_x, Rx: rotated angle and rotation along x axis
# theta_y, Ry: rotated angle and rotation along y axis
# theta_z, Rz: rotated angle and rotation along z axis
# r: 1D vector unfolded from R = RzRyRx
# T: translation
theta_x = 0 # in degree 
theta_y = 0 # in degree
theta_z = 3 # in degree
Rx = compute_rotation_x(np.radians(theta_x))
Ry = compute_rotation_y(np.radians(theta_y))
Rz = compute_rotation_z(np.radians(theta_z))
R = Rz @ Ry @ Rx
r = np.reshape(R, -1)
T = [0, 0, 0] # in meter

# Implement projective mapping 
# Derive the projective mapping parameters according to the planar object, camera parameters (intrinsic, and motion)
# Z: Object Depth
# F: focal length
# a0, a1, a2, b0, b1, b2: parameters of projective mapping, see course slides
# Initialization
a0 = 0
a1 = 1
a2 = 0
b0 = 0
b1 = 0
b2 = 1
c1 = 0
c2 = 0
# TODO: Deriving the parameters according to camera focal, motion, and object depth. Related variables are:
# r: the 1D rotation vector
# F: derived from camera.get_focal_length()
# T: the translation
# Z: object distance
Z = D
F = camera.get_focal_length()

#K: scaling factor
K = 0.5

# a0, a1, a2, b0, b1, b2, c1, c2
a0 = T[0] * F + r[2] * F * Z # 0
a1 = r[0] * Z * K
a2 = r[1] * Z /2
b0 = T[1] * F + r[5] * F * Z # 0
b1 = r[3] * Z /2
b2 = r[4] * Z * K
c1 = r[6] * Z               
c2 = r[7] * Z

print(a0, a1, a2, b0, b1, b2, c1, c2)

# Create projective mapper
mapper = ProjectiveMapping(a0, a1, a2, b0, b1, b2, c1, c2)

# Draw the motion field
# I: motion image
# px: x coordinate of the imaged point
# py: y coordinate of the imaged point
# d: displacement (motion vector)
# dx: x component of the displacement
# dy: y component of the displacement
I = np.zeros([h_img, w_img, 3], dtype=np.uint8) 
color = [0, 0, 255] # line color
thk = 3 # line thickness
for p in p_seq:
    # Generate motion with solved projective mapping
    px, py = p
    d = mapper.generate_motion([px-w_img/2, py-h_img/2]) #Remove principal translation to satisfy the formula     
    dx, dy = d
    px_1, py_1 = int(px), int(py)
    px_2, py_2 = int(px + dx), int(py + dy)

    # Draw line based on px_1 and px_2
    cv2.line(I, [px_1, py_1], [px_2, py_2], color, thk) 

cv2.imwrite(image_path + 'projective-motion.png', I)

