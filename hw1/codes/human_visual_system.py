import numpy as np
class HumanVisualSystem():
    def __init__(self):
        # Adopt Stockman and Sharpe 10 degree cone fundamentals for normalized spectral sensitivity:
        # Normalized spectral sensitivity S =  (1 / (A1 + A2)) (A1 exp (-L^2 / (2 * sigma_1^2) ) + A2 exp (-L^2 / (2 * sigma_2^2 )))
        # L = log(l / l_p), l: wavelength, l_p: peak wavelength
        # Reference: chatGPT
        self.A1_L = 0.0803
        self.A2_L = 0.886
        self.s1_L = 0.0993
        self.s2_L = 0.14
        self.lp_L = 650.1
        self.A1_M = 0.1122
        self.A2_M = 0.7474
        self.lp_M = 534.1
        self.s1_M = 0.0813
        self.s2_M = 0.13
        self.A1_S = 0.1392
        self.A2_S = 0.8068
        self.lp_S = 437
        self.s1_S = 0.542
        self.s2_S = 0.13
    def red_cone_response(self, light):
        # Apply parameters of long wavelength sensitivity 
        return light.I * self.response(self.A1_L, self.A2_L, self.s1_L, self.s2_L, self.lp_L, light.l)
    def green_cone_response(self, light):
        # Apply parameters of medium wavelength sensitivity 
        return light.I * self.response(self.A1_M, self.A2_M, self.s1_M, self.s2_M, self.lp_M, light.l)
    def blue_cone_response(self, light):
        # Apply parameters of blue wavelength sensitivity 
        return light.I * self.response(self.A1_S, self.A2_S, self.s1_S, self.s2_S, self.lp_S, light.l)
    def response(self, A1, A2, s1, s2, lp, l):
        Sp = 1 / (A1 + A2)
        L = np.log(l / lp)
        G1 = A1 * np.exp(-np.power(L, 2) / (2 * np.power(s1, 2)))
        G2 = A2 * np.exp(-np.power(L, 2) / (2 * np.power(s2, 2)))
        return Sp * (G1 + G2)
        


