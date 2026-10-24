# launch-directory-radar · 发布目录雷达

每天自动抓取各类 **launch / 产品目录站**（我们投过外链的目录）里「新收录的项目」，做词频分析找出热词、升温赛道和同类产品聚类，把数据与日报提交回本仓库，并推送摘要到飞书。

*Daily monitor of product-launch / tool directories: collects newly listed projects from every directory that exposes a public list (JSON API / RSS / Atom / sitemap / HTML "latest" page), runs keyword & cluster analysis, commits data + reports back, and posts a digest to Feishu.*

## 最新结果 Latest

<!-- LATEST:START -->
**2026-10-24** · 新增 1395 · 监控 197 个目录（今日成功 195）

Top 关键词: `video`(125)、`image`(86)、`photo`(80)、`agent`(78)、`browser`(73)、`text`(67)、`content`(64)、`design`(63)、`saas`(61)、`marketing`(49)

Top 双词: `ai agent`(34)、`ai video`(27)、`social media`(19)、`ai image`(18)、`ai writing`(16)、`generative ai`(13)、`ai content`(12)、`text prompt`(10)、`ai model`(9)、`content creation`(9)

升温: `suggest`、`fees`、`particularly`、`enhance`、`understanding`、`driving`、`framecomet`、`known`

> 今日数据显示，AI Agent基础设施（如沙箱环境、MCP目录）与AI视频生成（含Kling 4.0等）显著升温，同时AI销售自动化（SDR）需求强劲。独立开发者应聚焦构建Agent底层工具或垂直领域的视频/销售自动化应用，以切入高增长赛道。

完整报告: [reports/2026-10-24.md](reports/2026-10-24.md)
<!-- LATEST:END -->

## 筛查概况 Screening summary

共 **478** 个目录（来自投放台账 + canopystack.dev）；已启用监控 **197**（sitemap 111，rss 45，json_api 25，html_list 12，atom 4）；不可监控 **281**（no_public_list 162，stale 58，dead 19，false_positive 18，not_a_directory 10，blocked 5，form_only 5，js_only 4）。逐个目录的原因见 [SCREENING.md](SCREENING.md)。

## 架构 Architecture

```
directories.csv ──screen.py──► sources.yaml + SCREENING.md   （一次性/按需：探测每个目录能否监控）
                                   │
GitHub Actions (daily 01:30 UTC = 09:30 北京时间)
   monitor.py  ─► data/entries.jsonl, data/daily/DATE.json, data/health.json   （每个来源独立失败）
   analyze.py  ─► reports/DATE.md, reports/latest.md, reports/DATE.json, README 本节   （词频/双词/升温/聚类/跨目录重复 + 可选 LLM 摘要）
   git commit + pull --rebase + push
   notify.py   ─► 飞书自定义机器人（含本仓库地址）
```

| 文件 | 作用 |
|---|---|
| `directories.csv` | 目录清单：域名 / 提交入口 / 类型（仅公开信息，不含账号密码邮箱） |
| `sources.yaml` | 每个目录的监控配置：`id, domain, kind, url, parser, enabled, params, notes, last_screened` |
| `SCREENING.md` | 筛查结果总表：每个目录为什么启用 / 不启用 |
| `overrides.yaml` | 人工覆盖（误判、不是目录的站点），重新筛查时保留 |
| `config.yaml` | 我们自己的站点域名（用于识别“我们的站点已被目录展示”） |
| `radar/parsers.py` | 解析器：`rss` / `atom` / `json_api`（含 WordPress REST）/ `sitemap` / `html_list` |
| `screen.py` `monitor.py` `analyze.py` `notify.py` | 筛查 / 采集 / 分析 / 飞书通知 |

## 筛查如何工作 How screening works

`python screen.py`（可 `--only a.com,b.com`）对每个目录域名依次探测：首页（`rel=alternate` 订阅、页面脚本里出现的 `/api/...`、“New/Latest”链接）→ `/wp-json`（WordPress 自定义文章类型）与常见 `/api/*` →
`/feed /rss /atom.xml /launches.xml …` → `robots.txt` + `sitemap.xml`（挑出像“列表详情页”的路径前缀，看 lastmod）→ `/new /latest /recent …` HTML 列表页（要求重复链接模式稳定，并排除导航/分类菜单）。
按 `json_api > rss/atom > sitemap > html_list` 的优先级选第一个可用且“像列表而不是博客文章”的来源；否则标记 `not_monitorable`，原因为 `dead` / `blocked`（反爬/403）/ `login_wall` / `js_only` / `no_public_list` / `stale`（最新条目超过 120 天）/ `form_only` 等。
不使用任何登录态；探测使用礼貌的限速与超时。

## 数据 Data layout

- `data/entries.jsonl`：全部条目，按 `(source, url)` 去重，保留 `first_seen`。字段 `source,name,url,tagline,category,listed_at(UTC),permalink,first_seen,day`。
  首次接入某来源时：36 小时内的条目算“今日新增”；30 天内且有日期的条目作为趋势基线（`backfill`）；其余只记录最小去重信息（`baseline`）。sitemap 一次性出现大量新 URL（批量 lastmod 变化）也只作基线。
- `data/daily/YYYY-MM-DD.json`：当天新增条目（保留 60 天）。
- `data/health.json`：每个来源的健康状态（最近成功日期、连续失败天数；≥3 天标记 `flagged`）。
- `reports/YYYY-MM-DD.md|json`、`reports/latest.md`：日报（保留 90 天）。

## 如何新增来源 Add a source

在 `sources.yaml` 的 `sources:` 末尾加一项（加 `locked: true` 防止重新筛查覆盖）：

```yaml
- id: example-com
  domain: example.com
  kind: rss                 # rss | atom | json_api | sitemap | html_list
  url: https://example.com/feed.xml
  parser: rss               # 与 kind 相同
  enabled: true
  params: {}                # json_api: {fields: {name: title, url: website, date: createdAt}, list_path: entries}
                            # rss: {title_split: " — "}; sitemap: {prefix: tools, depth: 2}; html_list: {pattern: <regex>, external: false}
  notes: manual
  last_screened: 2026-10-24
  locked: true
```
或把域名加入 `directories.csv` 后运行 `python screen.py --only example.com`。

## 本地运行 Rerun

```bash
pip install -r requirements.txt
python screen.py            # 重新筛查全部目录（约 8 分钟）
python monitor.py           # 采集
QWEN_API_KEY=... python analyze.py   # 分析（无 key 或加 --no-llm 则跳过 LLM 摘要）
FEISHU_WEBHOOK_URL=... python notify.py
```
Actions 里也可手动触发：`gh workflow run daily-radar` （输入 `rescreen=true` 可先重新筛查）。

## Secrets / 变量

| 名称 | 类型 | 说明 |
|---|---|---|
| `QWEN_API_KEY` | secret | Qwen（OpenAI 兼容）API key，仅用于每日摘要；失败不影响流水线 |
| `FEISHU_WEBHOOK_URL` | secret | 飞书自定义机器人 webhook |
| `FEISHU_SECRET` | secret（可选） | 机器人启用“签名校验”时填写 |
| `QWEN_BASE_URL` / `QWEN_MODEL` | workflow env（非密） | 默认 `https://qwen.redreamality.com/v1` / `unsloth/Qwen3.8-27B-NVFP4` |

## 保活 Keepalive

GitHub 会在仓库 60 天无活动后停用定时 workflow。本项目每天都有数据提交，只要抓取有新增就会自动保活；如果某天没有任何变化（极少见），请留意 Actions 页面的停用提示并手动 `Enable workflow`。

## 注意 Notes

- 抓取内容来自第三方，仅作统计；LLM 摘要提示词会忽略条目中的任何指令。
- 目录清单只包含公开域名；账号、邮箱、密码等一律不进入本仓库。
