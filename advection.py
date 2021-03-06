import numpy as np
import matplotlib.pyplot as plt
import sys

"""
class to solve 1D advection equation
"""


class advectionPDE:

    def __init__(self, domain, f0, a, dx, dt):
        self.x = domain     # discretised x domain (assumed uniform)
        self.N = len(domain)
        self.f = np.array(f0)       # initial conditions
        self.fold = np.array(f0)    # variable to store old function values
        # numerical scheme for df/dx discretisation:
        self.spatialScheme = "forward"
        # numerical schemde for df/dt discretisation
        self.timeScheme = "central"
        self.a = a      # velocity
        self.dx = dx    # spatial step
        self.dt = dt    # time step
        self.writeOn = False    # write output to a file?
        self.writeNow = 0.      # stores time between writes

    # function that applies boundary conditions
    def correctBC(self, f):
        f[0] = 0
        f[self.N - 1] = 0

    # single iteration in time
    def step(self):
        # use the time scheme:
        f = self.d_dt(self.f, self.dt)
        # use the gradient scheme for each cell
        for i in range(1, self.N - 1):
            f[i] -= self.a * self.mdt * self.gradient(self.f, self.dx, i)
        # apply boundary conditions
        self.correctBC(f)

        # update function values
        self.fold = np.array(self.f)
        self.f = f

    # calculate how many time steps to perform
    # realTime indicates time is in seconds
    # realTime == False indicates time is given initerations
    def advance(self, time, realTime=True):
        if realTime:
            n = (int)(time / dt)
        else:
            n = time
        for i in range(n):
            self.step()

            # save to a file
            self.T = i * dt
            if self.writeOn:
                self.write()

    # discretisation of df/dx term
    def gradient(self, f, dx, i):
        if self.spatialScheme == "central":
            return (self.f[i + 1] - self.f[i - 1]) / dx / 2.
        elif self.spatialScheme == 'forward':
            return (self.f[i + 1] - self.f[i]) / dx
        elif self.spatialScheme == 'backward':
            return (self.f[i] - self.f[i - 1]) / dx
        else:
            sys.exit("wrong spatial scheme selected...\nprogram closing")

    # discretisation of df/dt term
    # mdt is a denominator of the time scheme
    # it is used to multiply the discretised gradient
    def d_dt(self, f, dt):
        if self.timeScheme == "central":
            f = np.array(self.fold * 1.)
            self.mdt = self.dt * 2.
        elif self.timeScheme == "forward":
            f = np.array(f)
            self.mdt = self.dt
        else:
            sys.exit("wrong time scheme selected...\nprogram closing")
        return f

    # file output function
    def write(self):
        # increase current time variable
        self.writeNow += self.dt
        # if the time variable is greater than the write interval
        # output data to a file
        if self.writeNow > self.writeEvery:
            # create file name based on current time (real time)
            name = "data/{0}.txt".format(self.T)
            x = np.zeros((2, self.N))
            x[0][:] = self.x[:]
            x[1][:] = self.f[:]
            np.savetxt(name, x.T)
            self.writeNow = 0.

    # initialize file writing
    # file is crated very deltaT (real time)
    def writeFile(self, deltaT):
        self.writeEvery = deltaT
        self.writeOn = True
        self.writeNow = 0.


a = 1.
domain = np.linspace(-40., 40., 100)
dx = domain[1] - domain[0]
T = 5.
dt = 0.1 * dx / a
f0 = 0.5 * np.exp(-domain ** 2)
f = 0.5 * np.exp(-(domain - T) ** 2)

PDE = advectionPDE(domain, f0, a, dx, dt)
PDE.timeScheme = "forward"
PDE.spatialScheme = "backward"
#PDE.writeFile(0.1)
PDE.advance(T)
plt.plot(domain, PDE.f, label="Simulation result")
plt.plot(domain, f0, label="initial condition")
plt.plot(domain, f, label="analytical result after time {0}".format(T))
#plt.legend(loc='outside')

plt.show()
