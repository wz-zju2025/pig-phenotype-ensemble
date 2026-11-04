# 2026-11-04 状态

资产检查已经跑过。猪的 Ensembl Sscrofa11.1 FASTA、release 116 GTF、Enformer 配置和权重、Borzoi `model0_best.h5`、AlphaGenome 权重目录、Translatomer checkpoint 都能打开。FAANG 峰文件不在数据目录里。

当时两张 A100 都有显存占用，0 号利用率约 99%，1 号约 6%。按训练计划，零样本前向和新头训练都没有启动。

集合预测器还没有参数。当前可交付的是模型目录、研究重点和闸门。下一动是放入猪的 H3K4me3 或 ATAC 峰，并等到一张卡空闲。
