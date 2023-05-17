# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:13:00 2021

@author: SCLAB503-01-LYR
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMessageBox,QFileDialog
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import QTimer,QThread,pyqtSignal


import os
import sys

from MainUI_d import Ui_MainWindow #UI檔案引入class


import requests
from requests.auth import HTTPDigestAuth
# from fake_useragent import UserAgent

class MainWindow4k(QtWidgets.QMainWindow):
    def __init__(self):
         super(MainWindow4k, self).__init__()
         self.ui = Ui_MainWindow()
         self.ui.setupUi(self)
         
         self.ui.btnRefresh.clicked.connect(self.RefreshData)
         self.ui.btnSetFocus.clicked.connect(self.SetFocus)
         self.ui.btnSetZoom.clicked.connect(self.SetZoom)
         self.ui.btnSetAutoFocus.clicked.connect(self.SetAutoFocus)
         self.ui.btnCompile.clicked.connect(self.dataCompile)
         
         # self.ua = UserAgent()
         self.url=''
         self.restext=''
         
         self.headers = {
             'Authorization': 'Digest username="root", realm="streaming_server", nonce="", uri="/cgi-bin/admin/remotefocus.cgi?channel=0&function=getstatus", algorithm="MD5", qop=auth, cnonce="", response="153c5856f4c0ab4693fba7e5b3210c22"'
             }
         
         self.myParams = {
             'channel': '0', 
             'function': 'getstatus'}
         
         
         self.my_focus = {
             'channel': '0', 
             'function': 'focus' , 
             'direction': 'direct', 
             'position': '720'}
         
         self.my_zoom ={
             'channel': '0', 
             'function': 'zoom' , 
             'direction': 'direct', 
             'position': '316'}
         
         self.my_auto ={
             'channel': '0', 
             'function': 'auto' , 
             'iris' : 1}
         
         self.payload={}
         self.data=[0,0]#focus,zoom
         
         self.trueFocus=0
         
         self.user='root'
         self.pwd='password'
         
    def getURL(self):
        self.url=self.ui.txtURL.text()
         
    def RefreshData(self):
        self.getURL()
        # self.url="http://192.168.50.40/cgi-bin/admin/remotefocus.cgi?channel=0&function=getstatus"
        
        # headers = {'Authorization': 'Digest username="root", realm="streaming_server", nonce="", uri="/cgi-bin/admin/remotefocus.cgi?channel=0&function=getstatus", algorithm="MD5", qop=auth, cnonce="", response="153c5856f4c0ab4693fba7e5b3210c22"'}
        
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload,auth=HTTPDigestAuth(self.user, self.pwd),params=self.myParams)
        
        restext=response.text
        
        a=restext.split('\r\n')
        b=a[7].split('=')#focus
        self.data[0]=int((b[1][1:-1]))
        b=a[6].split('=')#zoom
        self.data[1]=int((b[1][1:-1]))
        
        self.ui.txtPackage.setText(restext)
        
        self.ui.txtFocus.setText(str(self.data[0]))
        self.ui.txtZoom.setText(str(self.data[1]))
        
        self.dataCompile()
    
    def SetFocus(self):
        self.my_focus = {
             'channel': '0', 
             'function': 'focus' , 
             'direction': 'direct', 
             'position': str(self.ui.txtFocus.text() )}
        
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload,auth=HTTPDigestAuth(self.user, self.pwd),params=self.my_focus)
        self.RefreshData()
        self.dataCompile()
        
    def SetZoom(self):
        self.my_zoom ={
             'channel': '0', 
             'function': 'zoom' , 
             'direction': 'direct', 
             'position': str(self.ui.txtZoom.text())}
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload,auth=HTTPDigestAuth(self.user, self.pwd),params=self.my_zoom)
        self.RefreshData()
        self.dataCompile()
        
    def SetAutoFocus(self):
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload,auth=HTTPDigestAuth(self.user, self.pwd),params=self.my_auto)
        self.RefreshData()
        self.dataCompile()
        
    def dataCompile(self):
        focusstep=823
        if self.data[0]==0:
            self.trueFocus=3.9
        elif self.data[0]==822:
            self.trueFocus=10
        else:
            self.trueFocus=round(self.data[0] * ((10-3.9)/ focusstep),3) +3.9
            
        self.trueFocus='%.2f' % self.trueFocus
        #round(self.trueFocus,2)
        self.ui.lblFocusmm.setText(str(self.trueFocus))
            
         
if __name__ == '__main__':
     app = QtWidgets.QApplication([])
     window = MainWindow4k()
     window.show()
     sys.exit(app.exec_()) 