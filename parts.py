from multiprocessing.dummy import current_process
import pyarabic.araby as araby
from pyarabic.araby import is_tanwin, is_weak
SHADDA = chr(int('0x651', 16))
SUKOON = chr(int('0x652', 16))
SEFR = chr(int('0x660', 16))
WEAKS_HARAKAT = {
    'ي': chr(int('0x650', 16)),
    'ا': chr(int('0x64e', 16)),
    'و': chr(int('0x64f', 16))
}

harakat = {
    chr(int('0x64e', 16)): '^',
    chr(int('0x64F', 16)):'<',
    chr(int('0x650', 16)):'>',
    chr(int('0x651', 16)):'~',
    chr(int('0x652', 16)):'0',
    chr(int('0x653', 16)):'',
    chr(int('0x64B', 16)):'^^',
    chr(int('0x64C', 16)):'<<',
    chr(int('0x64D', 16)):'>>',
}

class Haraka:
    def __init__(self, haraka):
        assert haraka in araby.TASHKEEL
        self.haraka = haraka
        self.shadda = haraka == SHADDA
        self.tanween = haraka in araby.TANWIN
        self.sukoon = haraka == SUKOON
    def __repr__(self) -> str:
        return harakat[self.haraka]
    def tanween_to_tashkeel(self):
        if self.haraka == chr(int('0x64B', 16)): self.haraka = chr(int('0x64e', 16))
        if self.haraka == chr(int('0x64C', 16)): self.haraka = chr(int('0x64f', 16))
        if self.haraka == chr(int('0x64D', 16)): self.haraka = chr(int('0x650', 16))
    
class Harf:
    def __init__(self, harf, haraka = None):
        self.harf = harf
        self.saken = True
        self.haraka = None
        if haraka != None: 
            self.set_type(haraka)

    def set_type(self, haraka):
        assert type(haraka) == Haraka
        self.haraka = haraka
        self.saken = haraka.sukoon
    def __repr__(self) -> str:
        return self.harf

class Kalema:
    def __init__(self, text):
        assert len(text) > 0
        self.text = list(text)
        self.objects = self.convert_to_objects()
        self.daqqat = []
        self.arood_process()
    
    def __repr__(self) -> str:
        return ''.join(self.text) + ': ' + ''.join(self.daqqat)
    def convert_to_objects(self):
        res = []
        for i in self.text:
            if i in araby.LETTERS: res.append(Harf(i))
            elif i in araby.TASHKEEL: res.append(Haraka(i))
        return res

    def arood_process(self):
        self.process_shadda()
        self.process_tanween()
        self.attach_harakat()
        self.process_daqqat()

    def process_shadda(self): #Mashduud = harf + shadda + haraka
        objects = self.objects
        res = []
        for i in range(len(objects)):
            curr_obj = objects[i]
            if type(curr_obj) == Haraka and curr_obj.shadda:
                res.pop()
                mashdood_index = i-1
                mashdood_haraka_index = i+1
                assert type(objects[mashdood_index]) == Harf 
                assert type(objects[mashdood_haraka_index]) == Haraka
                sukoon = Haraka(SUKOON)
                saken = Harf(objects[mashdood_index].harf, sukoon)
                mutaharrek = Harf(objects[mashdood_index].harf, objects[mashdood_haraka_index])
                res.extend([saken, sukoon, mutaharrek])
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
        if type(objects[-1]) == Harf: self.attach_sukoon(len(objects)-1)
    
    def attach_sukoon(self, index):
        curr = self.objects[index]
        assert type(curr) == Harf
        sukoon = Haraka(SUKOON)
        curr.set_type(sukoon)
        self.objects.insert(index+1, sukoon)
    

    def process_tanween(self):
        objects = self.objects
        last = objects[-1]
        if (type(last) == Haraka and is_tanwin(last.haraka)):
            last.tanween_to_tashkeel()
            res = objects[:]
            res[-2].set_type(last)
            res.append(Harf('ن', Haraka(SUKOON)))
            self.objects = res

    def process_daqqat(self):
        for i in range(0,len(self.objects), 2):
            curr = self.objects[i]
            assert type(curr) == Harf
            if curr.saken: self.daqqat.append(0)
            else: self.daqqat.append(1)

class Jumla():
    def __init__(self, text):
        self.text = text
        words = text.split(' ')
        words = [Kalema(word) for word in words if word != '']
        self.kalemat = words
        self.tone = []
        self.get_tone()

    def get_tone(self):
        res = []
        for kalema in self.kalemat: res.extend(kalema.daqqat)
        self.tone = res
    def __repr__(self):
        return self.text + '\n' + ''.join([str(i) for i in self.tone])
