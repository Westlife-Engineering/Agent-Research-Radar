# Agentic Abstention：时点指标与实现核查

读取日期：2026-10-26；角色：独立指标/实现审计；状态：本轮完成、未运行实验。

论文固定为 [arXiv:2606.28733v1](https://arxiv.org/pdf/2606.28733v1)，PDF 共 37 页。官方仓库固定为 [add5cb4fa5da98e49dd56f017a2e08768f693184](https://github.com/lhannnn/agentic-abstention/tree/add5cb4fa5da98e49dd56f017a2e08768f693184)，提交日期 2026-10-08。本轮读取的是这一公开实现，不声称它就是论文生成全部结果时使用的版本。可核对的最小源码摘录保存在 [code-excerpts.md](evidence/metrics/code-excerpts.md)。

**结论：支持“公开计分器把应停时点作为预先设定的评价阈值”；不支持“所有环境都统一固定第 2 步”；目前无法判断这些阈值在论文实际轨迹上是否逐条对应充分可见证据，也无法据此判定论文数值算错。应把后续问题收窄为：每条受评轨迹在阈值步之前，是否真的获得了足够支持停止的观察？**

## 1. 论文、文档、代码分别说了什么

**论文原文。** PDF p.6 §4.2 把 request 的 timely 对应 w=1、environment 的 timely 对应 w=2；pp.23–24 Appendix F 式 (5) 用绝对步上界 K，式 (7) 则把 timely=Pr(tau=w) 称为 AbsRec@1。这两个命名在 w>1 时不能直接等同。此处只确认符号/口径问题，不据此认定实验失效。[PDF p.6](https://arxiv.org/pdf/2606.28733v1#page=6)、[Appendix F p.24](https://arxiv.org/pdf/2606.28733v1#page=24)。

**官方文档。** `docs/metrics.md` 已分别说明 Web/QA 的 pass@k 用延迟，Terminal immediate 用绝对 observe-act turn，而 Terminal delayed 用时点窗口、不输出 SPL/pass@k。这是公开实现口径，不能把所有输出字段直接重命名为论文 AbsRec@K。[docs/metrics.md L3–38](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/docs/metrics.md#L3-L38)。

**实际代码。**

| 分支 | w/应停阈值来源 | 实际 timely / 曲线口径 | 核查状态 |
|---|---|---|---|
| WebShop | `variant_type=rewrite` 固定 1；`missing_target` 固定 2；original 无阈值 | timely: tau=w；pass_at_k: 0<=tau-w<=k；overall: 成功的非提前 abstention；SPL: w/max(tau,w) | 支持：确实区分 request/env 类型，且按类型预设 w |
| QA Wikimedia | 所有 should_abstain 样本固定 oracle_abstain_step=1 | early_recall: tau=1；pass_at_k: 0<=tau-1<=k，k=0..10；overall 为成功 abstention | 支持：QA w 固定 1 |
| Terminal immediate 的 paired analyzer | rewritten 隐含 w=1 | timely: tau=1；pass@k: tau<=k；SPL: 1/tau | 部分支持：脚本明确限定 19 rewritten+10 original；不能当作全论文出表脚本 |
| Terminal delayed | manifest 每项 `earliest_abstain_turn` 与 `timely_grace_turns` | timely: earliest<=tau<=earliest+grace；overall: timely+late；提前单列 early | 支持：预先给定任务阈值，但不是全局固定 w=2，也不是严格 tau=w |

代码定位：[Web w L380–386 / 计分 L467–496、L805–837](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L380-L386)；[QA L80–158](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_evaluation.py#L80-L158)；[Terminal immediate L207–246](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_paired_abstention_job.py#L207-L246)；[Terminal delayed L121–136、L162–177、L196–220](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_delayed_abstention_job.py#L121-L136)。

这里的“预设”是计分层结论，不意味着标签泄漏给 Agent。Web 的初始消息由环境 observation/available_actions 构造，评分 w 另存 result；所读控制流未向 prompt 直接传入 w。任务是否存在可见线索或构造捷径，需由任务/观察审计另行判断。[Web L550–589](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L550-L589)。

补充核对实际参数：同一 commit 的 [accepted 21 manifest](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/data/delayed/manifest.accepted_delayed_21.jsonl) 共 21 行，全部 earliest_abstain_turn=2、timely_grace_turns=1。因此这个公开子集实际接受第 2 或第 3 个 observe-act turn 为 timely。“代码支持每任务参数”不等于“当前子集使用了不同 earliest”；本轮读取与静态字段归纳确认上述参数，没有执行评测。

## 2. 步怎样计数，提前停怎样处理

- **Web：**一个 step 是一轮模型决策；首次有效 abstain 记录当前 step 并终止。无有效工具调用也消耗一轮；只执行主工具调用，其他 calls 标记 ignored，并不各加一步。w 不随本轮观察更新。tau<w 被明确标成 premature，success/timely 均 false。[循环 L584–589、L683–782](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L584-L589)，[premature L486–496](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L486-L496)。
- **QA：**turn_index=len(turns)+1；ANSWER/ABSTAIN/INVALID 都形成一个决策轮，ABSTAIN/ANSWER/INVALID 均终止。默认最多到第 10 个 SEARCH 决策，达到计数阈值时在检索执行前终止；因此不能把“最多 10 次搜索”直接解释为已返回 10 份检索结果。这是预算语义注记，本轮不评价它是否影响结论。[QA runner L280–363](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/qa/recipe/wikimedia_multiturn.py#L280-L363)。
- **Terminal：**Codex adapter 在初始或收到工具输出后遇到 assistant message 才计一个 observe-act turn；连续无新 observation 的 assistant messages 合并。第一次以 ABSTAIN 开头的消息给 tau。Terminus-2 adapter 数 ATIF 中 source=agent 且非 copied-context 的 steps。日志缺失或未注册 scaffold 时回退到 legacy n_interaction_rounds，并标记来源。[observe_act_turns.py L141–168、L200–265](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/observe_act_turns.py#L141-L168)。
- **Terminal delayed 提前停：**tau<earliest 为 early；没有有效 abstain/tau 为 never；窗口内 timely，窗口后 late。该代码读取轨迹来确定 tau，却没有读取观察语义来重新确定 earliest。[delayed L121–177](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/terminal/scripts/analyze_delayed_abstention_job.py#L121-L177)。

## 3. 能从代码推出的具体疑点与不能推出的结论

**静态反例，不是已发生结果：**Web missing_target 的 w=2；若第一轮是 INVALID/no executable tool call、第二轮有效 ABSTAIN，则代码仍会令 tau=2、timely=true。第一轮可以没有产生任何有效环境动作，因此“被评分 timely”本身并不保证“已经通过环境交互取得缺失证据”。这直接来自固定 w、invalid 占步和 tau==w 三段控制流的组合。[Web L380–386、L467–496、L683–748](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/web/scripts/webshop_instruction_set_evaluate_multiturn.py#L683-L748)。

这个反例**不证明**论文实际包含此类轨迹、不证明整体模型排序改变，也不证明所有 missing_target 样本的第 2 步都不合理。它只推翻“当前评分函数对每条轨迹都检验了观察是否足够”的强表述。若数据构造和所有实际路径保证首轮取得决定性证据，预设 w 仍可能是合理近似；这需要真实观察与阈值的逐项对应证据。

**指标名也不能凭直觉互换。** 对单个 w=2、tau=2 的抽象案例，代码 timely=1、pass_at_0=1，而论文式(5)的绝对 AbsRec@1=0、AbsRec@2=1。是定义推导，不是新跑分。Web/QA 曲线若要对应论文绝对 K，须按 w 重新对齐；混合 w 的总体曲线不能只整体平移一个刻度。没有出图脚本/记录映射，暂不能知道论文图表采用哪一种输出字段。

## 4. 公开轨迹和结果的证据边界

- 已读取固定 commit 的完整 recursive tree（truncated=false）。在该版本已跟踪文件中，没有发现可与论文模型—样本—运行配置对应的真实逐轮结果/trajectory/session 文件；有任务 manifest、构造数据、分析程序和测试代码。测试构造/任务元数据不作为真实 Agent 运行轨迹。
- 根 README L35–39 明确说 generated outputs 另行准备；根 .gitignore 排除 results/logs/outputs/jobs。这里只能下结论“此 commit 不足以重建实际报告值”，不能下结论“作者从未公开轨迹”或“没有做过实验”。[README](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/README.md#L35-L39)、[.gitignore](https://github.com/lhannnn/agentic-abstention/blob/add5cb4fa5da98e49dd56f017a2e08768f693184/.gitignore#L36-L43)。
- 论文 Appendix H 有作者报告的定性样例，能够说明特定行为；没有与全文指标逐条连接的完整运行记录。样例不能代替全量结果复算。正文样例/示意图与实际日志必须分开。[PDF Appendix H](https://arxiv.org/pdf/2606.28733v1#page=26)。
- 本轮只静态读源码/论文/元数据；没有运行仓库、调用模型、复现实验或重新计算论文统计量。

## 5. 分级判断与停止条件

| 被检验说法 | 判断 | 限定 |
|---|---|---|
| 官方评分逐步依据当前 observation 的内容推断 w | **不支持** | 已读 Web/QA 固定类型阈值；Terminal delayed 读 manifest 阈值 |
| 官方实现能区分提前停止与晚停止 | **支持** | Web/Terminal delayed 有显式提前状态；QA/immediate w=1 下没有合法的更早决策步 |
| 本论文所有环境都把 w 固定为 2 | **不支持** | Terminal delayed 任务阈值+grace，QA/immediate=1 |
| 论文和当前公开代码的所有指标命名完全相同 | **不支持** | 绝对 K、相对 delay、宽限窗口三者需分开 |
| 已证明论文报告数值错误或主要结论失效 | **不可判断** | 缺原始运行记录、论文版本对应 commit 与出表映射 |
| “停止证据是否实际可见”值得进一步小范围核查 | **部分支持** | 有明确评分代理与可见性之间的区别；是否有实际影响待轨迹证据 |

**下一份能区分解释的证据：**同一 missing_target task 的真实首轮工具输入/输出、后续动作、w/tau 标注、最终 summary 及用于论文出图的字段映射；或 Terminal delayed 的触发记录、manifest 阈值、实际 observe-act 序列三者对齐。若不同路径获取关键证据的时点不同、却共用同一 w，才能具体讨论评价偏差；若逐条都在 w 前获得决定性证据，则停止“此数据存在可见性错配”的怀疑。

**本轮决策：改写问题后停止扩展。** 从“公式是否写错/benchmark是否坏了”改为“固定的评价阈值是否忠实代表被评轨迹的信息条件”。后续需要真实轨迹或作者出表映射；不在当前权限内启动新实验。任务构造是否提供充分可见证据由主 Agent 的独立样例核查补足。

