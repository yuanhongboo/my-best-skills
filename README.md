# my-best-skills

可以单独安装的 Codex 技能，以及可复制到自己项目的协作指令。比如，同一份代码变更可以交给独立检查者验收；同一堂编程课则由学习者亲手写代码，Codex 负责讲解和评阅。按任务选一份技能或项目指令即可。

| 想做什么 | 从哪里开始 |
| --- | --- |
| 设置个人协作习惯、普通代码审查和首轮标题 | [全局 AGENTS.md 示例](examples/global/AGENTS.md) |
| 给当前项目约定职责、目录和验收方式 | [项目指令选择指南](examples/projects/README.md) |
| 准备独立审阅的工单 | [审阅工单](examples/workflows/independent-review.md) |
| 做只读复盘或按日期生成报告 | [只读复盘](examples/automations/read-only-work-review.md) · [周期报告](examples/automations/daily-evidence-report.md) |

## 跨项目使用的技能

| 技能 | 什么时候用 |
| --- | --- |
| [对话命名](skills/conversation-title-naming/SKILL.md) | 依据创建时间和对话主题改名，并回读实际标题 |
| [交接文档](skills/agent-handoff-brief/SKILL.md) | 把现有进度、证据和下一步交给新的执行者 |
| [技术图文写作](skills/reader-first-tech-writing/SKILL.md) | 把源码与实验材料写成读者能跟上的技术文章 |
| [发布稿审阅与修订](skills/engineering-publication-edit/SKILL.md) | 为公众号、社交平台或技术专栏准备有依据的成稿 |
| [中文局部精修](skills/chinese-copy-edit/SKILL.md) | 诊断或修改指定段落，保留术语和作者判断 |
| [管理 Obsidian 笔记](skills/obsidian-vault-workflow/SKILL.md) | 定位正确的库，按现有目录、命名和双链组织笔记 |
| [岗位评估与申请材料](skills/job-opportunity-review/SKILL.md) | 判断岗位是否值得推进，按请求准备简历或面试材料 |
| [岗位扫描报告](skills/job-scan-report/SKILL.md) | 复核岗位来源，区分报告就绪、入队与投递回执 |
| [HyperFrames 视频制作](skills/hyperframes-video-production/SKILL.md) | 根据脚本、实测配音和画幅检查视频、字幕与封面 |
| [换装分镜](skills/outfit-transition-storyboard/SKILL.md) | 保持首帧、人物和换装动作在整段视频中的连续性 |
| [领域知识地图](skills/source-led-knowledge-map/SKILL.md) | 给一个主题建立问题索引、证据和更新记录 |
| [市场数据快照核验](skills/market-snapshot-audit/SKILL.md) | 核对数据时点、可比口径、报告与图表 |
| [移交审阅材料](skills/review-artifact-handoff/SKILL.md) | 核查文件包、版本和交付回执 |

## 适合安装在项目内的技能

| 技能 | 什么时候用 |
| --- | --- |
| [规格变更工作流](project-skills/spec-change-workflow/SKILL.md) | 从需求和场景走到实施、变更、验收与归档 |
| [独立产品 QA](project-skills/independent-product-qa/SKILL.md) | 按真实入口检查产品，并交付可复核的问题报告 |
| [文档编辑历史](project-skills/document-edit-history/SKILL.md) | 检查撤销、重做、重放和保存的语义 |
| [多代理派发](project-skills/delegate-project-work/SKILL.md) | 分配互不干扰的工作，约定决策与复核责任 |
| [文章独立冷读](project-skills/reader-cold-review/SKILL.md) | 从首次阅读者的视角检查理解障碍 |
| [代码风格审查](project-skills/change-style-audit/SKILL.md) | 对实际改动结合项目标准、指标及上下文做审阅 |
| [变更交付](project-skills/review-change-delivery/SKILL.md) | 核对提交、拉取请求、检查及合并各自的状态 |
| [项目故障调查](project-skills/investigate-project-defect/SKILL.md) | 从现象和反例定位原因，再验证修复 |

## 安装与试用

```sh
git clone https://github.com/yuanhongboo/my-best-skills.git
cd my-best-skills
```

全局技能复制到用户技能目录。项目技能复制到目标项目的 `.agents/skills/`。复制整个技能目录以带上引用和脚本。下例只安装两个技能；若目标已有同名目录，先对照内容，保留本地改动。已使用其他受支持技能目录时，沿用现有位置即可。

```sh
mkdir -p "$HOME/.agents/skills"
test -e "$HOME/.agents/skills/agent-handoff-brief" || cp -R skills/agent-handoff-brief "$HOME/.agents/skills/"

# 将此变量设为自己的项目目录
project_dir=../your-project
if test -d "$project_dir"; then
  mkdir -p "$project_dir/.agents/skills"
  test -e "$project_dir/.agents/skills/independent-product-qa" || cp -R project-skills/independent-product-qa "$project_dir/.agents/skills/"
fi
```

新会话中可以说“使用 `$agent-handoff-brief` 写一份交接说明，列出下一步可以复核的证据”。在安装了项目 QA 技能的工程中，可以说“使用 `$independent-product-qa` 只审查购物车的撤销操作，列出复现步骤”。安装机制见 [Codex 技能说明](https://learn.chatgpt.com/docs/build-skills)。

使用项目 `AGENTS.md` 时，从[项目指令列表](examples/projects/README.md)选取适用段落，合并到项目根目录或相关子目录。使用全局示例时，将需要的段落合并进自己的 `AGENTS.md`。希望配置模型时，参照[基础模型示例](examples/global/config.example.toml)合并两个键，备用 CLI 配置见 [astra-max.config.toml](examples/global/astra-max.config.toml)。可用模型以自己的宿主目录为准。

## 使用 conversation-title-naming

在具备对话列表、读取和改名工具的宿主中调用：

```text
使用 $conversation-title-naming 规范当前对话标题，并回读核验。
```

需要**每个新对话首轮自动命名**时，将下面的触发规则合并进全局 `AGENTS.md`（位于 `CODEX_HOME`，未设置时为 `~/.codex`）。保留已有内容，技能入口按实际安装目录调整：

```markdown
## 对话标题命名

新对话首轮结束前，读取 `$HOME/.agents/skills/conversation-title-naming/SKILL.md`，按其中的创建日期和命名规则只修改本对话标题，并回读核验。
```

全局指令的加载方式见 [OpenAI 官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。安装技能本身不等于每轮一定触发。批量处理历史对话需要单独授权；宿主缺少改名工具时，技能不能替代该能力。

## 只读辅助脚本

`title_metadata.py` 使用 Python 3.9+ 标准库和系统时区数据，转换时间或检查显式提供的离线快照：

```sh
python3 skills/conversation-title-naming/scripts/title_metadata.py date --value '2026-01-01T16:05:00Z'
```

它不会自动扫描或修改宿主数据库，也不会执行改名。快照格式及批量核验流程见 [历史整理与核验](skills/conversation-title-naming/references/batch-workflow.md)。

## 公开版的使用条件

示例使用通用角色、目录和合成场景。涉及业务的技能由使用者提供本地数据、工具及相应授权；仓库提供工作流程和列明的辅助脚本。现成的第三方插件、个人档案、自动化运行记录以及依赖私有后台的实现均未打包。
