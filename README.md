# my-best-skills

收集自己在实际协作中用得顺手的 Agent Skills。每个技能独立放在 `skills/` 下，保留完整的说明、参考资料和辅助脚本，方便单独安装与维护。

## 已收录

| 技能 | 用途 |
| --- | --- |
| [conversation-title-naming](skills/conversation-title-naming/SKILL.md) | 根据上海时区的真实创建日期，将对话标题统一为 `MMDD\|类型\|主题`，支持首轮命名和已授权的历史批量整理，并回读核验。 |

示例：`1107|发布|整理技能仓库`。

## 安装

克隆公开仓库：

```sh
git clone https://github.com/yuanhongboo/my-best-skills.git
cd my-best-skills
```

将所需技能的**整个目录**复制到当前环境的技能搜索目录。当前 Codex 用户级默认位置为 `~/.agents/skills/`，例如 `~/.agents/skills/conversation-title-naming/SKILL.md`。如果环境已在使用 `~/.codex/skills/` 等位置，沿用现有配置，避免重复安装同名技能。

Codex 会自动检测技能变化；未出现时重启。安装机制见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用 conversation-title-naming

在具备对话列表、读取和改名工具的宿主中调用：

```text
使用 $conversation-title-naming 规范当前对话标题，并回读核验。
```

需要**每个新对话首轮自动命名**时，将下面的触发规则合并进全局 `AGENTS.md`（位于 `CODEX_HOME`，未设置时为 `~/.codex`）。保留已有内容，技能入口按实际安装目录调整：

```markdown
## 对话标题命名

- 新对话首轮最终回复结束前，读取并执行 `conversation-title-naming` 技能。
- 技能入口为 `$HOME/.agents/skills/conversation-title-naming/SKILL.md`，按实际环境展开路径。
- 按该对话实际创建时间换算到 `Asia/Shanghai` 后，以 `MMDD|类型|主题` 命名；创建时间或主题无法可靠确定时保留原名。
- 只修改标题，并读取实际标题核验。无改名能力或调用失败时如实说明。
```

全局指令的加载方式见 [OpenAI 官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。安装技能本身不等于每轮一定触发。批量处理历史对话需要单独授权；宿主缺少改名工具时，技能不能替代该能力。

## 只读辅助脚本

`title_metadata.py` 使用 Python 3.9+ 标准库和系统时区数据，转换时间或检查显式提供的离线快照：

```sh
python3 skills/conversation-title-naming/scripts/title_metadata.py date --value '2026-01-01T16:05:00Z'
```

它不会自动扫描或修改宿主数据库，也不会执行改名。快照格式及批量核验流程见 [历史整理与核验](skills/conversation-title-naming/references/batch-workflow.md)。

## 目录

```text
skills/
└── conversation-title-naming/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/batch-workflow.md
    └── scripts/title_metadata.py
```

新增技能时，按 `skills/<skill-name>/SKILL.md` 组织；只提交技能需要的文件，会话快照、凭据和本地运行记录不放入仓库。
