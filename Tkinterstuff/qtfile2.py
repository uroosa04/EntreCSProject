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
import math

class Ui_Dialog(object):

    def getTrailInfo(self, x):
        global milesTraveled
        global elevationGain
        global elevationLoss
        if x==1:
            print("You have chosen Old Entrance Road!")
            milesTraveled=.84
            elevationGain = 120
            elevationLoss = 20
        elif x==2:
            print("You have chosen Donovan Trail!")
            milesTraveled=.71
            elevationGain = 240
            elevationLoss = 40
        elif x==3:
            print("You have chosen Bridges Trail!")
            milesTraveled=.65
            elevationGain = 40
            elevationLoss = 40
        elif x==4:
            print("You have chosen Crystal Cave Trail!")
            milesTraveled=.62
            elevationGain = 360
            elevationLoss = 40
        elif x==5:
            print("You have chosen Blinn River Trail!")
            milesTraveled=.53
            elevationGain = 20
            elevationLoss = 20
        elif x==6:
            print("You have chosen Old Baldy Trail!")
            milesTraveled=.53
            elevationGain = 440
            elevationLoss = 40
        elif x==7:
            print("You have chosen Foshee Trail!")
            milesTraveled=1.66
            elevationGain = 420
            elevationLoss = 360
        elif x==8:
            print("You have chosen Ashe Juniper Trail!")
            milesTraveled=2.49
            elevationGain = 320
            elevationLoss = 200
        elif x==9:
            print("You have chosen Old Horse Trail!")
            milesTraveled=.48
            elevationGain = 80
            elevationLoss = 20
        elif x==10:
            print("You have chosen Frio Canyon Trail!")
            milesTraveled=2.88
            elevationGain = 140
            elevationLoss = 140
        else:
            print("Invalid entry. Please try again.")

    def calculateTravelTime(self, trailNumber, paceIndex):
        _translate = QtCore.QCoreApplication.translate
        
        #Assign trail
        self.getTrailInfo(trailNumber)

        print(" ")

        #paceIndex=int(input("Input pace index 1 - 4, (1 for beginner, 4 for experienced hiker)"))

        print(" ")

        x =(milesTraveled / 10)
        fudgeFactor=round(x,1)
        #print("Fudge Factor: ", fudgeFactor)

        totalMiles = round((milesTraveled + fudgeFactor),1)
        int(totalMiles)
        print("Total Miles: " , totalMiles)


        climbingRate = 1000 #CONSTANT
        gainFactor = round(elevationGain / climbingRate,1)
        #print("Gain Factor: ", gainFactor)


        lossRate = 2000 #CONSTANT
        lossFactor = round((elevationLoss / lossRate),1)
        #print("Loss Factor: " , lossFactor)

        elevationFactor = (gainFactor - lossFactor)
        #print("Elevation Factor: " , elevationFactor)

        totalMovingTime = round(((totalMiles/paceIndex)+elevationFactor),1)
        print("Total Moving Time: ", totalMovingTime, " hours.")


        if ((totalMovingTime) > 0) :
            tempMovingTime=math.floor(totalMovingTime)
            numLongBreaks=int(tempMovingTime/4)
            leftoverMovingTime=tempMovingTime-numLongBreaks
            numshortbreaks=leftoverMovingTime
            shortbreakstime=(numshortbreaks * 5) 
            longbreakstime=numLongBreaks * 30
            print("Short Breaks: ", shortbreakstime, " minutes.")
            print("Long Breaks: ", longbreakstime, " minutes.")
        else :
            shortbreakstime=0
            longbreakstime=0
            print("Short Breaks: ", shortbreakstime, " minutes.")
            print("Long Breaks: ", longbreakstime, " minutes.") 


        totalTravelTime = round((totalMovingTime + (shortbreakstime/60) + (longbreakstime/60)),1)
        print("Total Travel Time: " , totalTravelTime, " hours.")
        self.algoData11.setText(_translate("Dialog", "Total Miles: " + str(totalMiles) + "\n" +
            "Total Moving Time: " + str(totalMovingTime) + " hrs" + "\n" +
            "Short Breaks Time: " + str(shortbreakstime) + " mins" + "\n" +
            "Long Breaks Time: " + str(longbreakstime) + " mins"+ "\n"
            "Total Total Time: " + str(totalTravelTime) + " hrs"))

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
                        timestamp = row[1]
                        lat = row[2] + row[3]
                        lon = row[4] + row[5]
                        alt = row[9] + row[10]
                        gpsList.append(row)

                print(gpsList[-1])
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
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read()
        data = json.loads(result)

        #Wheater Labels
        _translate = QtCore.QCoreApplication.translate
        wind = "Wind\n" + \
               "Chill: " + data['query']['results']['channel']['wind']['chill'] + data['query']['results']['channel']['units']['temperature'] + "\n" + "Direction: " + data['query']['results']['channel']['wind']['direction'] + "°" + "\n" + "Speed: " + data['query']['results']['channel']['wind']['speed'] + data['query']['results']['channel']['units']['speed']
        temp = ""
        dailyWeatherArray = data['query']['results']['channel']['item']['forecast']
        for x in range(3):
            temp += "\n"
            temp += "High: " + dailyWeatherArray[x]['high'] + data['query']['results']['channel']['units']['temperature']
            temp += "\n"
            temp += "Low: " + dailyWeatherArray[x]['low'] + data['query']['results']['channel']['units']['temperature']
            temp += "\n"
            temp += "Day: " + dailyWeatherArray[x]['day']
            temp += "\n"
            temp += dailyWeatherArray[x]['text']
            temp += "\n"

        extra = "Humidity: " + data['query']['results']['channel']['atmosphere']['humidity'] + "%" + "\n" + \
                "Pressure: " + str(round((float(data['query']['results']['channel']['atmosphere']['pressure']) * 0.02953), 2)) + data['query']['results']['channel']['units']['pressure'] + "\n" + \
                "Sunrise: " + data['query']['results']['channel']['astronomy']['sunrise'] + "\n" + \
                "Sunset: " + data['query']['results']['channel']['astronomy']['sunset']

        wind += "\n" + "\n" + extra
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
                self.trails = ["Old Entrance Road",
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
                for trail in self.trails:
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

    def selectRoute(self):
        self.routeNumber = 0
        for item in self.listWidget.selectedItems():
            self.routeNumber = self.trails.index(item.text()) #item.text
            self.stackedWidget.setCurrentIndex(2)

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
        self.page3Grid = QtWidgets.QGridLayout(self.page_3)
        self.page3Grid.setObjectName("page3Grid")
        self.page3GridLayoutWidget = QtWidgets.QWidget(self.page_3)
        self.page3GridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 221, 301))
        self.page3GridLayoutWidget.setObjectName("page3GridLayoutWidget")
        self.page3GridLayout = QtWidgets.QGridLayout(self.page3GridLayoutWidget)
        self.page3GridLayout.setContentsMargins(0, 0, 0, 0)
        self.page3GridLayout.setObjectName("page3GridLayout")
        self.algoData11 = QtWidgets.QLabel(self.page3GridLayoutWidget)
        self.algoData11.setObjectName("algoData11")
        self.page3GridLayout.addWidget(self.algoData11, 0, 1, 1, 1)
        self.algoData11.setFont(font)
        #self.algoData11.setAlignment(QtCore.Qt.AlignCenter)

        self.backButton3 = QtWidgets.QPushButton(self.page_3)
        self.backButton3.setGeometry(QtCore.QRect(270, 150, 93, 28))
        self.backButton3.setFont(BUTTONFONT)
        self.backButton3.setObjectName("backButton3")
        self.backButton3.setText("Back")
        self.CalculateButton = QtWidgets.QPushButton(self.page_3)
        self.CalculateButton.setGeometry(QtCore.QRect(270, 150, 93, 28))
        self.CalculateButton.setFont(BUTTONFONT)
        self.CalculateButton.setObjectName("CalculateButton")
        self.CalculateButton.setText("Calculate")
        self.page3Grid.addWidget(self.backButton3, 2, 2, 1, 1)
        self.page3Grid.addWidget(self.CalculateButton, 1, 2, 1, 1)
        self.page3Grid.addWidget(self.page3GridLayoutWidget, 1, 1, 3, 1)
        self.paceIndexBox = QtWidgets.QComboBox()
        self.paceIndexBox.addItems(['1', '2', '3', '4'])
        self.page3Grid.addWidget(self.paceIndexBox, 0, 2, 1, 1)

        #font = QtGui.QFont()
        #font.setFamily("Arial")
        #font.setPointSize(6)
        #font.setBold(True)
        #self.paceLabel = QtWidgets.QLabel(self.page_3)
        #self.paceLabel.setFont(font)
        #self.paceLabel.setStyleSheet("color: rgb(255, 255, 255);")
        #self.paceLabel.setObjectName("paceLabel")
        #self.paceLabel.setText("Choose Your Pace")#+ "\n" +"1 - Beginner" + "\n" + "4 - Expert")
        #self.paceLabel.setGeometry(QtCore.QRect(20, 170, 171, 21))
        #self.page3Grid.addWidget(self.paceLabel, 1, 2, 1, 1)
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
        self.pushButton.clicked.connect(lambda: self.selectRoute())
        self.CalculateButton.clicked.connect(lambda: self.calculateTravelTime(self.routeNumber + 1, self.paceIndexBox.currentIndex() + 1))
        self.backButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.backButton2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.backButton3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
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
