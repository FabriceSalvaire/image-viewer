####################################################################################################

from pathlib import Path
import numpy as np
from matplotlib import pylab as plt

####################################################################################################

# KalmanFilter
# Author: Du Ang
# Based on https://github.com/dougszumski/KalmanFilter/blob/master/kalman_filter.py by Doug Szumski.
# Differences with the original version:
#   - add control term
#   - use numpy multiplication
# Materials references: http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/
# Date: July 1, 2018

class KalmanFilter:
    """
    Simple Kalman filter
    """

    def __init__(self, X, F, Q, Z, H, R, P, B=np.array([0]), M=np.array([0])):
        """
        Initialise the filter
        Args:
            X: State estimate
            P: Estimate covariance
            F: State transition model
            B: Control matrix
            M: Control vector
            Q: Process noise covariance
            Z: Measurement of the state X
            H: Observation model
            R: Observation noise covariance
        """
        self.X = X
        self.P = P
        self.F = F
        self.B = B
        self.M = M
        self.Q = Q
        self.Z = Z
        self.H = H
        self.R = R

    def predict(self):
        """
        Predict the future state
        Args:
            self.X: State estimate
            self.P: Estimate covariance
            self.B: Control matrix
            self.M: Control vector
        Returns:
            updated self.X
        """
        # Project the state ahead
        self.X = self.F @ self.X + self.B @ self.M
        self.P = self.F @ self.P @ self.F.T + self.Q

        return self.X

    def correct(self, Z):
        """
        Update the Kalman Filter from a measurement
        Args:
            self.X: State estimate
            self.P: Estimate covariance
            Z: State measurement
        Returns:
            updated X
        """
        K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
        self.X += K @ (Z - self.H @ self.X)
        self.P = self.P - K @ self.H @ self.P

        return self.X

####################################################################################################

def filter_measures(ts, dpys, fdpys):
    stateMatrix = np.zeros((4, 1), np.float32)   # [x, y, delta_x, delta_y]
    estimateCovariance = np.eye(stateMatrix.shape[0])
    transitionMatrix = np.array(
        [[1, 0, 1, 0],
         [0, 1, 0, 1],
         [0, 0, 1, 0],
         [0, 0, 0, 1]],
        np.float32
    )
    processNoiseCov = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]],
        np.float32
    ) * 0.001
    measurementStateMatrix = np.zeros((2, 1), np.float32)
    observationMatrix = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0]],
        np.float32
    )
    measurementNoiseCov = np.array(
        [[1, 0],
         [0, 1]],
        np.float32
    ) * 1
    kalman = KalmanFilter(
        X=stateMatrix,
        P=estimateCovariance,
        F=transitionMatrix,
        Q=processNoiseCov,
        Z=measurementStateMatrix,
        H=observationMatrix,
        R=measurementNoiseCov
    )

    for i, (t, y) in enumerate(zip(ts, dpys)):
        x = 0
        current_measurement = np.array([[np.float32(x)], [np.float32(y)]])
        current_prediction = kalman.predict()
        cmx, cmy = current_measurement[0], current_measurement[1]
        cpx, cpy = current_prediction[0], current_prediction[1]
        print(f"{cmy} {cpy}")
        kalman.correct(current_measurement)
        fdpys[i] = cpy

####################################################################################################

ts = []
dts = []
dpys = []

data_path = 'wheel-log-1.txt'
data = Path(data_path).read_text()
start = None
tp = None
for line in data.splitlines():
    if 'wheel' in line:
        # print(line)
        line = line.replace('qml: wheel handler ', '').replace('QPoint(', '').replace(',', '').replace(')', '')
        # print(line)
        parts = line.split()
        print(parts)
        t = int(parts[0])
        x, y = [float(_) for _ in parts[1:3]]
        dax, day, dpx, dpy = [int(_) for _ in parts[3:]]
        if start is None:
            start = t
            t = 0
            dt = 0
        else:
            t -= start
            dt = t - tp
        tp = t
        ts.append(t)
        dts.append(dt)
        dpys.append(dpy)

ts = np.array(ts)
dts = np.array(dts)
dpys = np.array(dpys)
ys = np.add.accumulate(dpys)

# phase F
# m * dx/dt**2 = F - k * dx/dt
# m * dx = F * dt**2 - k * dx * dt
# dx * (m + k * dt) = F * dt**2
#
# phase k
# m * dv/dt = -k * v
# dv = -k / m * v * dt
# dx = v * dt

k = 0.0001
m = 1.
dxs = dpys * dts**2 / (dts*k + m) / 1000
dxs = np.add.accumulate(dxs)

# dt = 1
# N = 100
# txs = np.arange(0, N, dt)
# dxxs = np.zeros(N)
# xp = 0
# t = 0
# x = 0
# for i in range(dxs.shape[0]):
#     x = dxs[i]
#     if x == xp:
#         break

# k = 0.0001
# for t in range(1, N):
#     dx = np.exp(-k/m*t)*dt
#     xp += dx
#     print(xp)
#     dxxs[t] = xp

# fdpys = np.zeros(dpys.shape)
# filter_measures(ts, dpys, fdpys)

plt.grid()
plt.plot(ts, dpys, 'o-')
plt.plot(ts, ys, 'x-')
# plt.plot(ts, dxs, 'o-')
# plt.plot(ts, dxs/ys, 'o-')
# plt.plot(txs, -dxxs, 'o-')
# plt.plot(ts, fdpys, 'o-')
plt.show()
