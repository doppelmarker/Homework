"""
### Task 4.11
Implement a function, that receives changeable number of dictionaries (keys - letters, values - numbers) and combines them into one dictionary.
Dict values should be summarized in case of identical keys

>>> dict_1 = {'a': 100, 'b': 200}
>>> dict_2 = {'a': 200, 'c': 300}
>>> dict_3 = {'a': 300, 'd': 100}

>>> combine_dicts(dict_1, dict_2)
{'a': 300, 'b': 200, 'c': 300}
>>> combine_dicts(dict_1, dict_3)
{'a': 400, 'b': 200, 'd': 100}
>>> combine_dicts(dict_1, dict_2, dict_3)
{'a': 600, 'b': 200, 'c': 300, 'd': 100}
"""


def combine_dicts(*args):
    combined_dict = dict()
    for d in args:
        for k, v in d.items():
            combined_dict[k] = combined_dict.get(k, 0) + v
    return combined_dict
