import cv2
import numpy as np

image_path = 'homeworks/hw11/my_images/'
# I1: the anchor frame
# I2: the tracked frame
I1 = cv2.imread('homeworks/hw11/codes/venus/im2.ppm', cv2.IMREAD_UNCHANGED)
I2 = cv2.imread('homeworks/hw11/codes/venus/im6.ppm', cv2.IMREAD_UNCHANGED)
# Convert RGB image to gray image
I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)
cv2.imwrite(image_path + 'I1.png', I1)
cv2.imwrite(image_path + 'I2.png', I2)

# Get image size
# w: width
# h: height
w, h = I2.shape[1], I2.shape[0]
print('Image size: ', w, h)

# TODO: Compute its gradient images (I2x, I2y) according to the course lecture slides 
# (I2x(y, x), I2y(y, x)) stores the gradient vector of I at position (x, y) 
# Mathematical Definition: I2x(y, x) = I(y, x) - I(y, x-1), I2y(y, x) = I(y, x) - I(y-1, x) 
I2x = np.zeros(I2.shape, dtype=float) # Initialization
I2y = np.zeros(I2.shape, dtype=float)

# I2x: the gradient image in x direction
# I2y: the gradient image in y direction
for y in range(1, h):
    for x in range(1, w):
        I2x[y, x] = I2[y, x] - I2[y, x-1] * 0.99
        I2y[y, x] = I2[y, x] - I2[y-1, x] * 0.99

# use sobel filter to compute the gradient
# Sobel filter in x direction
# sobel_x = np.array([[0, 0, -0], [2, 0, -2], [0, 0, -0]])
# # Sobel filter in y direction
# sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) * 0
# for y in range(1, h-1):
#     for x in range(1, w-1):
#         I2x[y, x] = np.sum(I2[y-1:y+2, x-1:x+2] * sobel_x) * 0.5
#         I2y[y, x] = np.sum(I2[y-1:y+2, x-1:x+2] * sobel_y)

# Compute the magnitude images for viz.
# Gx: magnitudes of I2x: absolute value
# Gy: magnitudes of I2y: absolute value
# G: G(y, x) = sqrt(I2x(x, y)^2 + I2y(x, y)^2)
Gx = np.zeros(I2.shape, dtype=float) # Initialization
Gy = np.zeros(I2.shape, dtype=float)
G = np.zeros(I2.shape, dtype=float)
for y in range(h):
    for x in range(w):
        Gx[y, x] = abs(I2x[y, x])
        Gy[y, x] = abs(I2y[y, x])
        G[y, x] = np.sqrt(I2x[y, x] * I2x[y, x] + I2y[y, x] * I2y[y, x])

# Dump the images
Gx = Gx.astype(np.uint8)
Gy = Gy.astype(np.uint8)
G = G.astype(np.uint8)
cv2.imwrite(image_path + 'Gx.png', Gx)
cv2.imwrite(image_path + 'Gy.png', Gy)
cv2.imwrite(image_path + 'G.png', G)

# TODO: Estimate motion by multipoint method (assume w = 1 for all neighboring pixels) 
# r: (2r+1) x (2r+1) is the neighborhood of a pixel
# L: maximum refine iterations
# a: the alpha value to update motion
# Dx: horizontal motion field 
# Dy: vertical motion field
r = 1
L = 10
a = 1e-2
# Initialize the motion field
Dx = np.zeros(I1.shape)
Dy = np.zeros(I1.shape)
for l in range(L+1):
    print('Iteration: ', l) 
    for y in range(r, h-r):
        for x in range(r, w-r):
            # [dx, dy]: the motion vector of a pixel
            # e: the image error
            # (gx, gy): the partial derivative of the DFD error with respect to d
            dx, dy = Dx[y, x], Dy[y, x]
            gx = 0 #Initialization
            gy = 0 #Initialization
            # TODO: Update energy gradient gx and gy with DFD error (see slides) 
            # e = I1(y, x) - I2(y + dy, x + dx)
            # gx = d/dx e = -d/dx I2(y + dy, x + dx)
            # gy = d/dy e = -d/dy I2(y + dy, x + dx)
            gx = -I2x[y + int(dy), x + int(dx)] 
            gy = -I2y[y + int(dy), x + int(dx)]
            

            # update motion according to energy gradient
            Dx[y, x] = dx - a * gx
            Dy[y, x] = dy - a * gy

    # TODO: Draw predicted image I1_p from tracked frame I2 in this iteration
    # I1_p: the predicted image
    I1_p = np.zeros(I1.shape) #Initialization
    I1_p = I1_p.astype(np.uint8)
    for y in range(h):
        for x in range(w):
            I1_p[y, x] = I2[y + int(Dy[y, x]), x + int(Dx[y, x])]
    cv2.imwrite(image_path + 'I1_p-'+ str(l).zfill(2)+'.png', I1_p)
      
            

