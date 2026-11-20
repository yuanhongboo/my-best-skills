# 项目指令示例

选与项目主要职责相符的一份，将其中适用的部分复制到项目根目录的 `AGENTS.md`。已有项目指令时，保留其中的产品决策、真实入口和权限约定，合并相关段落。对混合项目，可以把只在某个子目录生效的规则放入那个子目录。发布、发送、账户变更等操作的授权来自实际任务，模板只描述如何核对范围与结果。

| 要处理的主要问题 | 建议起点 |
| --- | --- |
| 组件公开接口、消费者类型及浏览器交互 | [前端组件库](component-library/AGENTS.md) |
| 画布、属性面板、撤销和持久化的一致性 | [可视化编辑器](visual-editor/AGENTS.md) |
| 采集端过滤与旧记录回放 | [记录与回放工具](capture-replay/AGENTS.md) |
| 本地可用但打包后缺少文件或入口 | [命令行工具与多包发布](cli-release/AGENTS.md) |
| 学习者亲自完成代码，代理教练与评阅 | [亲手实践课程](tutored-course/AGENTS.md) |
| 模型、工具、插件及领域生命周期的分工 | [可扩展代理运行时](agent-runtime/AGENTS.md) |
| 任务恢复、重试、人工审核和投递状态 | [任务调度与执行器](task-runner/AGENTS.md) |
| 生成的新工程能否在仓库外独立使用 | [模板与脚手架生成器](template-generator/AGENTS.md) |
| 服务生命周期、路由归属与回滚 | [服务编排与维护](service-orchestration/AGENTS.md) |
| 告警证据、根因归属和恢复验收 | [告警分诊与诊断](incident-triage/AGENTS.md) |
| 来源去重、覆盖缺口及定期报告 | [资料跟踪与定期报告](research-monitor/AGENTS.md) |
| 历史信息可用时间、回放与实验可复现性 | [历史数据与决策仿真](simulation-lab/AGENTS.md) |
| 玩家输入、真实可达关卡与旧存档迁移 | [互动游戏](interactive-game/AGENTS.md) |
| 文章正本、公开资源、导航和订阅 | [技术内容网站](editorial-site/AGENTS.md) |
| 脚本、音画、字幕和发布成片的阶段验收 | [音视频制作](media-production/AGENTS.md) |
| 管理动作的目标集合、重试与操作回执 | [应用账户管理](account-operations/AGENTS.md) |
| 技能触发、相对资源和目录维护 | [技能与项目指令库](skill-library/AGENTS.md) |

需要给独立审阅者一份可单独理解的工单时，使用[独立审阅模板](../workflows/independent-review.md)。
