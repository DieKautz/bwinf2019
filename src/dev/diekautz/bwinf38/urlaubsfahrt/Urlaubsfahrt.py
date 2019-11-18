#!/usr/bin/python3
# ---------------------------------------------------------------------------------------------------------------------
# Filename: Urlaubsfahrt.py
# Autor: Anh Dang
# Version: 1.6
# Letztes Mal geöffnet/veraendert: 15.11.2019
# Funktion:
#    Dieses Programm versucht das Auto zum Ziel zu bringen.
#    Dabei versucht es außerdem an so wenigen Tankstellen wie möglich zu halten.
#    Gleichzeitig versucht die Familie so wenig zu zahlen wie möglich.
# ---------------------------------------------------------------------------------------------------------------------
import sys
import numpy as np


class FamilienAuto:
    # 1: Volumen des Tankes
    # 2: Wie viel Liter der Tank bisher hat
    # 3: Die Länge der Strecke, um ans Ziel zu kommen
    # 4: Verbrauch (in L) pro 100km
    # 5: Wie weit man bisher gefahren ist.
    tankV, tank, zielStrecke, verbrauch, gefahreneStrecke = [0 for i in range(5)]

    # die einzelnen Tankstellen mit ihrer Distanz und Preis an denen das Auto getankt hat
    tankstellen = 0  # type: np.ndarray

    # Hier wird die Adresse Distanz der Tankstelle gespeichert, wo man getankt hat, sowie die Menge
    anTankstellenGetankt = []

    def __init__(self, pfade: list):
        # "Platzhalter"
        print()

        for eingabe in pfade:
            # zuerst werden alle Informationen gespeichert
            self.saveData(eingabe)

            # ########## Berechnung start! ##########
            intervall = self.prepare()

            self.selectStation(intervall)

            self.compute()

            self.getDriveInfo(dateiname=eingabe)

    def saveData(self, input):
        """
        Alle Attribute werden geupdatet und bekommen ihren richtigen Wert zugewiesen.
        Außerdem werden auch noch zusätzlich alle Tankstellen gespeichert.
        SPEZIELL:
        Sollte der Benutzer den Pfad zur Datei angegeben haben!
        """
        try:
            datei = open(input, "r")
        except TypeError:
            # Es wurde Std.in verwendet
            datei = input

        # ---------- Daten über das Auto ----------
        self.verbrauch = int(next(datei).rstrip())
        self.tankV = int(next(datei).rstrip())
        self.tank = int(next(datei).rstrip())
        self.zielStrecke = int(next(datei).rstrip())
        anzahlTankstellen = int(next(datei).rstrip())

        # ----- Tankstellenpreis und Tankstellendistanz werden gespeichert -----
        self.tankstellen = np.zeros((anzahlTankstellen, 2), dtype=int)

        index, dateiInhalt = 0, datei.readlines()

        while index < anzahlTankstellen:
            # Die Infos über eine Tankstelle werden gespeichert
            # 1. Index = Distanz
            # 2. Index = Preis
            self.tankstellen[index], index = dateiInhalt[index].split(), index + 1

        # Die Tankstellen sind nicht nach ihrer Distanz sortiert => Muss noch gemacht werden
        self.tankstellen = self.tankstellen[self.tankstellen[:, 0].argsort()]

        datei.close()

    # ---------- Berechnung der Tankstellen-Aufteilung ----------
    def compute(self):
        """
        Hier wird nun die Literanzahl an der jewiligen Tankstelle hinzugefügt, die man
        an dieser Tankstelle getankt hat.
        Es wird dabei berechnet, wie viel er dazugetankt hat, wie viel er davon verbraucht hat und wie viel am Ende
        noch übrig geblieben ist.
        Wenn er beispielsweise für das erste Intervall 5L verbraucht hat, aber mit 10l losgefahren ist, dann
        hat er noch 5L übrig, die noch für die nächste Fahrt miteinberechnet werden.
        """
        tankstellenIndex = 0

        # Fährt gerade los
        verbrauch = self.anTankstellenGetankt[0][0] * self.verbrauch / 100
        self.tank -= verbrauch

        for vordereTankstelle in self.anTankstellenGetankt[1:]:
            vordereTankstelle, hintereTanktselle = vordereTankstelle[0], self.anTankstellenGetankt[tankstellenIndex][0]

            # ----- Tank -----
            # die Menge, die man noch tanken muss, um zur nächsten Tankstelle zu kommen
            dazutanken = (((vordereTankstelle - hintereTanktselle) * self.verbrauch) / 100) - self.tank

            # der gesamte Verbrauch, um zur nächsten Tankstelle zu kommen
            verbrauch = ((vordereTankstelle - hintereTanktselle) * self.verbrauch / 100)

            self.tank += dazutanken - verbrauch

            # Informationen speichern
            self.anTankstellenGetankt[tankstellenIndex].append(dazutanken)

            tankstellenIndex += 1

    def selectStation(self, intervall: list):
        """
        Diese Methode schaut nach, was die billigste Tankstelle ist und welche Tankstelle das beste Verhältnis
        zwischen Fahrdistanz und Preis hergibt.
        Am Ende wird geguckt, welche Tankstelle weiter weg ist.
        Beispiel:
            Die günstigste Tankstelle ist bei der Distanz 400km, während die Tankstelle mit dem bestem Verhältnis bei
            500km liegt. Logischerweise nimmt man daraufhin die 500 km, um noch beim nächstem Intervall
            genügend Tankstellen zur Auswahl zu haben.
            Ansonsten könnte es sein, dass man schon beim zweitem Intervall am der unteren Intervallgrenze ist,
            sodass man nur noch die "unterste" Tankstelle nehmen muss, auch wenn sie die Teuerste ist!
        """
        # 1. Zeigt den Bereich, in dem das Auto tanken darf
        # 3. Speichert die Distanz von einer Tankstellen zu anderen ab.
        interVallIndex, letzteDistanz, angepassteDistanz = 0, 0, []
        while self.gefahreneStrecke < self.zielStrecke:
            untereIntervallGrenze, obereIntervallGrenze = intervall[interVallIndex: interVallIndex + 1][0]

            # Kann das Auto schon zum Ziel?
            if untereIntervallGrenze == "Ziel":
                self.anTankstellenGetankt.append([self.zielStrecke, 0])
                return 0

            # Bedingung wegen: Falls die nächste obere Grenze das Ziel wäre
            # alle Tankstellen in diesem Bereich
            tankstellenImIntervall = self.tankstellen[(self.tankstellen[:, 0] >= untereIntervallGrenze) &
                                                      (self.tankstellen[:, 0] <= obereIntervallGrenze) &
                                                      (self.tankstellen[:, 0] <=
                                                       self.gefahreneStrecke + self.tankV / self.verbrauch * 100)]

            # ----- Verhältnis von jeder Tankstelle -----
            for distanz in tankstellenImIntervall[0]:
                angepassteDistanz.append(distanz - letzteDistanz)
                letzteDistanz = distanz
            verhaeltnis = np.divide(tankstellenImIntervall[:, 0], tankstellenImIntervall[:, 1])

            bestesVerhaeltnis = tankstellenImIntervall[
                verhaeltnis[:] == np.min(verhaeltnis)
                ]

            angepassteDistanz.clear()
            # ----- Billigste Tankstelle -----
            billigste = tankstellenImIntervall[
                tankstellenImIntervall[:, 1] == np.min(tankstellenImIntervall[:, 1])
                ]

            # Die billigste Tankstelle ist weiter hinten
            if billigste[0][0] >= bestesVerhaeltnis[0][0]:
                self.gefahreneStrecke = billigste[0][0]
                self.anTankstellenGetankt.append([billigste[0][0]])

            else:
                self.gefahreneStrecke = bestesVerhaeltnis[0][0]
                self.anTankstellenGetankt.append([bestesVerhaeltnis[0][0]])

            interVallIndex += 1

    def prepare(self) -> list:
        """
        Hier wird berechnet, an wie vielen Tankstellen das Auto maximal
        halten darf.
        Dafür werden Intervalle gebildert. Jedes dieser Intervalle speichert den Bereich von Tankstellen,
        die betankt werden dürfen, weil sie rechnerisch somit zur geringsten Tank-Anzahl kommen wird.
        Beispiel:
        [[100, 200], [300, 400]]
        Was man herauslesen kann:
            1. Das Auto darf maximal 2 Mal tanken, weil es nur 2 Intervalle gibt!
               => Hat so wenig getankt wie möglich.
            2. Das Auto darf nur eine Tankstelle in diesem jeweiligem Bereich tanken!
               => Also einmal eine Tankstelle zwischen 100km - 200km und zwischen 300km - 400km.
        :returns: Gibt in einer Liste alle Intervalle aus
        """

        # anzahlMaxTankstellen: Anzahl der Tankstellen, an denen das Auto tanken darf
        # distanz: Der Weg, der das Auto gefahren ist, wenn er immer die "letzte" Tankstelle nimmt.
        # intervall: Alle Intervalle.
        anzahlMaxTankstellen, distanz, intervall = 1, 0, []

        # niedrigste Start-Tankstelle (für minIntervall)
        naechsteUntersteTankstelle = self.zielStrecke
        while naechsteUntersteTankstelle >= self.tank / self.verbrauch * 100:
            naechsteUntersteTankstelle -= self.tankV / self.verbrauch * 100
            naechsteUntersteTankstelle = self.tankstellen[self.tankstellen[:, 0] >= naechsteUntersteTankstelle][0][0]

        # Von Start bis zur "letzten" Tankstelle (für maxIntervall)
        distanz = (self.tank / self.verbrauch) * 100

        intervall_index = 0
        while naechsteUntersteTankstelle < self.zielStrecke:
            # nächstes Intervall
            intervall.append([])

            # ------- Min-Intervall -------
            naechsteUntersteTankstelle = self.tankstellen[self.tankstellen[:, 0] <= naechsteUntersteTankstelle][-1][0]
            intervall[intervall_index].append(naechsteUntersteTankstelle)

            # ------- Max-Intervall -------
            # distanz der letzten Tankstelle berechnen, die das Auto mit seinem jetzigem Tank
            # erreichen kann
            distanz = self.tankstellen[self.tankstellen[:, 0] <= distanz, 0][-1]
            intervall[intervall_index].append(distanz)

            # Annahme: Es wird vollgetankt => Nächste weitentfernteste Tankstelle
            distanz += (self.tankV / self.verbrauch) * 100
            naechsteUntersteTankstelle += (self.tankV / self.verbrauch) * 100

            # Naechste Daten ins nächste Intervall
            intervall_index += 1

        intervall.append(["Ziel", self.zielStrecke])
        return intervall

    def getDriveInfo(self, dateiname: str):
        """
        Das Ergebnis wird nun Anhand einer Tabelle angezeigt, sodass man nachvollziehen kann,
        wo und wieviel man getankt hat, als auch wie viel man für die Fahrt gezahlt hat.
        """
        platzhalter = max([len(str(tankstelle[0])) for tankstelle in self.anTankstellenGetankt]) + 1
        gesamtGetankt = round(sum([i[1] for i in self.anTankstellenGetankt]), 3)
        gesamtBezahlt = round(
            sum(
                [
                    self.tankstellen[
                        self.tankstellen[:, 0] == tankstelle[0]
                        ]
                    [0][1] * tankstelle[1] for tankstelle in self.anTankstellenGetankt[:-1]
                ]
            ) / 100, 3
        )
        print("-" * 25 + f" {dateiname} " + "-" * 25, end="\n")
        print("     Tankstelle (in km)     Getankt (in Liter)     Preis (in €)", end="\n\n")

        vorlage = """         %.0fkm          |      %.3fL        |      %.2f€"""
        platzhalter += round(platzhalter / 2)
        for tankstelle in self.anTankstellenGetankt[: -1]:
            preisAnTankstelle, tankstellenDistanz, dazugetankt = self.tankstellen[
                                                                     self.tankstellen[:, 0] == tankstelle[0]
                                                                     ][0][1], \
                                                                 tankstelle[0], \
                                                                 tankstelle[1]
            print((vorlage % (tankstelle[0], dazugetankt, dazugetankt * preisAnTankstelle / 100)).replace(".", ","))
        print(f"\nInsgesamt getankt: {gesamtGetankt}L")
        print(f"Anzahl der durchgeführten Tankstopps: {len(self.anTankstellenGetankt[:-1])}")
        print(f"Insgesamt Bezahlt: {gesamtBezahlt}€", end="\n\n")

        # Attribute werden für die nächste Datei geleert
        self.anTankstellenGetankt.clear()
        self.gefahreneStrecke = 0


if __name__ == '__main__':
    vorlage = """Aufruf dieses Programmes:
      1) Datei als stdin übergeben:
          python3 Urlaubsfahrt.py < Datei.txt)
Oder: 2) Argumente hinzufügen:
          python3 Urlaubsfahrt.py [Pfad1, Pfad2, ...]                                        
"""
    pfade = []

    # Std.in verwendet oder nicht?
    if len(sys.argv) > 1:

        if ("-h" in sys.argv) or ("--help" in sys.argv):
            print(vorlage)
            sys.exit(0)

        [pfade.append(pfad) for pfad in sys.argv[1:] if pfad.endswith(".txt")]

        # Hat der User vergessen, die Pfade hinzuschreiben?
        if len(pfade) == 0:
            sys.exit("Eeeehm.... ich glaube, sie haben die Pfade vergessen hinzuschreiben...")

        FamilienAuto(pfade)

    else:
        FamilienAuto(sys.stdin)
