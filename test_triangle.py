#!/usr/bin/env python

from triangle import triangle

import numpy             as np
import matplotlib.pyplot as plt


from scipy.ndimage import gaussian_filter



X = np.linspace(0,2*np.pi,num=30)
Y = np.linspace(0,2*np.pi,num=40)


Xm,Ym = np.meshgrid(X,Y)

x = 0.25*(1+np.cos(Xm+Ym))
y = 0.25*(1+np.cos(Xm-Ym+np.pi/3.))

z = 1 -x -y

plt.figure(figsize=(8, 12))

plt.subplot(231)
plt.contourf(x)
plt.colorbar()
plt.title('variable x')

plt.subplot(232)
plt.contourf(y)
plt.colorbar()
plt.title('variable y')

plt.subplot(233)
plt.contourf(z)
plt.colorbar()
plt.title('variable z=1-x-y')



######################################
######################################
### Change triangle parameter here:
cb = triangle(num=3,alpha=0.2)
cb.get_color(x,y)
######################################
######################################



img  = cb.img[::-1,:,:]

img2 = gaussian_filter(img, sigma=1.2)

plt.subplot(234)
plt.imshow(img)
plt.title('triplet (x,y,z)')

plt.subplot(235)
plt.imshow(img2)
plt.title('blurred triplet (x,y,z)')


plt.subplot(236)
cb.draw(plt.gca(),xtext='variable x',ytext='variable y',ztext='variable z',fs=8)

plt.show()
