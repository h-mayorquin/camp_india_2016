string=" 1 1 0. 0. 0. 3.35  -1 \n 2 1 0. 0. 1. 2.5  1 \n 3 1 0. 0. 2. 1.058  2 \n"
for i in range(4,5):
    string=string+ " "+  str(i) + " 3 " + "%.1f "%(0.0) + "%.1f "%(0.0)+ "%.1f "%(i) + "%.1f "%(1.0) + str(i-1) +"\n"
print string

