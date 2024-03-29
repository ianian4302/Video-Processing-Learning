# This class provides utility functions for generating standard 3D sinusoidal patterns 
import numpy as np

class SinusoidalPatternGenerator():
    '''
    Inputs:
        w_mm: plane width in milli meters
        h_mm: plane height in milli meters
        w_pix: number of pixels on the horizontal direction
        h_pix: number of pixels on the vertical direction
        Tb: Beginning of the time
        Te: End of the time
    '''
    def __init__(self, w_mm, h_mm, w_pix, h_pix, Tb, Te):
        self.w_mm = w_mm
        self.h_mm = h_mm
        self.w_pix = w_pix
        self.h_pix = h_pix
        self.Te = Te
        self.Tb = Tb

    '''
    Inputs:
        fx: frequency on horizontal direction in cycles per mm
        fy: frequency on vertical direction in cycles per mm
        ft: frequency on temporal direction in frames per sec
        vx: velocity along horizontal direction in mm/sec
        vy: velocity along vertical direction in mm/sec
        intv: Interval for downsampling the frequency and spatial temporal variables
    Outputs:
        phi_st_seq: temporal spatial signal. A list of 4D vectors: [b, x, y, t], where x, y, t represents the temporal
        sample, and b represent the brightness (singal) on (x, y, t)
    '''
    def generate_moving_sinusoidals(self, fx, fy, ft, vx, vy, intv):
        # Set video dimension
        pix_per_mm = self.w_pix / self.w_mm # Resolution

        # Build time sequence with the interval (Tb, Te, dt) 
        t_vid_vec = []
        dt = self.Te / ft
        t = self.Tb
        while t < self.Te:
            t_vid_vec.append(t)
            t += dt

        # Build spatial-temporal and input signal sequence: phi_st_seq
        # Arrange variables from temporal to spatial for the convenience of viz.
        phi_st_seq = []
        
        for t_vid in t_vid_vec:
            for r in range(self.h_pix):
                for c in range(self.w_pix):
                    if r % intv == 0 and c % intv == 0: # Down sample frequencies for reducing the computing
                        # Compute input signal value as the brightness according to the specified sin pattern
                        x = c / pix_per_mm # In mm
                        y = r / pix_per_mm # In mm
                        t = t_vid / (self.Te - self.Tb)
                        dx = vx * t
                        dy = vy * t
                        b = np.sin(fx * 2 * np.pi * (x + dx) + fy * 2 * np.pi * (y + dy)) # Should located in (-1, 1)
                        phi_st_seq.append([b, c, r, t_vid]) 
        return phi_st_seq
