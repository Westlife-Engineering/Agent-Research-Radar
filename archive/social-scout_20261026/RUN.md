# Agent abstention 社交媒体侦察试运行记录

日期：2026-10-26（Asia/Shanghai）。状态：本轮侦察完成；OpenReview最新投稿/评审覆盖未完成。研究判断在本次聊天交付，本文件只用于追溯试运行。不是正式知识库来源页，也不是已确认研究缺口清单。

## 授权与隔离

- 用户明确允许只在本目录新建规则和过程记录。已有AGENTS.md、workflows、Raw、Wiki、索引和日志均只读；未运行实验、训练、正式多Agent Brainstorm或AutoResearch，未执行Git提交或推送，未执行小红书写操作。
- 参考对话：chatgpt-conversation://6adeeaa6-dd44-83ec-b63b-d15a6687b988，已通过read_thread读取最后一轮完整建议。其作用是流程参考，不是学术证据。
- 启动时已有4个修改文件：wiki/foundations/Evolution.md、wiki/frontier/Overview.md、wiki/harness/Overview.md、wiki/harness/workflows.md。本轮未编辑它们。收尾检查仍显示这4个既有修改。
- 只读参考：wiki/index.md、wiki/log.md末尾、workflows/query.md、wiki/harness/hooks.md、wiki/harness/verification.md、wiki/frontier/Overview.md的相关部分；它们用于理解用户已有知识，不替代新论文原文。

## 检索执行与证据可见性

小红书MCP登录有效。6组成功查询，每组返回20条卡片，合计120次展示、95个不同帖子ID；这些数字只是检索覆盖记录，绝非95份已读证据。6篇详情实际读取。上限未用满，因已形成足够的问题与反证入口而收束。

| 查询 | 用途与实际效果 |
| --- | --- |
| agent abstention | 找到两篇核心工作、同篇转载和tool-call vector讨论；后半混入自进化热点。相同查询重跑一次以恢复首轮截断，未重复计数。 |
| Agentic Abstention，最新排序 | 超时，未获得可用结果；不能据此声称完成最新排序扫描。 |
| agent 停手 | 扩展到中文困难描述；出现停手、越权与死循环等候选。 |
| abstention 质疑 | 返回大量不相关投稿抱怨；没有得到充分的独立技术反驳。 |
| agent abstention ICLR | 多为审稿/投稿讨论；未定位可核验的ICLR 2027核心论文。 |
| agent 求助 不确定性 | 测试旧术语入口；读到一篇主要依赖图片的泛化知识卡，未作为技术证据。 |
| abstention 失败 | 找到HERA线索，构成有效的动态扩展。 |

全部成功查询的最小卡片索引见search-index.json。未保存xsecToken、账户资料、图片签名链接或完整评论用户资料。

### 实际读取的6篇详情

| 帖子 | 可读范围 | 处理 |
| --- | --- | --- |
| [关于Agentic Abstention，一点思考](https://www.xiaohongshu.com/explore/6ade1725000000002403a5e7) | 正文；MCP未返回评论；6张图未读 | 指向2610.09624；将工具调用倾向与合适弃权分开。个人猜想不当成论文结论。 |
| [NeurIPS撞车](https://www.xiaohongshu.com/explore/6ad8e614000000002c034bcd) | 正文、默认10条一级评论及已返回的部分回复；hasMore=true；3张图未读 | 提供两篇不同论文身份。评论提出可复现性疑问，但未给实证反例；不以点赞或评论共识为证据。 |
| [为什么你的Agent越努力，越可能浪费钱？](https://www.xiaohongshu.com/explore/6a43dff3000000001603c825) | 正文；无返回评论；18张图未读 | 同一2606.28733的二次传播，不增加独立研究信号；不直接转用宣传数字。 |
| [HERA: harness和环境协同优化智能体弃权](https://www.xiaohongshu.com/explore/6acde4db000000001203d5af) | 正文；无返回评论；1张图未读 | 指向2610.06563；回读方法及Table 1后收窄优势判断。 |
| [Agentstain: LLM代理知道什么时候不行动？](https://www.xiaohongshu.com/explore/6a5760c4000000002201b4c9) | 正文；无返回评论；1张图未读 | 标题拼写有误，正文身份对应AgentAbstain 2607.10059；不当成另一论文。 |
| [Agent遇到不确定情况怎么办？](https://www.xiaohongshu.com/explore/6a1edf3b000000000603498b) | 仅简短正文；4张知识卡未读 | 缺少可核查技术正文，不纳入重点判断。 |

详情形成4个论文身份线索：Agentic Abstention、AgentAbstain、HERA、Tool-Call Vector。其中前两者有不同团队；HERA与Agentic Abstention有共同作者，不能当作独立复现。未尝试补全任何未读图片内容。链接可能需要登录或失效后的重新搜索。

## 6篇原始材料的定向阅读与判断边界

页码均为PDF自第一页计数；下面不是全文精读或复现实验声明。部分材料以HTML读取正文，以PDF文本确定页码。仅两篇的关键页另作图像目视核查。

| 材料与版本 | 核查位置 | 本轮用途与限制 |
| --- | --- | --- |
| [Agentic Abstention，2606.28733v1](https://arxiv.org/pdf/2606.28733v1) | §2 p.3；§3 pp.4–5；§4.2与§5 p.6；§6相关结果；Appendix A p.16；Appendix F pp.23–24 | 顺序停止、CONVOLVE及终止式澄清。目视p.6与p.24确认：正文的环境型w=2、AbsRec@2与附录AbsRec@1/绝对步数公式口径存在需代码核对的差异。暂不判定实现有错，不把及时率提升直接写成现实中最优停止。 |
| [AgentAbstain，2607.10059v1](https://arxiv.org/pdf/2607.10059v1) | §§2.1–2.4 pp.3–5；§3 pp.5–8；Appendix A p.21 | act/abstain最小扰动配对、关键提交动作、事后弃权。实际动作与口头拒绝需同时核对。作者列出单次运行、合成确定环境、未覆盖澄清后多轮恢复及长程累积风险等限制；不把跨模型相关性当因果。 |
| [HERA，2610.06563v1](https://arxiv.org/pdf/2610.06563v1) | HTML §§3–5；PDF Table 1/2 p.7；Appendix E.2 p.20 | 失败驱动环境/harness共同演化，含固定验证集和替代路径检查。目视p.7确认：共同演化Pair=70.0，初始失败任务生成基线=73.3；不能说所有指标最优。60对测试的该差距对应2对，尚不能作显著性或普遍优劣判断。 |
| [How Do Agentic LLMs Decide to Call Tools?，2610.09624v2](https://arxiv.org/pdf/2610.09624v2) | HTML §§3–4.3、§10；PDF §10 p.10 | 机制干预能改变call/no-call，含原生多轮决策点转移；作者明确不评估工具选择、参数或最终任务正确性。不将抑制调用等同于校准弃权。 |
| [Robots That Ask For Help / KnowNo，CoRL 2023](https://proceedings.mlr.press/v229/ren23a/ren23a.pdf) | §2 pp.2–3；§3 pp.4–5；§6 p.8 | 求助与多步不确定性对齐已有旧工作。统计保证依赖校准条件、准确帮助和已落地的观测/动作等假设；不外推到任意工具Agent。 |
| [Check Yourself Before You Wreck Yourself，2510.16492v1](https://arxiv.org/pdf/2510.16492v1) | HTML §§3–5；PDF p.1会议身份 | 2025年已在ToolEmu中研究选择性退出；LLM模拟与打分限制需要保留。是NeurIPS 2025 Workshop on Regulatable ML，不是主会论文身份。 |

额外仅作导航/摘要线索，未加入6篇定向正文证据包：

- [Ask Early, Ask Late, Ask Right，2605.07937](https://arxiv.org/abs/2605.07937)：摘要已明确研究澄清时机；足以阻止“从未研究何时问人”的宽泛空白表述，尚不足以评判实验。
- [Pay-per-search models are abstention models / MASH，ICLR 2026提交PDF](https://openreview.net/pdf?id=Dm6lP9YEsM)：读取检索返回的摘要/片段，非完整论文核查；作为selective help-seeking近邻候选，不采纳性能数字或最终录用身份。

## 会议与OpenReview核查

- [NeurIPS 2026官方Downloads列表](https://neurips.cc/Downloads/2026)同时含两篇核心标题，对应条目链接分别为https://neurips.cc/virtual/2026/poster/150912（Agentic Abstention）与https://neurips.cc/virtual/2026/poster/139558（AgentAbstain）。详情页本轮无法抓取，不对具体presentation等级作额外确认。
- HERA作者页与arXiv只确认2026-10-05预印本；未确认ICLR 2027投稿或录用，不凭格式/发布时间推断。
- Tool-Call Vector arXiv v2 Comments写Accepted by NeurIPS 2026 Main Poster；这是作者登记信息，本轮未补齐会议详情页确认。
- OpenReview：关键词/年份定向检索未核验ICLR 2027对应条目；搜索页面读取失败；公开API只读请求HTTP 429；MASH论坛显示browser verification/429。未绕过验证，未登录或更改任何配置。未取得可引用的本轮核心论文公开评审。
- 因此本轮是小红书线索＋原论文定向核查，不是完整的NeurIPS/ICLR OpenReview趋势调查。旧年份论文不能替代2027覆盖。

## 分流与流程修订

| 问题簇 | 本轮分流 | 下一个区分证据 |
| --- | --- | --- |
| 什么时候有足够证据停止，而非只是没搜到？ | 优先值得brainstorm；先补一轮小核查 | 对齐最早应停时点、Agent可见观察、评分实现；核查等观察但可解/不可解的任务对。 |
| 弃权是否混合了终止、暂缓、求助及恢复？ | 值得补充核查 | 以KnowNo、澄清时机等近邻检查已有覆盖，再查核心基准收到澄清后是否续跑、如何计成本。 |
| 共同演化学到了可迁移停止条件，还是合成任务特征？ | 值得补充核查，第二优先 | 对齐生成预算、同源/异源测试、逐对结果及checkpoint选择；从Table 1的边际率与Pair差异入手。 |
| 控制工具调用倾向是否足以支持合适弃权？ | 保留观察；机制区别了解即可 | 同时报告错误调用减少、正确调用损失及最终任务结果，排除普遍抑制解释。 |

本轮未确认领域新颖研究缺口。所有竞争解释都是试运行推断/待验证假设。以“2026年最近几篇工作开始把及时性、动作后果和成对评测放在同一研究图景下”描述观察；不称为首次发明不确定性/求助，也不从首次扫描推断热度上升。

建议在后续试运行中保持：

1. 查询分成精确词、中文困难、旧术语、反例四类；两次泛化查询噪声过高就转论文引用，不无限加关键词。
2. 按arXiv/标题/作者去重，并标明共同作者/同一系列；帖子热度只帮助发现，不评价证据。
3. 优先核对一条能改变判断的结论，再决定是否补读；本轮有效纠正了“新方向从零出现”“抑制工具=可靠弃权”“共同演化所有指标最好”。
4. 补读必须含最接近旧工作、方法/指标原文与一个反例入口。社交评论没有技术反证时明确说没有，不伪造争议。
5. 保存检索失败、图片未读、平台身份不明、正文与指标口径差异；不要让缺失被流畅总结掩盖。
6. 后续趋势比较需要可比较的时间窗/查询/排序；本轮综合搜索和一次最新排序失败不足以建立时间基线。

## 建议的下一轮文献型AutoResearch（未启动）

只处理一个不确定性：现有及时弃权评测中的“应停时点”，是否由Agent当时可见的证据决定，还是主要依赖构造者的隐藏标签/预设步数？

范围：Agentic Abstention的指标实现/少量公开轨迹，与AgentAbstain/HERA对应的阻塞证据判定对照；最多3份关键材料、一次针对性补充，不跑模型或实验。

竞争解释：A，观察已足够但模型不使用；B，观察不足，继续搜索合理；C，改善主要来自更保守的倾向或任务模板。反例必须含可修复的工具故障，以及不同搜索路径得到相同首次失败结果的可解任务。

- 继续：找到可核对的逐步观察与标注不一致，且近邻尚未解释，需要收窄评测问题。
- 改写：实现已正确处理证据时点，问题转为证据识别/使用；或已有澄清研究覆盖了宽泛设想。
- 停止：现有材料直接解释疑点；缺少逐步轨迹/代码不能验证；必须实验才能区分；或预算耗尽。停止不等于否定整个方向。

## 收尾

关键PDF页面已目视核查，临时渲染图在验收后移除。隔离目录保留AGENTS.md、RUN.md和search-index.json。未生成正式论文笔记或成果报告副本；未宣称Obsidian应用验收。仅检查本目录文件、引用结构与Git状态，不运行会把隔离试验当作正式来源的全库摄入流程。
