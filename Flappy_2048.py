#!/usr/bin/python3

import sys
from time import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random
import math
import pickle


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette()
        p.setColor(QPalette.Window, QColor(253, 255, 53))


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.sound()
        self.initUI()
        self.loopMenu()


    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Space and self.demarre and not self.Gameover and not self.inMenu:
                self.animation()

            elif event.key() == Qt.Key_Space and not self.demarre and not self.Gameover and not self.inMenu:
                self.initUI()
                self.update()
                self.loopMenu()

            elif event.key() == Qt.Key_Space and not self.demarre and not self.Gameover and self.inMenu:
                self.wave()


    def initUI(self):
        self.setFixedSize(800, 1000)
        self.setWindowTitle('Flappy 2048')
        self.setWindowIcon(QIcon('./ressources/images/icon.png'))
        self.inMenu = True                     #Etat dans le menu
        self.setCenter()
        self.Etat = "Press Space to jump"
        self.Gameover = False                   #Etat game over
        self.score = 1
        self.copie_score = 1
        self.gravity = 0.006
        self.vitesse = 0
        self.pts = [[150, 300]]
        self.angle = 360.0
        self.demarre = False
        self.tubeposhaut = [1500, -500]
        self.tubeposbas = [1500, 450]
        self.bare = 0
        self.barre = QImage("./ressources/images/barre.png")
        self.listetube = [[-200, 750], [-300, 650], [-400, 550], [-500, 450], [-600, 350], [-700, 250]]
        self.show()
        self.cond_passage = False
        self.couleur = {
            2:QColor(238, 228, 218),
            4:QColor(192, 57, 43),
            8:QColor(231, 76, 60),
            16:QColor(155, 89, 182),
            32:QColor(142, 68, 173),
            64:QColor(41, 128, 185),
            128:QColor(52, 152, 219),
            256:QColor(26, 188, 156),
            512:QColor(22, 160, 133),
            1024:QColor(39, 174, 96),
            2048:QColor(46, 204, 113),
            4096:QColor(241, 196, 15),
            8192:QColor(243, 156, 18),
            16384:QColor(230, 126, 34),
            32768:QColor(211, 84, 0),
            65536:QColor(52, 73, 94),
            131072:QColor(44, 62, 80)}
        self.tubscore = []
        for i in range(0, 10):
            condition = True
            while condition:
                nbr_aleatoire = random.randint(1, 12)
                if nbr_aleatoire not in self.tubscore and nbr_aleatoire != 1:
                    self.tubscore.append(nbr_aleatoire)
                    condition = False



    def paintEvent(self, event):
        painter = QPainter(self)
        pts = self.pts[:]
        painter.setRenderHint(QPainter.Antialiasing)
        self.rect = QRect(pts[0][0], pts[0][1], 100, 100)
        self.goal = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+800, 150, 150)

        self.tub1 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+500, 150, 150)
        self.tub2 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+650, 150, 150)
        self.tub3 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+950, 150, 150)
        self.tub4 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+350, 150, 150)
        self.tub5 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+1100, 150, 150)
        self.tub6 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+1250, 150, 150)
        self.tub7 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+1400, 150, 150)
        self.tub8 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+1550, 150, 150)
        self.tub9 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+350, 150, 150)
        self.tub10 = QRect(self.tubeposhaut[0], self.tubeposhaut[1]+200, 150, 150)

        self.tub = [self.tub1, self.tub2, self.tub3, self.tub4, self.tub5, self.tub6, self.tub7, self.tub8, self.tub9, self.tub10]

        self.goaladapter = QRect(self.tubeposhaut[0]-35, self.tubeposhaut[1]+825, 30, 110)

        self.tube1 = QRect(self.tubeposhaut[0], self.tubeposhaut[1], 150, 800)
        self.tube = QRect(self.tubeposbas[0], self.tubeposbas[1], 150, 800)
        center = self.rect.center()

        pen = QPen()
        pen.setBrush(QColor(100, 100, 100))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(8)
        painter.setPen(pen)
        font = QFont("Arial", 23, QFont.Bold)
        painter.setFont(font)


        ###Dessin des cubes autour de l'objectif
        for i in range(0, 10):
            self.taillepen = 23
            if len(str(2**self.tubscore[i])) > 5:
                self.taillepen = 20
            if len(str(2**self.tubscore[i])) > 7:
                self.taillepen = 17
            painter.setFont(QFont("Arial", self.taillepen, QFont.Bold))

            if 2**self.tubscore[i] <= 131072:
                for j in self.couleur:
                    if 2**self.tubscore[i] == j:
                        pickcouleur = self.couleur[j]
            else:
                pickcouleur = QColor(59, 59, 51)
            painter.setBrush(QBrush(pickcouleur))
            painter.drawRects(self.tub[i])
            if 2**self.tubscore[i] > 2:
                painter.setPen(QPen(QColor(255, 250, 250)))
            painter.drawText(self.tub[i], Qt.AlignCenter, str(2**self.tubscore[i]))
            painter.setPen(pen)
            painter.setFont(font)


        painter.setPen(pen)
        ###Dessin du cube objectif
        self.taillepen = 23
        if len(str(2**self.copie_score)) > 6:
            self.taillepen = 20
        if len(str(2**self.copie_score)) > 9:
            self.taillepen = 15
        painter.setFont(QFont("Arial", self.taillepen, QFont.Bold))
        if 2**self.copie_score <= 131072:
            for i in self.couleur:
                if 2**self.copie_score == i:
                    pickcouleur = self.couleur[i]
        else:
            pickcouleur = QColor(59, 59, 51)
        painter.setBrush(QBrush(pickcouleur))
        if not self.cond_passage:
            painter.drawRect(self.goal)
            if 2**self.copie_score > 2:
                pen.setBrush(QColor(255, 250, 250))
                painter.setPen(pen)

            painter.drawText(self.goal, Qt.AlignCenter, str(2**self.copie_score))


        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        ### Reglages taille police du score
        self.taillepen = 20
        if len(str(2**self.score)) >= 5:
            self.taillepen = 18
        if len(str(2**self.score)) >= 8:
            self.taillepen = 15
        if len(str(2**self.score)) >= 9:
            self.taillepen = 13
        font = QFont("Arial", self.taillepen, QFont.Bold)
        painter.setFont(font)


        ###Dessin du cube volant
        painter.translate(center.x(), center.y())
        painter.rotate(self.angle)
        painter.translate(-center.x(), -center.y())
        pen.setBrush(QColor(100, 100, 100))
        painter.setPen(pen)

        if 2**self.score <= 131072:
            for i in self.couleur:
                if 2**self.score == i:
                    pickcouleur = self.couleur[i]
        else:
            pickcouleur = QColor(59, 59, 51)
        painter.setBrush(QBrush(pickcouleur))
        painter.drawRect(self.rect)

        if 2**self.score > 2:
            painter.setPen(QPen(QColor(255, 250, 250)))

        painter.drawText(self.rect, Qt.AlignCenter, str(2**self.score))
        painter.end()


        ### Dessin menu
        peinteur = QPainter(self)
        if not self.demarre:
            peinteur.setBrush(QBrush(QColor(250, 250, 250, 170)))
            stylo = QPen()
            stylo.setBrush(QColor(100, 100, 100))
            peinteur.setPen(stylo)
            font = QFont("Arial", 35, QFont.Bold)
            peinteur.setFont(font)
            self.getBestScore()

            if self.Etat == "Game Over":
                peinteur.drawImage(0, 960, self.barre)
                peinteur.drawRect(0, 0, 800, 1080)
                peinteur.drawText(250, 500, self.Etat)
                self.setBestScore()

            if self.Etat == "Press Space to jump":
                peinteur.setFont(QFont("Arial", 20, QFont.Bold))
                peinteur.drawText(10, 950, "Best score : "+str(("{:,}".format(2**self.score_recup).replace(",", " "))))
                peinteur.setFont(QFont("Arial", 35, QFont.Bold))
                peinteur.drawText(150, 730, self.Etat)
                peinteur.drawImage(0, 960, self.barre)

        else:
            peinteur.drawImage(self.bare, 960, self.barre)
            peinteur.drawImage(self.bare+1004, 960, self.barre)
        peinteur.end()
        self.show()


    def loopMenu(self):
        i = 0
        while self.inMenu:
            self.pts[0][1] += math.cos(i)*4
            self.update()
            QApplication.processEvents()
            sleep(0.01)
            i += 0.03


    def closeEvent(self, event):
        sys.exit()


    def sound(self):
        self.luft = QSound("./ressources/sons/99_Luftballons.wav")
        self.flap = QSound("./ressources/sons/flap.wav")
        self.coin = QSound("./ressources/sons/coin.wav")
        self.punch = QSound("./ressources/sons/punch.wav")
        self.luft.play()
        self.luft.setLoops(QSound.Infinite)


    def wave(self):
        self.demarre = True
        self.Etat = " "
        self.inMenu = False
        for point in self.pts:
            while point[1] < 860 and not (self.rect).intersects(self.tube1) and not (self.rect).intersects(self.tube) and point[1] > -200:

                if (self.rect).intersects(self.goaladapter):
                    a, yp1, b, c = QRect.getCoords(self.goaladapter)
                    point[1] = yp1

                if (self.rect).intersects(self.goal):
                    self.vitesse = 0
                    self.angle = 360.0
                    self.tubeposhaut[0] -= 1.3
                    self.tubeposbas[0] -= 1.3
                    self.bare -= 1.3
                    sleep(0.004)

                collision = (self.rect).intersected(self.goal)

                x, a, b, c = QRect.getCoords(collision)

                if b == 216:
                    self.score += 1
                    self.cond_passage = True
                    self.coin.play()

                self.vitesse += self.gravity
                point[1] += self.vitesse
                self.looptube()
                self.loopbarre()
                self.tubeposhaut[0] -= 1
                self.tubeposbas[0] -= 1
                self.bare -= 1
                if self.angle < 400.0:
                    self.angle += 0.15

                self.update()
                QApplication.processEvents()
                sleep(0.00001)

            self.demarre = False
            self.colisiontube()
            self.punch.play()
            self.Etat = "Game Over"

            self.update()
            QApplication.processEvents()


    def loopbarre(self):
        if self.bare < -1004:
            self.bare = 0


    def looptube(self):
        if self.tubeposhaut[0] < -205:
            self.cond_passage = False
            self.listetube
            self.r = random.randint(0, 5)
            self.tubeposbas[1] = self.listetube[self.r][1]
            self.tubeposhaut[1] = self.listetube[self.r][0]
            self.tubeposbas[0] = 800
            self.tubeposhaut[0] = 800
            self.copie_score = self.score
            if self.score < 6:
                for i in range(0, 10):
                    condition = True
                    while condition:
                        nbrandom = random.randint(1, 12)
                        if nbrandom not in self.tubscore and nbrandom != self.score:
                            self.tubscore[i] = nbrandom
                            condition = False
            else:
                for i in range(0, 10):
                    condition = True
                    while condition:
                        nbrandom = random.randint(self.score-5, self.score+6)
                        if nbrandom not in self.tubscore and nbrandom != self.score:
                            self.tubscore[i] = nbrandom
                            condition = False


    def colisiontube(self):
        self.Gameover = True
        self.Etat = "Game Over"
        if (self.rect).intersects(self.tube1) or (self.rect).intersects(self.tube):
            self.pts[0][0] -= 5
            while self.pts[0][1] < 860:
                self.vitesse += self.gravity
                self.pts[0][1] += self.vitesse*3
                self.update()
                QApplication.processEvents()
                sleep(0.00002)
        self.Gameover = False


    def animation(self):
        self.vitesse = -1.3
        while self.angle > 325:
            self.angle -= 0.35
            self.update()
        self.flap.play()


    def getBestScore(self):
        try:
            with open("./ressources/score", "rb") as fichier:
                self.score_recup = pickle.load(fichier)
        except:
            with open("./ressources/score", "wb") as fichier:
                pickle.dump(0, fichier)

        with open("./ressources/score", "rb") as fichier:
            self.score_recup = pickle.load(fichier)


    def setBestScore(self):
        if 2**self.score > 2**self.score_recup:
            with open("./ressources/score", "wb") as fichier:
                pickle.dump(self.score, fichier)


    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = Application(sys.argv)
win = Window()
sys.exit(app.exec_())
