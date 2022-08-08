# define a function for merging tech stacks from multiple jobs
def merge_dictionary(dict_1, dict_2):
    dict_3 = {**dict_1, **dict_2}
    for key, value in dict_3.items():
        if key in dict_1 and key in dict_2:
            dict_3[key] = set([*value , *dict_1[key]]) #using set() to get the UNIQUE sub-tech-stacks
    return dict_3
