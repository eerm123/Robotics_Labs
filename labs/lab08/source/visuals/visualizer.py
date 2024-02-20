# -*- coding: utf-8 -*-

import sys
import time
import cv2
import numpy as np
import pyqtgraph as pg
from scipy import stats
from PyQt5.QtCore import QTimer
from pyqtgraph.Qt import QtCore

from ..helper.current_state import CurrentState


# plot measured distances at fixed interval
class Visualizer:
    UPDATE_INTERVAL = 1000  # ms

    MAX_DISTANCE = 1800
    US_Y = 150
    ENCODERS_Y = 120
    ENCODERS_ENHANCED_Y = 90
    CAMERA_Y = 90
    CURVE_COMPL_Y = 90
    US_AVG_Y = 60
    CURVE_KALMAN_Y = 150

    BACKGROUND_COLOR="#303030"
    CAMERA_COLOR="#bb83fc"

    def enable_plots_based_on_task(self, task):
        # Initialize variables for velocity plotting, Kalman plotting,
        # the three sensors (ultrasonic, encoders, camera)
        # and the complementary filter
        
        self.show_velocities = task in [1, 3, 4, 5]
        self.show_complementary = task in [3]
        self.show_kalman = task in [4]

        self.show_ultrasonic = task in [-1, 0, 1, 3]
        self.show_encoders = task in [-1, 0, 1, 2, 3, 4]
        self.show_encoders_enhanced = task in [2]
        self.show_camera = task in [-1, 0, 1, 4]
        self.show_ultrasonic_avg = task in [-1]

    def __init__(self, app, task_number):
        self.app = app
        self.win_distance = pg.GraphicsWindow()
        self.win_distance.setBackground(self.BACKGROUND_COLOR)
        self.start_time = time.time()

        self.draw_update_timer = QTimer()
        self.draw_update_timer.timeout.connect(self.draw)
        self.current_state = CurrentState()

        self.enable_plots_based_on_task(task_number)

        # Create a window for plotting
        self.win_distance.setWindowTitle('Distance Plotter')
        if self.show_kalman:
            self.win_distance.resize(1024, 640)
        else:
            self.win_distance.resize(1024, 320)
        distance_plot = self.win_distance.addPlot()
        distance_plot.setLabel('top', "Distance (mm)")
        distance_plot.setXRange(0, self.MAX_DISTANCE)
        distance_plot.hideAxis('left')
        distance_plot.hideAxis('top')
        distance_plot.setAspectLocked()
        distance_plot.addLegend(offset=(800, 20), labelTextColor=[0, 0, 0, 0], verSpacing=-10, labelTextSize='6pt')

        # Initialize curves for each sensor
        if self.show_ultrasonic:
            self.curve_us = distance_plot.plot([self.MAX_DISTANCE], [self.US_Y],
                                    pen=pg.mkPen(width=3, color='r'),
                                    brush=pg.mkBrush(radius=10, color='r'),
                                    symbol='o', symbolBrush='r', symbolSize=10,
                                    name='Ultrasonic')
        if self.show_encoders:
            self.curve_enc = distance_plot.plot([self.MAX_DISTANCE], [self.ENCODERS_Y],
                                    pen=pg.mkPen(width=3, color='g'),
                                    brush=pg.mkBrush(radius=10, color='g'),
                                    symbol='o', symbolBrush='g', symbolSize=10,
                                    name='Encoders')
        if self.show_ultrasonic_avg:
            self.curve_us_avg = distance_plot.plot([self.MAX_DISTANCE], [self.US_AVG_Y],
                                    pen=pg.mkPen(width=3, color='y'),
                                    brush=pg.mkBrush(radius=10, color='y'),
                                    symbol='o', symbolBrush='y', symbolSize=10,
                                    name='Averaged ultrasonic')
        if self.show_encoders_enhanced:
            self.curve_enc_enhanced = distance_plot.plot([self.MAX_DISTANCE], [self.ENCODERS_ENHANCED_Y],
                                    pen=pg.mkPen(width=3, color='b'),
                                    brush=pg.mkBrush(radius=10, color='b'),
                                    symbol='o', symbolBrush='b',symbolSize=10,
                                    name='Enc. + markers')
        if self.show_camera:
            self.curve_cam = distance_plot.plot([self.MAX_DISTANCE], [self.CAMERA_Y],
                                    pen=pg.mkPen(width=3, color=self.CAMERA_COLOR),
                                    brush=pg.mkBrush(radius=10, color=self.CAMERA_COLOR),
                                    symbol='o', symbolBrush=self.CAMERA_COLOR,symbolSize=10,
                                    name='Camera')
        if self.show_complementary:
            self.curve_compl = distance_plot.plot([self.MAX_DISTANCE], [self.CURVE_COMPL_Y],
                                    pen=pg.mkPen(width=3, color=2),
                                    symbol='o', symbolBrush=2,
                                    symbolSize=10, name='Complementary')
        if self.show_kalman:
            self.curve_kalman = distance_plot.plot([self.MAX_DISTANCE], [self.CURVE_KALMAN_Y],
                                    pen=pg.mkPen(width=3, color='y'),
                                    symbol='o', symbolBrush='y',
                                    symbolSize=10, name='Kalman')

        # Load a background image of a track
        img_arr = np.asarray(cv2.cvtColor(cv2.imread('map.png'), cv2.COLOR_BGR2RGB))
        img_item = pg.ImageItem(np.rot90(img_arr, -1))
        img_item.scale(1.37, 1.37)
        img_item.setZValue(-100)
        distance_plot.addItem(img_item)

        # Create a plot for visualizing velocities according to different sensors
        if self.show_velocities:
            # Create the plot background
            self.win_velocity = pg.GraphicsWindow()
            self.win_velocity.setBackground(self.BACKGROUND_COLOR)
            self.win_velocity.setWindowTitle('Velocity Plotter')
            self.win_velocity.resize(640, 320)
            velocity_plot = self.win_velocity.addPlot()
            velocity_plot.setLabel('left', "Velocity (mm/s)")
            velocity_plot.setLabel('bottom', "Time (s)")
            velocity_plot.addLegend()
            velocity_plot.setYRange(-200, 200)
            self.velocity_plot = velocity_plot

            # Initialize velocity curves for each sensor
            VEL_INIT_X = list(reversed([ -x*0.1 for x in range(100) ]))
            VEL_INIT_Y = [0]*100
            if self.show_ultrasonic:
                self.curve_us_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:],
                                            pen=pg.mkPen(width=1, color='r'),
                                            name='Ultrasonic')
            if self.show_encoders:
                self.curve_enc_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:],
                                            pen=pg.mkPen(width=1, color='g'),
                                            name='Encoders')
            if self.show_camera:
                self.curve_cam_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:],
                                            pen=pg.mkPen(width=1, color=self.CAMERA_COLOR),
                                            name='Camera')
            if self.show_complementary:
                self.curve_compl_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:],
                                            pen=pg.mkPen(width=1, color=2),
                                            name='Complementary')
            if self.show_kalman:
                self.curve_kalman_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:],
                                            pen=pg.mkPen(width=1, color='y'),
                                            name='Kalman')

        # Create a plot for visualizing Kalman filter behaviour
        if self.show_kalman:
            # Create the plot background
            self.win_distance.nextRow()
            kalman_plot = self.win_distance.addPlot()
            kalman_plot.setXRange(-10, 2000)
            kalman_plot.setYRange(0, 0.02)
            kalman_plot.hideAxis('left')
            kalman_plot.addLegend()

            # Initialize all Gaussian curves
            gaussian_names_and_colours = [
                    ("Camera", self.CAMERA_COLOR),
                    ("Encoders (delta)", 'g'),
                    ("Filtered result", 'y')
                ]
            self.gaussian_curves = {}
            for name, color in gaussian_names_and_colours:
                pen = pg.mkPen(width=1, color=color,
                               style=QtCore.Qt.DashLine if "(delta)" in name else QtCore.Qt.SolidLine)
                self.gaussian_curves[name] = kalman_plot.plot([], [],
                                            pen=pen,
                                            name=name)


    def draw(self):
        # Update the graphs only when the values are valid
        if self.show_ultrasonic and self.current_state.get_ultrasonic_distance() >= 0:
            self._draw_us(self.current_state.get_ultrasonic_distance())
            if self.show_velocities:
                self._draw_us_velocity(self.current_state.sensor_fusion['us_velocity'])

        if self.show_encoders and self.current_state.get_encoders_distance() >= 0:
            self._draw_enc(self.current_state.get_encoders_distance())
            if self.show_velocities:
                self._draw_enc_velocity(self.current_state.sensor_fusion['enc_velocity'])

        if self.show_ultrasonic_avg and self.current_state.get_ultrasonic_averaged_distance() >= 0:
            self._draw_us_avg(self.current_state.get_ultrasonic_averaged_distance())
                
        if self.show_encoders_enhanced and self.current_state.get_encoders_enhanced_distance() >= 0:
            self._draw_enc_enhanced(self.current_state.get_encoders_enhanced_distance())

        if self.show_camera and self.current_state.get_camera_distance() is not None and self.current_state.get_camera_distance() >= 0:
            self._draw_cam(self.current_state.get_camera_distance())
            if self.show_velocities:
                self._draw_cam_velocity(self.current_state.sensor_fusion['cam_velocity'])

        if self.show_complementary and self.current_state.get_complementary() >= 0:
            self._draw_compl(self.current_state.get_complementary())
            if self.show_velocities:
                self._draw_compl_velocity(self.current_state.get_complementary_velocity())

        if self.show_kalman:
            kalman_estimate = self.current_state.get_kalman()
            if kalman_estimate is not None and kalman_estimate >= 0:
                self._draw_kalman(kalman_estimate)

            self._draw_kalman_velocity(self.current_state.get_kalman_velocity())

            self._plot_gaussian(self.current_state.get_cam_gaussian(), "Camera")
            self._plot_gaussian(self.current_state.get_enc_gaussian(), "Encoders (delta)")
            self._plot_gaussian(self.current_state.get_kalman_result_gaussian(), "Filtered result")


    # Draws a position from the ultrasonic sensor to the map.
    def _draw_us(self, pos):
        x, y = self.curve_us.getData()
        x = np.append(x, pos)
        y = np.append(y, self.US_Y)
        self.curve_us.setData(x, y)

    # Draws a position from encoders to the map.
    def _draw_enc(self, pos):
        x, y = self.curve_enc.getData()
        x = np.append(x, pos)
        y = np.append(y, self.ENCODERS_Y)
        self.curve_enc.setData(x, y)

    # Draws a position from the ultrasonic sensor to the map.
    def _draw_us_avg(self, pos):
        x, y = self.curve_us_avg.getData()
        x = np.append(x, pos)
        y = np.append(y, self.US_AVG_Y)
        self.curve_us_avg.setData(x, y)

    # Draws a position from encoders to the map.
    def _draw_enc_enhanced(self, pos):
        x, y = self.curve_enc_enhanced.getData()
        x = np.append(x, pos)
        y = np.append(y, self.ENCODERS_ENHANCED_Y)
        self.curve_enc_enhanced.setData(x, y)

    # Draws a position from a camera to the map.
    def _draw_cam(self, pos):
        x, y = self.curve_cam.getData()
        x = np.append(x, pos)
        y = np.append(y, self.CAMERA_Y)
        self.curve_cam.setData(x, y)

    # Draws a complementary filtered result to the map.
    def _draw_compl(self, pos):
        x, y = self.curve_compl.getData()
        x = np.append(x, pos)
        y = np.append(y, self.CURVE_COMPL_Y)
        self.curve_compl.setData(x, y)

    # Draws a position from Kalman filter to the map.
    def _draw_kalman(self, pos):
        x, y = self.curve_kalman.getData()
        x = np.append(x, pos)
        y = np.append(y, 150)
        self.curve_kalman.setData(x, y)

    # Draws the velocity of the robot calculated from US measurements to the plot.
    def _draw_us_velocity(self, velocity):
        x, y = self.curve_us_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_us_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from encoder measurements to the plot.
    def _draw_enc_velocity(self, velocity):
        x, y = self.curve_enc_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_enc_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from camera measurements to the plot.
    def _draw_cam_velocity(self, velocity):
        x, y = self.curve_cam_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_cam_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from complementary filtered results to the plot.
    def _draw_compl_velocity(self, velocity):
        x, y = self.curve_compl_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_compl_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from camera measurements to the plot.
    def _draw_kalman_velocity(self, velocity):
        x, y = self.curve_kalman_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_kalman_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Plots Gaussian with given mu, sigma and name
    def _plot_gaussian(self, gaussian, name):
        if gaussian:
            x = np.arange(-100,2000)
            y = stats.norm.pdf(x, gaussian.mu, gaussian.sigma)
            self.gaussian_curves[name].setData(x, y)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.draw_update_timer.start(self.UPDATE_INTERVAL)
            self.app.exec_()
        else:
            raise Exception("Visualisation application did not start!")
