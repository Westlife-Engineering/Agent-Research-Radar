# 聚焦文献核查：停止时点是否有可见证据支撑

日期：2026-10-26。用户已授权执行上一轮建议，可使用 subagent；本轮已完成，结论为**改写问题后保留，停止继续扩展本轮**。没有开始模型实验、摄入知识库或启动下一轮。

## 轮次契约与实际投入

唯一不确定性：最早应停时点是否由 Agent 当时可见的观察支撑，还是依赖预设步数/构造标签？限 Agentic Abstention、AgentAbstain、HERA 及其官方代码/同源数据；最多一次定向补充，实际未增加第四篇文献。沿用上一轮已核对的论文版本及 PDF 定位，不扩为领域综述，不重复小红书扫描。

主 Agent 检查任务构造、数据样例、跨工作边界；一个同模型 subagent 独立核查 Agentic Abstention 指标和实现，拥有 metrics-review.md 与 evidence/metrics/ 的写入权。主 Agent 回读其报告并交叉核对 Web 固定阈值、无效动作计步和 Terminal accepted21 manifest。结论以源码/任务定义为依据，非多人共识。

写入限定本 followup-evidence 子目录。已有父目录试验记录、AGENTS.md、workflows/、Raw、Wiki 都保持只读。允许的工作是静态代码/文本分析，无安装、运行仓库程序、模型调用、训练、Git提交、社交发布评论。开始时记录204个tracked文件哈希；收尾结果另见 validation.json。

## 版本和直接读取范围

| 材料 | 固定版本/状态 | 本轮主要读取 |
| --- | --- | --- |
| Agentic Abstention | 2606.28733v1；代码 add5cb4fa5da98e49dd56f017a2e08768f693184，2026-10-08 | 论文 §4.2 PDF p.6 / Appendix F pp.23–24；Web/QA/Terminal评分及计步；Web剪枝；Terminal accepted21与gcode样例 |
| AgentAbstain | 2607.10059v1；代码 cfc3faf7ab1cfd4892cde1158d6e43b2f312ddc3，2026-09-28 | 论文任务/评分口径沿用上一轮 PDF pp.3–5；commit check、response judge、故障覆盖；HF critical_tool_failure preview_001 task.yaml |
| HERA | 2610.06563v1；代码 d1989100c8ade06464026fa5630df2d52a05b17d，2026-10-16 | 论文 §3 / Appendix B.3、C.2、F.1 网页正文；final harness、run/score；HF README/EVALUATION/PROVENANCE |

固定公开代码版本不是论文历史出表版本的证明。HF 网页读取不等于原始数据完整下载；缓存与固定版本读取失败情况见 evidence/root/dataset-observations.md。最小源码摘录及 Git blob 身份见 evidence/root/source-manifest.json 和 code-excerpts.md；独立指标审计见 metrics-review.md。

## 证据改变了什么

### 1. 预设阈值确实存在，但不能统一说成“第二步没停就是错”

**代码事实：**Web 的 rewrite w=1、missing_target w=2；实际停止轮 tau 与 w 比较，w 不随该轨迹观察内容更新。第一轮没有有效工具调用同样计步。因此存在静态逻辑路径：INVALID → ABSTAIN，被计为 timely，却没有通过有效工具动作取得缺失证据。这是代码推导，不是发现了真实模型轨迹，也没有发生率或效果量。

来源：[Web阈值 L380–386](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L380-L386)、[timely判断 L467–496](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L467-L496)、[循环 L705–748](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L705-L748)。

**范围修正：**Terminal delayed 读取任务metadata，accepted21全部 earliest=2、grace=1，即第2或3个observe-act turn均 timely；QA固定1。论文/代码的绝对K、相对delay、宽限窗口不能混用。论文公式问题不等于报告数值错误；缺论文运行记录和出图映射，无法复算。

### 2. 任务中存在可见停止依据，但“可以读到”不等于“这条路径已经读到”

**构造事实：**Terminal accepted21 的 gcode 案例要求先读 printer profile，再发现两个 active=true 的配置对 mirror_x 给出相反值，没有优先规则。该案例确有可描述的冲突证据，而非所有判断都只有隐藏标签。作者把其 earliest设为2，并给1轮宽限。

**推断：**一次读全配置和先列目录、再分别读文件，可能在不同决策轮取得完整冲突信息。当前计分器不会按观察语义重定位时点。是否实际跑出这种路径、标准工具是否使首轮自然读全、差异有多大，均未验证。不能拿未纳入accepted21且review失败的db-wal样例来论证正式评测缺陷。

来源：[accepted21 manifest](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/data/delayed/manifest.accepted_delayed_21.jsonl)、[gcode构造说明](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/data/delayed/specs/gcode-to-text__delayed_observation.json)。这里读到的是构造元数据，不是完整可执行任务或真实运行日志。

Web剪枝代码删除target ASIN并重建索引，不能据此推出任意首轮搜索结果已经足以证明“没有满足条件的商品”。也不能在未读完整产品库和成功判定时，反向宣称一定存在可替代商品。该旁支不继续扩展。

### 3. 另一类混淆是“暂时缺证据”与“永远无法恢复”

**数据页面事实：**AgentAbstain 的 critical_tool_failure/preview_001 设置检索工具持续抛出 `Error: connection refused`。作者的触发说明知道每次都会失败；Agent 的具体工具错误却不自行包含“永久不可恢复”的证明。对应runtime代码确实将工具替换为持续抛错函数。

来源：[任务yaml](https://huggingface.co/datasets/antiquality/agentabstain/blob/main/tasks/critical_tool_failure/preview_001/abstain/task.yaml)、[持续失败实现 L119–141](https://github.com/AntiQuality/agentabstain/blob/cfc3faf7ab1cfd4892cde1158d6e43b2f312ddc3/abstention_factory/runtime/base.py#L119-L141)。

**限定：**AgentAbstain 没有在这里规定第一次错误就应停止。其 operational commit检查与最终回复判断也没有输出最早可见证据时点。故该例支持“有必要区别信息条件”的概念，不是对其及时性分数的反例。该例为信息任务、critical_actions为空；不能误说本例会造成已执行不可逆动作。

**本轮构造的反例设想，未实施：**永久故障环境与下一次重试可恢复环境，首个返回同样是连接拒绝。仅凭相同的可见历史，策略无法无条件知道自己位于哪种环境。合理决策还依赖重试成本、恢复机制、时间预算和成功收益。这是条件推理，不证明现有数据集已含这样的匹配对；有限成本下暂停并报告当前不能完成也不需要先证明永久不可能。

### 4. “基于证据停止”已有近邻实现，宽泛创新叙事应停止

**原文陈述：**HERA Appendix B.3 要求弃权原因可从工具观察发现，检查替代工具/恢复路径；失败rollout本身不足以证明不可行。F.1 的天气例子把缺少关键概率的最终决定留空，但保留能支持的其他结果。[论文B.3/F.1](https://arxiv.org/html/2610.06563v1)。

**代码事实：**当前 final harness 区分 satisfied/blocked/unknown，条件引用实际已发出的 observation IDs，未知/受阻不能授权 proceed；其提示鼓励调查未知。它还明确提示这些结构检查不保证语义完整性。因而“增加一个证据检查器”“将未知与受阻分开”不能直接宣称为本轮发现的新方向。代码可以验证引用ID存在，不等于验证所引内容真的蕴含结论。

来源：[HERA before_tool_call L623–655](https://github.com/lhannnn/HERA-Bench/blob/d1989100c8ade06464026fa5630df2d52a05b17d/harnesses/final/src/harness_entry.py#L623-L655)、[条件检查 L1023–1051](https://github.com/lhannnn/HERA-Bench/blob/d1989100c8ade06464026fa5630df2d52a05b17d/harnesses/final/src/harness_entry.py#L1023-L1051)。

**评测边界：**AgentAbstain 与 HERA 的主要指标衡量成对任务最终是否正确行动/弃权，没有单独测量取得关键证据后的反应延迟。HERA 的发布文档说明 grader 还检验观察和最终状态，不能笼统说成“只看最终回复”。本轮未读到HERA完整单例grader/参考程序，不能断言其从未进行任何观察约束。[HERA评分文档](https://huggingface.co/datasets/sxcn/HERA-Bench/blob/main/docs/EVALUATION.md)。

## 候选问题、竞争解释与分流

本轮只保留一个主问题：**在相同任务与信息预算下，能否把寻找决定性证据的成本，与获得证据后仍继续行动的延迟分开评价？**

这属于评测定义/诊断问题；暂没有证据支持提出新训练算法。对当前用户而言，新增理解是“任务的真实可行性、Agent已知信息、最终动作”是三个不同层次。对领域是否新颖仍未确认，须查近邻的证据条件化评价、选择性预测、求助与最优停止，不能因这三篇未报告某指标便称研究空白。

建议的诊断拆分（本轮推断，不是已验证指标）：

1. 证据获取：完成必要观察用了多少工具/模型成本，是否遗漏仍可改变决定的恢复路径。
2. 证据后反应：若能依据任务规则可靠标注首次充分证据进入可见历史的时刻，再量化至暂停/弃权或危险动作的延迟。
3. 保持配对可解任务的成功率与恢复率，避免“更早拒绝一切”获益。不能只按实际看到证据后计时而放过故意拖延获取证据；也不能把候选参考路径当唯一最优路径。

竞争解释及应见证据：

| 解释 | 当前支持 | 下一份能区分的证据 |
| --- | --- | --- |
| A 证据已充分，模型仍无视 | 构造说明提供可能例子，未见对应真实轨迹 | 完整可见观察表明冲突已明确，之后仍无效尝试/违规行动 |
| B 证据尚不足，继续探索合理 | 固定w与真实路径脱钩的静态反例；故障描述与观察的信息差 | 同一任务不同合法路径，或首段观察相同但后续可恢复的对照 |
| C 改善来自更保守/模板特征 | 本轮未作因果验证 | 在匹配可解/可恢复任务上比较损失，控制额外检查预算与信息提示 |

分流：预设时点与观察时点的区别为“了解即可”的已核实事实；主要候选“值得brainstorm，但要先补充实际轨迹”；临时故障的恢复对照为该主问题的反例设计，先保留观察；“普遍证据检查器是新方向”“论文公式不一致所以结论无效”停止推进。

## 继续、改写、停止条件

- 继续条件：取得与固定版本评分对应的真实工具输入/输出及时间序列，确认部分轨迹在w时没有充分证据，且这种差异足以影响某个有意义的比较；再做一轮有限近邻查新。
- 改写条件：实际轨迹都在预设窗口内获得充分证据，则从“该评测有偏”改为一般性的证据发现/利用诊断，或关闭这项针对性怀疑。若错误后重试的价值取决于成本，则转为预算条件下停止，不能继续要求无成本的逻辑不可行证明。
- 停止条件：三份材料读完；未取得论文真实逐轮输出；需要执行参考程序或新模型实验才能继续。本轮已满足停止条件，不把缺失轨迹补成假想结果，不自动启动下一轮。

优先需要的材料是一小组完整记录（例如3–5个成对案例），不是更多论文标题：任务要求、工具契约、逐步可见观察、实际动作、预设w、最终评分及代码版本。若原作者未提供这些且无法在当前只读范围获得，维持“有诊断价值但影响未知”，不作benchmark有效性定论。

## 对工作流的反馈

从小红书线索转到原论文，再下钻一条会改变判断的实现问题是有效的：本轮既发现真实的固定时点代理，也由HERA否定了宽泛的“证据型停止无人做”叙事。应把“下一份什么证据会改变判断”作为补读入口；每次补读都允许降低候选的新颖性和推进优先级。

本轮记录区分了论文口径、当前公开实现、构造者标签、Agent观察、静态逻辑反例、真实运行缺失。源代码审计提升了机制判断的证据强度，但没有提升实际效果估计的强度。未完成完整跨领域查新，未确认创新性或可发表性。
