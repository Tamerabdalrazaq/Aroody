from analysis import get_composition
from parts import Jumla
from tester import test

# test = Jumla('ذُو العَقلِ يَشقَى فِي النَعيمِ بِعَقلِهِي')
test()
jumla = Jumla("دَمْعٌ جرَى فقضَى في الرَّبْعِ ما وجَبَا")
print(jumla.tone)
print(get_composition(jumla.tone))
