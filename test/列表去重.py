def deduplicate_list_of_dicts(input_list):
    unique_set = set(tuple(sorted(d.items())) for d in input_list)
    deduplicated_list = [dict(item) for item in unique_set]
    return deduplicated_list

# 示例输入列表
input_list = [
    {"a": 1, "b": 2},
    {"b": 2, "a": 1},
    {"c": 3, "d": 4},
    {"a": 1, "b": 2},
]

deduplicated_list = deduplicate_list_of_dicts(input_list)
print(deduplicated_list)