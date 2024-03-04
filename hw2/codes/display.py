import numpy as np

class Display():
    def __init__(self, image_width, image_height):
        self.w = image_width
        self.h = image_height
        self.clear_buffer()
        self.gd = 2.4 # Gamma correction parameter

    def gamma_correct(self, vc, gc):
        return np.power(vc, gc / self.gd)

    def output_brightness(self, vd):
        return np.power(vd, self.gd)

    def write_buffer(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.B[x[1], x[0], :] = [int(b * 255), int(g * 255), int(r * 255)]

    def output_buffer(self):
        return self.B

    def clear_buffer(self):
        self.B = np.zeros([self.h, self.w, 3], dtype=np.uint8) # Screen buffer

    
