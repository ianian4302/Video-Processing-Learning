k = 0.6
sobel_x = np.array([[0, 0, 0], [-1, 0, 1], [0, 0, 0]])
# Sobel filter in y direction
sobel_y = np.array([[0, 1, 0], [0, 0, 0], [0, -1, 0]])
for y in range(1, h-1):
    for x in range(1, w-1):
        I2x[y, x] = np.sum(I2[y-1:y+2, x-1:x+2] * sobel_x * k)
        I2y[y, x] = np.sum(I2[y-1:y+2, x-1:x+2] * sobel_y * k)