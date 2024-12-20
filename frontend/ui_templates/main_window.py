# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\frontend\ui_templates\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(475, 285)
        MainWindow.setMinimumSize(QtCore.QSize(475, 285))
        MainWindow.setMaximumSize(QtCore.QSize(475, 285))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\frontend\\ui_templates\\p_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(16, 16))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lb_select_fuel_type = QtWidgets.QLabel(self.centralwidget)
        self.lb_select_fuel_type.setGeometry(QtCore.QRect(40, 0, 131, 31))
        self.lb_select_fuel_type.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_select_fuel_type.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_select_fuel_type.setObjectName("lb_select_fuel_type")
        self.lb_default_alarm_time = QtWidgets.QLabel(self.centralwidget)
        self.lb_default_alarm_time.setGeometry(QtCore.QRect(40, 80, 131, 31))
        self.lb_default_alarm_time.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_default_alarm_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_default_alarm_time.setObjectName("lb_default_alarm_time")
        self.cb_fuel_type = QtWidgets.QComboBox(self.centralwidget)
        self.cb_fuel_type.setGeometry(QtCore.QRect(40, 40, 131, 31))
        self.cb_fuel_type.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cb_fuel_type.setStyleSheet("QComboBox {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 20px;\n"
"    border-left: 2px solid #2980b9;\n"
"    background-color: #3498db;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(frontend/ui_templates/down_arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid #2980b9;\n"
"    background-color: #ecf0f1;\n"
"    selection-background-color: #3498db;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"")
        self.cb_fuel_type.setObjectName("cb_fuel_type")
        self.cb_fuel_type.addItem("")
        self.cb_fuel_type.addItem("")
        self.cb_fuel_type.addItem("")
        self.cb_fuel_type.addItem("")
        self.cb_fuel_type.addItem("")
        self.cb_fuel_type.addItem("")
        self.te_default_alarm_time = QtWidgets.QTimeEdit(self.centralwidget)
        self.te_default_alarm_time.setGeometry(QtCore.QRect(40, 120, 131, 31))
        self.te_default_alarm_time.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.te_default_alarm_time.setStyleSheet("QTimeEdit {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QTimeEdit::up-button, QTimeEdit::down-button {\n"
"    width: 18px;\n"
"    border: none;\n"
"    background-color: #3498db;\n"
"}\n"
"\n"
"QTimeEdit::up-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    image: url(frontend/ui_templates/up_arrow.png);\n"
"}\n"
"\n"
"QTimeEdit::down-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    image: url(frontend/ui_templates/down_arrow.png);\n"
"}\n"
"\n"
"QTimeEdit:hover {\n"
"    border-color: #3498db;\n"
"}\n"
"")
        self.te_default_alarm_time.setAlignment(QtCore.Qt.AlignCenter)
        self.te_default_alarm_time.setObjectName("te_default_alarm_time")
        self.te_sleep_time = QtWidgets.QTimeEdit(self.centralwidget)
        self.te_sleep_time.setGeometry(QtCore.QRect(280, 120, 131, 31))
        self.te_sleep_time.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.te_sleep_time.setStyleSheet("QTimeEdit {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QTimeEdit::up-button, QTimeEdit::down-button {\n"
"    width: 18px;\n"
"    border: none;\n"
"    background-color: #3498db;\n"
"}\n"
"\n"
"QTimeEdit::up-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    image: url(frontend/ui_templates/up_arrow.png);\n"
"}\n"
"\n"
"QTimeEdit::down-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    image: url(frontend/ui_templates/down_arrow.png);\n"
"}\n"
"\n"
"QTimeEdit:hover {\n"
"    border-color: #3498db;\n"
"}\n"
"")
        self.te_sleep_time.setAlignment(QtCore.Qt.AlignCenter)
        self.te_sleep_time.setObjectName("te_sleep_time")
        self.lb_sleep_time = QtWidgets.QLabel(self.centralwidget)
        self.lb_sleep_time.setGeometry(QtCore.QRect(270, 80, 151, 31))
        self.lb_sleep_time.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_sleep_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_sleep_time.setObjectName("lb_sleep_time")
        self.lb_alarm_text = QtWidgets.QLabel(self.centralwidget)
        self.lb_alarm_text.setGeometry(QtCore.QRect(0, 30, 471, 41))
        self.lb_alarm_text.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_alarm_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_alarm_text.setObjectName("lb_alarm_text")
        self.bt_speech_to_text = QtWidgets.QPushButton(self.centralwidget)
        self.bt_speech_to_text.setGeometry(QtCore.QRect(190, 130, 91, 70))
        self.bt_speech_to_text.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_speech_to_text.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: transparent;\n"
"    padding: 8px 16px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 6px;\n"
"    background-color: #3498db;\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"    text-align: center;\n"
"    min-width: 50px;\n"
"    min-height: 50px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"    border-color: #2980b9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1f618d;\n"
"    border-color: #1f618d;\n"
"}\n"
"")
        self.bt_speech_to_text.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\frontend\\ui_templates\\microphone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_speech_to_text.setIcon(icon1)
        self.bt_speech_to_text.setIconSize(QtCore.QSize(35, 35))
        self.bt_speech_to_text.setObjectName("bt_speech_to_text")
        self.lb_alarm = QtWidgets.QLabel(self.centralwidget)
        self.lb_alarm.setGeometry(QtCore.QRect(0, 70, 471, 41))
        self.lb_alarm.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_alarm.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_alarm.setObjectName("lb_alarm")
        self.bt_settings = QtWidgets.QPushButton(self.centralwidget)
        self.bt_settings.setGeometry(QtCore.QRect(430, 10, 31, 31))
        self.bt_settings.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_settings.setStyleSheet("QPushButton {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"QPushButton:hover {\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        self.bt_settings.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\frontend\\ui_templates\\setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_settings.setIcon(icon2)
        self.bt_settings.setIconSize(QtCore.QSize(28, 40))
        self.bt_settings.setObjectName("bt_settings")
        self.sl_fuel_threshold = QtWidgets.QSlider(self.centralwidget)
        self.sl_fuel_threshold.setGeometry(QtCore.QRect(300, 40, 160, 31))
        self.sl_fuel_threshold.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sl_fuel_threshold.setStyleSheet("QSlider {\n"
"    background: #ecf0f1;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #3498db;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    margin-top: -6px;\n"
"    margin-bottom: -6px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    background: #ecf0f1;\n"
"    border: none;\n"
"    height: 6px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background: #2980b9;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background: #1abc9c;\n"
"}")
        self.sl_fuel_threshold.setMinimum(100)
        self.sl_fuel_threshold.setMaximum(200)
        self.sl_fuel_threshold.setSingleStep(5)
        self.sl_fuel_threshold.setPageStep(1)
        self.sl_fuel_threshold.setProperty("value", 105)
        self.sl_fuel_threshold.setOrientation(QtCore.Qt.Horizontal)
        self.sl_fuel_threshold.setTickInterval(5)
        self.sl_fuel_threshold.setObjectName("sl_fuel_threshold")
        self.le_fuel_threshold = QtWidgets.QLineEdit(self.centralwidget)
        self.le_fuel_threshold.setGeometry(QtCore.QRect(230, 40, 61, 31))
        self.le_fuel_threshold.setStyleSheet("QLineEdit {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #3498db;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #7f8c8d;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    color: #2c3e50;\n"
"}\n"
"\n"
".error {\n"
"        border: 2px solid red;\n"
"        background-color: #f8d7da;\n"
"    }")
        self.le_fuel_threshold.setObjectName("le_fuel_threshold")
        self.lb_select_fuel_threshold = QtWidgets.QLabel(self.centralwidget)
        self.lb_select_fuel_threshold.setGeometry(QtCore.QRect(230, 0, 231, 31))
        self.lb_select_fuel_threshold.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_select_fuel_threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_select_fuel_threshold.setObjectName("lb_select_fuel_threshold")
        self.bt_save_settings = QtWidgets.QPushButton(self.centralwidget)
        self.bt_save_settings.setGeometry(QtCore.QRect(390, 210, 71, 51))
        self.bt_save_settings.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_save_settings.setStyleSheet("QPushButton {\n"
"    background-color: #2ecc71;\n"
"    color: white;\n"
"    border: 2px solid #27ae60;\n"
"    border-radius: 8px;\n"
"    padding: 10px 20px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #27ae60;\n"
"    border: 2px solid #1e8449;\n"
"    color: #ecf0f1;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1e8449;\n"
"    border: 2px solid #1d6f43;\n"
"    color: #bdc3c7;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #bdc3c7;\n"
"    border: 2px solid #95a5a6;\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.bt_save_settings.setObjectName("bt_save_settings")
        self.lb_sound_wave_gif = QtWidgets.QLabel(self.centralwidget)
        self.lb_sound_wave_gif.setGeometry(QtCore.QRect(160, 210, 151, 41))
        self.lb_sound_wave_gif.setText("")
        self.lb_sound_wave_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_sound_wave_gif.setObjectName("lb_sound_wave_gif")
        self.le_fuel_demo_price = QtWidgets.QLineEdit(self.centralwidget)
        self.le_fuel_demo_price.setGeometry(QtCore.QRect(180, 220, 61, 31))
        self.le_fuel_demo_price.setStyleSheet("QLineEdit {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #3498db;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #7f8c8d;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    color: #2c3e50;\n"
"}\n"
"\n"
".error {\n"
"        border: 2px solid red;\n"
"        background-color: #f8d7da;\n"
"    }")
        self.le_fuel_demo_price.setObjectName("le_fuel_demo_price")
        self.lb_fuel_demo_price = QtWidgets.QLabel(self.centralwidget)
        self.lb_fuel_demo_price.setGeometry(QtCore.QRect(0, 220, 181, 31))
        self.lb_fuel_demo_price.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_fuel_demo_price.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_fuel_demo_price.setObjectName("lb_fuel_demo_price")
        self.cb_select_mic = QtWidgets.QComboBox(self.centralwidget)
        self.cb_select_mic.setGeometry(QtCore.QRect(130, 170, 291, 31))
        self.cb_select_mic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cb_select_mic.setStyleSheet("QComboBox {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"    padding: 4px;\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 4px;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 20px;\n"
"    border-left: 2px solid #2980b9;\n"
"    background-color: #3498db;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(frontend/ui_templates/down_arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid #2980b9;\n"
"    background-color: #ecf0f1;\n"
"    selection-background-color: #3498db;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"")
        self.cb_select_mic.setCurrentText("")
        self.cb_select_mic.setMaxVisibleItems(40)
        self.cb_select_mic.setObjectName("cb_select_mic")
        self.lb_select_mic = QtWidgets.QLabel(self.centralwidget)
        self.lb_select_mic.setGeometry(QtCore.QRect(30, 170, 101, 31))
        self.lb_select_mic.setStyleSheet("QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 4px;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QLabel.headline {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    background-color: #f0f8ff;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 12px;\n"
"}\n"
"\n"
"QLabel.subheadline {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    margin-bottom: 8px;\n"
"}\n"
"\n"
"QLabel:disabled {\n"
"    color: #7f8c8d;\n"
"}\n"
"")
        self.lb_select_mic.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_select_mic.setObjectName("lb_select_mic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 475, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " "))
        self.lb_select_fuel_type.setText(_translate("MainWindow", "Kraftstoffart"))
        self.lb_default_alarm_time.setText(_translate("MainWindow", "Weckzeit"))
        self.cb_fuel_type.setItemText(0, _translate("MainWindow", "Super E10", "super_e10"))
        self.cb_fuel_type.setItemText(1, _translate("MainWindow", "Super E5"))
        self.cb_fuel_type.setItemText(2, _translate("MainWindow", "Super Plus"))
        self.cb_fuel_type.setItemText(3, _translate("MainWindow", "Diesel"))
        self.cb_fuel_type.setItemText(4, _translate("MainWindow", "LKW Diesel"))
        self.cb_fuel_type.setItemText(5, _translate("MainWindow", "LPG"))
        self.lb_sleep_time.setText(_translate("MainWindow", "Schlafenszeit"))
        self.lb_alarm_text.setText(_translate("MainWindow", "Alarm gesetzt für:"))
        self.lb_alarm.setText(_translate("MainWindow", "00:00 Uhr"))
        self.lb_select_fuel_threshold.setText(_translate("MainWindow", "Kraftstoffschwelle"))
        self.bt_save_settings.setText(_translate("MainWindow", "Ok"))
        self.lb_fuel_demo_price.setText(_translate("MainWindow", "DEMO Sprit Preis"))
        self.lb_select_mic.setText(_translate("MainWindow", "Mikrofon"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
