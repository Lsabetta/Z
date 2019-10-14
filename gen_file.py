import numpy as np
with open("sin_data.txt", "w") as o_file:
    for i in range(0, 5000, 10):
        o_file.write(str(6+4*np.sin(i/1000. +1.5))+'\t'+str(i)+'\n')
        
        
        
