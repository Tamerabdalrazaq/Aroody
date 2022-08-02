from buhoor import get_composition
from parts import Jumla
from tester import test

# test = Jumla('ذُو العَقلِ يَشقَى فِي النَعيمِ بِعَقلِهِي')
test()
jumla = Jumla('فَقَبَّلَت ناظِري تُغالِطُني')
print(jumla.tone)
beats = ''.join([str(i) for i in jumla.tone])
print(get_composition(beats))