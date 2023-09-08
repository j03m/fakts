#!/usr/bin/env python2.7                                                        

import matplotlib.pyplot as plt                                                 
import sympy                                                                    

x = sympy.symbols('x')                                                          
y = 1 + sympy.sin(sympy.sqrt(x**2 + 20))                                         
lat = sympy.latex(y)                                                            

#add text                                                                       
plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)                                  

#hide axes                                                                      
fig = plt.gca()                                                                 
fig.axes.get_xaxis().set_visible(False)                                         
fig.axes.get_yaxis().set_visible(False)                                         
plt.draw() #or savefig                                                          
plt.show()