"""一组独立输入：按最终记录判断哪些键真正改变。"""


def test_my_apply_changes_case(apply_changes):
    original = {"x": 1, "keep": 0}
    updates = [("x", 5), ("x", 1), ("temp", 7), ("new", -2)]
    removals = ["temp", "keep", "missing"]

    result = apply_changes(original, updates, removals)

    assert result == {
        "record": {"x": 1, "new": -2},
        "changed": {"keep", "new"},
    }
    assert original == {"x": 1, "keep": 0}
    assert updates == [("x", 5), ("x", 1), ("temp", 7), ("new", -2)]
    assert removals == ["temp", "keep", "missing"]
