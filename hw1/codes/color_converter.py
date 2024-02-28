import numpy as np

class ColorConverter():
    def __init__(self):
        pass
    def rgb_to_yuv(self, r, g, b):
        M = np.array([[0.299, 0.587, 0.114], 
                     [-0.147, -0.289, 0.436],
                     [0.615, -0.515, -0.1]])
        c1 = np.array([r, g, b])
        c2 = M @ c1

        #Ensure uv values to be in (0, 1) 
        y, u, v = c2[0], c2[1], c2[2]
        u = u + 0.5
        v = v + 0.5
        u = u if (u >= 0) else 0
        u = u if (u < 1) else 1
        v = v if (v >= 0) else 0
        v = v if (v < 1) else 1
        return y, u, v
   
