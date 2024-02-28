import numpy as np

class Camera():
    def __init__(self, fov, image_width, image_height):
        # Projection matrix
        F = fov * np.pi / 180 
        w, h = image_width, image_height
        f = h / (2 * (np.tan(F / 2))) #Focal length
        self.P = np.array([[f, 0, w / 2],
                           [0, f, h / 2],
                           [0, 0, 1]])
        self.I = np.zeros([h, w, 3], dtype=np.uint8)
        self.w = w
        self.h = h
        
        # Gamman correction parameters
        self.gc = 1.7
    def project_to_image_position(self, X):
        X = np.array(X)
        x = self.P @ X
        x /= x[2]
        # Flip Y to fit image direction
        x[1] = self.h - x[1] 
        # Floor to get integer position
        return x[:2].astype(int)

    def write_image(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.I[x[1], x[0], :] = [int(b * 255), int(g * 255), int(r * 255)]

    def output_image(self):
        return self.I

    def get_output_voltage(self, Bc):
        return np.power(Bc, 1 / self.gc)

    def get_gamma(self):
        return self.gc
