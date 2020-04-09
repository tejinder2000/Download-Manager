import os
import sys
import urllib.request

import humanize
import pafy
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtCore

from pynotifier import Notification
from main import Ui_MainWindow

status = 0


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()
        self.OS_Management()

    def InitUI(self):
        ## contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)
        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()
        self.Move_Box_5()
        self.Move_Box_6()
        # self.Apply_light_style()

    def Handle_Buttons(self):
        ## Handle all buttons in app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)
        self.pushButton_6.clicked.connect(self.Get_Video_Data)
        self.pushButton_8.clicked.connect(self.Download_Video)
        self.pushButton_7.clicked.connect(self.Save_Browse)
        self.pushButton_4.clicked.connect(self.Playlist_Download)
        self.pushButton_3.clicked.connect(self.Playlist_Save_Browse)
        self.pushButton_5.clicked.connect(self.Save_Browse_Audio)
        self.pushButton_9.clicked.connect(self.Download_Audio_Data)

        self.pushButton_10.clicked.connect(self.Open_Home)
        self.pushButton_12.clicked.connect(self.Open_Download)
        self.pushButton_11.clicked.connect(self.Open_Youtube)
        self.pushButton_13.clicked.connect(self.Open_Settings)
        self.pushButton_17.clicked.connect(self.Get_Playlist_Data)

        # self.pushButton_8.clicked.connect(self.Video_Progress)

        self.pushButton_14.clicked.connect(self.Apply_DarkGrey_Style)
        self.pushButton_15.clicked.connect(self.Apply_DarkBlue_Style)
        self.pushButton_16.clicked.connect(self.Apply_light_style)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handle_Browse(self):
        ## enable browsing to pick save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        ## Downloading in file

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)

                if self.checkBox_2.isChecked():
                    self.Push_Notification()

                QMessageBox.information(self, "Download Completed", "The Download Completed Successfully")

                if self.checkBox.isChecked():
                    os.system("shutdown ")

                if self.checkBox_3.isChecked():
                    exit()

            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
                return

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Browse(self):
        ## Save location in the line edit
        pass

    #####################################################
    ######## DOwnload Youtube Videos #########

    def Save_Browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_6.setText(str(save_location[0]))

    def Get_Video_Data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL")
        else:
            video = pafy.new(video_url)

            streams = video.streams
            for s in streams:
                size = humanize.naturalsize(s.get_filesize())
                data = "{} {} {} ".format(s.resolution, size, s.extension)
                self.comboBox_2.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_6.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Enter valid URL or save location")

        else:
            video = pafy.new(video_url)

            video_stream = video.streams
            video_quality = self.comboBox_2.currentIndex()
            download = video_stream[video_quality].download(callback=self.Video_Progress, filepath=save_location)
            if self.checkBox_2.isChecked():
                self.Push_Notification()

            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully")

            if self.checkBox.isChecked():
                os.system("shutdown ")

            if self.checkBox_3.isChecked():
                exit()

            s = 'Download Complete'

            QApplication.processEvents()

        if s == 'Download Complete':
            self.Reset()

    def Video_Progress(self, total, received, ratio, rate, time):
        readed_data = received
        if total > 0:
            download_percentage = readed_data * 100 / total
            self.progressBar_3.setValue(download_percentage)

            remaining_time = round((time) / 60, 2)

            self.label_5.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def Reset(self):
        self.progressBar_3.setValue(0)
        self.comboBox_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_6.clear()
        self.label_5.clear()
        status = 1

    #############################################
    ############ Playlist Download #############

    def Get_Playlist_Data(self):
        ###### For quality retrival #####
        video_url = self.lineEdit_5.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL")
        else:
            playlist = pafy.get_playlist(video_url)
            playlist_videos = playlist['items']

            c = 0
            for video in playlist_videos:
                QApplication.processEvents()

                current_video = video['pafy']
                current_video_stream = current_video.streams
                current_video_stream = current_video.streams

                c = 1
                if c == 1:
                    break

            for s in current_video_stream:
                size = humanize.naturalsize(s.get_filesize())
                data = "{} {} {} {} ".format(s.mediatype, s.resolution, size, s.extension)
                self.comboBox.addItem(data)

    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_4.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1

        quality = self.comboBox.currentIndex()

        self.lcdNumber.display(current_video_in_download)

        for video in playlist_videos:
            QApplication.processEvents()
            quality = self.comboBox.currentIndex()
            current_video = video['pafy']
            current_video_stream = current_video.streams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)

            current_video_in_download += 1
            print(current_video_stream)

    def Playlist_Progress(self, total, received, ratio, rate, time):
        readed_data = received
        if total > 0:
            download_percentage = readed_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_4.setText(playlist_save_location)

    ###############################################
    ############ Download Audio ###############

    def Save_Browse_Audio(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_8.setText(str(save_location[0]))

    def Download_Audio_Data(self):
        audio_url = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()

        if audio_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL")

        else:
            video = pafy.new(audio_url)
            best_audio = video.getbestaudio()
            download = best_audio.download(filepath=save_location, callback=self.Video_Progress1)
            success = 'Download Complete'

            if self.checkBox_2.isChecked():
                self.Push_Notification()

            QMessageBox.information(self, "Download Complete", 'Your Audio file has been downloaded successfully')

            if self.checkBox.isChecked():
                os.system("shutdown ")

            if self.checkBox_3.isChecked():
                exit()

        if success == 'Download Complete':
            self.Reset1()

    def Video_Progress1(self, total, received, ratio, rate, time):
        readed_data = received
        if total > 0:
            download_percentage = readed_data * 100 / total
            self.progressBar_4.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_7.setText(str('{} minutes remaining'.format(remaining_time)))

            QApplication.processEvents()

    def Reset1(self):
        self.progressBar_4.setValue(0)
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.label_7.clear()

    ###################################################
    ################# UI changes ###################

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)

    ################################################
    ############### App Themes ##################

    def Apply_DarkGrey_Style(self):
        style = open('Themes/darkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkBlue_Style(self):
        style = open('Themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_light_style(self):
        style = open('Themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    ###########################################
    ############# App Anmation #############

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation1.setDuration(1000)
        box_animation1.setStartValue(QRect(0, 0, 0, 0))
        box_animation1.setEndValue(QRect(60, 30, 381, 131))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(1000)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(460, 20, 371, 131))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(1000)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(60, 170, 381, 131))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(1000)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(480, 170, 361, 131))
        box_animation4.start()
        self.box_animation4 = box_animation4

    def Move_Box_5(self):
        box_animation5 = QPropertyAnimation(self.groupBox_5, b"geometry")
        box_animation5.setDuration(1000)
        box_animation5.setStartValue(QRect(0, 0, 0, 0))
        box_animation5.setEndValue(QRect(50, 320, 381, 131))
        box_animation5.start()
        self.box_animation5 = box_animation5

    def Move_Box_6(self):
        box_animation6 = QPropertyAnimation(self.groupBox_6, b"geometry")
        box_animation6.setDuration(1000)
        box_animation6.setStartValue(QRect(0, 0, 0, 0))
        box_animation6.setEndValue(QRect(470, 320, 381, 131))
        box_animation6.start()
        self.box_animation6 = box_animation6

    def state_changed(self):
        if self.checkBox.isChecked():
            print(self.checkBox.isChecked())

    def OS_Management(self):
        self.checkBox.checkState()
        if self.checkBox.checkState() == 1:
            print('working')

    def Push_Notification(self):
        Notification(
            title='Download Complete',
            description='Your Download has been successfully completed',

            duration=5,
            urgency=Notification.URGENCY_CRITICAL
        ).send()





def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
