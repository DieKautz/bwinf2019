import sys
import numpy as np


class Auto:

    tankV, tank, ziel, verbrauch, Strecke = [0 for i in range(5)]


    tankstellen = 0 


    getankt = []

    def __init__(self, pfade: list):

        print()

        for eingabe in pfade:

            self.saveData(eingabe)


            intervall = self.prepare()

            self.Stationwählen(intervall)

            self.compute()

            self.getDriveInfo(dateiname=eingabe)

    def saveData(self, input):

        try:
            datei = open(input, "r")
        except TypeError:

            datei = input


        self.verbrauch = int(next(datei).rstrip())
        self.tankV = int(next(datei).rstrip())
        self.tank = int(next(datei).rstrip())
        self.ziel = int(next(datei).rstrip())
        anzahlTankstellen = int(next(datei).rstrip())


        self.tankstellen = np.zeros((anzahlTankstellen, 2), dtype=int)

        index, dateiInhalt = 0, datei.readlines()

        while index < anzahlTankstellen:

            self.tankstellen[index], index = dateiInhalt[index].split(), index + 1


        self.tankstellen = self.tankstellen[self.tankstellen[:, 0].argsort()]

        datei.close()


    def compute(self):

        tankstellenIndex = 0


        verbrauch = self.getankt[0][0] * self.verbrauch / 100
        self.tank -= verbrauch

        for vordereTankstelle in self.getankt[1:]:
            vordereTankstelle, hintereTanktselle = vordereTankstelle[0], self.getankt[tankstellenIndex][0]


            dazutanken = (((vordereTankstelle - hintereTanktselle) * self.verbrauch) / 100) - self.tank

            # der gesamte Verbrauch, um zur nächsten Tankstelle zu kommen
            verbrauch = ((vordereTankstelle - hintereTanktselle) * self.verbrauch / 100)

            self.tank += dazutanken - verbrauch

            # Informationen speichern
            self.getankt[tankstellenIndex].append(dazutanken)

            tankstellenIndex += 1

    def Stationwählen(self, intervall: list):

        interVallIndex, letzteDistanz, angepassteDistanz = 0, 0, []
        while self.Strecke < self.ziel:
            unterGrenze, obereGrenze = intervall[interVallIndex: interVallIndex + 1][0]


            if unterGrenze == "Ziel":
                self.getankt.append([self.ziel, 0])
                return 0


            tankInt = self.tankstellen[(self.tankstellen[:, 0] >= unterGrenze) &
                                                      (self.tankstellen[:, 0] <= obereGrenze) &
                                                      (self.tankstellen[:, 0] <=
                                                       self.Strecke + self.tankV / self.verbrauch * 100)]


            for distanz in tankInt[0]:
                angepassteDistanz.append(distanz - letzteDistanz)
                letzteDistanz = distanz
            verhaeltnis = np.divide(tankInt[:, 0], tankInt[:, 1])

            bestesVerhaeltnis = tankInt[
                verhaeltnis[:] == np.min(verhaeltnis)
                ]

            angepassteDistanz.clear()

            billigste = tankInt[
                tankInt[:, 1] == np.min(tankInt[:, 1])
                ]

            # Die billigste Tankstelle ist weiter hinten
            if billigste[0][0] >= bestesVerhaeltnis[0][0]:
                self.Strecke = billigste[0][0]
                self.getankt.append([billigste[0][0]])

            else:
                self.Strecke = bestesVerhaeltnis[0][0]
                self.getankt.append([bestesVerhaeltnis[0][0]])

            interVallIndex += 1

    def prepare(self) -> list:

        anzahlMaxTankstellen, distanz, intervall = 1, 0, []


        naechsteUntersteTankstelle = self.ziel
        while naechsteUntersteTankstelle >= self.tank / self.verbrauch * 100:
            naechsteUntersteTankstelle -= self.tankV / self.verbrauch * 100
            naechsteUntersteTankstelle = self.tankstellen[self.tankstellen[:, 0] >= naechsteUntersteTankstelle][0][0]


        distanz = (self.tank / self.verbrauch) * 100

        intervall_index = 0
        while naechsteUntersteTankstelle < self.ziel:

            intervall.append([])


            naechsteUntersteTankstelle = self.tankstellen[self.tankstellen[:, 0] <= naechsteUntersteTankstelle][-1][0]
            intervall[intervall_index].append(naechsteUntersteTankstelle)


            distanz = self.tankstellen[self.tankstellen[:, 0] <= distanz, 0][-1]
            intervall[intervall_index].append(distanz)


            distanz += (self.tankV / self.verbrauch) * 100
            naechsteUntersteTankstelle += (self.tankV / self.verbrauch) * 100


            intervall_index += 1

        intervall.append(["Ziel", self.ziel])
        return intervall

    def getDriveInfo(self, dateiname: str):

        platzhalter = max([len(str(tankstelle[0])) for tankstelle in self.getankt]) + 1
        gesamtGetankt = round(sum([i[1] for i in self.getankt]), 3)
        gesamtBezahlt = round(
            sum(
                [
                    self.tankstellen[
                        self.tankstellen[:, 0] == tankstelle[0]
                        ]
                    [0][1] * tankstelle[1] for tankstelle in self.getankt[:-1]
                ]
            ) / 100, 3
        )
        print("-" * 25 + f" {dateiname} " + "-" * 25, end="\n")
        print("     Tankstelle (in km)     Getankt (in Liter)     Preis (in €)", end="\n\n")

        vorlage = """         %.0fkm    %.3fl    %.2f€"""
        platzhalter += round(platzhalter / 2)
        for tankstelle in self.getankt[: -1]:
            preisAnTankstelle, tankstellenDistanz, dazugetankt = self.tankstellen[
                                                                     self.tankstellen[:, 0] == tankstelle[0]
                                                                     ][0][1], \
                                                                 tankstelle[0], \
                                                                 tankstelle[1]
            print((vorlage % (tankstelle[0], dazugetankt, dazugetankt * preisAnTankstelle / 100)).replace(".", ","))
        print(f"\nInsgesamt getankt: {gesamtGetankt}L")
        print(f"Anzahl der durchgeführten Tankstopps: {len(self.getankt[:-1])}")
        print(f"Insgesamt Bezahlt: {gesamtBezahlt}€", end="\n\n")


        self.getankt.clear()
        self.Strecke = 0



pfade = ['fahrt1.txt','fahrt2.txt','fahrt3.txt','fahrt4.txt','fahrt5.txt']
Auto(pfade)