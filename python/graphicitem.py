#!/usr/bin/env python
#
# Copyright 2019
# ghostop14
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt as Qtc
from PyQt5.QtCore import QSize

import os
import sys

from gnuradio import gr
import pmt

class GrGraphicItem(gr.sync_block, QLabel):
    def __init__(self,imageFile,scaleImage=True,fixedSize=False,setWidth=0,setHeight=0):
        gr.sync_block.__init__(self, name = "GrGraphicsItem", in_sig = None, out_sig = None)
        QLabel.__init__(self)
        
        if not os.path.isfile(imageFile):
            print("[GrGraphicsItem] ERROR: Unable to find file " + imageFile)
            sys.exit(1)
            
        try:
            self.pixmap = QPixmap(imageFile)
        except OSError as e:
            print("[GrGraphicsItem] ERROR: " + e.strerror)
            sys.exit(1)
        
        self.scaleImage = scaleImage
        self.fixedSize = fixedSize
        self.setWidth = setWidth
        self.setHeight = setHeight
        super().setPixmap(self.pixmap)
        
        self.message_port_register_in(pmt.intern("filename"))
        self.set_msg_handler(pmt.intern("filename"), self.msgHandler)   
        
    def msgHandler(self, msg):
        try:    
            newVal = pmt.to_python(pmt.cdr(msg))

            if type(newVal) == str:
                if not os.path.isfile(imageFile):
                    print("[GrGraphicsItem] ERROR: Unable to find file " + imageFile)
                    return
                
                try:
                    self.pixmap = QPixmap(imageFile)
                except OSError as e:
                    print("[GrGraphicsItem] ERROR: " + e.strerror)
                    return
                
                super().setPixmap(self.pixmap)
                update()
            else:
                print("[GrGraphicsItem] Error: Value received was not an int or a bool: %s" % str(e))
                
        except Exception as e:
            print("[GrGraphicsItem] Error with message conversion: %s" % str(e))

    def minimumSizeHint(self):
        return QSize(self.pixmap.width(),self.pixmap.height())

    def resizeEvent(self, event):
        if self.scaleImage:
            w = super().width()
            h = super().height()
            
            super().setPixmap(self.pixmap.scaled(w,h,Qtc.KeepAspectRatio))
        elif self.fixedSize and self.setWidth > 0 and self.setHeight > 0:
            super().setPixmap(self.pixmap.scaled(self.setWidth,self.setHeight,Qtc.KeepAspectRatio))

        