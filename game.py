from random import SystemRandom

alle_tegels = range(21, 37)
aantal_dobbelstenen = 8
rnd = SystemRandom()
worm_dobbel = 0
worm_punten = 5

def gooi_dobbelstenen(aantal):
    return [rnd.randrange(0, 6) for _ in range(aantal)]

def tegel_wormen(tegel_waarde):
    return (tegel_waarde - 17) // 4

def aantal_punten(waarde):
    if waarde == worm_dobbel:
        return worm_punten
    return waarde

class Beurt:
    def __init__(self):
        self.gepakt = []
        self.punten = 0
        self.dobbelstenen = aantal_dobbelstenen

    def gooi(self):
        self.worp = gooi_dobbelstenen(self.dobbelstenen)
        return self.worp

    def pak_stenen(self, waarde):
        assert waarde in self.worp
        assert waarde not in self.gepakt

        aantal = self.worp.count(waarde)
        self.gepakt += [waarde] * aantal
        self.punten += aantal * aantal_punten(waarde)
        self.dobbelstenen -= aantal

    def te_pakken_stenen(self):
        return set(self.worp) - set(self.gepakt)

    def gepakte_punten(self):
        return sum(self.gepakt) + worm_punten * self.gepakt.count(worm_dobbel)

    def kan_stenen_pakken(self):
        te_pakken = self.te_pakken_stenen()
        return len(te_pakken) > 0

    def kan_tegel_pakken(self, tegel):
        return worm_dobbel in self.gepakt and self.gepakte_punten() >= tegel

class Spel:
    def __init__(self, spelers):
        self.tegels = set(alle_tegels)
        self.spelers = spelers

    def pak_tegel(self, tegel):
        assert tegel in self.tegels
        self.tegels.remove(tegel)

    def speel(self):
        # Puntentelling
        self.speel_alle_tegels()

    def speel_alle_tegels(self):
        while self.tegels:
            for speler in self.spelers:
                print(speler, "aan de beurt")
                print("Tegels:", self.tegels)
                beurt = Beurt()
                while True:
                    worp = beurt.gooi()
                    print("Worp:", worp)

                    if not beurt.kan_stenen_pakken():
                        print("Mislukt")
                        tegel = speler.lever_tegel_in()
                        if tegel:
                            self.tegels.add(tegel)
                        self.tegels.remove(max(self.tegels))
                        break

                    actie = speler.beslis(beurt, self.tegels)
                    print("Actie:", actie)
                    if actie > 20:
                        assert beurt.kan_tegel_pakken(actie)
                        self.pak_tegel(actie)
                        speler.ontvang_tegel(actie)
                        break
                    else:
                        beurt.pak_stenen(actie)
                        print("Gepakt:", beurt.gepakt)
                        print("Punten:", beurt.gepakte_punten())

                if not self.tegels:
                    return


class Speler:
    def __init__(self):
        self.tegels = []

    def beslis(self, beurt, tegels):
        for tegel in tegels:
            if beurt.kan_tegel_pakken(tegel):
                return tegel

        te_pakken = beurt.te_pakken_stenen()
        if worm_dobbel in te_pakken and beurt.worp.count(worm_dobbel) >= 2:
            return worm_dobbel
        if 5 in te_pakken and beurt.worp.count(5) >= 2:
            return 5

        return max(te_pakken)

    def ontvang_tegel(self, tegel):
        self.tegels.append(tegel)

    def lever_tegel_in(self):
        if self.tegels:
            return self.tegels.pop()
        else:
            return None

    def tegel_wormen(self):
        return sum([tegel_wormen(t) for t in self.tegels])

    def __repr__(self):
        return "Speler %d, %d punten" % (id(self), self.tegel_wormen())

if __name__ == "__main__":
    spelers = [Speler(), Speler(), Speler()]
    spel = Spel(spelers)
    spel.speel()
    print(spelers)
