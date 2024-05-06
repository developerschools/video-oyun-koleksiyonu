from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTextEdit, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, 
    QTextBrowser
)
import sqlite3

# Video oyunlarını temsil eden bir sınıf.
class Oyun:
    def __init__(self, ad, turu, platform):
        self.ad = ad  # Oyunun adı
        self.turu = turu  # Oyunun türü
        self.platform = platform  # Oyunun platformu
        self.degerlendirmeler = []  # Oyun için yapılan değerlendirmelerin listesi

    def __str__(self):
        return "{} - {} - {}".format(self.ad, self.turu, self.platform)

    # Yeni bir değerlendirme ekler.
    def degerlendir(self, oyuncu_adi, puan, yorum):
        self.degerlendirmeler.append({"oyuncu_adi": oyuncu_adi, "puan": puan, "yorum": yorum})

# Kullanıcının oyun koleksiyonunu temsil eden sınıf.
class Koleksiyon:
    def __init__(self):
        self.oyunlar = []  # Koleksiyonda bulunan oyunların listesi

    # Yeni bir oyun ekler.
    def oyun_ekle(self, oyun):
        self.oyunlar.append(oyun)

# Kullanıcıyı temsil eden sınıf.
class Oyuncu:
    def __init__(self, ad):
        self.ad = ad  # Oyuncunun adı
        self.koleksiyon = Koleksiyon()  # Oyuncunun oyun koleksiyonu

# Kullanıcı arayüzü için QWidget sınıfından türetilmiş sınıf.
class OyunArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Oyun Koleksiyonu Yonetimi")
        self.init_ui()  # Arayüzü başlatan metot.
        self.create_db()

    def init_ui(self):
        # Arayüz bileşenlerini oluşturma ve düzenleme.

        # Oyun bilgilerini girmek için QLabel ve QLineEdit bileşenleri.
        self.label_oyun_ad = QLabel("Oyun Adı:")
        self.input_oyun_ad = QLineEdit()

        self.label_oyun_turu = QLabel("Oyun Turu:")
        self.input_oyun_turu = QLineEdit()

        self.label_oyun_platform = QLabel("Oyun Platformu:")
        self.input_oyun_platform = QLineEdit()

        # Oyun ekleme düğmesi.
        self.button_oyun_ekle = QPushButton("Oyun Ekle")
        self.button_oyun_ekle.clicked.connect(self.oyun_ekle)  # Oyun ekleme düğmesine tıklandığında oyun_ekle() fonksiyonunu çağırır.

        # Kullanıcının koleksiyonundaki oyunları listeleyen bileşen.
        self.liste_oyunlar = QListWidget()
        self.liste_oyunlar.itemClicked.connect(self.oyun_secildi)  # Oyun listesinden bir oyun seçildiğinde oyun_secildi() fonksiyonunu çağırır.

        # Değerlendirme bilgilerini girmek için QLabel, QLineEdit ve QTextEdit bileşenleri.
        self.label_degerlendirme = QLabel("Degerlendirme:")
        self.label_oyuncu_adi = QLabel("Oyuncu Adı:")
        self.input_oyuncu_adi = QLineEdit()

        self.label_puan = QLabel("Puan:")
        self.input_puan = QLineEdit()

        self.label_yorum = QLabel("Yorum:")
        self.input_yorum = QTextEdit()

        # Oyun değerlendirme düğmesi.
        self.button_degerlendir = QPushButton("Degerlendir")
        self.button_degerlendir.clicked.connect(self.oyun_degerlendir)  # Degerlendirme düğmesine tıklandığında oyun_degerlendir() fonksiyonunu çağırır.

        # Değerlendirmeleri gösteren bileşen.
        self.text_degerlendirmeler = QTextBrowser()

        # Oyun satın alma düğmesi.
        self.button_satin_al = QPushButton("Satin Al")
        self.button_satin_al.clicked.connect(self.oyun_satin_al)  # Satin Al düğmesine tıklandığında oyun_satin_al() fonksiyonunu çağırır.

        # Arayüz bileşenlerini düzenleme
        layout_oyun_ad = QHBoxLayout()
        layout_oyun_ad.addWidget(self.label_oyun_ad)
        layout_oyun_ad.addWidget(self.input_oyun_ad)

        layout_oyun_turu = QHBoxLayout()
        layout_oyun_turu.addWidget(self.label_oyun_turu)
        layout_oyun_turu.addWidget(self.input_oyun_turu)

        layout_oyun_platform = QHBoxLayout()
        layout_oyun_platform.addWidget(self.label_oyun_platform)
        layout_oyun_platform.addWidget(self.input_oyun_platform)

        layout_oyun_ekle = QHBoxLayout()
        layout_oyun_ekle.addWidget(self.button_oyun_ekle)

        layout_degerlendirme = QHBoxLayout()
        layout_degerlendirme.addWidget(self.label_degerlendirme)

        layout_oyuncu_adi = QHBoxLayout()
        layout_oyuncu_adi.addWidget(self.label_oyuncu_adi)
        layout_oyuncu_adi.addWidget(self.input_oyuncu_adi)

        layout_puan = QHBoxLayout()
        layout_puan.addWidget(self.label_puan)
        layout_puan.addWidget(self.input_puan)

        layout_yorum = QHBoxLayout()
        layout_yorum.addWidget(self.label_yorum)
        layout_yorum.addWidget(self.input_yorum)

        layout_degerlendir = QHBoxLayout()
        layout_degerlendir.addWidget(self.button_degerlendir)

        # Arayüzü düzenleme
        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_oyun_ad)
        self.layout.addLayout(layout_oyun_turu)
        self.layout.addLayout(layout_oyun_platform)
        self.layout.addLayout(layout_oyun_ekle)
        self.layout.addWidget(self.liste_oyunlar)
        self.layout.addLayout(layout_degerlendirme)
        self.layout.addLayout(layout_oyuncu_adi)
        self.layout.addLayout(layout_puan)
        self.layout.addLayout(layout_yorum)
        self.layout.addLayout(layout_degerlendir)
        self.layout.addWidget(self.text_degerlendirmeler)
        self.layout.addWidget(self.button_satin_al)
        self.setLayout(self.layout)

        # Kullanıcı ve oyunlar listesi oluşturma.
        self.oyuncu = Oyuncu("Oyuncu")
        self.oyunlar = []

    # Yeni bir oyun ekler.
    def oyun_ekle(self):
        oyun_ad = self.input_oyun_ad.text()
        oyun_turu = self.input_oyun_turu.text()
        oyun_platform = self.input_oyun_platform.text()

        # Gerekli alanların doldurulup doldurulmadığını kontrol eder.
        if not oyun_ad or not oyun_turu or not oyun_platform:
            QMessageBox.warning(self, "Uyari", "Lütfen tüm alanları doldurun!")
            return

        # Oyun nesnesi oluşturur ve koleksiyona ekler.
        oyun = Oyun(oyun_ad, oyun_turu, oyun_platform)
        self.oyuncu.koleksiyon.oyun_ekle(oyun)
        self.oyunlar.append(oyun)
        self.liste_oyunlar.addItem(str(oyun))
        self.insert_game_to_db(oyun_ad, oyun_turu, oyun_platform) # Veritabanına ekleme
        QMessageBox.information(self, "Bilgi", "Oyun başarıyla eklendi!")

    # Listeden bir oyun seçildiğinde çağrılır ve oyunun değerlendirmelerini gösterir.
    def oyun_secildi(self, item):
        self.text_degerlendirmeler.clear()
        oyun_adi = item.text()
        for oyun in self.oyunlar:
            if str(oyun) == oyun_adi:
                for degerlendirme in oyun.degerlendirmeler:
                    self.text_degerlendirmeler.append("{} - Puan: {}\n{}\n".format(degerlendirme['oyuncu_adi'], degerlendirme['puan'], degerlendirme['yorum']))

    # Oyunu değerlendirir.
    def oyun_degerlendir(self):
        oyun_adi = self.liste_oyunlar.currentItem().text()
        oyuncu_adi = self.input_oyuncu_adi.text()
        puan = self.input_puan.text()
        yorum = self.input_yorum.toPlainText()

        # Gerekli alanların doldurulup doldurulmadığını kontrol eder.
        if not oyuncu_adi or not puan or not yorum:
            QMessageBox.warning(self, "Uyari", "Lütfen tüm alanları doldurun!")
            return

        # Seçilen oyunu bulur ve değerlendirme yapar.
        for oyun in self.oyunlar:
            if str(oyun) == oyun_adi:
                oyun.degerlendir(oyuncu_adi, puan, yorum)
                self.text_degerlendirmeler.append("{} - Puan: {}\n{}\n".format(oyuncu_adi, puan, yorum))
                self.insert_review_to_db(oyun.ad, oyuncu_adi, puan, yorum) # Veritabanına ekleme
                QMessageBox.information(self, "Bilgi", "Oyun başarıyla değerlendirildi!")
                return

    # Oyun satın alma işlemini gerçekleştirir.
    def oyun_satin_al(self):
        QMessageBox.information(self, "Bilgi", "Oyun satın alındı!")

    # Veritabanını oluşturur
    def create_db(self):
        self.conn = sqlite3.connect('oyunlar.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Oyunlar (
                            id INTEGER PRIMARY KEY,
                            ad TEXT NOT NULL,
                            tur TEXT NOT NULL,
                            platform TEXT NOT NULL
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Degerlendirmeler (
                            id INTEGER PRIMARY KEY,
                            oyun_id INTEGER,
                            oyuncu_adi TEXT NOT NULL,
                            puan INTEGER NOT NULL,
                            yorum TEXT NOT NULL,
                            FOREIGN KEY(oyun_id) REFERENCES Oyunlar(id)
                            )''')
        self.conn.commit()

    # Oyunu veritabanına ekler
    def insert_game_to_db(self, ad, tur, platform):
        self.cur.execute("INSERT INTO Oyunlar (ad, tur, platform) VALUES (?, ?, ?)", (ad, tur, platform))
        self.conn.commit()

    # Değerlendirmeyi veritabanına ekler
    def insert_review_to_db(self, oyun_ad, oyuncu_adi, puan, yorum):
        self.cur.execute("SELECT id FROM Oyunlar WHERE ad=?", (oyun_ad,))
        oyun_id = self.cur.fetchone()[0]
        self.cur.execute("INSERT INTO Degerlendirmeler (oyun_id, oyuncu_adi, puan, yorum) VALUES (?, ?, ?, ?)", (oyun_id, oyuncu_adi, puan, yorum))
        self.conn.commit()

# Ana uygulama döngüsü.
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OyunArayuzu()
    window.show()
    sys.exit(app.exec_())
