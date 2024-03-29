import numpy as np

class FourierTransformer():
    def __init__(self, ft_seq, fx_seq, fy_seq):
        self.ft_seq = ft_seq
        self.fx_seq = fx_seq
        self.fy_seq = fy_seq
        self.fr_seq = []
        for ft in ft_seq:
            for fx in fx_seq:
                for fy in fy_seq:
                    self.fr_seq.append([fx, fy, ft])

    def transform(self, phi_st_seq):
        # Get frequency response by computing fourier transform on the input signals
        phi_fr_seq = []
        for f in self.fr_seq:
            fx, fy, ft = f[0], f[1], f[2]
            phi_fr_real = 0
            phi_fr_img = 0
            for phi_st in phi_st_seq:
                b, x, y, t = phi_st[0], phi_st[1], phi_st[2], phi_st[3]
                angle = 0
                # TODO: Caculate the required angle:
                # 1. Inner product of the spatial-temporal and frequency variables
                # 2. Multiply constant term -2 pi 
                angle = -2 * np.pi * (fx * x + fy * y + ft * t)
                cos_term = np.cos(angle)
                sin_term = np.sin(angle)
                phi_fr_real += b * cos_term - 0 * sin_term
                phi_fr_img += b * sin_term + 0 * cos_term

            print('fx:', fx, 'fy:', fy, 'ft:', ft, 'phi fr real:', phi_fr_real, 'phi fr img:', phi_fr_img)
            phi_fr_seq.append([phi_fr_real, phi_fr_img, fx, fy, ft])

        return phi_fr_seq

    def inverse_transform(self, phi_fr_seq, st_seq):
        phi_st_seq = []
        count = 0
        for st in st_seq:
            x, y, t = st[0], st[1], st[2]
            phi_st_real = 0
            phi_st_img = 0
            for phi_fr in phi_fr_seq:
                phi_fr_real, phi_fr_img, fx, fy, ft = phi_fr[0], phi_fr[1], phi_fr[2], phi_fr[3], phi_fr[4]
                angle = 0 # Initialization
                # TODO: Caculate the required angle:
                # 1. Inner product of the spatial-temporal and frequency variables
                # 2. Multiply constant term 2 pi 
                angle = 2 * np.pi * (fx * x + fy * y + ft * t)
                cos_term = np.cos(angle)
                sin_term = np.sin(angle)
                phi_st_real += (phi_fr_real * cos_term - phi_fr_img * sin_term)
                phi_st_img += (phi_fr_real * sin_term + phi_fr_img * cos_term)
            phi_st_real /= len(st_seq)
            phi_st_img /= len(st_seq)
            phi_st_seq.append([phi_st_real, x, y, t])

        #Normalize to [-1, 1]
        max_phi = max([phi_st[0] for phi_st in phi_st_seq])
        min_phi = min([phi_st[0] for phi_st in phi_st_seq])
        print('max reconstructed val:', max_phi, 'min reconstructed val:', min_phi)
        for idx, phi_st in enumerate(phi_st_seq):
            phi_st_seq[idx][0] = 2 * (phi_st[0] - min_phi) / (max_phi - min_phi) - 1 
        
        return phi_st_seq

    def compute_response_magnitudes(self, phi_fr_seq):
        fr_mag_seq = [np.sqrt(phi_fr[0] * phi_fr[0] + phi_fr[1] * phi_fr[1]) for phi_fr in phi_fr_seq]
        min_mag, max_mag = min(fr_mag_seq), max(fr_mag_seq)
        return fr_mag_seq, min_mag, max_mag

    def prepare_image(self, h, w):
        self.Ifr = np.zeros([h, w, 3], dtype = np.uint8)

    def draw_response_to_image(self, r, c, mag, min_mag, max_mag, intv):
        # Normalization
        if (max_mag != min_mag):
            mag_viz = (mag - min_mag) / (max_mag - min_mag) # Mapping the value from (min_mag, max_mag) to (0, 1)
        else:
            mag_viz = 0

        # Draw response with thickness as the specified interval
        self.Ifr[r:r+intv, c:c+intv, :] = int(mag_viz * 255) # Mapping to integer

    def output_image(self):
        return self.Ifr
       

