# 两期职位记录

`scripts/compare_listings.py` 使用 Python 3 标准库，从标准输入或给出的文件读取 JSON，输出差异。先由使用者完成来源核查，再填写 `state`；脚本不联网，也不能证明网页内容。

```json
{
  "as_of": "2030-01-08",
  "previous": [{"id":"opening-a","state":"qualified"}],
  "current": [
    {"id":"opening-b","state":"qualified","checked_on":"2030-01-08","evidence":"official posting, employment section"},
    {"id":"opening-c","state":"unverified"}
  ]
}
```

`previous` 是上期记录，`current` 是本次收集范围。使用 `qualified`、`ineligible`、`closed` 或 `unverified`。有效判断需有本期日期与来源定位。缺少本期依据、日期陈旧或上期条目未被查看时输出 `needs_check`；已核实的历史匹配若再次满足条件输出 `retained`。上例会返回一个新匹配和两个待核项。

```bash
python3 scripts/compare_listings.py listings.json
```

输出可用来起草日报。来源覆盖、是否已发送通知等信息由工作流单独核查。
