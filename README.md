# ternary
This is a simple python class to create a single 2D color plot of three 2D variables x,y,z such that x+y+z=1

In other words, it creates a color plot where the colorbar is a ternary plot of x,y,z

Run test_triangle to produce an example plot.


#######
Tested with matplotlib v3.3.4 and python v3.8.8


#######
cb = triangle(num,alpha) creates a triangle object with num subdivisions (default 4) and color blending coefficient alpha (default 0)
cb.get_color(x,y) generates the color field of the 2D variables (x,y)
the color field is the cb.img attribute
cb.draw() plots the ternary colorbar
