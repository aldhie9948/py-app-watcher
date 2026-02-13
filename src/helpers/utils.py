def groupby(data: list, key: str):
    from collections import defaultdict

    grouped = defaultdict(list)
    for item in data:
        grouped[item[key]].append(item)
    return dict(grouped)
