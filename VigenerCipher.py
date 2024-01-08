class VigenersCipher:
    def __init__(self, klucz):
        self.klucz = klucz.upper()
        self.polski_alfabet = (
            "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ" + "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
        )

    def indeks_polski(self, znak):
        return self.polski_alfabet.index(znak)

    def szyfruj(self, tekst):
        zaszyfrowany_tekst = ""
        klucz_index = 0

        for znak in tekst:
            if znak in self.polski_alfabet:
                offset = (
                    self.indeks_polski(znak)
                    + self.indeks_polski(self.klucz[klucz_index])
                ) % len(self.polski_alfabet)
                zaszyfrowany_tekst += self.polski_alfabet[offset]

                klucz_index = (klucz_index + 1) % len(self.klucz)
            else:
                zaszyfrowany_tekst += znak

        return zaszyfrowany_tekst

    def deszyfruj(self, zaszyfrowany_tekst):
        tekst = ""
        klucz_index = 0

        for znak in zaszyfrowany_tekst:
            if znak in self.polski_alfabet:
                offset = (
                    self.indeks_polski(znak)
                    - self.indeks_polski(self.klucz[klucz_index])
                    + len(self.polski_alfabet)
                ) % len(self.polski_alfabet)
                tekst += self.polski_alfabet[offset]

                klucz_index = (klucz_index + 1) % len(self.klucz)
            else:
                tekst += znak

        return tekst
