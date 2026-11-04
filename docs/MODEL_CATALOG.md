# 模型目录

检索日期：2026-11-04。

## 检索边界

本目录收录直接预测分子表型的序列模型，以及可能当作特征提取器的基因组语言模型。范围是原始论文、Nature 系列论文、公开 GitHub 仓库，以及本机已经下载的 Enformer、Borzoi、AlphaGenome、Basenji 和 Translatomer。

“一万个同类型模型”这个数量没有对应对象。序列到功能的监督模型，主模型和常用专家模型是几十个。自监督基因组语言模型再增加几十个家族和尺寸变体。把同一篇论文里的每个 fold、每个组织头或每个 notebook 单独计数，仍然到不了一万。逐行阅读不存在的一万个运行代码，不会提高猪的预测。

下面每个模型只记录和猪表型迁移有关的事实：物种、输入、输出、能否进入集合。未在本次打开原文核对的条目标为二手来源。

## A. 进入集合设计的监督模型

| 模型 | 来源 | 训练物种 | 和猪表型的关系 | 本机 |
| --- | --- | --- | --- | --- |
| Enformer | Avsec 等，*Nature Methods*，2021。本机 `config.json`：人 5313 轨、鼠 1643 轨，11 层注意力，宽度 1536 | 人、小鼠 | 零样本主干。Maillard 等在猪、牛、鸡上比较后，Enformer 优于 DeepSEA | 有 PyTorch 权重 |
| Borzoi | Linder 等，*Nature Genetics* 57:949–961，2025。DOI [10.1038/s41588-024-02053-6](https://doi.org/10.1038/s41588-024-02053-6)，PMID 39779956 | 人、小鼠 | 第二阶段主干。输入约 524 kb，预测 RNA-seq 覆盖，并可派生转录、剪接和多聚腺苷酸化效应。论文报告 replicate 平均后更好。官方转移学习只换输出头 | 有 `model0_best.h5` 和 baskerville 转移教程 |
| AlphaGenome | Avsec 等，*Nature* 649:1206–1218，2026。DOI [10.1038/s41586-025-10014-0](https://doi.org/10.1038/s41586-025-10014-0) | 人、小鼠 | 对照模型。1 Mb 输入，人 5930 轨或鼠 1128 轨，11 类输出，分辨率到 1 bp。物种标记没有猪。论文在 26 项变异效应评估中 25 项持平或超过外部模型 | 有研究代码；权重是外部目录的符号链接 |
| Basenji / Basenji2 | Kelley 等的卷积前代模型。Enformer 论文和 AlphaGenome 综述把它列为前代 | 人、小鼠 | 不单独进集合。保留为 Borzoi/Enformer 的方法来源 | 本机有代码和人基因组 |
| Translatomer | He 等，*Nature Machine Intelligence*，2024。DOI [10.1038/s42256-024-00915-6](https://doi.org/10.1038/s42256-024-00915-6) | 人、小鼠 | 预测核糖体谱，输入还要细胞类型 RNA-seq。第一版没有猪的配对翻译数据，不进主干 | 有 checkpoint |

## B. 已经用到猪、但不替代上面主干的工作

| 工作 | 来源 | 作用 |
| --- | --- | --- |
| 跨物种染色质注释 | Maillard 等，*G3*，2026。DOI [10.1093/g3journal/jkag230](https://doi.org/10.1093/g3journal/jkag230)。预印本 DOI [10.1101/2025.10.16.682871](https://doi.org/10.1101/2025.10.16.682871) | 用 DeepBind、DeepSEA、Enformer 预测猪、牛、鸡和欧洲海鲈的 TF、可及性和组蛋白。猪 H3K4me3 全部组织合并的最好 AUPRC 为 0.765 ± 0.009。非保守序列上仍有预测能力。鱼类明显变差。结论是先零样本，再做物种特异训练 |
| DeepGCF | Li 等，*Cell Genomics*，2023。PMID [37868039](https://pubmed.ncbi.nlm.nih.gov/37868039/) | 分别训练人、猪 DeepSEA，再用伪孪生网络给直系区域打功能保守分。输入是 386 个人类和 374 个猪的功能谱。它输出保守分数，不输出全套分子轨迹 |
| PigGTEx | Teng 等，*Nature Genetics* 56:112–123，2024。DOI [10.1038/s41588-023-01585-7](https://doi.org/10.1038/s41588-023-01585-7) | 5457 个 RNA-seq、1602 个全基因组、34 个组织的 molQTL 资源。它是评价和日后微调的表型来源，不是序列神经网络。处理数据在 [piggtex.farmgtex.org](http://piggtex.farmgtex.org/) |

DeepSEA（Zhou 等）和 DeepBind（Alipanahi 等，2015）只作为 Maillard 实验里的弱基线保留。新的集合不再以它们为主干。

## C. 专家模型

这些模型只预测一类表型。AlphaGenome 论文把其中的剪接模型当作被统一模型比较的外部方法。它们可以在对应任务上做对照，不并进第一版权重。

| 模型 | 表型 | 本次依据 |
| --- | --- | --- |
| SpliceAI | 剪接位点 | AlphaGenome 论文点名的剪接外部模型 |
| Pangolin | 剪接使用 | 同上 |
| Sei | 短序列调控类别，约 4 kb | TraitGym 预印本表 2，Chen 等，2022。预印本 DOI [10.1101/2025.02.11.637758](https://doi.org/10.1101/2025.02.11.637758) |
| ChromBPNet | 染色质可及性、碱基分辨率 | AlphaGenome 的二手综述把它列为可及性专家模型。本次未单篇核对原文 |
| ProCapNet | 转录起始 | 同上，二手来源 |
| Orca | 三维染色质接触 | 同上，二手来源 |
| ExPecto | 表达变异效应 | Enformer 的公开介绍把它列为被超越的前代。本次未单篇核对原文 |
| scBasset | 单细胞可及性 | Borzoi 转移教程使用其示例数据桶。它解决的是单细胞，不是组织大轨道 |
| BigRNA | RNA | *The DNA dialect* 综述把它和 Enformer、Borzoi、AlphaGenome 并列，并标明为预印本（Celaj 等，2023）。PMC12953581 |

## D. 自监督基因组语言模型

它们学习序列表示，不直接输出 ENCODE/GTEx 式实验轨道。TraitGym 预印本比较后，CADD 和 GPN-MSA 在孟德尔和复杂疾病性状上较好，Enformer 和 Borzoi 在复杂非疾病性状上较好。猪的分子表型更接近后一类，所以第一版主干用监督模型。

Wu 等，*Nature Communications*，2025，DOI [10.1038/s41467-025-65823-8](https://doi.org/10.1038/s41467-025-65823-8)，用零样本嵌入比较了 DNABERT-2、Nucleotide Transformer v2、HyenaDNA、Caduceus-Ph 和 GROVER。没有一个模型在全部任务上领先。

| 家族 | 本次看到的事实 | 是否进入猪表型集合 |
| --- | --- | --- |
| DNABERT、DNABERT-2 | DNABERT-2 为多物种 BPE 模型，ICLR 2024。代码：[MAGICS-LAB/DNABERT_2](https://github.com/MAGICS-LAB/DNABERT_2) | 短序列分类可以后补，不预测轨道 |
| Nucleotide Transformer / NT-v2 | 多物种掩码语言模型。目录页给出 PMID 39609566，本次未打开原文 | 同上 |
| HyenaDNA | 人基因组，长上下文卷积。NeurIPS 2023，二手综述 | 同上 |
| Caduceus | 人基因组，双向 Mamba。Schiff 等，2024 | 同上 |
| GROVER | 人基因组 BPE | 同上 |
| GPN、GPN-MSA、PhyloGPN、GPN-Star | 对齐或系统发育预训练，主要用于变异效应。代码：[songlab-cal/gpn](https://github.com/songlab-cal/gpn) | 可作变异分数对照。猪上要用猪的多序列比对，目前没有 |
| Evo、Evo 2 | 生成式长上下文模型。目录页把 Evo 2 标为 Brixi 等，*Nature*，2026，PMID 41781614。本次未打开原文。训练语料跨界，不是人鼠功能轨道 | 不预测猪的组织轨道 |
| GENERator | arXiv:2502.07272 的模型表把 Enformer、DNABERT-2、HyenaDNA、NT、Caduceus、GROVER、Evo 2 放在一起比较规模 | 生成模型，不进集合 |

## E. 明确不收录

- 本机 `Number_sure` 是 MNIST 手写数字模型，和基因组无关。
- Geneformer、scGPT 吃的是单细胞表达，不是 DNA 序列到实验轨道。
- ESM、AlphaMissense 是蛋白质或错义变异模型。
- AgroNT 面向植物。
- 只换一个 checkpoint 尺寸、一个 Colab 或一个 fold 的副本，不另计为新模型。

## F. 本机五类基因组模型的角色

| 目录 | 角色 |
| --- | --- |
| Enformer | 零样本猪轨迹 |
| Borzoi | 日后唯一允许训练的新头 |
| alphagenome_work | 人鼠同源窗口对照 |
| Basenji2 | 方法档案，不单独训练 |
| Translatomer | 翻译任务延期 |
| pigmaster | 本计划、闸门和集合接口 |
