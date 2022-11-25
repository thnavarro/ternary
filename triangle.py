#!/usr/bin/env python


import numpy             as np
from matplotlib.patches     import Polygon, ConnectionPatch,Arrow
from matplotlib.collections import PatchCollection



class triangle():


###########################################################################
## Create a collection of patches consisting of triangles with RGB colors 

   def __init__(self,num=4,h=np.sqrt(3)/2.,alpha=0):

      self.p     = None
      self.num   = num
      self.h     = h
      self.alpha = alpha

      if self.num > 9:
       print('Too many colors!')
       print('Are you sure you want that?')
       exit()

      self.alpha = max(min(self.alpha,1),0)

      dX = np.array([[1,0],[1,0],[1,0]])
      dY = np.array([[0.5,h],[0.5,h],[0.5,h]])
      
      X0 = np.array([[0,0],[1,0],[0.5,h]])   # upward   triangle
      X1 = np.array([[0.5,h],[1,0],[1.5,h]]) # downward triangle
      
      tri = []
      
      for i in range(num):
        for j in range(num-i):
          tri.append((X0+i*dX+j*dY)/self.num)
      
      for i in range(num-1):
        for j in range(num-1-i):
          tri.append((X1+i*dX+j*dY)/self.num)
   
      #print('Nb triangles : ',len(X))
      
      patches = []
      for i in range(len(tri)):
          polygon = Polygon(tri[i], True)
          patches.append(polygon)

      #patches.append(ConnectionPatch((0,0),(0.5,0.5),"data","data"))
      
      le = 0.05
      dx = -dY[0][0]*le
      dy = -dY[0][1]*le
      for i in range(num+1):
        tick = Arrow(1.*i*dX[0][0]/num,0.,dx,dy,0.) # bottom ticks
        patches.append(tick)
        tick = Arrow(0.5+(i*dY[0][0])/num,self.h-(i*dY[0][1])/num,le,0.,0.) # right ticks
        patches.append(tick)
        tick = Arrow(i*dY[0][0]/num,i*dY[0][1]/num,dx,-dy,0.) # left ticks
        patches.append(tick)
            
      self.p = PatchCollection(patches, alpha=0.9)
      
      colors = []
      for i in range(len(tri)):
         x = tri[i].mean(0)[0]
         # linear transform from [1/(2num);(2num-1)/(2num)] to [0;2]
         xc = (2*x*num-1)/(num-1.)
      
         #y = tri[i].mean(0)[1]
         y = (tri[i].max(0)[1] + tri[i].min(0)[1])/2.
         # linear transform from [h/(2num);(2num-1)h/(2num)] to [0;1]
         yc = (y*2*num-h)/(2*h*(num-1))
      
         rvb =  np.zeros(3)
         rvb[1] = (xc-yc)/2.
         rvb[2] = yc
         rvb[0] = 1. - rvb[2] - rvb[1]
         #rvb[1] = (xc-yc)/2.
         #rvb[0] = yc
         #rvb[2] = 1. - rvb[0] - rvb[1]
      
         # deal w/ rounding errors to be sure to have 0<=rgb<=1
         eps = 1e-3
         rvb = 0.5 + (1-eps)*(rvb-0.5)
      
         if np.min(rvb) < 0:
            print('Problem, rvb<0')
            print(x,y,xc,yc,rvb)
            exit()
      
         div = np.max(rvb)*(1-self.alpha) + self.alpha
         rvb = rvb/div
         rvb = rvb**0.7 # change contrast

         colors.append(rvb)
      
         #plt.scatter(x,y,c='k')
      
      self.p.set_color(colors)
      self.p.set_edgecolor('k')
      self.p.set_linewidth(1)
      
      #return(p,h)
   
   
###########################################################################
## create a field of rbg values from two fields of x and y values
## with x+y+z = 1 and 0 <= (x,y,z) <=1

   def get_color(self,xfield,yfield):
   
     ## check x and y size and 0< x+y <1
     ## unravel/ravel to deal with any size

     n = self.num

     self.img  = np.zeros((xfield.shape[0],xfield.shape[1],4))
     self.img2 = np.zeros((xfield.shape[0],xfield.shape[1],4))

     for j in range(xfield.shape[1]):
       for i in range(xfield.shape[0]):
   
          x = xfield[i,j]
          y = yfield[i,j]
          z = 1. - x - y
    
          if x>0 and x<1 and y>0 and y<1 and z>0 and z<1:
    
             xi = int(x*n)
             yi = int(y*n)
             zi = int(z*n)
    
             offset = 0
             for l in range(n):
               if xi == l: ci     = offset + n-l-1 - yi
               else:       offset = offset + n-l
             if xi+yi != n-1:
              if zi == n-2-xi-yi:
               ci = ci + n*(n+1)/2 - 1 - xi
  
             if ci >= n*n: 
               print('Problem, triangle does not exist')
               print(x,y,z)
               print(xi,yi,zi,ci,i,j)
               exit()
 
             #self.img[i,j] = self.p.properties()['facecolors'][ci] # f matplotlib < v3.3.3
             self.img[i,j] = self.p.get_facecolor()[int(ci)]
   

          rvb =  np.zeros(3)
          rvb[2] = x
          rvb[0] = y
          rvb[1] = 1. - rvb[0] - rvb[2]

          div = np.max(rvb)*(1-self.alpha) + self.alpha
          rvb = rvb/div

          if np.max(rvb) <= 1. and np.min(rvb) >= 0.:
              self.img2[i,j] = np.concatenate((rvb,[1.0]))
          else:
              self.img2[i,j] = np.array([1.0,1.0,1.0,0.0])


###########################################################################
## Draw triangle in given axes handle

   def draw(self,ax,xtext='x-axis',ytext='y-axis',ztext='z-axis',fs=12):

      import matplotlib.pyplot as plt

      ax.add_collection(self.p)
      
      pad = 0.2
      plt.xlim(xmin=0-pad,xmax=1+pad)
      plt.ylim(ymin=0-pad,ymax=self.h+pad)
      plt.axis('off')
      
      pad = 0.1
      plt.text(0.5,-2*pad,xtext, \
         verticalalignment='center',horizontalalignment='center',fontsize=fs)
      plt.text(0.8+pad,self.h/2.+pad,ytext,rotation= -60, \
         verticalalignment='center',horizontalalignment='center',fontsize=fs)
      plt.text(0.2-pad,self.h/2.+pad,ztext,rotation= 60, \
         verticalalignment='center',horizontalalignment='center',fontsize=fs)
      
      pad = 0.08
      
      plt.text(0.01-pad,-pad-0.01,'0',fontsize=fs,horizontalalignment='center')
      plt.text(1.01-pad,-pad-0.01,'1',fontsize=fs,horizontalalignment='center')
      plt.text(1.+pad,0.,'0',verticalalignment='center',fontsize=fs)
      plt.text(0.5+pad,self.h,'1',verticalalignment='center',fontsize=fs)
      plt.text(0.5-pad,self.h+pad,'0',fontsize=fs)
      plt.text(0.-pad,pad,'1',fontsize=fs)
      
      plt.gca().set_aspect(1)


   

