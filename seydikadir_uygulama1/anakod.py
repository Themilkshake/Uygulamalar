import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QPushButton
from openpyxl import Workbook
import folium
from UI import *

#----VERİTABANI KISMI----

import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabani.db') 
curs = conn.cursor()

#Toplam 18 sütun. Eğer paketler tablosu yoksa, paketler tablosunu sütunlarıyla birlikte yazdırır.
sorguCreateTablePaketler = ("CREATE TABLE IF NOT EXISTS paketler(Paket_Numarasi INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, TakimAdi TEXT NOT NULL, TakimId TEXT NOT NULL, GondermeSaati TEXT NOT NULL, Pitch TEXT NOT NULL, Yaw TEXT NOT NULL, Roll TEXT NOT NULL, Basinc1 TEXT NOT NULL, Basinc2 TEXT NOT NULL, Yukseklik1 TEXT NOT NULL, Yukseklik2 TEXT NOT NULL, IrtifaFarki TEXT NOT NULL, InisHizi TEXT NOT NULL, Sicaklik TEXT NOT NULL, PilGerilimi TEXT NOT NULL, GPS1Latitude TEXT NOT NULL, GPS1Longitude TEXT NOT NULL, GPS1Altitude TEXT NOT NULL)")
curs.execute(sorguCreateTablePaketler)
conn.commit()
a = 1

#--------------------------

#------Thread sınıfı-------
class MyThread(QThread):
    # Güncelleme sinyali tanımlama
    update_signal = pyqtSignal()

    # İş parçacığı ana metodu
    def run(self):
        while True:
            # Güncelleme sinyalini gönderme
            self.update_signal.emit()
            # 1000 milisaniye (1 saniye) bekleme
            self.msleep(1000)
#--------------------------

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Butonlar burada tanımlanır.
        self.actionS_r_m.clicked.connect(self.KAPAT)
        # self.excel_kaydet.clicked.connect(self.excelkaydet)
        # self.label.setPixmap(QPixmap("gorsel/logo.png"))
        # self.setWindowIcon(QIcon('gorsel/logo.png'))
        #-------------------------------------------------
        # layout oluşturma
        # self.layout = QGridLayout(self.tableWidget_1)
        # self.layout2 = QVBoxLayout(self.tableWidget_2)
        # self.layout3 = QVBoxLayout(self.tableWidget_3)

        # Matplotlib figürünü PyQt5 arayüze yerleştirme
        # self.figure1, self.ax1 = plt.subplots()
        # self.figure2, self.ax2 = plt.subplots()
        # self.figure3, self.ax3 = plt.subplots()
        # self.figure4, self.ax4 = plt.subplots()
        # self.figure5, self.ax5 = plt.subplots()
        # self.figure6, self.ax6 = plt.subplots()
        # self.canvas = FigureCanvas(self.figure1)
        # self.canvas2 = FigureCanvas(self.figure2)
        # self.canvas3 = FigureCanvas(self.figure3)
        # self.canvas4 = FigureCanvas(self.figure4)
        # self.canvas5 = FigureCanvas(self.figure5)
        # self.canvas6 = FigureCanvas(self.figure6)
        # # GPS widget'ı.
        # self.webview = QWebEngineView(self)
        # self.webview2 = QWebEngineView(self)
        # self.ax1.plot(data)
        # self.ax2.plot(data)
        # self.ax3.plot(data)
        # self.ax4.plot(data)
        # self.ax5.plot(data)
        # self.ax6.plot(data)
        # # GPS'in layout'u.
        # self.layout2.addWidget(self.webview)
        # # Grafiklerin layout'u.
        # self.layout.addWidget(self.canvas, 0, 0)
        # self.layout.addWidget(self.canvas2, 0, 1)
        # self.layout.addWidget(self.canvas3, 0, 2)
        # self.layout.addWidget(self.canvas4, 1, 0)
        # self.layout.addWidget(self.canvas5, 1, 1)
        # self.layout.addWidget(self.canvas6, 1, 2)

        # Thread oluşturma ve başlatma
        self.thread = MyThread()
        self.thread.update_signal.connect(self.LISTELE)
        self.thread.update_signal.connect(self.update_graph)
        self.thread.update_signal.connect(self.update_graph2)
        self.thread.update_signal.connect(self.tablo_asagi_tut)
        self.thread.update_signal.connect(self.konum)
        self.thread.start()
        #-------------------------------------------------
        # self.tableWidget.clear()
        # self.LISTELE()

    self ali(self):
         self.su

    def konum(self):
        # Folium map oluştur
        m = folium.Map(location=[41.086149, 28.917113], zoom_start=40, zoom_control=False)
        # Marker ekle
        folium.Marker(location=[41.086149, 28.917113], icon=folium.Icon(icon="glyphicon-screenshot")).add_to(m)
        # Folium mapi html olarak kaydet
        m.save("map.html")
        # görüntüle
        self.webview.setHtml(open("map.html").read())


    def excelkaydet(self):

        # SQLite veritabanı bağlantısı oluştur
        conn = sqlite3.connect('veritabani.db')  # 'veritabani.db' dosya adını kendi SQLite veritabanı dosyanıza uygun şekilde değiştirin
        query = "SELECT * FROM paketler"  # 'tablo' yerine kendi tablo adınızı kullanın

        # SQLite verilerini sorgula
        cursor = conn.execute(query)

        # Sütun başlıklarını al
        columns = [description[0] for description in cursor.description]

        # Workbook ve Worksheet oluştur
        wb = Workbook()
        ws = wb.active

        # Sütun başlıklarını ekleyin
        ws.append(columns)

        # SQLite verilerini Excel dosyasına ekle
        for row in cursor.fetchall():
            ws.append(row)

        # Excel dosyasını kaydet
        wb.save('veritabani_verileri.xlsx')  # 'veritabani_verileri.xlsx' dosya adını istediğiniz bir adla değiştirin

        # Bağlantıyı kapat
        conn.close()

    def tablo_asagi_tut(self):
        self.tableWidget.verticalScrollBar().setValue(self.tableWidget.verticalScrollBar().maximum())

    def KAPAT(self):
        # paketler tablosunu siler.
        conn.execute("DROP TABLE IF EXISTS paketler;") 
        conn.commit()
        conn.close()
        self.close() 
        
    def LISTELE(self):
        self.tableWidget.setHorizontalHeaderLabels(('PAKET NUMARASI','TAKIM ADI','TAKIM ID','GONDERME SAATİ','PITCH','YAW','ROLL','BASINC1','BASINC2','YUKSEKLİK1','YUKSEKLİK2','IRTIFA FARKI','INIS HIZI','SICAKLIK','PIL GERİLİMİ','GPS1 Latitude','GPS1 Longitude','GPS1 Altitude'))

        curs.execute("SELECT * FROM paketler")
        rows = curs.fetchall()

        self.tableWidget.setRowCount(len(rows))  # Tablonun satır sayısını ayarla

        for satirIndeks, satirVeri in enumerate(rows):
            for sutunIndeks, sutunVeri in enumerate(satirVeri):
                item = QTableWidgetItem(str(sutunVeri))
                self.tableWidget.setItem(satirIndeks, sutunIndeks, item)

        curs.execute("INSERT INTO paketler(TakimAdi, TakimId, GondermeSaati, Pitch, Yaw, Roll, Basinc1, Basinc2, Yukseklik1, Yukseklik2, IrtifaFarki, InisHizi, Sicaklik, PilGerilimi, GPS1Latitude, GPS1Longitude, GPS1Altitude) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(a,a,d,k,a,a,a,a,a,a,a,a,a,a,a,a,a))

        conn.commit()


    def update_graph(self):

        # Rastgele veri oluşturup grafik üzerinde göster
        #data = [0,0,0,0,0,0,0,0,0,0]
        self.ax1.clear()
        self.ax1.plot(data)
        
        self.ax3.clear()
        self.ax3.plot(data)
        self.ax4.clear()
        self.ax4.plot(data)
        self.ax5.clear()
        self.ax5.plot(data)
        self.ax6.clear()
        self.ax6.plot(data)
        # self.layout.addWidget(self.canvas)
        global d
        d = random.randint(1, 10)
        data.append(d)
        data.pop(0)
        # plt.clf()
        self.canvas.draw()
        self.canvas3.draw()
        self.canvas4.draw()
        self.canvas5.draw()
        self.canvas6.draw()
        print("çizdi, data = " + str(data))

    
    def update_graph2(self):
        # Rastgele veri oluşturup grafik üzerinde göster
        global k
        k = random.randint(1, 10)
        self.ax2.clear()
        self.ax2.plot(data2)
        data2.append(k)
        data2.pop(0)
        # plt.clf()
        self.canvas2.draw()
        print("çizdi2, data2 = " + str(data2))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


