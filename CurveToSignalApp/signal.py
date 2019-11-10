import numpy as np

class Signal:
    
    def __init__(self, aPoints):
        self.aPoints     = aPoints
        self.__dX        = aPoints[0]
        self.__dY        = aPoints[1]
        self.__nN        = len(aPoints[0])
        self.__nNumCoeff = 10
        
    def get_Fourier_coefficients(self):
        acFourierCoeff = [self.__get_Fourier_coefficient(k) for k in range(0, self.__nN-1)]
        return acFourierCoeff

    def __get_Fourier_coefficient(self, k):
        cFourierCoeff = 1./float(self.__nN)*sum([self.__dY[l] * np.exp(-1j*k*l*2*np.pi/self.__nN) for l in range(0, self.__nN-1)])
        return cFourierCoeff

    def __prepare_data(self):
        pass

    def __interpolate(self):
        pass
    
    def __fourier_series_coeff_numpy(self, f, T, N, return_complex=True):
        """Calculates the first 2*N+1 Fourier series coeff. of a periodic function.

        Given a periodic, function f(t) with period T, this function returns the
        coefficients a0, {a1,a2,...},{b1,b2,...} such that:

        f(t) ~= a0/2+ sum_{k=1}^{N} ( a_k*cos(2*pi*k*t/T) + b_k*sin(2*pi*k*t/T) )

        If return_complex is set to True, it returns instead the coefficients
        {c0,c1,c2,...}
        such that:

        f(t) ~= sum_{k=-N}^{N} c_k * exp(i*2*pi*k*t/T)

        where we define c_{-n} = complex_conjugate(c_{n})

        Refer to wikipedia for the relation between the real-valued and complex
        valued coeffs at http://en.wikipedia.org/wiki/Fourier_series.

        Parameters
        ----------
        f : the periodic function, a callable like f(t)
        T : the period of the function f, so that f(0)==f(T)
        N_max : the function will return the first N_max + 1 Fourier coeff.

        Returns
        -------
        if return_complex == False, the function returns:

        a0 : float
        a,b : numpy float arrays describing respectively the cosine and sine coeff.

        if return_complex == True, the function returns:

        c : numpy 1-dimensional complex-valued array of size N+1

        """
        # From Shanon theoreom we must use a sampling freq. larger than the maximum
        # frequency you want to catch in the signal.
        f_sample = 2 * N
        # we also need to use an integer sampling frequency, or the
        # points will not be equispaced between 0 and 1. We then add +2 to f_sample
        t, dt = np.linspace(0, T, f_sample + 2, endpoint=False, retstep=True)

        y = np.fft.rfft(f) / t.size

        if return_complex:
            return y
        else:
            y *= 2
            return y[0].real, y[1:-1].real, -y[1:-1].imag

    def calculate_signal_from_Fourier_coeff(self):
        T = self.__nPeriod 
        N = self.__nNumCoeff          
        aFourierCoeff = self.get_Fourier_coefficients()
        adYCalc = []
        for t in range(0, T-1):
            dYCalc_neg  = sum([np.conjugate(aFourierCoeff[-k]) * np.exp(2*np.pi*1j*k*t/float(T)) for k in range(-N, 0)])
            dYCalc_pos  = sum([aFourierCoeff[k] * np.exp(2*np.pi*1j*k*t/float(T)) for k in range(1, N)])
            adYCalc[t] = dYCalc_neg + dYCalc_pos 
        return adYCalc 