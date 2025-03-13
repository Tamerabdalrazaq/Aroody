import math
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
        return self.name

    def __eq__(self, __o: object) -> bool:
        assert type(__o) == Tafaeela
        return self.main_beat == __o.main_beat and self.name == __o.name


class Bahr:
    # zehaf_punishment points reduced for Hathf, Qalb, Zeyada
    # allowed_zehaf_beat to be 0,1 or 2 (both) or -1 (none) in Hathf, Qalb, Zeyada
    def __init__(self, name, tafaaeel, zehaf_punishment = (1, 4, 4), allowed_zehaf_beat = (2,2,2)):
        self.name = name
        self.tafaaeel = tafaaeel
        beats_str = ''
        for tafaeela in tafaaeel:
            beats_str += tafaeela.main_beat
        self.beats_str = beats_str
        self.length = len(beats_str)
        self.zehaf_punishment = zehaf_punishment
        self.allowed_zehaf_beat = allowed_zehaf_beat

    def __repr__(self) -> str:
        return self.name

    def is_member(self, tafaaeel, partial=False):
        if len(tafaaeel) > len(self.tafaaeel):
            return False
        for i in range(len(tafaaeel)):
            if tafaaeel[i] != self.tafaaeel[i]:
                return False
        return partial or len(tafaaeel) == len(self.tafaaeel)
    
    # Get the punishment scored based on wheter the current Bahr allows the zehaf with this beat
    #  and the total number of zehafat thus far. (increase as more zehafat are commited) 
    def get_zehaf_punishment(self, zehaf, beat, zehafat_count):
        if self.allowed_zehaf_beat[zehaf] in [beat, 2]:
            punishment = 1*(self.zehaf_punishment[zehaf])
        else:
            punishment = 2*(self.zehaf_punishment[zehaf])
        return  punishment + zehafat_count*0.5


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
faaelatun = Tafaeela('فاعلاتن', '1011010', ['1011010', '111010', '101101', '11101'])
mafaulatu = Tafaeela('مفعولات', '1010101', ['1010101', '101101', '11101'])


TAFAEELAT.extend([faaolon, faaolon_wafer, mafaaelun, mustafaelun,
                  faaelun, mutafaaelun, mufaaalatun])

# taweel = Bahr('taweel', (faaolon, mafaaelun, faaolon, mafaaelun), (1, 3, 3), (0, -1, -1))
taweel = Bahr('الطويل', (faaolon, mafaaelun, faaolon, mafaaelun))
baseet = Bahr('البسيط', (mustafaelun, faaelun, mustafaelun, faaelun))
madeed = Bahr('المديد', (faaelatun, faaelun, faaelatun))
# kamel = Bahr('kamel', (mutafaaelun, mutafaaelun, mutafaaelun), (3, 1, 2), (-1, 1, 2))
kamel = Bahr('الكامل', (mutafaaelun, mutafaaelun, mutafaaelun))
wafer = Bahr('الوافر', (mufaaalatun, mufaaalatun, faaolon_wafer))
rujz = Bahr('الرجز', (mustafaelun, mustafaelun, mustafaelun))
ramal = Bahr('الرمل', (faaelatun, faaelatun, faaelatun))
sareea = Bahr('السريع', (mustafaelun, mustafaelun, faaelun))
khafeef = Bahr('الخفيف', (faaelatun, mustafaelun, faaelatun))
munsareh = Bahr('المنسرح', (mustafaelun, mafaulatu, mustafaelun))
hazaj = Bahr('الهزج', (mafaaelun, mafaaelun))
mutadarak = Bahr('المتدارك', (faaelun, faaelun, faaelun, faaelun))
mutaqareb = Bahr('المتقارب', (faaolon, faaolon, faaolon, faaolon))

# BUHOOR.extend([test])
BUHOOR.extend([taweel, baseet, madeed,  kamel, wafer,
              rujz, ramal, sareea,  hazaj, khafeef, munsareh, mutaqareb, mutadarak])
