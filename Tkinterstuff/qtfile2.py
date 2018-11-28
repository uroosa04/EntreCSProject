# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import reverse_geocoder as rg
import os
class Ui_Dialog(object):
    
    def gpsRequest(self):

        lat = ""
        lon = ""
        alt = ""
        timestamp = ""
        gpsList = []

        try:
            with open('data.nmea') as fp:
                line = csv.reader(fp)
                print(line)
                for row in line:
                    if(row[0] == "$GPGGA"):
                        gpsList.append(row) 

                print(gpsList[-1])
                list = gpsLIst[-1]
                time = list[1]
                hour = int(str(time)[:2])
                hour = hour - 6
                timestamp = "Time: " + str(hour) + ":" + time[2:4] + ":" + time[4:6]
                lat = "Latitude: " + list[2] + list[3]
                lon = "Longitude: " + list[4] + list[5]
                alt = "Altutude: " + list[9] + list[10]
                fp.close()
        except:
            print("Cannot Process GPS File Data.")

        _translate = QtCore.QCoreApplication.translate
        self.GPSlabel21.setText(_translate("Dialog", lat))
        self.GPSlabel31.setText(_translate("Dialog", lon))
        #self.GPSlabel12.setText(_translate("Dialog", "TextLabel"))
        self.GPSlabel11.setText(_translate("Dialog", timestamp))
        self.GPSlabel41.setText(_translate("Dialog", alt))
        #self.GPSlabel22.setText(_translate("Dialog", "TextLabel"))
        #self.GPSlabel32.setText(_translate("Dialog", "TextLabel"))
        #self.GPSlabel42.setText(_translate("Dialog", "TextLabel"))
        self.GPSDataLabel.setText(_translate("Dialog", "GPS Data"))

    def doRequest(self):
        coordinates = (29.7604, -95.3698)
        results = rg.search(coordinates)
        city = results[0]['name']
        state = results[0]['admin1']
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # Where city and state goes
        cityAndState = city + ", " + state
        parse = "\"" + cityAndState + "\")"
        yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="
        yql_query += parse
        try:
            yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
            result = urlopen(yql_url).read()
            data = json.loads(result)
        except:
            _translate = QtCore.QCoreApplication.translate
            wind = ""
            temp = ""

            try:
<<<<<<< HEAD
                yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
                result = urlopen(yql_url).read()
                data = json.loads(result.decode('utf-8'))
=======
                if os.stat("wind").st_size == 0 or os.stat("temp").st_size == 0:
                    wind += "No"
                    temp += "Network"
                else :
                    with open('wind', 'r') as myfile:
                        wind += myfile.read()
                    with open('temp', 'r') as myfile:
                        temp += myfile.read()
>>>>>>> weather
            except:
                wind += "No"
                temp += "Network"

            self.weatherLabel.setText(_translate("Dialog", wind))
            self.weatherLabel2.setText(_translate("Dialog", temp))
            # self.weatherLabel3.setText(_translate("Dialog", extra))
            # print(data)
            self.weatherLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            self.weatherLabel2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            # self.weatherLabel3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        else:

            #Wheater Labels
            _translate = QtCore.QCoreApplication.translate
            wind = "Wind\n" + \
                   "Chill: " + data['query']['results']['channel']['wind']['chill'] + data['query']['results']['channel']['units']['temperature'] + "\n" + "Direction: " + data['query']['results']['channel']['wind']['direction'] + "°" + "\n" + "Speed: " + data['query']['results']['channel']['wind']['speed'] + data['query']['results']['channel']['units']['speed']
            temp = ""
            dailyWeatherArray = data['query']['results']['channel']['item']['forecast']
            for x in range(3):
                temp += dailyWeatherArray[x]['day']
                temp += "\n"
                temp += "High: " + dailyWeatherArray[x]['high'] + data['query']['results']['channel']['units']['temperature']
                temp += "\n"
                temp += "Low: " + dailyWeatherArray[x]['low'] + data['query']['results']['channel']['units']['temperature']
                temp += "\n"
                temp += dailyWeatherArray[x]['text']
                temp += "\n"
                if(x <= 1) :
                    temp += "\n"

            extra = "Humidity: " + data['query']['results']['channel']['atmosphere']['humidity'] + "%" + "\n" + \
                    "Pressure: " + str(round((float(data['query']['results']['channel']['atmosphere']['pressure']) * 0.02953), 2)) + data['query']['results']['channel']['units']['pressure'] + "\n" + \
                    "Sunrise: " + data['query']['results']['channel']['astronomy']['sunrise'] + "\n" + \
                    "Sunset: " + data['query']['results']['channel']['astronomy']['sunset']

            wind += "\n" + "\n" + extra
            file2write_wind = open("wind", 'w')
            file2write_wind.write(wind)
            file2write_wind.close()
            file2write_temp = open("temp", 'w')
            file2write_temp.write(temp)
            file2write_temp.close()

            self.weatherLabel.setText(_translate("Dialog", wind))
            self.weatherLabel2.setText(_translate("Dialog", temp))
            #self.weatherLabel3.setText(_translate("Dialog", extra))
            #print(data)
            self.weatherLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            self.weatherLabel2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            #self.weatherLabel3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)


    def assertGarner(self):
        for item in self.ParkNameWidget.selectedItems():
            if item.text() == self.parks[0]: #Garner State Park
                self.doRequest()

                _translate = QtCore.QCoreApplication.translate
                trails = ["Old Entrance Road",
                          "Donovan Trail",
                          "Bridges Trail",
                          "Crystal Cave Trail",
                          "Blinn River Trail",
                          "Old Blady Trail",
                          "Foshee Trail",
                          "Ashe Juniper Trail",
                          "Old Horse Trail",
                          "Frio Canyon Trail"
                          ]

                i = 0
                for trail in trails:
                    item = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item)
                    item = self.listWidget.item(i)
                    item.setText(_translate("Dialog", trail))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    i += 1
                self.stackedWidget.setCurrentIndex(1)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Coming Soon!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setWindowTitle("Error")
                msg.exec()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 480)
        Dialog.setFixedSize(320,480)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #Dialog.showFullScreen()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        Dialog.setFont(font)
        Dialog.setStyleSheet("")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout_1 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_1.setObjectName("gridLayout_1")

        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(-2, -2, 411, 311))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setAutoFillBackground(False)
        self.page.setStyleSheet("#page {background-image: url(:/newPrefix/mountain.jpg);\n"
"}")
        self.page.setObjectName("page")


        BUTTONFONT = QtGui.QFont()
        BUTTONFONT.setFamily("Arial")
        BUTTONFONT.setPointSize(11)    #Font for all buttons
        BUTTONFONT.setBold(True)
        BUTTONFONT.setWeight(75)


        self.OkayButton = QtWidgets.QPushButton(self.page)
        self.OkayButton.setGeometry(QtCore.QRect(300, 260, 93, 28))
        self.OkayButton.setObjectName("OkayButton")
        self.OkayButton.setFont(BUTTONFONT)

        self.GPSButton = QtWidgets.QPushButton(self.page)
        self.GPSButton.setGeometry(QtCore.QRect(15, 260, 50, 28))
        self.GPSButton.setObjectName("GPSButton")
        self.GPSButton.setFont(BUTTONFONT)

        self.ParkNameWidget = QtWidgets.QListWidget(self.page)
        self.ParkNameWidget.setGeometry(QtCore.QRect(10, 70, 391, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ParkNameWidget.setFont(font)
        self.ParkNameWidget.setAutoFillBackground(False)
        self.ParkNameWidget.setStyleSheet("color: rgb(157, 157, 157);\n"
"background-color: rgba(226, 226, 226, 200);")
        self.ParkNameWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.ParkNameWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.ParkNameWidget.setUniformItemSizes(False)
        self.ParkNameWidget.setWordWrap(False)
        self.ParkNameWidget.setSelectionRectVisible(False)
        self.ParkNameWidget.setObjectName("ParkNameWidget")

        '''item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ParkNameWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ParkNameWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ParkNameWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.ParkNameWidget.addItem(item)'''

        self.RouteLabel = QtWidgets.QLabel(self.page)
        self.RouteLabel.setGeometry(QtCore.QRect(80, 20, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.RouteLabel.setFont(font)
        self.RouteLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.RouteLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RouteLabel.setObjectName("RouteLabel")

        self.pageGrid = QtWidgets.QGridLayout(self.page)
        self.pageGrid.setObjectName("pageGrid")
        self.pageGrid.addWidget(self.RouteLabel, 0, 0, 1, 1)
        self.pageGrid.addWidget(self.ParkNameWidget, 1, 0, 1, 1)
        self.pageGrid.addWidget(self.OkayButton, 2, 0, 1, 1)
        self.pageGrid.addWidget(self.GPSButton, 3, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setStyleSheet("#page_2 {background-image: url(:/newPrefix/mountain.jpg);}")
        self.page_2.setObjectName("page_2")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.page_2)
        self.graphicsView.setGeometry(QtCore.QRect(10, 40, 371, 111))
        self.graphicsView.setObjectName("graphicsView")
        self.listWidget = QtWidgets.QListWidget(self.page_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 200, 241, 81))
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.listWidget.setFont(font)
        self.ChooseRouteLabel = QtWidgets.QLabel(self.page_2)
        self.ChooseRouteLabel.setGeometry(QtCore.QRect(20, 170, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ChooseRouteLabel.setFont(font)
        self.ChooseRouteLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ChooseRouteLabel.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.page_2)
        self.pushButton.setGeometry(QtCore.QRect(280, 200, 91, 31))
        '''font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)'''
        self.pushButton.setFont(BUTTONFONT)
        self.pushButton.setObjectName("pushButton")
        self.backButton = QtWidgets.QPushButton(self.page_2)
        self.backButton.setGeometry(QtCore.QRect(280, 240, 93, 28))
        '''font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)'''

        self.backButton.setFont(BUTTONFONT)
        self.backButton.setObjectName("backButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.page_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 39, 371, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.weatherLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.weatherLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherLabel.setObjectName("weatherLabel")
        self.horizontalLayout.addWidget(self.weatherLabel)
        self.weatherLabel2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.weatherLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherLabel2.setObjectName("weatherLabel2")
        self.horizontalLayout.addWidget(self.weatherLabel2)
        '''self.weatherLabel3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.weatherLabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherLabel3.setObjectName("weatherLabel3")
        self.horizontalLayout.addWidget(self.weatherLabel3)'''

        self.page2Grid = QtWidgets.QGridLayout(self.page_2)
        self.page2Grid.addWidget(self.label, 0, 0, 1, 1)
        self.page2Grid.addWidget(self.graphicsView, 1, 0, 1, 3)
        self.page2Grid.addWidget(self.ChooseRouteLabel, 2, 0, 1, 1)
        self.page2Grid.addWidget(self.horizontalLayoutWidget, 1, 0, 1, 3)
        self.page2Grid.addWidget(self.listWidget, 3, 0, 2, 2)
        self.page2Grid.addWidget(self.pushButton, 3, 2, 1, 1)
        self.page2Grid.addWidget(self.backButton,4, 2, 1, 1)
        self.stackedWidget.addWidget(self.page_2)


        self.page_3 = QtWidgets.QWidget()
        self.page_3.setStyleSheet("#page_3 {background-image: url(:/newPrefix/mountain.jpg);}")
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)

        self.page_4 = QtWidgets.QWidget()
        self.page_4.setStyleSheet("#page_4 {background-image: url(:/newPrefix/mountain.jpg);}")
        self.page_4.setObjectName("page_4")
        self.gridLayoutWidget = QtWidgets.QWidget(self.page_4)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 221, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.GPSlabel21 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel21.setObjectName("GPSlabel21")
        self.gridLayout.addWidget(self.GPSlabel21, 1, 0, 1, 1)
        self.GPSlabel31 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel31.setObjectName("GPSlabel31")
        self.gridLayout.addWidget(self.GPSlabel31, 2, 0, 1, 1)
        self.GPSlabel12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel12.setObjectName("GPSlabel12")
        self.gridLayout.addWidget(self.GPSlabel12, 0, 1, 1, 1)
        self.GPSlabel11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel11.setObjectName("GPSlabel11")
        self.gridLayout.addWidget(self.GPSlabel11, 0, 0, 1, 1)
        self.GPSlabel41 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel41.setObjectName("GPSlabel41")
        self.gridLayout.addWidget(self.GPSlabel41, 3, 0, 1, 1)
        self.GPSlabel22 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel22.setObjectName("GPSlabel22")
        self.gridLayout.addWidget(self.GPSlabel22, 1, 1, 1, 1)
        self.GPSlabel32 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel32.setObjectName("GPSlabel32")
        self.gridLayout.addWidget(self.GPSlabel32, 2, 1, 1, 1)
        self.GPSlabel42 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GPSlabel42.setObjectName("GPSlabel42")
        self.gridLayout.addWidget(self.GPSlabel42, 3, 1, 1, 1)
        self.GPSDataLabel = QtWidgets.QLabel(self.page_4)
        self.GPSDataLabel.setGeometry(QtCore.QRect(260, 20, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GPSDataLabel.setFont(font)
        self.GPSDataLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.GPSDataLabel.setObjectName("GPSDataLabel")
        self.backButton2 = QtWidgets.QPushButton(self.page_4)
        self.backButton2.setGeometry(QtCore.QRect(270, 150, 93, 28))
        '''font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)'''

        self.backButton2.setFont(BUTTONFONT)
        self.backButton2.setObjectName("backButton2")

        self.page4Grid = QtWidgets.QGridLayout(self.page_4)
        self.page4Grid.addWidget(self.gridLayoutWidget, 0, 0, 4, 2)
        self.page4Grid.addWidget(self.GPSDataLabel, 0, 3, 1, 1)
        self.page4Grid.addWidget(self.backButton2, 2, 3, 1, 1)
        self.stackedWidget.addWidget(self.page_4)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)

        self.GPSButton.clicked.connect(lambda: self.gpsRequest())
        self.OkayButton.clicked.connect(lambda: self.assertGarner())#lambda: self.stackedWidget.setCurrentIndex(1))
        self.GPSButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.backButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.backButton2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.gridLayout_1.addWidget(self.stackedWidget)#, 0, 0, 1, 1)
        self.gridLayout_1.setContentsMargins(0,0,0,0)



    def retranslateUi(self, Dialog):
        self.parks = ["Garner State Park",
                 "Yosemite National Park",
                 "Big Bend State Park",
                 "Yellow Stone National Park"]

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.OkayButton.setText(_translate("Dialog", "OK"))
        self.GPSButton.setText(_translate("Dialog", "GPS"))
        self.ParkNameWidget.setSortingEnabled(False)
        __sortingEnabled = self.ParkNameWidget.isSortingEnabled()
        self.ParkNameWidget.setSortingEnabled(False)

        i = 0
        for location in self.parks:
            item = QtWidgets.QListWidgetItem()
            self.ParkNameWidget.addItem(item)
            item = self.ParkNameWidget.item(i)
            item.setText(_translate("Dialog", location))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            i += 1

        """item = self.ParkNameWidget.item(0)
        item.setText(_translate("Dialog", "Yosemite National Park"))
        item = self.ParkNameWidget.item(1)
        item.setText(_translate("Dialog", "Big Bend State Park"))
        item = self.ParkNameWidget.item(2)
        item.setText(_translate("Dialog", "Yellow Stone National Park"))"""

        self.ParkNameWidget.setSortingEnabled(__sortingEnabled)
        self.RouteLabel.setText(_translate("Dialog", "Choose Your Location"))
        self.label.setText(_translate("Dialog", "Weather"))
        self.ChooseRouteLabel.setText(_translate("Dialog", "Choose Your Route"))
        self.pushButton.setText(_translate("Dialog", "Continue"))
        self.backButton.setText(_translate("Dialog", "Back"))


        self.backButton2.setText(_translate("Dialog", "Back"))

import resource

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
