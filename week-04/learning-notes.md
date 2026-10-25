# W4 追加实验：个人核验记录

- **一次预测与修正**：对 `source = {"seed": 7, "sample_sizes": [10, 20, 30]}` 使用 `seed=9, index=1, replacement=25` 时，我起初把 `25` 放在列表第一项。核对 Python 从 0 开始的索引后，确定第 2 项才是 `index=1`，预期新方案为 `{"seed": 9, "sample_sizes": [10, 25, 30]}`；旧方案应保持原值。
- **被实验证据否定的解释**：检验“只复制外层字典就能保护旧配置”时，Notebook 中 `source.copy()` 让字典身份检查为 `False`，但内层列表身份检查为 `True`；修改新方案的列表后，旧方案的列表也变了。因此只复制字典不足以隔离这份配置。
- **最终关系**：`variant.py` 每次创建新字典和新 `sample_sizes` 列表，再更新新方案的 seed 与指定位置。相同参数调用两次，结果内容相等，但字典和列表分别独立；修改第一份不会影响第二份或 `source`。
- **实际核验**：学生测试对 `reference` 为 `3 passed`，对 `direct` 为 `3 failed`，对 `shallow` 为 `3 failed`；对 `student` 为 `3 passed`。教师公开验收对 `student` 为 `24 passed`。故障实现的断言失败是预期结果。
- **范围**：必做项目已完成；Notebook 后续选做练习未做。`demo.ipynb` 的运行输出仍是本地未提交改动。
