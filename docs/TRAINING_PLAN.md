# 训练计划

日期：2026-11-04。本文件是可执行顺序。每一步有数据和硬件闸门。闸门失败时脚本退出，不启动优化器。

## 资源上限

- GPU：最多一张空闲 A100，显存占用目标低于 20 GB。两张卡都有作业时跳过。
- CPU 盘点、文件检查和文档不受这个限制。
- 不下载 Evo 2、Nucleotide Transformer 2.5B 或其他十亿级语言模型。它们不输出实验轨道。

## 阶段 0：资产盘点

命令：

```bash
python scripts/audit_local_assets.py
```

检查猪参考序列、GTF、Enformer 配置和权重、Borzoi 权重、AlphaGenome 权重链接、Translatomer checkpoint。输出写到 `outputs/audit.json`，该目录不入库。

2026-11-04 的盘点结果见运行日志。阶段 0 不更新参数。

## 阶段 1：Enformer 零样本子集

前提：

- 猪 fasta 可读，染色体名称为 Ensembl 风格的 `1`–`18`、`X`、`Y`、`MT`。
- 至少一份猪的 FAANG 峰文件在本地，优先 H3K4me3，其次 ATAC。Maillard 等使用的公共峰来自 GSE158430。
- 一张 GPU 的已用显存低于 8 GB，利用率低于 20%。否则改期。

操作：

1. 每条常染色体抽固定数量的 196,608 bp 窗口。窗口名单先写死并入库，避免评价时改抽样。
2. 用本机 Enformer PyTorch 权重做前向，只保留与组蛋白或可及性最接近的人轨道。
3. 与峰重叠计算 AUPRC、AUROC。
4. 和 Maillard 等报告的猪 H3K4me3 AUPRC 0.765 比较。

这一步是评价，不是梯度训练。

## 阶段 2：Borzoi 猪头

前提：

- 阶段 1 的 AUPRC 进入文献同一量级。
- 至少两条肝脏轨道已经做成 Borzoi 要求的 w5，并有 `targets.txt`。
- 自有 ATAC 已经完成过滤 BAM 和覆盖轨道。比对未完成时不制作伪轨道。

操作按本机 baskerville 转移教程：

1. BAM 或已有覆盖转为 BigWig，再转为 w5。
2. 写 `targets.txt`：索引、轨道名、缩放、软硬裁剪、链配对。
3. 按猪基因组区间做 TFRecord，留出 18 和 X。
4. 加载 Borzoi trunk，丢掉原 dense head，只训练新头。
5. 损失沿用 Borzoi 的 Poisson 和 multinomial。不改 trunk 学习率以外的结构。trunk 学习率设为 0。

停止：留出染色体不如阶段 1 的 Enformer，就丢弃新头。

## 阶段 3：晚融合

前提：阶段 1 完成。阶段 2 可以缺席。

对每个评价窗口记录 Enformer 分数、Borzoi 猪头分数和直系同源 AlphaGenome 分数。默认融合是秩次平均。缺一组就跳过该组。融合权重若要学习，只用非留出染色体，并且参数量限于每组一个标量。

## 阶段 4：翻译

Translatomer 需要序列和匹配的 RNA-seq。猪的配对核糖体谱不在当前数据里。有公开或自有 Ribo-seq 之后，单独评价，不回头改前三个阶段的主干。

## 当前闸门

| 闸门 | 2026-11-04 状态 | 后果 |
| --- | --- | --- |
| 猪参考序列和 GTF | 本机已有 Ensembl Sscrofa11.1 toplevel FASTA 和 release 116 GTF | 阶段 0 可以通过 |
| FAANG 峰文件进入本仓库数据目录 | 未放置 | 阶段 1 不运行 |
| GPU 空闲 | 盘点时两张 A100 都有显存占用，其中一张利用率约 99% | 不提交前向或训练 |
| 肝脏覆盖轨道 | 自有 ATAC 尚未形成可训练 w5 | 阶段 2 不运行 |

下一次允许启动计算的条件是：峰文件到位，并且 `nvidia-smi` 显示至少一张卡的利用率低于 20%、已用显存低于 8 GB。
