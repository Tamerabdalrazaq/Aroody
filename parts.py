import enum
from multiprocessing.dummy import current_process
import pyarabic.araby as araby
from pyarabic.araby import is_tanwin, is_weak
SHADDA = chr(int('0x651', 16))
SUKOON = chr(int('0x652', 16))
HARAKA_ANY = '_'

HUROOF = {
    'ALEF': chr(int('0x627', 16)),
    'MADDA': chr(int('0x622', 16)),
    'HAMZAT_WASL': chr(int('0x627', 16)),
}


TASHKEEL = {
    'SUKOON': chr(int('0x652', 16)),
    'SHADDA': chr(int('0x651', 16)),
    'KASRA': chr(int('0x650', 16)),
    'DAMMA': chr(int('0x64F', 16)),
    'FATHATAN': chr(int('0x64B', 16)),
    'FATHA': chr(int('0x64e', 16)),
}


HUROOF_WAY = [
    chr(int('0x627', 16)),  # ا
    chr(int('0x648', 16)),  # و
    chr(int('0x649', 16)),  # ى
    chr(int('0x64A', 16)),  # ي
]

WEAKS_HARAKAT = {
    'ي': chr(int('0x650', 16)),
    'ا': chr(int('0x64e', 16)),
    'و': chr(int('0x64f', 16)),
    'ى': chr(int('0x64e', 16)),
}

harakat_repr = {
    chr(int('0x64e', 16)): '^',
    chr(int('0x64F', 16)): '<',
    chr(int('0x650', 16)): '>',
    chr(int('0x651', 16)): '~',
    chr(int('0x652', 16)): '0',
    chr(int('0x653', 16)): '',
    chr(int('0x64B', 16)): '^^',
    chr(int('0x64C', 16)): '<<',
    chr(int('0x64D', 16)): '>>',
}

TANWEEN_TO_TASHKEEL = {
    chr(int('0x64B', 16)): chr(int('0x64e', 16)),
    chr(int('0x64C', 16)): chr(int('0x64f', 16)),
    chr(int('0x64D', 16)):  chr(int('0x650', 16))
}

HAMZAT_QAT3_BEDAYA = "أإ"

COMMON_KALEMAT = {
    
}

def starts_with_wasl(kalema):
    assert type(kalema) == Kalema
    assert type(kalema.objects[0]) == Harf
    return kalema.objects[0].harf == HUROOF['HAMZAT_WASL']


def handle_cutting_wasl(curr, prev):
    prev_huroof, curr_huroof = prev.huroof, curr.huroof
    assert (type(curr) == type(prev) == Kalema)
    assert (type(prev_huroof[-1]) == type(prev_huroof[-2])
            == type(curr_huroof[0]) == Harf)
    first_harf, last_harf, penultimate_harf = curr_huroof[0], \
        prev_huroof[-1], prev_huroof[-2]
    assert (first_harf.harf == HUROOF['HAMZAT_WASL'])
    curr.cut_hamzat_wasl()
    if last_harf.haraka.sukoon:
        penult_haraka = penultimate_harf.haraka.haraka
        if last_harf.harf in HUROOF_WAY and penult_haraka == WEAKS_HARAKAT[last_harf.harf]:
            prev.cut_last_WAY()
        else:
            prev.tahreek_last_harf()


def test_objects_correctness(objects):
    for i, obj in enumerate(objects):
        assert (type(obj) == Haraka or type(obj) == Harf), "error in object correctness"
        assert (i == len(objects) - 1 or
                type(objects[i+1]) == (Haraka if type(obj) == Harf else Harf)), \
                    "error in object correctness"


def untie_shadda(i, res, objects):
    res.pop()
    mashdood_index = i-1
    mashdood_haraka_index = i+1
    assert type(objects[mashdood_haraka_index]) == Haraka and  type(objects[mashdood_index]) == Harf,  "ضع الحركة بعد الشدّة لا قبلها"
    sukoon = Haraka(SUKOON)
    saken = Harf(objects[mashdood_index].harf, sukoon)
    mutaharrek = Harf(
        objects[mashdood_index].harf, objects[mashdood_haraka_index])
    res.extend([saken, sukoon, mutaharrek])


def untie_madda(curr_obj, res):
    sukoon = Haraka(SUKOON)
    fatha = Haraka(TASHKEEL['FATHA'])
    curr_obj.set_harf(HUROOF['ALEF'])
    curr_obj.set_type(fatha)
    emerged_alef = Harf(HUROOF['ALEF'], sukoon)
    res.extend([curr_obj, fatha, emerged_alef])


class Haraka:
    def __init__(self, haraka):
        assert haraka in araby.TASHKEEL or haraka == HARAKA_ANY
        self.haraka = haraka
        self.shadda = haraka == SHADDA
        self.tanween = haraka in araby.TANWIN
        self.sukoon = haraka == SUKOON

    def __repr__(self) -> str:
        return harakat_repr[self.haraka]

    def tanween_to_tashkeel(self):
        self.haraka = TANWEEN_TO_TASHKEEL[self.haraka]
        self.shadda = False
        self.tanween = False
        self.sukoon = False


class Harf:
    def __init__(self, harf, haraka=None):
        self.harf = harf
        self.saken = True
        self.haraka = None
        if haraka != None:
            self.set_type(haraka)

    def set_type(self, haraka):
        assert type(haraka) == Haraka
        self.haraka = haraka
        self.saken = haraka.sukoon

    def set_harf(self, harf):
        self.harf = harf

    def __repr__(self) -> str:
        return self.harf
    
    def __eq__(self, value):
        if type(value) == Harf:
            return self.harf == value.harf
        elif type(value) == str:
            return len(value) == 1 and value == self.harf
        raise Exception("Invalid comparison to Harf object")

class Kalema:
    def __init__(self, text):
        assert len(text) > 0
        self.text = list(text)
        self.objects = self.convert_to_objects()
        self.huroof = []
        self.daqqat = []
        self.arood_process()

    def __iter__(self):
        return iter(self.huroof)


    def __repr__(self) -> str:
        return ''.join(self.text) + ': ' + ''.join(self.daqqat)

    def __eq__(self, other):
        if type(other) not in [str, Kalema]:
            raise Exception('Invalid comparison between Kalema and object')
        for i, ch in enumerate(other):
            if ch != self.huroof[i]:
                return False
        return True


    def convert_to_objects(self):
        res = []
        for i in self.text:
            if i in araby.LETTERS:
                res.append(Harf(i))
            elif i in araby.TASHKEEL:
                res.append(Haraka(i))
            else:
                raise Exception("Invalid Input")
        return res
    
    def swap_objects(self, i, j):
        self.objects[i], self.objects[j] = self.objects[j], self.objects[i]

    def arood_process(self):
        self.prepare_shadda_position()
        self.process_shadda_madda()
        self.process_tanween()
        self.attach_harakat()
        self.trim_harakat()  # from here on only modify self.huroof not self.objects
        self.process_madd_wasat()
        self.process_hamzat_qat3_bedaya()
        self.process_awwal_mutaharrek()

    def prepare_shadda_position(self):
        objects = self.objects
        for i in range(len(objects)):
            curr_obj = objects[i]
            prev_obj = objects[i-1]
             
            if type(curr_obj) == Haraka and curr_obj.shadda:
                if (type(prev_obj) == Haraka):
                     self.swap_objects(i, i-1)
                elif(type(prev_obj) == Harf):
                    if(len(objects) == i+1 or type(objects[i+1]) == Harf):
                        objects.insert(i+1, Haraka(TASHKEEL['FATHA']))

    def process_shadda_madda(self):  # Mashduud = harf + shadda + haraka
        objects = self.objects
        res = []
        for i in range(len(objects)):
            curr_obj = objects[i]
            if type(curr_obj) == Haraka and curr_obj.shadda:
                untie_shadda(i, res, objects)
            elif type(curr_obj) == Harf and curr_obj.harf == HUROOF['MADDA']:
                untie_madda(curr_obj, res)
            else:
                res.append(curr_obj)
        self.objects = res

    def attach_harakat(self):
        objects = self.objects
        i = 0
        while i < (len(objects)-1):
            curr, next = objects[i], objects[i+1]
            if type(curr) == Harf and type(next) == Haraka:
                curr.set_type(next)
            elif type(curr) == Harf and type(next) == Harf:
                self.attach_sukoon(i)
            i += 1
        if type(objects[-1]) == Harf:
            self.attach_sukoon(len(objects)-1)

    def attach_sukoon(self, index):
        curr = self.objects[index]
        assert type(curr) == Harf
        sukoon = Haraka(SUKOON)
        curr.set_type(sukoon)
        self.objects.insert(index+1, sukoon)

    def process_tanween(self):
        objects = self.objects
        last = objects[-1]
        penultimate = objects[-2]
        if (type(penultimate) == Haraka and penultimate.haraka == TASHKEEL['FATHATAN']):
            penultimate.tanween_to_tashkeel()
        elif(type(last) == Haraka and last.haraka == TASHKEEL['FATHATAN']):
            self.objects.pop()
        elif (type(last) == Haraka and is_tanwin(last.haraka)):
            last.tanween_to_tashkeel()
            res = objects[:]
            assert type(res[-2]) == Harf, 'Error in process tanween'
            res[-2].set_type(last)
            res.append(Harf('ن', Haraka(SUKOON)))
            self.objects = res

    def process_daqqat(self):
        daqqat = []
        for i in range(0, len(self.objects), 2):
            curr = self.objects[i]
            assert type(curr) == Harf, 'error in process_daqqat'
            if curr.saken:
                daqqat.append(0)
            else:
                daqqat.append(1)
        self.daqqat = daqqat
        return daqqat

    def cut_last_WAY(self):
        last_harf = self.objects[-2]
        assert (type(last_harf) == Harf and last_harf.harf in HUROOF_WAY)
        self.objects = self.objects[:-2]
        assert (type(self.objects[-1]) ==
                Haraka and type(self.objects[-2]) == Harf)

    def tahreek_last_harf(self):
        last_harf = self.objects[-2]
        assert (type(last_harf) == Harf)
        last_harf = self.objects[-2]
        assert (type(last_harf)) == Harf and (last_harf.saken)
        updated_objects = self.objects[:]
        updated_objects.pop()
        kasra = Haraka(TASHKEEL['KASRA'])
        last_harf.set_type(kasra)
        updated_objects.append(kasra)
        self.objects = updated_objects

    def cut_hamzat_wasl(self):
        assert (self.objects[0].harf == HUROOF['HAMZAT_WASL'])
        self.objects = self.objects[2:]

    def trim_harakat(self):
        objects = self.objects
        trimmed = []
        test_objects_correctness(objects)
        trimmed = list(filter((lambda x: type(x) == Harf), objects))
        self.huroof = trimmed

    def process_madd_wasat(self):
        huroof = self.huroof
        for i in range(1, len(huroof))[::-1]:
            harf = huroof[i]
            if  harf.harf in HUROOF_WAY and harf.saken:
                prev_harf = huroof[i-1]
                if prev_harf.saken:
                    prev_harf.set_type(Haraka(WEAKS_HARAKAT[harf.harf]))

    def process_hamzat_qat3_bedaya(self):
        huroof = self.huroof
        if huroof[0].harf in HAMZAT_QAT3_BEDAYA:
            huroof[0].set_type(Haraka(TASHKEEL['FATHA']))

    def process_awwal_mutaharrek(self):
        first_harf = self.huroof[0]
        if not first_harf.saken:
            return
        if first_harf.harf == HUROOF['HAMZAT_WASL']:
            return
        first_harf.saken = False
        first_harf.haraka = HARAKA_ANY


class Jumla():
    def __init__(self, text):
        self.text = text.strip()
        words = text.split(' ')
        words = [Kalema(word) for word in words if word != '']
        self.kalemat = words
        self.tone = []
        self.process()

    def process(self):
        self.process_hamza()
        self.get_tone()

    def process_hamza(self):
        for i, kalema in enumerate(self.kalemat):
            if starts_with_wasl(kalema) and i > 0:
                curr, prev = kalema, self.kalemat[i-1]
                handle_cutting_wasl(curr, prev)

    def get_tone(self):
        res = []
        for kalema in self.kalemat:
            res.extend(kalema.process_daqqat())
        self.tone = res

    def __repr__(self):
        return self.text + '\n' + ''.join([str(i) for i in self.tone])



"""
تحسينات ممكنة:
قائمة كلمات معروفة مع إيقاعها
بداية كل كلمة تبدأ بمتحرّك! باستنثاء الكلمات الواصلة بألف الوصل

"""