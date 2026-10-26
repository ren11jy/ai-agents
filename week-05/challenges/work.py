"""W5 综合选做：按合同完成函数，使用 challenges 中的公开测试验收。"""


def summarize_values(values):
    """按首次出现顺序去重，统计频数，并记录重复值。"""
    unique = []
    counts = {}
    repeated = set()

    for number in values:
        if number in counts:
            counts[number] += 1
            repeated.add(number)
        else:
            unique.append(number)
            counts[number] = 1

    return {"unique": unique, "counts": counts, "repeated": repeated}

def apply_changes(original, updates, removals):
    """在原记录的副本上先更新后删除，并比较最终变化。"""
    record = dict(original)

    for key, value in updates:
        record[key] = value

    for key in removals:
        if key in record:
            del record[key]

    # 只在一边出现的键：最终新增或删除
    changed = set(original) ^ set(record)

    # 两边都有的键：检查最终值是否不同
    for key in set(original) & set(record):
        if original[key] != record[key]:
            changed.add(key)

    return {"record": record, "changed": changed}

def compare_measurements(ids, baseline, current, threshold):
    """对齐两次测量；不修改输入，返回独立的新结果。

    ids 为无重复的字符串列表；baseline、current 为等长的一维整数
    NumPy 数组；值范围为 [-1000000, 1000000]；threshold 为非负整数。
    返回 {"delta": 新的一维整数数组 current - baseline,
          "alerts": abs(delta) > threshold 的编号列表，保留输入顺序,
          "normal": 其余编号到 current 值的字典}。
    恰好等于阈值属于正常；空输入也要返回三个对应的空容器。
    先把 NumPy 整数转成 Python int 再计算，避免小 dtype 溢出。
    """
    raise NotImplementedError("请实现 compare_measurements")
