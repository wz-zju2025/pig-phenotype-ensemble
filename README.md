# PigPhenotypeEnsemble

一个面向猪的分子表型集合预测器。输入是猪参考基因组序列，输出是基因表达、染色质可及性、组蛋白修饰和剪接相关分数。第一优先组织是肝脏。

本仓库记录模型检索、研究重点和训练闸门。权重、参考基因组和测序数据不放在这里。

## 现在的决定

监督式序列到表型模型不能把权重拼成一个文件。Enformer、Borzoi、AlphaGenome、Basenji 和 Translatomer 的输入长度、分辨率、物种头和输出轨道互不兼容。AlphaGenome 的物种标记只有人和小鼠。

集合模型采用晚融合：

1. 冻结的 Enformer，在猪序列上做零样本轨迹预测。
2. 冻结的 Borzoi trunk，只在猪的实验轨道就绪后训练新的输出头。
3. AlphaGenome 只在人鼠直系同源窗口上提供对照分数，不把猪基因组直接送进它的物种头。
4. Translatomer 留到有猪的 RNA-seq 和核糖体谱之后，预测翻译，不进入第一版主干。

已发表的猪上证据支持这条顺序。Maillard 等在 FAANG 数据上比较了人鼠训练的 DeepBind、DeepSEA 和 Enformer，猪的 H3K4me3 最好 AUPRC 为 0.765，Enformer 高于 DeepSEA。他们的结论是先用人训练模型做跨物种注释，再训练物种特异模型。

## 文档

- [模型目录](docs/MODEL_CATALOG.md)
- [研究重点](docs/RESEARCH_PLAN.md)
- [训练计划](docs/TRAINING_PLAN.md)
- [当前状态](docs/STATUS.md)

## 本地检查

复制 `config/local_paths.example.json` 为 `config/local_paths.json`，填上本机路径后运行：

```bash
python scripts/audit_local_assets.py
```

训练在闸门通过之前不会启动。
