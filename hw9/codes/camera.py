from human_visual_system import *
import numpy as np

class Camera():
    def __init__(self, fov, image_width, image_height, frames_per_second=30):
        # Projection matrix
        F = fov * np.pi / 180 
        w, h = image_width, image_height
        f = h / (2 * (np.tan(F / 2))) #Focal length
        self.P = np.array([[f, 0, w / 2],
                           [0, f, h / 2],
                           [0, 0, 1]])
        # Store focal length
        self.focal = f

        # Latent image: # stored exposure information, value: 0 - 1
        self.I_lat = np.zeros([h, w, 3]) 

        # Scanned image: raster scanning on the latent image
        self.I = np.zeros([h, w, 3])

        # Output attenuation image: raster scanning on the latent image
        self.I_att = np.zeros([h, w, 3])

        # Store image size
        self.w = w
        self.h = h
        
        # Gamman correction parameters
        self.gc = 1.7

        # Record specified frame per second.
        self.fps = frames_per_second

        # Compute line rate and intervals according to fps and fsy
        # fl: line rate (lines per second) = fps * self.h (lines per frame)
        # Tl: line interval = 1 / fl
        # Tl_r: real scanning time
        self.compute_line_rate()
        self.compute_line_interval_ms()

        # Specify horizontal retrace time (Th) and vertical retrace time
        # Th should not larger than Tl
        self.Th = 0.01 * self.Tl

        # Set vertical retrace time in ms
        self.Tv = 0.05

        # Compute real scanning time and scanned lines in a frame
        self.compute_line_scanning_time()

        # Compute scanning time per raster
        self.compute_raster_interval()

        # Scanned raster index
        self.r_idx = 0
        self.elapsed_time_ms_scan = 0
        self.scanned_lines = 0
        self.completed = False

    def compute_line_rate(self):
        # self.h denotes lines per frame
        self.fl =  self.fps * self.h

    def compute_line_interval_ms(self):
        sec2ms = 1000
        self.Tl = sec2ms / self.fl

    def compute_line_scanning_time(self):
        self.Tl_r = self.Tl - self.Th
    
    def compute_raster_interval(self):
        self.Tr = self.Tl / self.w


    def get_focal_length(self):
        return self.focal
    def get_line_interval(self):
        return self.Tl

    def get_raster_scanning_time(self):
        return self.Tr

    def get_raster_index(self):
        return self.r_idx

    def expose(self, lights):
        # Assume the exposure is simultaneously on an area and the exposure time is 0
        # Here we use previous sharpe model for HVS as the camera sensor exposure model
        hvs = HumanVisualSystem()
        for light in lights: 
            r = g = b = 0 # Initialize r, g, b to zeros
            y = u = v = 0 # Initialize y, u, v to zeros

            # Get receptor responses
            r = hvs.red_cone_response(light)
            g = hvs.green_cone_response(light)
            b = hvs.blue_cone_response(light)

            # Capture lights in camera
            x = self.project_to_image_position(light.X)
            self.write_latent_image(x, r, g, b)

    def raster_scan(self, delta_time_ms):
        # Line interval = self.Tr * self.w  + self.Th
        t0 = self.elapsed_time_ms_scan
        t1 = self.elapsed_time_ms_scan + delta_time_ms
        sec2ms = 1000
        T_frame_ms = sec2ms / self.fps 
        l = self.scanned_lines

        if t1 <= T_frame_ms - self.Tv: # Before vertical retracing
           # Determine the elapsed time after horizontally retracing on current line
           t_line = t1 - l * self.Tl
           if t_line <= self.Tl_r:
               # Line scanning
               scan_idx_next = (int) (t_line / self.Tr)
               scan_idx_prev = self.r_idx - self.scanned_lines * self.w
               # The scanning is during horizontal retracing if next scan idx > self.w - 1
               for _ in range(scan_idx_prev, min(scan_idx_next, self.w)):
                   self.raster_scan_one_time()
           elif t_line <= self.Tl: # Re-tracingg
               pass
           else:
               self.scanned_lines += 1
               self.r_idx = self.scanned_lines * self.w

           # Update elapsed time 
           self.elapsed_time_ms_scan = t1
        elif t1 <= T_frame_ms: # During vertical retracing
           # Update elapsed time 
           self.elapsed_time_ms_scan = t1
        else: # Finish vertical retracing
           self.completed = True
           self.elapsed_time_ms_scan = 0

    def raster_scan_one_time(self):
        # Recover image coordinate from raster index. 
        # Let (x[0], x[1]) denote the image coordinate, then r_idx = x[1] * w + x[0].
        x = [0, 0]
        x[1] = int(self.r_idx / self.w)
        x[0] = self.r_idx - x[1] * self.w

        # Record current target raster, after scanning it, the target raster is moved.
        r, g, b = self.I_lat[x[1], x[0], :]
        self.write_scanned_image(x, r, g, b)

        # Increase raster index
        self.r_idx += 1

    def restart_scanning_frame(self):
        self.I = np.zeros([self.h, self.w, 3])
        self.I_att = np.zeros([self.h, self.w, 3])
        self.completed = False
        self.r_idx = 0
        self.scanned_lines = 0

    def frame_completed(self):
        # Indicate whether frame scanning is completed or not.
        return self.completed

    def project_to_image_position(self, X):
        X = np.array(X)
        x = self.P @ X
        x /= x[2]
        # Flip Y to fit image direction
        x[1] = self.h - x[1] 
        # Floor to get integer position
        return x[:2].astype(int)

    def write_latent_image(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.I_lat[x[1], x[0], :] = [r, g, b]

    def write_scanned_image(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.I[x[1], x[0], :] = [r, g, b]

    def output_scanned_image(self):
        # Return scanned image 
        return self.I

    def output_attenuation_image(self):
        # Simulate camera output voltages to the display. 
        # Assuming the scanned image accurately stores brightness information, the output voltages to the display represent an image that distorts the scanned image.
        self.I_att = np.zeros([self.h, self.w, 3])
        for y in range(self.h):
            for x in range(self.w):
                for idx, Bc in enumerate(self.I[y, x]):
                    self.I_att[y, x, idx] = self.get_output_voltage(Bc)
        return self.I_att

    # Used for quick viz. of scanning observation
    def output_attenuation_image_scanned(self, scan_idx_prev, scan_idx_next):
        for idx in range(scan_idx_prev, scan_idx_next):
            y = int(idx / self.w)
            x = idx - y * self.w
            for idx, Bc in enumerate(self.I[y, x]):
                self.I_att[y, x, idx] = self.get_output_voltage(Bc)
        return self.I_att

    def get_output_voltage(self, Bc):
        # Simulate signal attenuation in relation to input brightness on the voltage.
        return np.power(Bc, 1 / self.gc)

    def get_gamma(self):
        return self.gc
