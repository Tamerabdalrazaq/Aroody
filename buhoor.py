from gettext import find
from pip import main


class Tafaeela:
    def __init__(self, name, main_beat, variants) -> None:
        self.name = name
        self.main_beat = main_beat
        self.variants = variants

    def has_variant(self, variant):
        return variant in self.variants
    def __repr__(self) -> str:
        return self.name[::-1]
    def __eq__(self, __o: object) -> bool:
        assert type(__o) == Tafaeela
        return self.main_beat == __o.main_beat

faaolon = Tafaeela('فعولن', '11010', ['11010','1101', '1010', '101'])
faaolon_wafer = Tafaeela('فعولن الوافر', '11010', ['11010'])
mafaaelun = Tafaeela('مفاعيلن', '1101010', ['1101010', '110110', '110101', '101010', '11010'])
mustafaelun = Tafaeela('مستفعلن', '1010110', ['1010110', '110110', '101110', '101010'])
faaelun = Tafaeela('فاعلن', '10110', ['10110', '1110', '1010'])
mutafaaelun = Tafaeela('متفاعلن', '1110110', ['1110110', '1010110'])
mufaaalatun = Tafaeela('مفاعلتن', '1101110', ['1101110', '1101010', '110101', '110110', '101110', '101010', '10110'])
tafaeelat = [faaolon, mafaaelun, mustafaelun, faaelun, mutafaaelun, mufaaalatun]

class Bahr:
    def __init__(self, name, tafaaeel) -> None:
        self.name = name
        self.tafaeel = tafaaeel
    
    def __repr__(self) -> str:
        return self.name[::-1]
    
    def is_member(self, tafaaeel, partial=False):
        if len(tafaaeel) > len(self.tafaeel): return False
        for i in range(len(tafaaeel)):
            if tafaaeel[i] != self.tafaeel[i]: return False
        return partial or len(tafaaeel) == len(self.tafaeel)
    
taweel = Bahr('الطويل', (faaolon, mafaaelun,faaolon, mafaaelun))
baseet = Bahr('البسيط', (mustafaelun, faaelun,mustafaelun, faaelun))
kamel = Bahr('الكامل', (mutafaaelun,mutafaaelun,mutafaaelun))
wafer = Bahr('الوافر', (mufaaalatun,mufaaalatun,faaolon_wafer))

buhur = [taweel, baseet, kamel, wafer]

def find_tafeela(beats):
    compatiable = []
    for tafaeela in tafaeelat:
        if tafaeela.has_variant(beats):
            compatiable.append(tafaeela)
    return compatiable

def find_bahr(tafaaeel, partial = False):
    compatible = []
    for bahr in buhur:
        if bahr.is_member(tafaaeel, partial):
            compatible.append(bahr)
    return compatible

def get_composition(beats):
    compositions = []
    def rec(beats, sequence = []):
        if len(beats) == 0:
            buhur_res = find_bahr(sequence)
            if len(buhur_res) > 0: 
                compositions.append((sequence, buhur_res))
                return
        if len(beats) <= 2: return 
        n = len(beats)
        for i in range(3, min(8, n+1)):
            left, right = beats[:i], beats[i:]
            compatiable = find_tafeela(left)
            for comp in compatiable:    
                current_tafaaeel = sequence + [comp]
                if find_bahr(current_tafaaeel, partial=True):
                    rec(right, current_tafaaeel)
    rec(beats)
    return compositions
# print((get_composition('1101110110111011010')))
# print('hi')