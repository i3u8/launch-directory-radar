# launch-directory-radar · 发布目录雷达

每天自动抓取各类 **launch / 产品目录站**（我们投过外链的目录）里「新收录的项目」，做词频分析找出热词、升温赛道和同类产品聚类，把数据与日报提交回本仓库，并推送摘要到飞书。

*Daily monitor of product-launch / tool directories: collects newly listed projects from every directory that exposes a public list (JSON API / RSS / Atom / sitemap / HTML "latest" page), runs keyword & cluster analysis, commits data + reports back, and posts a digest to Feishu.*

## 最新结果 Latest

<!-- LATEST:START -->
**2026-10-28** · 新增 1564 · 监控 197 个目录（今日成功 183）

聚焦小词 Top 15:

- `travel dau rental` ×4（2 目录） 🆕：Rent Bike In Amritsar for Convenient and Affordable Travel -；Bike on Rent in Agra for Convenient City Travel - Dau Rental
- `effective pest control` ×3（3 目录） 🆕：Effective Pest Control Solutions for a Healthier Environment；Fair Deal
- `leading manufacturer` ×4（3 目录） 🆕：Super Duplex S32750 Tubes Manufacturers in India；Super Duplex S32750 Tubes Suppliers in India
- `football match prediction` ×2（2 目录） 🆕：Footalytics；Footalytics — AI football match predictions — score 45/100 (
- `image video studio` ×2（2 目录） 🆕：Eidora；Eidora AI image & video studio — 40 models, credits on the b
- `method commission pay` ×2（2 目录） 🆕：Invisible Engine；Invisible Engine | Your Unfair Search Advantage — score 50/1
- `tiny desk concert` ×2（2 目录） 🆕：Tiny Desk AI；Tiny Desk AI Put your friends in an AI Tiny Desk concert vid
- `attract targeted traffic` ×2（2 目录） 🆕：Best SEO Services India；SEO INDIA
- `biodegradable areca leaf` ×2（2 目录） 🆕：Areca Palm Leaf Plates Exporter；biodegradable dinnerware Exporter
- `bookkeeping case study` ×2（2 目录） 🆕：Accounting & Bookkeeping (FNS40222) Assignment Help；FNS40222 Accounting & Bookkeeping Assignment Help
- `cause pain swelling` ×2（2 目录） 🆕：Common Wrist Injuries and Conditions: Wrist Specialist in PC；ommon Wrist Injuries and Conditions: Wrist Specialist in PCM
- `damage restoration los` ×2（3 目录） 🆕：Fire Damage Restoration Los Angeles: Complete Guide to Fire,；Water Damage Restoration Los Angeles: Complete Guide to Wate
- `engine plan write` ×2（2 目录） 🆕：Invisible Engine | Your Unfair Search Advantage — score 50/1；Invisible Engine Plan, write, and launch affiliate websites 
- `eye makeup cosmetic` ×2（2 目录） 🆕：Browse Professional Eye Makeup Cosmetics in Zambia；Find Professional Eye Makeup Cosmetics in Zambia
- `kids early learning` ×2（2 目录） 🆕：kids early learning Lyndhurst；kids early learning centre Lyndhurst

微赛道归纳:

- 印度自行车租赁：travel dau rental、travel dau —— 提供印度城市（如阿姆利则、阿格拉）的便捷自行车租赁服务
- 害虫防治服务：effective pest control、ant control cockroach —— 提供针对蟑螂等害虫的有效控制解决方案
- 工业管材制造：leading manufacturer —— 专注于超级双相不锈钢管等工业管材的制造与供应
- AI足球预测：football match prediction —— 利用AI技术进行足球比赛比分预测
- AI图像视频创作：image video studio、tiny desk concert —— 提供多模型AI图像视频生成及趣味AI演唱会视频制作工具
- SEO与内容营销：method commission pay、attract targeted traffic、publishe topical authority、engine plan write —— 提供SEO优化、联盟网站构建及提升搜索排名的数字营销服务

完整报告: [reports/2026-10-28.md](reports/2026-10-28.md)
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
| `generic_terms.txt` | 大词/泛词清单（video、image、agent、ai agent、social media…），报告会抑制这些词；可自由增删 |
| `radar/parsers.py` | 解析器：`rss` / `atom` / `json_api`（含 WordPress REST）/ `sitemap` / `html_list` |
| `screen.py` `monitor.py` `analyze.py` `notify.py` | 筛查 / 采集 / 分析 / 飞书通知 |

## 筛查如何工作 How screening works

`python screen.py`（可 `--only a.com,b.com`）对每个目录域名依次探测：首页（`rel=alternate` 订阅、页面脚本里出现的 `/api/...`、“New/Latest”链接）→ `/wp-json`（WordPress 自定义文章类型）与常见 `/api/*` →
`/feed /rss /atom.xml /launches.xml …` → `robots.txt` + `sitemap.xml`（挑出像“列表详情页”的路径前缀，看 lastmod）→ `/new /latest /recent …` HTML 列表页（要求重复链接模式稳定，并排除导航/分类菜单）。
按 `json_api > rss/atom > sitemap > html_list` 的优先级选第一个可用且“像列表而不是博客文章”的来源；否则标记 `not_monitorable`，原因为 `dead` / `blocked`（反爬/403）/ `login_wall` / `js_only` / `no_public_list` / `stale`（最新条目超过 120 天）/ `form_only` 等。
不使用任何登录态；探测使用礼貌的限速与超时。

## 聚焦小词如何计算 Niche-term ranking

报告不再展示 video / image / agent 这类大词，而是找「小而具体」的词（unigram / bigram / trigram）：

1. **抑制泛词**：`generic_terms.txt` 中的词；由泛词单独组成的 n-gram（如 `social media`）；以及按全语料文档频率自动判定的头部词（单词出现在 >1.5% 的产品里、bigram >0.7%、trigram >0.4%）。
2. **候选条件**：今日出现在 2–15 个**不同产品**（同一产品被多个目录收录只算 1 个）、且来自 ≥2 个目录。
3. **排序**：稀有度（IDF）× log(今日数) × 今日/30天基线比 × n-gram 加权（bigram ×1.5、trigram ×1.9），30天基线里没出现过的词加权并标 🆕。
4. **去重**：单复数合并；若某词覆盖的产品与更高分的词重叠 ≥75%（如 bigram 包含 unigram）则丢弃。
5. 报告章节：聚焦小词 Top 15（含目录数与示例产品）、新出现的词、同日小簇（3–10 个相似产品）；可选 Qwen 把小词归并成微赛道（失败不影响流水线）。

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
