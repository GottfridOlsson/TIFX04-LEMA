# created: 2022-04-22, 13:55
# skeleton for dataanalysis in KANDXXX

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

gaussian_filter1d([1.0, 2.0, 3.0, 4.0, 5.0], 1)
#scipy.ndimage.gaussian_filter1d(input, sigma, axis=- 1, order=0, output=None, mode='reflect', cval=0.0, truncate=4.0)


t = [0,   1,  2,  3,  4,  5,  6,  7,  8,  9, 10]
x = [10, 11, 12, 12, 13, 15, 16, 20, 25, 35, 45]

v = np.gradient(x)/np.gradient(t)

print(len(x), len(t), len(v))
plt.plot(t, v)
plt.plot(t, x)
plt.show()
# export data to file

#gör mappar för .tsv och .csv och utjämnade osv!