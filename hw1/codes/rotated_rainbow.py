import numpy as np

class Light():
   def __init__(self, pos, time, wavelength):
      self.X = pos
      self.t = time
      self.l = wavelength
      self.I = 1 # e: intensity, assume the light intensity is independent of position, time, and wavelength

class RotatedRainbow():
    def __init__(self):
        # Settings for scene
        self.radii_m = [100, 200, 300, 400, 500, 600, 700] # Base radii of rainbow circles in meters 
        self.rotation_deg_per_sec = 100 # rotated speed in degrees per second
        self.bins_circle = 360 # bins per circle
        self.angular_division_deg = 360 / self.bins_circle # Angular division of each bin
        self.radial_samples_circle = 20 # samples along radial direction for each circle 
        self.circle_thickness_m = 100 # circle thickness in meters 
        self.onset_sec = 0 # Start time of the lights 
        self.distance = 2000 # rainbow distance in meters

        # Light wavelengths reference: chatgpt
        # Red: 620-750 nanometers
        # Orange: 590-620 nanometers
        # Yellow: 570-590 nanometers
        # Green: 495-570 nanometers
        # Blue: 450-495 nanometers
        # Indigo: 420-450 nanometers
        # Violet: 380-420 nanometers 
        # Wavelengths corresponding to upper segment of the rainbow in nanometers at onset
        # (Violet, Indigo, Blue, Green, Yellow, Orange, Red) 
        self.upper_wavelengths_nn = [400, 430, 475, 530, 580, 620, 750]

        # Wavelengths corresponding to upper segment of the rainbow in nanometers at onset
        # (Red, Orange, Yellow, Green, Blue, Indigo, Violet)
        self.lower_wavelengths_nn = [380, 420, 450, 520, 570, 600, 700]    
        
    # elapsed_sec: Duration for rainbow ratation in seconds 
    def generate_lights(self, elapsed_sec):
        # Compute delta angle in radian
        t = elapsed_sec
        Ad = elapsed_sec * self.rotation_deg_per_sec * np.pi / 180
        lights = []
        for idx, radius in enumerate(self.radii_m):
            for sample in range(self.radial_samples_circle):
                r = radius + (sample / self.radial_samples_circle) * self.circle_thickness_m
                # Sampling along circle
                for b in range(self.bins_circle):
                    # Baseline angle
                    Ab = b * self.angular_division_deg * np.pi / 180
                    
                    # Final angle
                    Af = Ab + Ad

                    # Compute final position X
                    X = [r * np.cos(Af), r * np.sin(Af), self.distance]
                
                    # Get corresponding wavelength
                    if (b < self.bins_circle / 2):
                       l = self.upper_wavelengths_nn[idx]
                    else:
                       l = self.lower_wavelengths_nn[idx] 
                    
                    # Record light   
                    light = Light(X, t, l)
                    lights.append(light)
        return lights
