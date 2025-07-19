import json
import buhoor

def beats_to_arood_writing(beats):
    res = [('/' if x == 1 else '0') for x in beats]
    return ''.join(res)

def format_pretty_dict(data):
    max_key_length = max(len(key) for key in data)  # Find longest key for alignment
    max_value = max(data.values())  # Find max value for scaling
    
    chart = "\n".join(f"{key.ljust(max_key_length)} | {'█' * int((value / max_value) * 20)} ({value})" 
                      for key, value in data.items())
    
    return chart

def format_buhoor_scores_dict(d):
    formatted = {key.name: d[key] for key in d.keys()}
    return format_pretty_dict(formatted)


def get_bahr_by_id(data, target_id):
    for obj in data:
        if obj.id == target_id:
            return obj
    return None  # if not found

def pad_vector_n(vector, n):
    return vector + [0] * (n - len(vector))

def get_bahr_by_name(name):
    for bahr in buhoor.BUHOOR:
        if bahr.name == name:
            return bahr
    return None


COMMON_WORDS = [
    "فِي",   # حرف الجر
    "مِنْ",  # حرف الجر
    "عَلَى", # حرف الجر
    "إِلَى", # حرف الجر
    "أَنَّ", # حرف توكيد
    "عَنْ",  # حرف الجر
    "لَا",   # نفي
    "مَا",   # نفي أو استفهام
    "إِنَّ", # حرف توكيد وشرط
    "كَانَ", # فعل ماضي
    "مَعَ",  # حرف جر
    ("هذا","هاذا"), # اسم إشارة
    ("هذه","هاذِهِ"), # اسم إشارة
    ("هذان","هاذانِ"), # اسم إشارة
    ("هؤلاء","هاؤُلَاءِ"), # اسم إشارة
    ("ذلك","ذَالِكَ"),# اسم إشارة
    ("ذلكم","ذَالِكُم"),# اسم إشارة
    ("ذلكما","ذَالِكُمَا"),# اسم إشارة
    ("ذلكن","ذَالِكُنَّ"),# اسم إشارة
    "الَّذِي", # اسم موصول
    "كَمَا",  # أداة تشبيه
    "أَنَا",  # ضمير المتكلم
    "هِيَ",   # ضمير الغائب مؤنث
    "أَوْ",   # حرف عطف
    "نَحْنُ", # ضمير المتكلم جمع
    "بَعْدَ", # ظرف زمان/مكان
    "لَهُ",   # ضمير في حالة الجر
    "لَكِنْ", # أداة استدراك
    "عِنْدَ", # حرف جر
    "يَكُونُ",# فعل مضارع ناقص
    "حَيْثُ", # أداة موصول
    "بَيْنَ", # ظرف مكان
    "حَتَّى", # أداة حصر
    "لَهُمْ", # ضمير في حالة الجر جمع
    "قَالَ",  # فعل ماضي
    "فَإِنَّ",# حرف شرط
    "الَّذِينَ", # اسم موصول جمع
    "عَلَيْكَ", # حرف جر + ضمير
    "دُونَ",  # حرف جر
    "لَهَا",  # ضمير في حالة الجر مؤنث
    "شَيْءٌ", # اسم
    "فِيهِ",  # حرف جر + ضمير
    "أَيْضًا", # ظرف
    "لِأَنَّهُ", # حرف سبب + ضمير
    "الْآنَ",  # ظرف زمان
    "مُنْذُ",  # ظرف زمان
    "تِلْكَ",  # اسم إشارة مؤنث
    "قَبْلَ",  # ظرف زمان
    "هَلْ",   # أداة استفهام
    "عَلَيْهِ", # حرف جر + ضمير
    "مِثْلَ", # حرف جر تشبيه
    "كُنْتُ", # فعل ماضي + ضمير
    "لِأَنَّ",# أداة سبب وتوكيد
    "هُنَاكَ", # ظرف مكان
    "فَقَطْ", # أداة حصر
    "حَوْلَ", # حرف جر
    "مَرَّةٌ", # ظرف زمان
    "تَحْتَ",  # حرف جر
    "رُبَّ",  # أداة قسم
    "بِدُونِ", # حرف جر
    ("الله", "الْلَاهُ"),
]
