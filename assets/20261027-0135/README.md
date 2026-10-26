# 20261027-0135 正式报告绘图资产

对应[正式报告](../../reports/2026-10-27/0135-report.md)。[draw_figures.py](draw_figures.py) 从本聊天原绘图工具调用恢复，保留全部文字、布局、配色与数据；为适应正式目录调整输出位置，并增加 `--output-dir` 参数和来源注释。

## 重新生成

在仓库根目录运行，默认覆盖本资产目录的三张 PNG：

```powershell
python assets/20261027-0135/draw_figures.py
```

核对时可输出到本轮独立临时目录，不覆盖正式图片：

```powershell
python assets/20261027-0135/draw_figures.py --output-dir .scratch/figure-check
```

实际核对环境：Windows、Python 3.11.2、Pillow 12.2.0、matplotlib 3.10.8；字体使用 `C:/Windows/Fonts/msyh.ttc` 和 `msyhbd.ttc`。字体文件不随仓库分发。脚本只读本地字体、写入三张图片，不访问网络；依赖缺失时不会自动安装。其他环境需提供字体并调整源码中的字体路径；字体或依赖版本变化可能改变渲染结果。

## 图片、数据与来源

- `harness-routes.png`：Pillow 机制示意图。来源为 [OO-Harness v1 §3](https://arxiv.org/html/2610.28380v1#S3)、[Harness² v1 §2](https://arxiv.org/html/2610.14224v1#S2)、[RRSI v1 §3](https://arxiv.org/html/2609.24972v1#S3)。三条并列路线，不表示演进顺序或性能排名。
- `routing-evidence.png`：matplotlib 数值图。来源为 [OO-Harness v1 §5.1.1、表2](https://arxiv.org/html/2610.28380v1#S5.SS1.SSS1)。数据内嵌在源码的 `pairs`，分别为 `(64.88, 77.52)`、`(40.03, 40.56)`、`(33.33, 37.70)`，每对依次为只看任务与任务加基础轨迹。不同任务指标仅行内比较；单次消融运行；任务版包含0.7自报置信门槛，差值不是完全隔离的轨迹因果效应。
- `memory-evidence.png`：Pillow 自拟场景示意图，不是论文样本或数据图。解释依据为 [显式记忆比较 v1 §3–6](https://arxiv.org/html/2610.24671v1)、[Raw-RAG v1 §5.2–5.3](https://arxiv.org/html/2610.30755v1#S5.SS2)、[LightMem复现 v2 §6](https://arxiv.org/html/2607.29104v2#S6)。紧预算关系有条件，不表示所有压缩记忆必然丢失信息。

## 恢复验收

2026-10-27 在上述现有环境重新运行源码，三幅新图与正式图片均逐字节一致，像素比对也通过；正式图片未被替换。正式文件 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| harness-routes.png | `40dc483ac2721790b21a4cad3c7e4d4c89a1d13f2eaefd5b67b40514d112e022` |
| memory-evidence.png | `64db4c58184e08340c2503eda21da9c981715c3f6104c8ab7c5263a796b147eb` |
| routing-evidence.png | `9396693e6a19cd7ef24d530093368147250f72670fc597f5dc11aba0ef5d449f` |

源码、内嵌数据和本说明属于正式资产，随图片保留；临时核对输出在验收后清理。
