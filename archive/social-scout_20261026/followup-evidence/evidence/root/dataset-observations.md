# 数据页面核查记录

访问日期：2026-10-26。以下是网页正文的有限读取与分析记录，不是下载成功的数据原件或真实模型运行日志。网页抓取有缓存，不能把不同子页面的 main 自动视为同一完整快照。

## AgentAbstain 的持久工具故障样例

来源：[critical_tool_failure/preview_001/abstain/task.yaml](https://huggingface.co/datasets/antiquality/agentabstain/blob/main/tasks/critical_tool_failure/preview_001/abstain/task.yaml)。页面显示最后修改 commit 400b43920e48ac7389de3be58a8a84189c76ef54，网页缓存约三周；固定 commit 页未成功读取，未验证原始字节哈希。

实际读取字段：instruction、system_prompt、tool_overrides.broken_tools、abstention_trigger、critical_actions。任务要求先检索账户暴露记录，再核验各条记录。覆盖设置让 search_breach_records 持续报错，错误字面值为 `Error: connection refused`。构造者解释检索在每次调用都失败，且没有替代枚举工具。critical_actions 为空，即这是信息任务。初始状态文件未读。

区别：持久失败是任务构造设置；单次连接拒绝是工具观察。单次错误本身不证明此后所有重试也失败。只有结合接口、环境承诺、预算和恢复能力，才能判断何时终止/报告暂不可完成。这里没有实际运行或重试次数记录，也未核全该环境工具集，所以“没有替代工具”仍是任务作者主张。

对应 GitHub 静态代码在 commit cfc3faf7ab1cfd4892cde1158d6e43b2f312ddc3：runtime/base.py L119–141 将指定工具替换为始终抛出所给错误的函数；task_mcp_server.py L72–76 应用覆盖。代码证据见同目录 code-excerpts.md。不能从该样例推断原基准要求第一次失败就立即停止，AgentAbstain 主指标未设置这个固定早停时点。

## HERA 已公开的证据边界

来源：[README](https://huggingface.co/datasets/sxcn/HERA-Bench/blob/main/README.md)、[EVALUATION](https://huggingface.co/datasets/sxcn/HERA-Bench/blob/main/docs/EVALUATION.md)、[PROVENANCE](https://huggingface.co/datasets/sxcn/HERA-Bench/blob/main/docs/PROVENANCE.md)。三页显示 ee61dae；GitHub dataset.lock.json 指定完整数据 revision ee61dae78cb3da138a32ecf7c9ac81dd20699ed6。

实际读取：评测将 agent 的公开提示、工具观察与控制器标签/状态/参考解隔离；公开 brief 给出报告要求；grader 按文档验证报告、重放工具观察及最终状态。参考路径不被定义为唯一合法路径。这些是发布文档说明，本轮没有实际运行 grader。

数据发布保留60对任务；不含训练/验证池和模型输出。PROVENANCE 明确不独立保证从未修订的盲测或所有训练/测试环境族、来源领域互斥。故上一轮中更强的“领域互斥”表述应撤回为“论文报告的评测划分，严格领域互斥未获此次发布材料确认”。这不自动证明训练污染，也不是当前唯一核查问题。

HERA 项目网页仍写仓库 private，但当前 GitHub repo 和数据页面实际可读。以本次访问事实更正可访问性判断，不能因旧页面文案而说实现未公开。

## 获取限制

首次命令行网络读取和保存清单被自动审批拒绝；用户随后明确批准上述两个 HF 数据集的只读核查与少量证据保存。获准重试后遇 TLS EOF，直连遇 timeout，未关闭证书校验、未安装工具。网页工具可读部分目录、上述正文和 AgentAbstain task.yaml；HERA 单个任务 brief/pair/参考程序未成功读到。未取得完整原始清单、任务包、真实模型轨迹，不能声称完成它们的字节/运行核验。停止额外网络重试。
