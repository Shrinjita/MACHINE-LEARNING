#!/usr/bin/env python
"""
Facial landmark annotation tool

This program expects either a single image as an argument, or a directory
with many images, and a number n of images to be processed in that directory.
In this last case, names are sorted, and images at positions 0, floor(N/n),
floor(2N/n), ... floor((n - 1)N/n) are selected.

Output is to stdout and follows a csv format:
  'image_fname,' +
  'leye_x,leye_y,reye_x,reye_y,nose_x,nose_y, ' +
  'lmouth_x,lmouth_y,rmouth_x,rmouth_y,' +
  'rect_top_x,rect_top_y,rect_width,rect_height'

It is not necessary to annotate all points, and images can be skipped when
in multiple image mode.

Run without arguments for usage information.
"""
from __future__ import print_function
from __future__ import division
import os
import argparse
import warnings
import json

import cv2
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import matplotlib.cbook
from imutils import paths
#warnings.filterwarnings('ignore', category=matplotlib.cbook.mplDeprecation)

def enum(**enums):
    return type('Enum', (), enums)


class InteractiveViewer(object):
    def __init__(self, img_path, curr_file):
        self.img_path = img_path
        self.curr_file = curr_file
        self.key_pressed = False
        self.key_event = None
        self.rect_clicked = False

        self.rect_coords = [(0, 0), (0, 0)]

        # Left Ear
        self.lear_coords1 = None
        self.lear_coords2 = None
        self.lear_coords3 = None
        self.lear_coords4 = None
        self.lear_coords5 = None

        self.rear_coords1 = None
        self.rear_coords2 = None
        self.rear_coords3 = None
        self.rear_coords4 = None
        self.rear_coords5 = None

        self.leyeb_coords = None
        self.reyeb_coords = None

        self.leye_coords1 = None
        self.leye_coords2 = None
        self.leye_coords3 = None
        self.leye_coords4 = None

        self.reye_coords1 = None
        self.reye_coords2 = None
        self.reye_coords3 = None
        self.reye_coords4 = None

        self.nose_coords = None
        self.tongue_coords = None

        self.tmouth_coords = None
        self.rmouth_coords = None
        self.bmouth_coords = None
        self.lmouth_coords = None

        self.chin_coords = None
        self.head_coords = None

        self.image = cv2.imread(img_path)
        h,w,_ = self.image.shape
        img_res = 512
        self.rw,self.rh = img_res,img_res
        if w<h:
            self.rh = int(img_res * (h/w))
        else:
            self.rw = int(img_res * (w/h))
        self.image = cv2.resize(self.image, (self.rw, self.rh), interpolation= cv2.INTER_AREA)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.clone = self.image.copy()

        self.fig = None
        self.im_ax = None

        self.button_rect = None
        
        self.button_lear1 = None
        self.button_lear2 = None
        self.button_lear3 = None
        self.button_lear4 = None
        self.button_lear5 = None

        self.button_rear1 = None
        self.button_rear2 = None
        self.button_rear3 = None
        self.button_rear4 = None
        self.button_rear5 = None

        self.button_leyeb = None
        self.button_reyeb = None
        
        self.button_leye1 = None
        self.button_leye2 = None
        self.button_leye3 = None
        self.button_leye4 = None

        self.button_reye1 = None
        self.button_reye2 = None
        self.button_reye3 = None
        self.button_reye4 = None

        self.button_nose = None
        self.button_tongue = None

        self.button_tmouth = None
        self.button_rmouth = None
        self.button_bmouth = None
        self.button_lmouth = None

        self.button_chin = None
        self.button_head = None

        self.button_done = None
        self.button_skip = None

        self.is_finished = False
        self.is_skipped = False

        self.to_reset = True

        self.States = enum(GET_RECT=1,

                            GET_LEAR_LB = 2,
                            GET_LEAR_LM = 3,
                            GET_LEAR_T = 4,
                            GET_LEAR_RM = 5,
                            GET_LEAR_RB = 6,

                            GET_REAR_LB = 7,
                            GET_REAR_LM = 8,
                            GET_REAR_T = 9,
                            GET_REAR_RM = 10,
                            GET_REAR_RB = 11,

                            GET_LEYEB = 12,
                            GET_REYEB = 13,

                            GET_LEYE1 = 14,
                            GET_LEYE2 = 15,
                            GET_LEYE3 = 16,
                            GET_LEYE4 = 17,

                            GET_REYE1 = 18,
                            GET_REYE2 = 19,
                            GET_REYE3 = 20,
                            GET_REYE4 = 21,

                            GET_NOSE = 22,

                            GET_TMOUTH = 23,
                            GET_RMOUTH = 24,
                            GET_BMOUTH = 25,
                            GET_LMOUTH = 26,
                            
                            GET_CHIN = 27,
                            GET_HEAD = 28,
                            GET_TONGUE = 29)

        self.curr_state = self.States.GET_RECT


    def redraw_annotations(self):
        
        if self.to_reset:

            self.image = self.clone.copy()

            cv2.rectangle(self.image, self.rect_coords[0], self.rect_coords[1],
                      (0, 255, 0), 3)
            if self.lear_coords1 is not None:
                cv2.circle(self.image, self.lear_coords1, 3, (0, 255, 0), -1)
            if self.lear_coords2 is not None:
                cv2.circle(self.image, self.lear_coords2, 3, (0, 255, 0), -1)
            if self.lear_coords3 is not None:
                cv2.circle(self.image, self.lear_coords3, 3, (0, 255, 0), -1)
            if self.lear_coords4 is not None:
                cv2.circle(self.image, self.lear_coords4, 3, (0, 255, 0), -1)
            if self.lear_coords5 is not None:
                cv2.circle(self.image, self.lear_coords5, 3, (0, 255, 0), -1)

            if self.rear_coords1 is not None:
                cv2.circle(self.image, self.rear_coords1, 3, (0, 255, 0), -1)
            if self.rear_coords2 is not None:
                cv2.circle(self.image, self.rear_coords2, 3, (0, 255, 0), -1)
            if self.rear_coords3 is not None:
                cv2.circle(self.image, self.rear_coords3, 3, (0, 255, 0), -1)
            if self.rear_coords4 is not None:
                cv2.circle(self.image, self.rear_coords4, 3, (0, 255, 0), -1)
            if self.rear_coords5 is not None:
                cv2.circle(self.image, self.rear_coords5, 3, (0, 255, 0), -1)
            
            if self.leyeb_coords is not None:
                cv2.circle(self.image, self.leyeb_coords, 3, (0, 255, 0), -1)
            if self.reyeb_coords is not None:
                cv2.circle(self.image, self.reyeb_coords, 3, (0, 255, 0), -1)
            
            if self.leye_coords1 is not None:
                cv2.circle(self.image, self.leye_coords1, 3, (255, 0, 0), -1)
            if self.leye_coords2 is not None:
                cv2.circle(self.image, self.leye_coords2, 3, (255, 0, 0), -1)
            if self.leye_coords3 is not None:
                cv2.circle(self.image, self.leye_coords3, 3, (255, 0, 0), -1)
            if self.leye_coords4 is not None:
                cv2.circle(self.image, self.leye_coords4, 3, (255, 0, 0), -1)
            
            if self.reye_coords1 is not None:
                cv2.circle(self.image, self.reye_coords1, 3, (255, 0, 0), -1)
            if self.reye_coords2 is not None:
                cv2.circle(self.image, self.reye_coords2, 3, (255, 0, 0), -1)
            if self.reye_coords3 is not None:
                cv2.circle(self.image, self.reye_coords3, 3, (255, 0, 0), -1)
            if self.reye_coords4 is not None:
                cv2.circle(self.image, self.reye_coords4, 3, (255, 0, 0), -1)
            
            if self.nose_coords is not None:
                cv2.circle(self.image, self.nose_coords, 3, (255, 0, 0), -1)

            if self.tongue_coords is not None:
                cv2.circle(self.image, self.tongue_coords, 3, (255, 0, 0), -1)
            
            if self.tmouth_coords is not None:
                cv2.circle(self.image, self.tmouth_coords, 3, (255, 0, 0), -1)
            if self.rmouth_coords is not None:
                cv2.circle(self.image, self.rmouth_coords, 3, (255, 0, 0), -1)
            if self.bmouth_coords is not None:
                cv2.circle(self.image, self.bmouth_coords, 3, (255, 0, 0), -1)
            if self.lmouth_coords is not None:
                cv2.circle(self.image, self.lmouth_coords, 3, (255, 0, 0), -1)
            
            if self.chin_coords is not None:
                cv2.circle(self.image, self.chin_coords, 3, (255, 0, 0), -1)
            if self.head_coords is not None:
                cv2.circle(self.image, self.head_coords, 3, (255, 0, 0), -1)

        else:
            if(self.curr_state == self.States.GET_LEAR_LB):
                cv2.circle(self.image, self.lear_coords1, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_LEAR_LM):
                cv2.circle(self.image, self.lear_coords2, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_LEAR_T):
                cv2.circle(self.image, self.lear_coords3, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_LEAR_RM):
                cv2.circle(self.image, self.lear_coords4, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_LEAR_RB):
                cv2.circle(self.image, self.lear_coords5, 3, (0, 255, 0), -1)

            elif(self.curr_state == self.States.GET_REAR_LB):
                cv2.circle(self.image, self.rear_coords1, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_REAR_LM):
                cv2.circle(self.image, self.rear_coords2, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_REAR_T):
                cv2.circle(self.image, self.rear_coords3, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_REAR_RM):
                cv2.circle(self.image, self.rear_coords4, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_REAR_RB):
                cv2.circle(self.image, self.rear_coords5, 3, (0, 255, 0), -1)
            

            elif(self.curr_state == self.States.GET_LEYEB):
                cv2.circle(self.image, self.leyeb_coords, 3, (0, 255, 0), -1)
            elif(self.curr_state == self.States.GET_REYEB):
                cv2.circle(self.image, self.reyeb_coords, 3, (0, 255, 0), -1)
            
            elif(self.curr_state == self.States.GET_LEYE1):
                cv2.circle(self.image, self.leye_coords1, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_LEYE2):
                cv2.circle(self.image, self.leye_coords2, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_LEYE3):
                cv2.circle(self.image, self.leye_coords3, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_LEYE4):
                cv2.circle(self.image, self.leye_coords4, 3, (255, 0, 0), -1)
            
            elif(self.curr_state == self.States.GET_REYE1):
                cv2.circle(self.image, self.reye_coords1, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_REYE2):
                cv2.circle(self.image, self.reye_coords2, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_REYE3):
                cv2.circle(self.image, self.reye_coords3, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_REYE4):
                cv2.circle(self.image, self.reye_coords4, 3, (255, 0, 0), -1)
            
            elif(self.curr_state == self.States.GET_NOSE):
                cv2.circle(self.image, self.nose_coords, 3, (255, 0, 0), -1)

            elif(self.curr_state == self.States.GET_TONGUE):
                cv2.circle(self.image, self.tongue_coords, 3, (255, 0, 0), -1)
            
            elif(self.curr_state == self.States.GET_TMOUTH):
                cv2.circle(self.image, self.tmouth_coords, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_RMOUTH):
                cv2.circle(self.image, self.rmouth_coords, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_BMOUTH):
                cv2.circle(self.image, self.bmouth_coords, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_LMOUTH):
                cv2.circle(self.image, self.lmouth_coords, 3, (255, 0, 0), -1)
            
            elif(self.curr_state == self.States.GET_CHIN):
                cv2.circle(self.image, self.chin_coords, 3, (255, 0, 0), -1)
            elif(self.curr_state == self.States.GET_HEAD):
                cv2.circle(self.image, self.head_coords, 3, (255, 0, 0), -1)
            
        self.im_ax.imshow(self.image)


    def update_button_labels(self):
        if(self.curr_state == self.States.GET_RECT):
            self.button_rect.label.set_text('Rectangle\n({},{})'.format(
                self.rect_coords[0], self.rect_coords[1]))
        
        elif(self.curr_state == self.States.GET_LEAR_LB):
            self.button_lear1.label.set_text(
                'L Ear - LB\n{}'.format(self.lear_coords1))
        elif(self.curr_state == self.States.GET_LEAR_LM):
            self.button_lear2.label.set_text(
                'L Ear - LM\n{}'.format(self.lear_coords2))
        elif(self.curr_state == self.States.GET_LEAR_T):
            self.button_lear3.label.set_text(
                'L Ear - T\n{}'.format(self.lear_coords3))
        elif(self.curr_state == self.States.GET_LEAR_RM):
            self.button_lear4.label.set_text(
                'L Ear - RM\n{}'.format(self.lear_coords4))
        elif(self.curr_state == self.States.GET_LEAR_RB):
            self.button_lear5.label.set_text(
                'L Ear - RB\n{}'.format(self.lear_coords5))
        
        elif(self.curr_state == self.States.GET_REAR_LB):
            self.button_rear1.label.set_text(
                'R Ear - LB\n{}'.format(self.rear_coords1))
        elif(self.curr_state == self.States.GET_REAR_LM):
            self.button_rear2.label.set_text(
                'R Ear - LM\n{}'.format(self.rear_coords2))
        elif(self.curr_state == self.States.GET_REAR_T):
            self.button_rear3.label.set_text(
                'R Ear - T\n{}'.format(self.rear_coords3))
        elif(self.curr_state == self.States.GET_REAR_RM):
            self.button_rear4.label.set_text(
                'R Ear - RM\n{}'.format(self.rear_coords4))
        elif(self.curr_state == self.States.GET_REAR_RB):
            self.button_rear5.label.set_text(
                'R Ear - RB\n{}'.format(self.rear_coords5))
        
        elif(self.curr_state == self.States.GET_LEYEB):
            self.button_leyeb.label.set_text(
                'L Eyebrow\n{}'.format(self.leyeb_coords))
        elif(self.curr_state == self.States.GET_REYEB):
            self.button_reyeb.label.set_text(
                'R Eyebrow\n{}'.format(self.reyeb_coords))

        elif(self.curr_state == self.States.GET_LEYE1):
            self.button_leye1.label.set_text(
                'L Eye - T\n{}'.format(self.leye_coords1))
        elif(self.curr_state == self.States.GET_LEYE2):
            self.button_leye2.label.set_text(
                'L Eye - R\n{}'.format(self.leye_coords2))
        elif(self.curr_state == self.States.GET_LEYE3):
            self.button_leye3.label.set_text(
                'L Eye - B\n{}'.format(self.leye_coords3))
        elif(self.curr_state == self.States.GET_LEYE4):
            self.button_leye4.label.set_text(
                'L Eye - L\n{}'.format(self.leye_coords4))
        
        elif(self.curr_state == self.States.GET_REYE1):
            self.button_reye1.label.set_text(
                'R Eye - T\n{}'.format(self.reye_coords1))
        elif(self.curr_state == self.States.GET_REYE2):
            self.button_reye2.label.set_text(
                'R Eye - R\n{}'.format(self.reye_coords2))
        elif(self.curr_state == self.States.GET_REYE3):
            self.button_reye3.label.set_text(
                'R Eye - B\n{}'.format(self.reye_coords3))
        elif(self.curr_state == self.States.GET_REYE4):
            self.button_reye4.label.set_text(
                'R Eye - L\n{}'.format(self.reye_coords4))
        
        elif(self.curr_state == self.States.GET_NOSE):
            self.button_nose.label.set_text(
                'Nose\n{}'.format(self.nose_coords))
        
        elif(self.curr_state == self.States.GET_TONGUE):
            self.button_tongue.label.set_text(
                'Tongue\n{}'.format(self.tongue_coords))
        
        elif(self.curr_state == self.States.GET_TMOUTH):
            self.button_tmouth.label.set_text(
                'Mouth - T\n{}'.format(self.tmouth_coords))
        elif(self.curr_state == self.States.GET_RMOUTH):
            self.button_rmouth.label.set_text(
                'Mouth - R\n{}'.format(self.rmouth_coords))
        elif(self.curr_state == self.States.GET_BMOUTH):
            self.button_bmouth.label.set_text(
                'Mouth - B\n{}'.format(self.bmouth_coords))
        elif(self.curr_state == self.States.GET_LMOUTH):
            self.button_lmouth.label.set_text(
                'Mouth - L\n{}'.format(self.lmouth_coords))
        
        elif(self.curr_state == self.States.GET_CHIN):
            self.button_chin.label.set_text(
                'Chin\n{}'.format(self.chin_coords))
        elif(self.curr_state == self.States.GET_HEAD):
            self.button_head.label.set_text(
                'Head\n{}'.format(self.head_coords))
        else:
            print("Unknown state encountered! Returning.....")


    def on_click(self, event):
        if event.inaxes != self.im_ax:
            return
        self.rect_clicked = False

        if self.curr_state == self.States.GET_RECT:
            self.rect_coords[0] = (int(event.xdata), int(event.ydata))
            self.rect_clicked = True

        elif self.curr_state == self.States.GET_LEAR_LB:
            self.lear_coords1 = (int(event.xdata), int(event.ydata))
            self.button_lear1.label.set_text(
                'L Ear - LB\n{}'.format(self.lear_coords1))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEAR_LM:
            self.lear_coords2 = (int(event.xdata), int(event.ydata))
            self.button_lear2.label.set_text(
                'L Ear - LM\n{}'.format(self.lear_coords2))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEAR_T:
            self.lear_coords3 = (int(event.xdata), int(event.ydata))
            self.button_lear3.label.set_text(
                'L Ear - T\n{}'.format(self.lear_coords3))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEAR_RM:
            self.lear_coords4 = (int(event.xdata), int(event.ydata))
            self.button_lear4.label.set_text(
                'L Ear - RM\n{}'.format(self.lear_coords4))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEAR_RB:
            self.lear_coords5 = (int(event.xdata), int(event.ydata))
            self.button_lear5.label.set_text(
                'L Ear - RB\n{}'.format(self.lear_coords5))
            self.redraw_annotations()
        
        elif self.curr_state == self.States.GET_REAR_LB:
            self.rear_coords1 = (int(event.xdata), int(event.ydata))
            self.button_rear1.label.set_text(
                'R Ear - LB\n{}'.format(self.rear_coords1))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REAR_LM:
            self.rear_coords2 = (int(event.xdata), int(event.ydata))
            self.button_rear2.label.set_text(
                'R Ear - LM\n{}'.format(self.rear_coords2))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REAR_T:
            self.rear_coords3 = (int(event.xdata), int(event.ydata))
            self.button_rear3.label.set_text(
                'R Ear - T\n{}'.format(self.rear_coords3))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REAR_RM:
            self.rear_coords4 = (int(event.xdata), int(event.ydata))
            self.button_rear4.label.set_text(
                'R Ear - RM\n{}'.format(self.rear_coords4))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REAR_RB:
            self.rear_coords5 = (int(event.xdata), int(event.ydata))
            self.button_rear5.label.set_text(
                'R Ear - RB\n{}'.format(self.rear_coords5))
            self.redraw_annotations()

        elif self.curr_state == self.States.GET_LEYEB:
            self.leyeb_coords = (int(event.xdata), int(event.ydata))
            self.button_leyeb.label.set_text(
                'L Eyebrow\n{}'.format(self.leyeb_coords))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REYEB:
            self.reyeb_coords = (int(event.xdata), int(event.ydata))
            self.button_reyeb.label.set_text(
                'R Eyebrow\n{}'.format(self.reyeb_coords))
            self.redraw_annotations()

        elif self.curr_state == self.States.GET_LEYE1:
            self.leye_coords1 = (int(event.xdata), int(event.ydata))
            self.button_leye1.label.set_text(
                'L Eye - T\n{}'.format(self.leye_coords1))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEYE2:
            self.leye_coords2 = (int(event.xdata), int(event.ydata))
            self.button_leye2.label.set_text(
                'L Eye - R\n{}'.format(self.leye_coords2))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEYE3:
            self.leye_coords3 = (int(event.xdata), int(event.ydata))
            self.button_leye3.label.set_text(
                'L Eye - B\n{}'.format(self.leye_coords3))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LEYE4:
            self.leye_coords4 = (int(event.xdata), int(event.ydata))
            self.button_leye4.label.set_text(
                'L Eye - L\n{}'.format(self.leye_coords4))
            self.redraw_annotations()
        
        elif self.curr_state == self.States.GET_REYE1:
            self.reye_coords1 = (int(event.xdata), int(event.ydata))
            self.button_reye1.label.set_text(
                'R Eye - T\n{}'.format(self.reye_coords1))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REYE2:
            self.reye_coords2 = (int(event.xdata), int(event.ydata))
            self.button_reye2.label.set_text(
                'R Eye - R\n{}'.format(self.reye_coords2))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REYE3:
            self.reye_coords3 = (int(event.xdata), int(event.ydata))
            self.button_reye3.label.set_text(
                'R Eye - B\n{}'.format(self.reye_coords3))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_REYE4:
            self.reye_coords4 = (int(event.xdata), int(event.ydata))
            self.button_reye4.label.set_text(
                'R Eye - L\n{}'.format(self.reye_coords4))
            self.redraw_annotations()

        elif self.curr_state == self.States.GET_NOSE:
            self.nose_coords = (int(event.xdata), int(event.ydata))
            self.button_nose.label.set_text(
                'Nose\n{}'.format(self.nose_coords))
            self.redraw_annotations()
        
        elif self.curr_state == self.States.GET_TONGUE:
            self.tongue_coords = (int(event.xdata), int(event.ydata))
            self.button_tongue.label.set_text(
                'Tongue\n{}'.format(self.tongue_coords))
            self.redraw_annotations()

        elif self.curr_state == self.States.GET_TMOUTH:
            self.tmouth_coords = (int(event.xdata), int(event.ydata))
            self.button_tmouth.label.set_text(
                'Mouth T\n{}'.format(self.tmouth_coords))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_RMOUTH:
            self.rmouth_coords = (int(event.xdata), int(event.ydata))
            self.button_rmouth.label.set_text(
                'Mouth R\n{}'.format(self.rmouth_coords))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_BMOUTH:
            self.bmouth_coords = (int(event.xdata), int(event.ydata))
            self.button_bmouth.label.set_text(
                'Mouth B\n{}'.format(self.bmouth_coords))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_LMOUTH:
            self.lmouth_coords = (int(event.xdata), int(event.ydata))
            self.button_lmouth.label.set_text(
                'Mouth L\n{}'.format(self.lmouth_coords))
            self.redraw_annotations()
        
        elif self.curr_state == self.States.GET_CHIN:
            self.chin_coords = (int(event.xdata), int(event.ydata))
            self.button_chin.label.set_text(
                'Chin\n{}'.format(self.chin_coords))
            self.redraw_annotations()
        elif self.curr_state == self.States.GET_HEAD:
            self.head_coords = (int(event.xdata), int(event.ydata))
            self.button_head.label.set_text(
                'Head\n{}'.format(self.head_coords))
            self.redraw_annotations()


    def on_release(self, event):
        if event.inaxes != self.im_ax:
            return

        self.rect_clicked = False

        if self.curr_state == self.States.GET_RECT:
            self.rect_coords[1] = (int(event.xdata), int(event.ydata))

            cv2.rectangle(self.image, self.rect_coords[0], self.rect_coords[1],
                          (0, 255, 0), 3)

            self.button_rect.label.set_text('Rectangle\n({},{})'.format(
                self.rect_coords[0], self.rect_coords[1]))


            self.im_ax.imshow(self.image)


    def on_key_press(self, event):
        self.key_event = event
        self.key_pressed = True


    def on_mouse_move(self, event):
        if not self.rect_clicked or event.inaxes != self.im_ax:
            return

        self.rect_coords[1] = (int(event.xdata), int(event.ydata))
        self.to_reset = True
        self.redraw_annotations()



    def connect(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)


    def button_event(self, event):
        self.key_pressed = False

        if event.inaxes == self.button_rect.ax:
            self.rect_coords = [(0, 0), (0, 0)]
            self.curr_state = self.States.GET_RECT

        elif event.inaxes == self.button_lear1.ax:
            if(self.lear_coords1):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lear_coords1 = None
            self.curr_state = self.States.GET_LEAR_LB
        elif event.inaxes == self.button_lear2.ax:
            if(self.lear_coords2):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lear_coords2 = None
            self.curr_state = self.States.GET_LEAR_LM
        elif event.inaxes == self.button_lear3.ax:
            if(self.lear_coords3):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lear_coords3 = None
            self.curr_state = self.States.GET_LEAR_T
        elif event.inaxes == self.button_lear4.ax:
            if(self.lear_coords4):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lear_coords4 = None
            self.curr_state = self.States.GET_LEAR_RM
        elif event.inaxes == self.button_lear5.ax:
            if(self.lear_coords5):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lear_coords5 = None
            self.curr_state = self.States.GET_LEAR_RB
        
        elif event.inaxes == self.button_rear1.ax:
            if(self.rear_coords1):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rear_coords1 = None
            self.curr_state = self.States.GET_REAR_LB
        elif event.inaxes == self.button_rear2.ax:
            if(self.rear_coords2):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rear_coords2 = None
            self.curr_state = self.States.GET_REAR_LM
        elif event.inaxes == self.button_rear3.ax:
            if(self.rear_coords3):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rear_coords3 = None
            self.curr_state = self.States.GET_REAR_T
        elif event.inaxes == self.button_rear4.ax:
            if(self.rear_coords4):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rear_coords4 = None
            self.curr_state = self.States.GET_REAR_RM
        elif event.inaxes == self.button_rear5.ax:
            if(self.rear_coords5):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rear_coords5 = None
            self.curr_state = self.States.GET_REAR_RB

        elif event.inaxes == self.button_leyeb.ax:
            if(self.leyeb_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.leyeb_coords = None
            self.curr_state = self.States.GET_LEYEB
        elif event.inaxes == self.button_reyeb.ax:
            if(self.reyeb_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.reyeb_coords = None
            self.curr_state = self.States.GET_REYEB
        
        elif event.inaxes == self.button_leye1.ax:
            if(self.leye_coords1):
                self.to_reset = True
            else:
                self.to_reset = False
            self.leye_coords1 = None
            self.curr_state = self.States.GET_LEYE1
        elif event.inaxes == self.button_leye2.ax:
            if(self.leye_coords2):
                self.to_reset = True
            else:
                self.to_reset = False
            self.leye_coords2 = None
            self.curr_state = self.States.GET_LEYE2
        elif event.inaxes == self.button_leye3.ax:
            if(self.leye_coords3):
                self.to_reset = True
            else:
                self.to_reset = False
            self.leye_coords3 = None
            self.curr_state = self.States.GET_LEYE3
        elif event.inaxes == self.button_leye4.ax:
            if(self.leye_coords4):
                self.to_reset = True
            else:
                self.to_reset = False
            self.leye_coords4 = None
            self.curr_state = self.States.GET_LEYE4
        
        elif event.inaxes == self.button_reye1.ax:
            if(self.reye_coords1):
                self.to_reset = True
            else:
                self.to_reset = False
            self.reye_coords1 = None
            self.curr_state = self.States.GET_REYE1
        elif event.inaxes == self.button_reye2.ax:
            if(self.reye_coords2):
                self.to_reset = True
            else:
                self.to_reset = False
            self.reye_coords2 = None
            self.curr_state = self.States.GET_REYE2
        elif event.inaxes == self.button_reye3.ax:
            if(self.reye_coords3):
                self.to_reset = True
            else:
                self.to_reset = False
            self.reye_coords3 = None
            self.curr_state = self.States.GET_REYE3
        elif event.inaxes == self.button_reye4.ax:
            if(self.reye_coords4):
                self.to_reset = True
            else:
                self.to_reset = False
            self.reye_coords4 = None
            self.curr_state = self.States.GET_REYE4

        elif event.inaxes == self.button_nose.ax:
            if(self.nose_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.nose_coords = None
            self.curr_state = self.States.GET_NOSE
        
        elif event.inaxes == self.button_tongue.ax:
            if(self.tongue_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.tongue_coords = None
            self.curr_state = self.States.GET_TONGUE

        elif event.inaxes == self.button_tmouth.ax:
            if(self.tmouth_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.tmouth_coords = None
            self.curr_state = self.States.GET_TMOUTH
        elif event.inaxes == self.button_rmouth.ax:
            if(self.rmouth_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.rmouth_coords = None
            self.curr_state = self.States.GET_RMOUTH
        elif event.inaxes == self.button_bmouth.ax:
            if(self.bmouth_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.bmouth_coords = None
            self.curr_state = self.States.GET_BMOUTH
        elif event.inaxes == self.button_lmouth.ax:
            if(self.lmouth_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.lmouth_coords = None
            self.curr_state = self.States.GET_LMOUTH
        
        elif event.inaxes == self.button_chin.ax:
            if(self.chin_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.chin_coords = None
            self.curr_state = self.States.GET_CHIN
        elif event.inaxes == self.button_head.ax:
            if(self.head_coords):
                self.to_reset = True
            else:
                self.to_reset = False
            self.head_coords = None
            self.curr_state = self.States.GET_HEAD

        elif event.inaxes == self.button_done.ax:
            self.is_finished = True

        elif event.inaxes == self.button_skip.ax:
            self.is_skipped = True

        if self.to_reset:
            self.redraw_annotations()
            self.update_button_labels()


    def init_subplots(self):
        self.fig = plt.figure(os.path.basename(self.img_path), figsize=(12,12))

        self.im_ax = self.fig.add_subplot(1, 2, 1)
        self.im_ax.set_title('Input')
        self.im_ax.imshow(self.image, interpolation='nearest')

        self.button_rect = Button(plt.axes([0.5, 0.8, 0.30, 0.05]), # x, y, w, h
                                  'Rectangle ()')
        self.button_rect.on_clicked(self.button_event)

        self.button_nose = Button(plt.axes([0.5, 0.7, 0.10, 0.05]),
                                  'Nose ()')
        self.button_nose.on_clicked(self.button_event)

        self.button_chin = Button(plt.axes([0.5, 0.625, 0.10, 0.05]),
                                    'Chin ()')
        self.button_chin.on_clicked(self.button_event)

        self.button_head = Button(plt.axes([0.5, 0.55, 0.10, 0.05]),
                                    'Head ()')
        self.button_head.on_clicked(self.button_event)

        self.button_leyeb = Button(plt.axes([0.5, 0.475, 0.10, 0.05]),
                                    'L Eyebrow ()')
        self.button_leyeb.on_clicked(self.button_event)

        self.button_reyeb = Button(plt.axes([0.5, 0.4, 0.10, 0.05]),
                                    'R Eyebrow ()')
        self.button_reyeb.on_clicked(self.button_event)


        self.button_lear1 = Button(plt.axes([0.61, 0.7, 0.10, 0.05]),
                                    'L Ear - LB ()')
        self.button_lear1.on_clicked(self.button_event)

        self.button_lear2 = Button(plt.axes([0.61, 0.625, 0.10, 0.05]),
                                    'L Ear - LM ()')
        self.button_lear2.on_clicked(self.button_event)

        self.button_lear3 = Button(plt.axes([0.61, 0.55, 0.10, 0.05]),
                                    'L Ear - T ()')
        self.button_lear3.on_clicked(self.button_event)

        self.button_lear4 = Button(plt.axes([0.61, 0.475, 0.10, 0.05]),
                                    'L Ear - RM ()')
        self.button_lear4.on_clicked(self.button_event)

        self.button_lear5 = Button(plt.axes([0.61, 0.4, 0.10, 0.05]),
                                    'L Ear - RB ()')
        self.button_lear5.on_clicked(self.button_event)

        self.button_rear1 = Button(plt.axes([0.72, 0.7, 0.10, 0.05]),
                                    'R Ear - LB ()')
        self.button_rear1.on_clicked(self.button_event)

        self.button_rear2 = Button(plt.axes([0.72, 0.625, 0.10, 0.05]),
                                    'R Ear - LM ()')
        self.button_rear2.on_clicked(self.button_event)

        self.button_rear3 = Button(plt.axes([0.72, 0.55, 0.10, 0.05]),
                                    'R Ear - T ()')
        self.button_rear3.on_clicked(self.button_event)

        self.button_rear4 = Button(plt.axes([0.72, 0.475, 0.10, 0.05]),
                                    'R Ear - RM ()')
        self.button_rear4.on_clicked(self.button_event)

        self.button_rear5 = Button(plt.axes([0.72, 0.4, 0.10, 0.05]),
                                    'R Ear - RB ()')
        self.button_rear5.on_clicked(self.button_event)

        self.button_leye1 = Button(plt.axes([0.83, 0.8, 0.10, 0.05]),
                                  'L Eye - T ()')
        self.button_leye1.on_clicked(self.button_event)

        self.button_leye2 = Button(plt.axes([0.83, 0.75, 0.10, 0.05]),
                                  'L Eye - R ()')
        self.button_leye2.on_clicked(self.button_event)

        self.button_leye3 = Button(plt.axes([0.83, 0.7, 0.10, 0.05]),
                                  'L Eye - B ()')
        self.button_leye3.on_clicked(self.button_event)

        self.button_leye4 = Button(plt.axes([0.83, 0.65, 0.10, 0.05]),
                                  'L Eye - L ()')
        self.button_leye4.on_clicked(self.button_event)

        self.button_tongue = Button(plt.axes([0.83, 0.60, 0.10, 0.05]),
                                  'Tongue ()')
        self.button_tongue.on_clicked(self.button_event)

        self.button_reye1 = Button(plt.axes([0.83, 0.55, 0.10, 0.05]),
                                  'R Eye - T ()')
        self.button_reye1.on_clicked(self.button_event)

        self.button_reye2 = Button(plt.axes([0.83, 0.5, 0.10, 0.05]),
                                  'R Eye - R ()')
        self.button_reye2.on_clicked(self.button_event)

        self.button_reye3 = Button(plt.axes([0.83, 0.45, 0.10, 0.05]),
                                  'R Eye - B ()')
        self.button_reye3.on_clicked(self.button_event)

        self.button_reye4 = Button(plt.axes([0.83, 0.4, 0.10, 0.05]),
                                  'R Eye - L ()')
        self.button_reye4.on_clicked(self.button_event)

        self.button_tmouth = Button(plt.axes([0.5, 0.3, 0.10, 0.05]),
                                    'Mouth - T ()')
        self.button_tmouth.on_clicked(self.button_event)

        self.button_rmouth = Button(plt.axes([0.61, 0.3, 0.10, 0.05]),
                                    'Mouth - R ()')
        self.button_rmouth.on_clicked(self.button_event)

        self.button_bmouth = Button(plt.axes([0.72, 0.3, 0.10, 0.05]),
                                    'Mouth - B ()')
        self.button_bmouth.on_clicked(self.button_event)

        self.button_lmouth = Button(plt.axes([0.83, 0.3, 0.10, 0.05]),
                                    'Mouth - L ()')
        self.button_lmouth.on_clicked(self.button_event)

        self.button_done = Button(plt.axes([0.5, 0.15, 0.45, 0.05]),
                                  'Done')
        self.button_done.on_clicked(self.button_event)

        self.button_skip = Button(plt.axes([0.5, 0.09, 0.45, 0.05]),
                                  'Skip')
        self.button_skip.on_clicked(self.button_event)

        self.update_button_labels()


    def fill_default_coords(self):
        # Left Ear - 5
        if self.lear_coords1 is None:
            self.lear_coords1 = (-1, -1)
        if self.lear_coords2 is None:
            self.lear_coords2 = (-1, -1)
        if self.lear_coords3 is None:
            self.lear_coords3 = (-1, -1)
        if self.lear_coords4 is None:
            self.lear_coords4 = (-1, -1)
        if self.lear_coords5 is None:
            self.lear_coords5 = (-1, -1)
        
        # Right Ear - 5
        if self.rear_coords1 is None:
            self.rear_coords1 = (-1, -1)
        if self.rear_coords2 is None:
            self.rear_coords2 = (-1, -1)
        if self.rear_coords3 is None:
            self.rear_coords3 = (-1, -1)
        if self.rear_coords4 is None:
            self.rear_coords4 = (-1, -1)
        if self.rear_coords5 is None:
            self.rear_coords5 = (-1, -1)
        
        # Left Eye - 4
        if self.leye_coords1 is None:
            self.leye_coords1 = (-1, -1)
        if self.leye_coords2 is None:
            self.leye_coords2 = (-1, -1)
        if self.leye_coords3 is None:
            self.leye_coords3 = (-1, -1)
        if self.leye_coords4 is None:
            self.leye_coords4 = (-1, -1)
        
        # Right Eye - 4
        if self.reye_coords1 is None:
            self.reye_coords1 = (-1, -1)
        if self.reye_coords2 is None:
            self.reye_coords2 = (-1, -1)
        if self.reye_coords3 is None:
            self.reye_coords3 = (-1, -1)
        if self.reye_coords4 is None:
            self.reye_coords4 = (-1, -1)
        
        # Nose tip
        if self.nose_coords is None:
            self.nose_coords = (-1, -1)
        
        # Tongue tip
        if self.tongue_coords is None:
            self.tongue_coords = (-1, -1)
        
        # Mouth - 4
        if self.tmouth_coords is None:
            self.tmouth_coords = (-1, -1)
        if self.rmouth_coords is None:
            self.rmouth_coords = (-1, -1)
        if self.bmouth_coords is None:
            self.bmouth_coords = (-1, -1)
        if self.lmouth_coords is None:
            self.lmouth_coords = (-1, -1)
        
        # Eyebrows
        if self.leyeb_coords is None:
            self.leyeb_coords = (-1, -1)
        if self.reyeb_coords is None:
            self.reyeb_coords = (-1, -1)
        
        # Chin
        if self.chin_coords is None:
            self.chin_coords = (-1, -1)
        
        # Head
        if self.head_coords is None:
            self.head_coords = (-1, -1)


    def save_annotations(self):
        self.fill_default_coords()
        if "pet_landmarks" not in f_data:
            f_data["pet_landmarks"] = []    
        f_data["pet_landmarks"].append({
                  self.curr_file: {
                  "Ears":{
                    "left":
                    {
                        "left_bottom": [self.lear_coords1[0], self.lear_coords1[1]],
                        "left_mid": [self.lear_coords2[0], self.lear_coords2[1]],
                        "top": [self.lear_coords3[0], self.lear_coords3[1]],
                        "right_mid": [self.lear_coords4[0], self.lear_coords4[1]],
                        "right_bottom": [self.lear_coords5[0], self.lear_coords5[1]]
                    },
                    "right":
                    {
                        "left_bottom": [self.rear_coords1[0], self.rear_coords1[1]],
                        "left_mid": [self.rear_coords2[0], self.rear_coords2[1]],
                        "top": [self.rear_coords3[0], self.rear_coords3[1]],
                        "right_mid": [self.rear_coords4[0], self.rear_coords4[1]],
                        "right_bottom": [self.rear_coords5[0], self.rear_coords5[1]]
                    },
                  },
                  "Eyebrows":
                  {
                        "left": [self.leyeb_coords[0], self.leyeb_coords[1]],
                        "right": [self.reyeb_coords[0], self.reyeb_coords[1]],
                  },
                  "Eyes":{
                    "left":
                    {
                        "top": [self.leye_coords1[0], self.leye_coords1[1]],
                        "right": [self.leye_coords2[0], self.leye_coords2[1]],
                        "bottom": [self.leye_coords3[0], self.leye_coords3[1]],
                        "left": [self.leye_coords4[0], self.leye_coords4[1]]
                    },
                    "right":
                    {
                        "top": [self.reye_coords1[0], self.reye_coords1[1]],
                        "right": [self.reye_coords2[0], self.reye_coords2[1]],
                        "bottom": [self.reye_coords3[0], self.reye_coords3[1]],
                        "left": [self.reye_coords4[0], self.reye_coords4[1]]
                    }
                  },
                  "Nose": [self.nose_coords[0], self.nose_coords[1]],
                  "Tongue": [self.tongue_coords[0], self.tongue_coords[1]],
                  "Mouth":
                  {
                    "top": [self.tmouth_coords[0], self.tmouth_coords[1]],
                    "right": [self.rmouth_coords[0], self.rmouth_coords[1]],
                    "bottom": [self.bmouth_coords[0], self.bmouth_coords[1]],
                    "left": [self.lmouth_coords[0], self.lmouth_coords[1]]
                  },
                  "Chin": [self.chin_coords[0], self.chin_coords[1]],
                  "Head": [self.head_coords[0], self.head_coords[1]],
                  "Face_Rect": [self.rect_coords[0][0], self.rect_coords[0][1],
                  self.rect_coords[1][0], self.rect_coords[1][1]],
                  "Height": self.rh,
                  "Width": self.rw
                  }
        })
        f_winner.seek(0)
        json.dump(f_data, f_winner, sort_keys = True, indent = 4, ensure_ascii = False)
        # print('{0},{1},{2},{3},{4},{5},{6},{7},{8}'
        #       ',{9},{10},{11},{12},{13},{14}'.format(
        #           os.path.basename(self.img_path),
        #           self.leye_coords[0], self.leye_coords[1],
        #           self.reye_coords[0], self.reye_coords[1],
        #           self.nose_coords[0], self.nose_coords[1],
        #           self.lmouth_coords[0], self.lmouth_coords[1],
        #           self.rmouth_coords[0], self.rmouth_coords[1],
        #           self.rect_coords[0][0], self.rect_coords[0][1],
        #           self.rect_coords[1][0] -
        #           self.rect_coords[0][0] + 1,
        #           self.rect_coords[1][1] -
        #           self.rect_coords[0][1] + 1))


    def run(self):
        self.init_subplots()
        self.connect()

        while True:
            # Wait for output, and 'update' figure
            plt.pause(0.03)

            # Exit
            if (self.is_finished
                    or (self.key_pressed and self.key_event.key == 'q')
                    or self.is_skipped):
                break

        plt.close()

        if self.is_finished:
            self.save_annotations()
            return 0 # finished normally
        elif self.is_skipped:
            return 0
        else:
            return 1 # aborted (pressed 'q')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Annotate one or more face images. Output to stdout.')
    base_group = parser.add_mutually_exclusive_group()
    base_group.add_argument('-d', '--dirimgs', type=str,
                            help='dir with images')
    base_group.add_argument('-i', '--img', type=str,
                            help='single image')
    parser.add_argument('-s', '--start_from', type=int, default=1,
                            help='For videos, provide a number to continue processing from')

    args = parser.parse_args()
    if args.dirimgs is None and args.img is None:
        parser.print_help()

    return args


def main(args):
    if args.dirimgs is not None:
        flist = sorted(paths.list_images(args.dirimgs))
        # print('image_fname,leye_x,leye_y,reye_x,reye_y,nose_x,nose_y,'
        #       'lmouth_x,lmouth_y,rmouth_x,rmouth_y,'
        #       'rect_top_x,rect_top_y,rect_width,rect_height')
        cnt = args.start_from - 1
        for curr_file in flist[args.start_from-1:]:
            cnt += 1
            print("Processing image #{} - {}".format(cnt, curr_file))
            img_path = os.path.join(args.dirimgs, curr_file)
            viewer = InteractiveViewer(img_path, curr_file)
            if viewer.run() == 1:
                #print('break at 366')
                print("Processing complete!")
                break
            else:
                #print('continue at 369')
                continue

    elif args.img is not None:
        # print('image_fname,leye_x,leye_y,reye_x,reye_y,nose_x,nose_y,'
        #       'lmouth_x,lmouth_y,rmouth_x,rmouth_y,'
        #       'rect_top_x,rect_top_y,rect_width,rect_height')

        img_path = args.img
        curr_file = os.path.basename(img_path)
        viewer = InteractiveViewer(img_path, curr_file)
        viewer.run()


if __name__ == '__main__':
    f_winner = open(r"C:\Users\Shrinjita Paul\Documents\GitHub\ImgCap\ANNOTATIONS\AnnotationTool\landmark_output.json", 'r+')
    f_data = json.load(f_winner)
    main(parse_arguments())
    f_winner.close()
    