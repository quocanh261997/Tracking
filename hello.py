import pylab as plt
mysamples = []
mylinear = []
myquadratic = []
myexponential = []
for i in range(0,30):
    mysamples.append(i)
    mylinear.append(i)
    myquadratic.append(i**2)
    myexponential.append(1.5**i)
plt.figure('lin')
plt.title("Linear")
plt.plot(mysamples,mylinear,'b-',label="linear",linewidth=2.0)
plt.plot(mysamples,myquadratic,'ro',label="quadratic",linewidth=3.0)
plt.legend()
plt.figure('exponent')
plt.plot(mysamples,myexponential,'g--',label="exponential",linewidth=4.0)
plt.legend()
plt.show()
