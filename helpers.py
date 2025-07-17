import json


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