import numpy as np

class Signal:
    
    def __init__(self, aPoints):
        self.aPoints        = aPoints
        self.acFourierCoeff = []        
        self.__dX           = aPoints[0]
        self.__dY           = aPoints[1]
        self.__nN           = len(aPoints[0])
        self.__nNumCoeff    = 50
        self.__prepare_data()

    def __prepare_data(self):
        self.__interpolate()

    def __interpolate(self):
        x = np.arange(self.__dX[0], self.__dX[self.__nN-1])
        self.__dY = np.interp(x, self.__dX, self.__dY)
        self.__dX = x
        self.__nN = len(self.__dY)
    
    def get_Fourier_coefficients(self):
        acFourierCoeff = [self.__get_Fourier_coefficient(k) for k in range(0, self.__nN)]
        self.acFourierCoeff = acFourierCoeff
        return acFourierCoeff

    def __get_Fourier_coefficient(self, k):
        cFourierCoeff = 1./float(self.__nN)*sum([self.__dY[l] * np.exp(-1j*k*l*2*np.pi/float(self.__nN)) for l in range(0, self.__nN)])
        return cFourierCoeff

    def __get_coefficients(self):
        acFourierCoeff = [self.__get_coefficient(l) for l in range(0, self.__nN)]
        return acFourierCoeff

    def __get_coefficient(self, l):
        cFourierCoeff = sum([self.acFourierCoeff[k] * np.exp(1j*k*l*2*np.pi/float(self.__nN)) for k in range(0, self.__nN)])
        return cFourierCoeff

    def calculate_signal_from_Fourier_coeff(self):
        if not self.acFourierCoeff:
           self.get_Fourier_coefficients()
        adYCalc = self.__get_coefficients()
        np.testing.assert_array_almost_equal(self.__dY, adYCalc)
        return adYCalc 
    