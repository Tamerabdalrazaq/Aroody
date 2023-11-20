from analysis import analyze_tone
from parts import Jumla
from tester import test

# test = Jumla('ذُو العَقلِ يَشقَى فِي النَعيمِ بِعَقلِهِي')
test()
jumla = Jumla("قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيْبٍ وَمَنْزِلِ")
print(jumla.tone)
print(analyze_tone(jumla.tone)[0])
print(analyze_tone(jumla.tone)[1])
