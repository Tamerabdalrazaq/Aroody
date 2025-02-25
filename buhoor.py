TAFAEELAT = []
BUHOOR = []


class Tafaeela:
    def __init__(self, name, main_beat, variants) -> None:
        self.name = name
        self.main_beat = main_beat
        self.variants = variants

    def __contains__(self, variant):
        return variant in self.variants

    def __repr__(self) -> str:
        return self.name[::-1]

    def __eq__(self, __o: object) -> bool:
        assert type(__o) == Tafaeela
        return self.main_beat == __o.main_beat and self.name == __o.name


class Bahr:
    def __init__(self, name, tafaaeel) -> None:
        self.name = name
        self.tafaaeel = tafaaeel
        beats_str = ''
        for tafaeela in tafaaeel:
            beats_str += tafaeela.main_beat
        self.beats_str = beats_str
        self.length = len(beats_str)

    def __repr__(self) -> str:
        return self.name

    def is_member(self, tafaaeel, partial=False):
        if len(tafaaeel) > len(self.tafaaeel):
            return False
        for i in range(len(tafaaeel)):
            if tafaaeel[i] != self.tafaaeel[i]:
                return False
        return partial or len(tafaaeel) == len(self.tafaaeel)


faaolon = Tafaeela('فعولن', '11010', ['11010', '1101', '1010', '101', '110'])
faaolon_wafer = Tafaeela('فعولن الوافر', '11010', ['11010'])
mafaaelun = Tafaeela('مفاعيلن', '1101010', [
                     '1101010', '110110', '110101', '101010', '11010'])
mustafaelun = Tafaeela('مستفعلن', '1010110', [
                       '1010110', '110110', '101110', '101010'])
faaelun = Tafaeela('فاعلن', '10110', ['10110', '1110', '1010'])
mutafaaelun = Tafaeela('متفاعلن', '1110110', ['1110110', '1010110'])
mufaaalatun = Tafaeela('مفاعلتن', '1101110', [
                       '1101110', '1101010', '110101', '110110', '101110', '101010', '10110'])

TAFAEELAT.extend([faaolon, faaolon_wafer, mafaaelun, mustafaelun,
                  faaelun, mutafaaelun, mufaaalatun])

test = Bahr('test', (faaolon,))
taweel = Bahr('taweel', (faaolon, mafaaelun, faaolon, mafaaelun))
baseet = Bahr('baseet', (mustafaelun, faaelun, mustafaelun, faaelun))
kamel = Bahr('kamel', (mutafaaelun, mutafaaelun, mutafaaelun))
wafer = Bahr('wafer', (mufaaalatun, mufaaalatun, faaolon_wafer))
mutaqareb = Bahr('mutaqareb', (faaolon, faaolon, faaolon, faaolon))
rujz = Bahr('rujz', (mustafaelun, mustafaelun, mustafaelun))
hazaj = Bahr('hazaj', (mafaaelun, mafaaelun))
mutadarak = Bahr('mutadarak', (faaelun, faaelun, faaelun, faaelun))

# BUHOOR.extend([test])
BUHOOR.extend([taweel, baseet, kamel, wafer,
              rujz, hazaj, mutaqareb, mutadarak])
