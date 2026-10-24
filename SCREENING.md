# SCREENING — 目录可监控性筛查 / Directory monitorability screening

- 目录总数 total directories: **478**
- 已启用 enabled: **197** (sitemap: 111, rss: 45, json_api: 25, html_list: 12, atom: 4)
- 不可监控 not monitorable: **281** (no_public_list: 162, stale: 58, dead: 19, false_positive: 18, not_a_directory: 10, blocked: 5, form_only: 5, js_only: 4)
- 最近筛查 last screened: 2026-10-24

Reasons: `dead` 无法连接/404/5xx/停放; `blocked` 反爬/403/Cloudflare; `login_wall` 需登录; `js_only` 纯前端渲染无 SSR 内容/无 feed; `no_public_list` 站点正常但无公开可抓的“最新”列表/feed/sitemap; `form_only` 仅表单入口。

| # | domain | kind | enabled | why / notes | sample size | newest entry (UTC) |
|---|---|---|---|---|---|---|
| 1 | 10015.io | atom [/tool-feed](https://10015.io/tool-feed) | ✅ |  | 49 | 2026-10-20 |
| 2 | pitchwall.co | atom [/rss](https://pitchwall.co/rss) | ✅ |  | 30 | 2026-10-22 |
| 3 | postlaunchkit.com | atom [/feed.xml](https://postlaunchkit.com/feed.xml) | ✅ |  | 50 | 2026-10-23 |
| 4 | tools.robingood.com | atom [/feed](https://tools.robingood.com/feed) | ✅ |  | 30 | 2026-10-24 |
| 5 | canadawebdir.com | html_list [/index.php](https://canadawebdir.com/index.php?list=latest) | ✅ |  | 21 |  |
| 6 | canadiandirectory.org | html_list [/index.php](https://www.canadiandirectory.org/index.php?list=latest) | ✅ |  | 10 |  |
| 7 | hotweburls.com | html_list [/index.php](https://www.hotweburls.com/index.php?list=latest) | ✅ |  | 15 |  |
| 8 | lpdl.org | html_list [/index.php](https://lpdl.org/index.php?list=latest) | ✅ |  | 21 |  |
| 9 | marketinginternetdirectory.com | html_list [/index.php](https://www.marketinginternetdirectory.com/index.php?list=latest) | ✅ |  | 21 |  |
| 10 | novatools.ai | html_list [/new](https://novatools.ai/new) | ✅ |  | 86 |  |
| 11 | promotebusinessdirectory.com | html_list [/index.php](https://promotebusinessdirectory.com/index.php?list=latest) | ✅ |  | 21 |  |
| 12 | sitelike.org | html_list [/latest.aspx](https://www.sitelike.org/latest.aspx) | ✅ | sitemap /sitemap.xml has 150000 urls but no recognisable listing path | 77 |  |
| 13 | siteswebdirectory.com | html_list [/index.php](https://www.siteswebdirectory.com/index.php?list=latest) | ✅ |  | 12 |  |
| 14 | submissionwebdirectory.com | html_list [/index.php](https://www.submissionwebdirectory.com/index.php?list=latest) | ✅ |  | 25 |  |
| 15 | thehackstack.com | html_list [/latest](https://thehackstack.com/latest) | ✅ |  | 51 |  |
| 16 | usalistingdirectory.com | html_list [/index.php](https://www.usalistingdirectory.com/index.php?list=latest) | ✅ |  | 25 |  |
| 17 | aig123.com | json_api [/wp-json/wp/v2/sites](https://www.aig123.com/wp-json/wp/v2/sites?per_page=40&orderby=date&order=desc) | ✅ |  | 40 | 2026-10-23 |
| 18 | aimojo.io | json_api [/wp-json/wp/v2/organization](https://aimojo.io/wp-json/wp/v2/organization?per_page=40&orderby=date&order=desc) | ✅ |  | 40 | 2026-10-23 |
| 19 | aitoolly.com | json_api [/api/products](https://aitoolly.com/api/products) | ✅ |  | 50 | 2026-10-23 |
| 20 | aitools.sh | json_api [/wp-json/wp/v2/thirstylink](https://aitools.sh/wp-json/wp/v2/thirstylink?per_page=40&orderby=date&order=desc) | ✅ |  | 21 | 2026-10-21 |
| 21 | aitoolshunt.com | json_api [/wp-json/wp/v2/ai-tool](https://aitoolshunt.com/wp-json/wp/v2/ai-tool?per_page=40&orderby=date&order=desc) | ✅ |  | 3 | 2026-10-04 |
| 22 | azn8.com | json_api [/api/v1/listings](https://azn8.com/api/v1/listings) | ✅ |  | 20 | 2026-10-24 |
| 23 | canopystack.dev | json_api [/api/launches](https://canopystack.dev/api/launches) | ✅ |  | 500 | 2026-10-24 |
| 24 | gateofai.com | json_api [/wp-json/wp/v2/community_tool](https://gateofai.com/wp-json/wp/v2/community_tool?per_page=40&orderby=date&order=desc) | ✅ | json /wp-json/wp/v2/ai_tool rejected: feed content looks like articles, not listings; json /wp-json/wp/v2/tutorial rejected: feed content lo | 28 | 2026-10-23 |
| 25 | hyzenpro.com | json_api [/api/tools](https://hyzenpro.com/api/tools) | ✅ |  | 219 | 2026-10-07 |
| 26 | launch.ignlab.net | json_api [/api/v1/listings](https://launch.ignlab.net/api/v1/listings) | ✅ |  | 30 | 2026-10-24 |
| 27 | listedstartups.com | json_api [/api/listings](https://listedstartups.com/api/listings) | ✅ |  | 100 | 2026-10-24 |
| 28 | madewithstack.com | json_api [/api/products](https://www.madewithstack.com/api/products) | ✅ |  | 24 | 2026-10-12 |
| 29 | my2077.com | json_api [/api/site](https://my2077.com/api/site) | ✅ |  | 8 |  |
| 30 | nocodelib.com | json_api [/api/tools](https://nocodelib.com/api/tools) | ✅ |  | 84 | 2026-09-12 |
| 31 | promoteindex.com | json_api [/api/v1/trending](https://promoteindex.com/api/v1/trending) | ✅ |  | 10 | 2026-10-19 |
| 32 | saaspirate.com | json_api [/wp-json/wp/v2/deals](https://saaspirate.com/wp-json/wp/v2/deals?per_page=40&orderby=date&order=desc) | ✅ | json /wp-json/wp/v2/black-friday-deals rejected: feed content looks like articles, not listings | 40 | 2026-10-19 |
| 33 | thewebisfree.com | json_api [/wp-json/wp/v2/hp_listing](https://www.thewebisfree.com/wp-json/wp/v2/hp_listing?per_page=40&orderby=date&order=desc) | ✅ |  | 40 | 2026-10-23 |
| 34 | toolgrep.com | json_api [/api/products](https://toolgrep.com/api/products) | ✅ |  | 20 |  |
| 35 | totool.cc | json_api [/api/tools](https://totool.cc/api/tools) | ✅ |  | 20 |  |
| 36 | usefuturestack.com | json_api [/api/tools](https://www.usefuturestack.com/api/tools) | ✅ |  | 12 | 2026-07-02 |
| 37 | webgora.com | json_api [/api/products](https://webgora.com/api/products) | ✅ |  | 20 | 2026-10-22 |
| 38 | webrankdirectory.org | json_api [/api/v1/listings](https://webrankdirectory.org/api/v1/listings) | ✅ |  | 20 | 2026-10-23 |
| 39 | whatareyoubuilding.ai | json_api [/api/products](https://whatareyoubuilding.ai/api/products) | ✅ |  | 25 | 2026-10-24 |
| 40 | worthtotry.com | json_api [/api/v1/tools](https://worthtotry.com/api/v1/tools) | ✅ |  | 10 | 2026-10-24 |
| 41 | zoipi.com | json_api [/api/tools](https://zoipi.com/api/tools) | ✅ |  | 50 |  |
| 42 | a2place.com | rss [/rss](https://a2place.com/rss) | ✅ |  | 50 | 2026-10-24 |
| 43 | agentic.ai | rss [/feed.xml](https://agentic.ai/feed.xml) | ✅ | short titles (name-like) | 50 | 2026-10-23 |
| 44 | agentsearchengine.app | rss [/feed.xml](https://agentsearchengine.app/feed.xml) | ✅ |  | 39 | 2026-10-19 |
| 45 | agentsindex.ai | rss [/rss.xml](https://agentsindex.ai/rss.xml) | ✅ | short titles (name-like) | 382 | 2026-10-24 |
| 46 | aiai.tools | rss [/feed](https://aiai.tools/feed) | ✅ |  | 10 | 2026-07-09 |
| 47 | aijuhe.org | rss [/feed.xml](https://aijuhe.org/feed.xml) | ✅ |  | 40 | 2026-09-08 |
| 48 | ailibri.com | rss [/rss](https://ailibri.com/rss) | ✅ |  | 20 | 2026-10-05 |
| 49 | aisuggests.ai | rss [/feed.xml](https://aisuggests.ai/feed.xml) | ✅ |  | 100 | 2026-10-23 |
| 50 | aisuqp.xyz | rss [/feed.xml](https://aisuqp.xyz/feed.xml) | ✅ | short titles (name-like) | 60 | 2026-10-23 |
| 51 | aitoolsarena.com | rss [/feed](https://aitoolsarena.com/feed) | ✅ |  | 10 | 2026-08-15 |
| 52 | aitoolsdirectory.com | rss [/items.rss](https://aitoolsdirectory.com/items.rss) | ✅ |  | 761 |  |
| 53 | aitoolsup.com | rss [/feed/](https://aitoolsup.com/feed/) | ✅ | short titles (name-like) | 10 | 2026-09-12 |
| 54 | anyfp.com | rss [/rss.xml](https://tooltrove.net/rss.xml) | ✅ | home redirects to tooltrove.net; short titles (name-like) | 50 | 2026-10-21 |
| 55 | aoyii.com | rss [/feed](https://www.aoyii.com/feed) | ✅ | short titles (name-like) | 50 | 2026-10-23 |
| 56 | aweblist.org | rss [/rss](https://aweblist.org/rss) | ✅ |  | 50 | 2026-10-24 |
| 57 | awesomeindie.com | rss [/rss/products.xml](https://awesomeindie.com/rss/products.xml) | ✅ |  | 50 | 2026-10-24 |
| 58 | bestaitools.com | rss [/feed](https://www.bestaitools.com/feed) | ✅ |  | 10 | 2026-10-23 |
| 59 | dealmyapp.com | rss [/feed.xml](https://dealmyapp.com/feed.xml) | ✅ |  | 20 | 2026-10-23 |
| 60 | directory6.org | rss [/rss](https://directory6.org/rss) | ✅ |  | 50 | 2026-10-24 |
| 61 | directoryfire.com | rss [/rss](https://directoryfire.com/rss) | ✅ |  | 20 | 2026-10-16 |
| 62 | elf08.com | rss [/rss](https://elf08.com/rss) | ✅ |  | 10 | 2026-10-09 |
| 63 | exampledir.com | rss [/rss](https://exampledir.com/rss) | ✅ |  | 50 | 2026-10-24 |
| 64 | foundr.ai | rss [/rss/tools.xml](https://foundr.ai/rss/tools.xml) | ✅ | short titles (name-like) | 50 | 2026-10-12 |
| 65 | huludirectory.com | rss [/rss](https://huludirectory.com/rss) | ✅ |  | 50 | 2026-10-24 |
| 66 | indieindex.xyz | rss [/rss.xml](https://indieindex.xyz/rss.xml) | ✅ | short titles (name-like) | 319 | 2026-10-23 |
| 67 | land-book.com | rss [/rss.xml](https://land-book.com/rss.xml) | ✅ |  | 50 | 2026-10-23 |
| 68 | launchingnext.com | rss [/rss/](https://www.launchingnext.com/rss/) | ✅ | short titles (name-like) | 15 | 2026-10-23 |
| 69 | linki.hu | rss [/rss.xml](https://linki.hu/rss.xml) | ✅ | short titles (name-like) | 47 | 2026-10-18 |
| 70 | news.bensbites.com | rss [/feed](https://www.bensbites.com/feed) | ✅ | home redirects to bensbites.com | 20 | 2026-10-22 |
| 71 | nextool.ai | rss [/functions/v1/rss](https://nextool.ai/functions/v1/rss) | ✅ |  | 50 | 2026-10-07 |
| 72 | nothumansearch.ai | rss [/feed.xml](https://nothumansearch.ai/feed.xml) | ✅ |  | 50 | 2026-10-24 |
| 73 | onemilliondirectory.com | rss [/rss](https://onemilliondirectory.com/rss) | ✅ |  | 30 | 2026-10-20 |
| 74 | peplio.com | rss [/feed/](https://peplio.com/feed/) | ✅ | json /wp-json/wp/v2/pcg_comic rejected: feed content looks like articles, not listings; short titles (name-like) | 10 | 2026-10-23 |
| 75 | planet-ai.net | rss [/rss.xml](https://planet-ai.net/rss.xml) | ✅ |  | 50 | 2026-10-24 |
| 76 | populardirectory.biz | rss [/rss](https://populardirectory.biz/rss) | ✅ |  | 50 | 2026-10-19 |
| 77 | royallinkup.com | rss [/rss](https://royallinkup.com/rss) | ✅ | short titles (name-like) | 20 | 2026-06-30 |
| 78 | saasolution.io | rss [/feed.xml](https://saasolution.io/feed.xml) | ✅ |  | 50 | 2026-10-23 |
| 79 | startfa.st | rss [/rss.xml](https://startfa.st/rss.xml) | ✅ | short titles (name-like) | 50 | 2026-09-01 |
| 80 | startup88.com | rss [/feed](https://startup88.com/feed) | ✅ |  | 100 | 2026-10-21 |
| 81 | startupaitools.com | rss [/feed/](https://www.startupaitools.com/feed/) | ✅ | short titles (name-like) | 10 | 2026-10-23 |
| 82 | startups.snapmunk.com | rss [/rss](https://startups.snapmunk.com/rss) | ✅ |  | 100 | 2026-10-23 |
| 83 | tagshub.com | rss [/rss](https://tagshub.com/rss) | ✅ |  | 120 | 2026-10-05 |
| 84 | thequestion.it | rss [/feed/](https://www.thequestion.it/feed/) | ✅ |  | 10 | 2026-10-20 |
| 85 | verzeichnis4you.de | rss [/feed](https://verzeichnis4you.de/feed) | ✅ |  | 6 | 2026-10-23 |
| 86 | zearches.com | rss [/rss.php](https://zearches.com/rss.php) | ✅ |  | 50 | 2026-10-24 |
| 87 | abilogic.com | sitemap [/sitemap_directory.xml.gz](https://www.abilogic.com/sitemap_directory.xml.gz) | ✅ |  | 300 | 2026-10-23 |
| 88 | agents-launch.lovable.app | sitemap [/sitemap.xml](https://agents-launch.lovable.app/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 89 | agents.net | sitemap [/sitemap.xml](https://agents.net/sitemap.xml) | ✅ |  | 300 | 2026-10-11 |
| 90 | aiagentautomation.site | sitemap [/sitemap.xml](https://aiagentautomation.site/sitemap.xml) | ✅ | feed /rss.xml found but entries are blog/news posts | 184 | 2026-10-23 |
| 91 | aiagentehub.com | sitemap [/sitemap.xml](https://www.aiagentehub.com/sitemap.xml) | ✅ |  | 164 | 2026-10-21 |
| 92 | aiagentrating.com | sitemap [/sitemap.xml](https://aiagentrating.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 93 | aiagents.org | sitemap [/sitemap.xml](https://aiagents.org/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 94 | aiagentsdirectory.com | sitemap [/sitemap.xml](https://aiagentsdirectory.com/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 95 | aiagentslive.com | sitemap [/sitemap.xml.gz](https://aiagentslive.com/sitemap.xml.gz) | ✅ |  | 300 | 2026-10-23 |
| 96 | aibrew.io | sitemap [/sitemap.xml](https://www.aibrew.io/sitemap.xml) | ✅ |  | 11 | 2026-08-20 |
| 97 | aicompare.to | sitemap [/sitemap.xml](https://aicompare.to/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 98 | aier.im | sitemap [/sitemap.xml](https://aier.im/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 99 | aiforme.wiki | sitemap [/sitemap.xml](https://aiforme.wiki/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 63 |  |
| 100 | aiheron.com | sitemap [/sitemap.xml](https://aiheron.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 18 |  |
| 101 | aiimagegenerator.io | sitemap [/sitemap_index.xml](https://aiimagegenerator.io/sitemap_index.xml) | ✅ | json /wp-json/wp/v2/ai_tools rejected: feed content looks like articles, not listings | 56 | 2026-10-23 |
| 102 | aiimagetools.io | sitemap [/sitemap.xml](https://aiimagetools.io/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 30 |  |
| 103 | aimarketing.directory | sitemap [/sitemap.xml](https://www.aimarketing.directory/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 60 |  |
| 104 | aisotools.com | sitemap [/sitemap.xml](https://aisotools.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 105 | aisuperhub.io | sitemap [/sitemap.xml](https://www.aisuperhub.io/sitemap.xml) | ✅ |  | 264 | 2026-10-21 |
| 106 | aitoolboard.com | sitemap [/sitemap.xml](https://aitoolboard.com/sitemap.xml) | ✅ |  | 300 | 2026-10-20 |
| 107 | aitoolclaw.com | sitemap [/sitemap-index.xml](https://aitoolclaw.com/sitemap-index.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 108 | aitoolscapital.com | sitemap [/sitemap.xml](https://aitoolscapital.com/sitemap.xml) | ✅ |  | 300 | 2026-10-12 |
| 109 | aitoolseekers.com | sitemap [/sitemap.xml](https://aitoolseekers.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 110 | altimateguide.com | sitemap [/sitemap.xml](https://altimateguide.com/sitemap.xml) | ✅ |  | 164 | 2026-10-22 |
| 111 | apprater.net | sitemap [/sitemap.xml](https://apprater.net/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 112 | bestaiagents.ai | sitemap [/sitemap.xml](https://bestaiagents.ai/sitemap.xml) | ✅ |  | 287 | 2026-07-29 |
| 113 | bestaivideosoftware.com | sitemap [/sitemap.xml](https://bestaivideosoftware.com/sitemap.xml) | ✅ |  | 74 | 2026-10-23 |
| 114 | bestwebdesigntools.com | sitemap [/sitemap.xml](https://bestwebdesigntools.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 115 | blogs-collection.com | sitemap [/sitemap.xml](https://www.blogs-collection.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 116 | brouseai.com | sitemap [/sitemap.xml](https://www.brouseai.com/sitemap.xml) | ✅ |  | 300 | 2026-10-12 |
| 117 | businessfreedirectory.biz | sitemap [/sitemap.xml](https://businessfreedirectory.biz/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 48 |  |
| 118 | catalogo-ia.com | sitemap [/sitemap.xml](https://catalogo-ia.com/sitemap.xml) | ✅ |  | 300 | 2026-10-11 |
| 119 | chipjourney.com | sitemap [/directory/sitemap/](https://chipjourney.com/directory/sitemap/) | ✅ | sitemap /sitemap.xml has 495 urls but no recognisable listing path; sitemap has no lastmod; first-seen dates only | 12 |  |
| 120 | clapstorm.com | sitemap [/sitemap.xml](https://www.clapstorm.com/sitemap.xml) | ✅ | feed /rss.xml found but entries are blog/news posts | 300 | 2026-10-24 |
| 121 | corpus.blog | sitemap [/sitemap.xml](https://corpus.blog/sitemap.xml) | ✅ | feed /blog/feed found but entries are blog/news posts | 300 | 2026-10-23 |
| 122 | curlship.com | sitemap [/sitemap.xml](https://curlship.com/sitemap.xml) | ✅ | json /api/listings rejected: feed content looks like articles, not listings; feed /feed.xml found but feed content looks like articles, not  | 300 | 2026-10-24 |
| 123 | dang.ai | sitemap [/sitemap.xml](https://dang.ai/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 124 | develif.com | sitemap [/sitemap.xml](https://develif.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 125 | directory-index.com | sitemap [/sitemap.xml](https://directory-index.com/sitemap.xml) | ✅ |  | 190 | 2026-10-23 |
| 126 | discoverly.tech | sitemap [/sitemap.xml](https://discoverly.tech/sitemap.xml) | ✅ |  | 44 | 2026-10-23 |
| 127 | dowseai.com | sitemap [/sitemap.xml](https://dowseai.com/sitemap.xml) | ✅ |  | 263 | 2026-10-22 |
| 128 | dynamite-ai.com | sitemap [/sitemap.xml](https://dynamite-ai.com/sitemap.xml) | ✅ |  | 300 | 2026-09-10 |
| 129 | earlylaunch.co | sitemap [/sitemap.xml](https://earlylaunch.co/sitemap.xml) | ✅ |  | 300 | 2026-08-14 |
| 130 | entireweb.com | sitemap [/sitemap.xml](https://www.entireweb.com/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 131 | findtools.ai | sitemap [/sitemap-index.xml](https://www.findtools.ai/sitemap-index.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 132 | forwardfuture.com | sitemap [/sitemap.xml](https://forwardfuture.com/sitemap.xml) | ✅ |  | 300 | 2026-10-22 |
| 133 | freeaitool.ai | sitemap [/sitemap.xml](https://freeaitool.ai/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 134 | futuretools.io | sitemap [/sitemap.xml](https://futuretools.io/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 135 | gptbot.io | sitemap [/sitemap.xml](https://gptbot.io/sitemap.xml) | ✅ |  | 123 | 2026-09-30 |
| 136 | greenrocket.app | sitemap [/sitemap.xml](https://greenrocket.app/sitemap.xml) | ✅ |  | 60 | 2026-10-23 |
| 137 | humanornot.co | sitemap [/sitemap.xml](https://www.humanornot.co/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 221 |  |
| 138 | indiefollow.top | sitemap [/sitemap.xml](https://indiefollow.top/sitemap.xml) | ✅ |  | 166 | 2026-10-24 |
| 139 | infrabase.ai | sitemap [/sitemap.xml](https://infrabase.ai/sitemap.xml) | ✅ |  | 92 | 2026-10-20 |
| 140 | iuu.ai | sitemap [/sitemap.xml](https://iuu.ai/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 141 | joinly.xyz | sitemap [/sitemap.xml](https://joinly.xyz/sitemap.xml) | ✅ |  | 300 | 2026-10-19 |
| 142 | justbuildapps.com | sitemap [/sitemap.xml](https://justbuildapps.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 143 | launchfree.io | sitemap [/sitemap.xml](https://launchfree.io/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 144 | launchranked.com | sitemap [/sitemap.xml](https://launchranked.com/sitemap.xml) | ✅ |  | 130 | 2026-10-08 |
| 145 | launchsignal.ai | sitemap [/sitemap.xml](https://launchsignal.ai/sitemap.xml) | ✅ |  | 100 | 2026-10-24 |
| 146 | linkwith.us | sitemap [/sitemap.xml](https://linkwith.us/sitemap.xml) | ✅ |  | 20 | 2026-08-20 |
| 147 | listai.cc | sitemap [/sitemap.xml](https://listai.cc/sitemap.xml) | ✅ | feed /feed.xml found but entries are blog/news posts | 300 | 2026-10-24 |
| 148 | llmrelevance.com | sitemap [/sitemap.xml](https://www.llmrelevance.com/sitemap.xml) | ✅ |  | 300 | 2026-10-22 |
| 149 | llmslist.com | sitemap [/sitemap.xml](https://llmslist.com/sitemap.xml) | ✅ |  | 185 | 2026-10-23 |
| 150 | meweblink.com | sitemap [/sitemap.xml](https://meweblink.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 11 |  |
| 151 | navs.site | sitemap [/sitemap.xml](https://navs.site/sitemap.xml) | ✅ | feed /rss.xml found but entries are blog/news posts | 300 | 2026-10-24 |
| 152 | neuron.co.uk | sitemap [/sitemap.xml](https://neuron.co.uk/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 72 |  |
| 153 | nextweekai.com | sitemap [/sitemap-index.xml](https://nextweekai.com/sitemap-index.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 83 |  |
| 154 | openfuture.ai | sitemap [/sitemap.xml](https://openfuture.ai/sitemap.xml) | ✅ |  | 75 | 2026-10-24 |
| 155 | peerpush.com | sitemap [/sitemap.xml](https://peerpush.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 156 | phototoolfinder.com | sitemap [/sitemap.xml](https://phototoolfinder.com/sitemap.xml) | ✅ |  | 300 | 2026-10-21 |
| 157 | pickapps.org | sitemap [/sitemap.xml](https://pickapps.org/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 204 |  |
| 158 | playlin.io | sitemap [/sitemap.xml](https://playlin.io/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 159 | powerfulwebsites.io | sitemap [/sitemap.xml](https://powerfulwebsites.io/sitemap.xml) | ✅ |  | 300 | 2026-07-10 |
| 160 | pwa.directory | sitemap [/sitemap.xml](https://pwa.directory/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 161 | rajaharimau.xyz | sitemap [/sitemap.xml](https://rajaharimau.xyz/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 162 | rankmyai.com | sitemap [/sitemap.xml](https://www.rankmyai.com/sitemap.xml) | ✅ |  | 300 | 2026-10-14 |
| 163 | reviewai.net | sitemap [/sitemap_index.xml](https://reviewai.net/sitemap_index.xml) | ✅ |  | 300 | 2026-10-19 |
| 164 | saasdealer.com | sitemap [/sitemap.xml](https://www.saasdealer.com/sitemap.xml) | ✅ |  | 277 | 2026-10-21 |
| 165 | saasworthy.com | sitemap [/sitemap.xml](https://www.saasworthy.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 166 | seooptimizationdirectory.com | sitemap [/sitemap.xml](https://seooptimizationdirectory.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 47 |  |
| 167 | shipboard.live | sitemap [/sitemap.xml](https://gitshipped.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 168 | sideprojects.net | sitemap [/sitemap.xml](https://sideprojects.net/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 169 | softwareworld.co | sitemap [/sitemap.xml](https://www.softwareworld.co/sitemap.xml) | ✅ | home http 403 (anti-bot challenge) | 300 | 2026-10-23 |
| 170 | startupbenchmarks.com | sitemap [/sitemap.xml](https://startupbenchmarks.com/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 171 | startups.fyi | sitemap [/sitemap.xml](https://www.startups.fyi/sitemap.xml) | ✅ |  | 300 | 2026-10-20 |
| 172 | stork.ai | sitemap [/sitemap.xml](https://www.stork.ai/sitemap.xml) | ✅ | feed /blog/rss.xml found but entries are blog/news posts | 300 | 2026-10-22 |
| 173 | superlaunch.in | sitemap [/sitemap.xml](https://superlaunch.in/sitemap.xml) | ✅ | feed /blog/feed.xml found but entries are blog/news posts | 88 | 2026-09-01 |
| 174 | tap4.ai | sitemap [/sitemap.xml](https://tap4.ai/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 175 | techtools.cz | sitemap [/sitemap.xml](https://techtools.cz/sitemap.xml) | ✅ |  | 79 | 2026-10-19 |
| 176 | thataicollection.com | sitemap [/sitemaps/index.xml](https://thataicollection.com/sitemaps/index.xml) | ✅ |  | 300 | 2026-10-23 |
| 177 | the-ai-toolhub.lovable.app | sitemap [/sitemap.xml](https://the-ai-toolhub.lovable.app/sitemap.xml) | ✅ | feed /rss.xml found but entries are blog/news posts | 30 | 2026-10-07 |
| 178 | theagentbenchmark.com | sitemap [/sitemap.xml](https://theagentbenchmark.com/sitemap.xml) | ✅ |  | 300 | 2026-10-16 |
| 179 | thenextaitool.com | sitemap [/sitemaps/sitemap-index.xml](https://nextaitool.com/sitemaps/sitemap-index.xml) | ✅ | home redirects to nextaitool.com; sitemap has no lastmod; first-seen dates only | 300 |  |
| 180 | tipseason.com | sitemap [/sitemap.xml](https://www.tipseason.com/sitemap.xml) | ✅ |  | 300 | 2026-08-15 |
| 181 | toolmaticai.com | sitemap [/sitemap.xml](https://toolmaticai.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 182 | toolpilot.ai | sitemap [/sitemap.xml](https://www.toolpilot.ai/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 183 | tools.landin.page | sitemap [/sitemap.xml](https://tools.landin.page/sitemap.xml) | ✅ |  | 300 | 2026-10-22 |
| 184 | toolsfine.com | sitemap [/sitemap.xml](https://toolsfine.com/sitemap.xml) | ✅ |  | 71 | 2026-10-11 |
| 185 | toools.design | sitemap [/sitemap.xml](https://www.toools.design/sitemap.xml) | ✅ |  | 31 | 2026-10-20 |
| 186 | topaitools.net | sitemap [/sitemap.xml](https://topaitools.net/sitemap.xml) | ✅ |  | 300 | 2026-07-23 |
| 187 | trillionagent.com | sitemap [/sitemap.xml](https://trillionagent.com/sitemap.xml) | ✅ |  | 300 | 2026-10-22 |
| 188 | truewebdirectory.com | sitemap [/sitemap.xml](https://truewebdirectory.com/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 189 | uneed.best | sitemap [/sitemap_index.xml](https://www.uneed.best/sitemap_index.xml) | ✅ |  | 300 | 2026-12-17 |
| 190 | vidirect.org | sitemap [/sitemap.xml](https://vidirect.org/sitemap.xml) | ✅ |  | 19 | 2026-10-01 |
| 191 | viesearch.com | sitemap [/sitemap.xml](https://viesearch.com/sitemap.xml) | ✅ |  | 300 | 2026-10-24 |
| 192 | webapps.directory | sitemap [/sitemap.xml](https://webapps.directory/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 193 | webdirectory.top | sitemap [/sitemap.xml](https://webdirectory.top/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 300 |  |
| 194 | webinhalt.de | sitemap [/sitemap.xml](https://www.webinhalt.de/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 195 | whattheai.tech | sitemap [/sitemap.xml](https://whattheai.tech/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 196 | yo.directory | sitemap [/sitemap.xml](https://yo.directory/sitemap.xml) | ✅ |  | 300 | 2026-10-23 |
| 197 | youtools.ai | sitemap [/sitemap.xml](https://youtools.ai/sitemap.xml) | ✅ | sitemap has no lastmod; first-seen dates only | 92 |  |
| 198 | 01webdirectory.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 135 urls but no recognisable listing path |  |  |
| 199 | 10words.io | not_monitorable | ❌ | no_public_list |  |  |
| 200 | 2001jeux.fr | not_monitorable | ❌ | no_public_list: feed /rss.xml found but feed content looks like articles, not listings; sitemap /sitemap.xml has 1752 urls but no recognisab |  |  |
| 201 | 247webdirectory.com | not_monitorable | ❌ | false_positive: manual override: regional category page, not a latest list |  |  |
| 202 | 63243.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 14400 urls but no recognisable listing path |  |  |
| 203 | 82470.com | not_monitorable | ❌ | no_public_list |  |  |
| 204 | 9sites.net | not_monitorable | ❌ | no_public_list |  |  |
| 205 | a-zbusinessfinder.com | not_monitorable | ❌ | false_positive: manual override: regional business category page, not a latest list |  |  |
| 206 | ababtools.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1007 urls but no recognisable listing path |  |  |
| 207 | abc-directory.com | not_monitorable | ❌ | no_public_list |  |  |
| 208 | abicloud.org | not_monitorable | ❌ | no_public_list |  |  |
| 209 | acedirectory.org | not_monitorable | ❌ | no_public_list |  |  |
| 210 | activdirectory.net | not_monitorable | ❌ | no_public_list |  |  |
| 211 | activesearchresults.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 182 urls but no recognisable listing path |  |  |
| 212 | addfreewebdirectory.com | not_monitorable | ❌ | stale: newest entry is 3871d old; source looks stale | 36 | 2016-03-19 |
| 213 | addonbiz.com | not_monitorable | ❌ | not_a_directory: manual override: job-listings post type | 40 | 2026-10-24 |
| 214 | advertise.aitoptools.com | not_monitorable | ❌ | js_only: sitemap /sitemap.xml has 1 urls but no recognisable listing path |  |  |
| 215 | agentmrr.ai | not_monitorable | ❌ | no_public_list |  |  |
| 216 | agentwebmap.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 80 urls but no recognisable listing path |  |  |
| 217 | ai-all.info | not_monitorable | ❌ | stale: newest entry is 425d old; source looks stale | 20 | 2025-08-24 |
| 218 | ai-best.deals | not_monitorable | ❌ | stale: newest entry is 161d old; source looks stale | 125 | 2026-05-15 |
| 219 | ai-hunter.io | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 220 | ai2people.com | not_monitorable | ❌ | stale: newest entry is 156d old; source looks stale | 10 | 2026-05-20 |
| 221 | aiagents.directory | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 527 urls but no recognisable listing path |  |  |
| 222 | aicentraltools.com | not_monitorable | ❌ | stale: newest entry is 172d old; source looks stale | 12 | 2026-05-04 |
| 223 | aidirectory.org | not_monitorable | ❌ | stale: short titles (name-like); newest entry is 577d old; source looks stale | 10 | 2025-03-25 |
| 224 | aiexplorebox.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 171 urls but no recognisable listing path |  |  |
| 225 | aifind.ru | not_monitorable | ❌ | stale: newest entry is 437d old; source looks stale | 300 | 2025-08-12 |
| 226 | aiforbusinesses.com | not_monitorable | ❌ | stale: newest entry is 652d old; source looks stale | 272 | 2025-01-10 |
| 227 | aigenerator.tools | not_monitorable | ❌ | stale: newest entry is 190d old; source looks stale | 2142 | 2026-04-16 |
| 228 | aihunt.one | not_monitorable | ❌ | no_public_list: sitemap /wp-sitemap.xml has 43 urls but no recognisable listing path; sitemap /sitemap.xml has 43 urls but no recognisable l |  |  |
| 229 | aiinfinity-meetpatel.notion.site | not_monitorable | ❌ | js_only: sitemap /sitemap.xml has 23 urls but no recognisable listing path |  |  |
| 230 | ainavhub.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 231 | ainewsbase.com | not_monitorable | ❌ | not_a_directory: manual override: news feed | 10 | 2026-10-23 |
| 232 | aiparabellum.com | not_monitorable | ❌ | no_public_list: feed /rss found but feed content looks like articles, not listings; sitemap /sitemap_index.xml has 1527 urls but no recognis |  |  |
| 233 | aipulse.fyi | not_monitorable | ❌ | stale: newest entry is 367d old; source looks stale | 300 | 2025-10-21 |
| 234 | aitogrow.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap_index.xml has 9 urls but no recognisable listing path; sitemap /sitemap.xml has 9 urls but no recognisable  |  |  |
| 235 | aitoolfor.org | not_monitorable | ❌ | stale: newest entry is 346d old; source looks stale | 300 | 2025-11-12 |
| 236 | aitoolmall.com | not_monitorable | ❌ | stale: newest entry is 532d old; source looks stale | 10 | 2025-05-09 |
| 237 | aitoolnet.com | not_monitorable | ❌ | false_positive: manual override: anchor text is a raw URL, name extraction unreliable | 29 |  |
| 238 | aitools.neilpatel.com | not_monitorable | ❌ | dead: home redirects to ubersuggest.com; sitemap /sitemap.xml has 215 urls but no recognisable listing path |  |  |
| 239 | aitools.rdlab.tw | not_monitorable | ❌ | no_public_list |  |  |
| 240 | aitoolsia.com | not_monitorable | ❌ | no_public_list: sitemap /wp-sitemap.xml has 1 urls but no recognisable listing path; sitemap /sitemap.xml has 1 urls but no recognisable lis |  |  |
| 241 | aitoolsmarketer.com | not_monitorable | ❌ | no_public_list: feed /rss.xml found but feed content looks like articles, not listings; sitemap /sitemap.xml has 17 urls but no recognisable |  |  |
| 242 | aitoolsmasters.com | not_monitorable | ❌ | no_public_list: home redirects to 7parabian.com |  |  |
| 243 | aitoprank.com | not_monitorable | ❌ | dead: feed /rss found but feed content looks like articles, not listings; sitemap /wp-sitemap.xml has 30 urls but no recognisable listing pa |  |  |
| 244 | aivalley.ai | not_monitorable | ❌ | stale: newest entry is 1275d old; source looks stale | 4 | 2023-04-27 |
| 245 | aiwarehub.com | not_monitorable | ❌ | stale: newest entry is 240d old; source looks stale | 207 | 2026-02-25 |
| 246 | akama.com | not_monitorable | ❌ | false_positive: manual override: html pattern matched geo category page | 49 |  |
| 247 | alabamaindex.com | not_monitorable | ❌ | no_public_list |  |  |
| 248 | alivelinks.org | not_monitorable | ❌ | false_positive: manual override: html page is a category navigation menu | 90 |  |
| 249 | allbusinessdirectory.biz | not_monitorable | ❌ | false_positive: manual override: html page links are site navigation, not listings | 40 |  |
| 250 | allstartups.info | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 251 | allstatesusadirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 252 | allydirectory.com | not_monitorable | ❌ | stale: newest entry is 6441d old; source looks stale | 300 | 2009-03-05 |
| 253 | alternativeto.net | not_monitorable | ❌ | blocked: home http 403 (anti-bot challenge); anti-bot / forbidden; no probe path accessible |  |  |
| 254 | appli.st | not_monitorable | ❌ | no_public_list |  |  |
| 255 | athenelinks.com | not_monitorable | ❌ | no_public_list |  |  |
| 256 | australiawebdirectory.net | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 257 | backdata.net | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 11 urls but no recognisable listing path |  |  |
| 258 | bahiacar.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 394 urls but no recognisable listing path |  |  |
| 259 | bai.tools | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 16 urls but no recognisable listing path |  |  |
| 260 | bestwebsites.info | not_monitorable | ❌ | no_public_list |  |  |
| 261 | bis-project.eu | not_monitorable | ❌ | no_public_list |  |  |
| 262 | blog-search.com | not_monitorable | ❌ | no_public_list |  |  |
| 263 | blogarama.com | not_monitorable | ❌ | false_positive: manual override: category page of blogs, not latest list | 36 |  |
| 264 | brestlinks.com | not_monitorable | ❌ | no_public_list |  |  |
| 265 | britainbusinessdirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 266 | brownbook.net | not_monitorable | ❌ | no_public_list |  |  |
| 267 | browseinter.net | not_monitorable | ❌ | no_public_list: feed /comments-15.rss found but feed content looks like articles, not listings; sitemap /sitemap.xml has 1330 urls but no re |  |  |
| 268 | business-software.com | not_monitorable | ❌ | false_positive: manual override: html pattern matched video/blog pages | 300 | 2026-10-23 |
| 269 | businessdir.cleaningviews.com | not_monitorable | ❌ | no_public_list |  |  |
| 270 | businessfreedirectory.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 271 | businessindex.hotelyolac.com | not_monitorable | ❌ | no_public_list |  |  |
| 272 | businessseek.biz | not_monitorable | ❌ | false_positive: manual override: html page links are site navigation, not listings | 54 |  |
| 273 | businesstoolvault.com | not_monitorable | ❌ | stale: newest entry is 614d old; source looks stale | 300 | 2025-02-17 |
| 274 | caida.eu | not_monitorable | ❌ | no_public_list |  |  |
| 275 | chameleonwebservices.com | not_monitorable | ❌ | no_public_list |  |  |
| 276 | chatgate.ai | not_monitorable | ❌ | dead: sitemap /sitemap.xml has 5050 urls but no recognisable listing path; sitemap /sitemap_index.xml has 5050 urls but no recognisable list |  |  |
| 277 | cipinet.com | not_monitorable | ❌ | no_public_list |  |  |
| 278 | crazyaboutstartups.com | not_monitorable | ❌ | dead |  |  |
| 279 | ctrlalt.cc | not_monitorable | ❌ | stale: newest entry is 1292d old; source looks stale | 40 | 2023-04-10 |
| 280 | curlie.org | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 281 | d-i-r.com | not_monitorable | ❌ | stale: newest entry is 721d old; source looks stale | 300 | 2024-11-02 |
| 282 | dailyfreeaitools.com | not_monitorable | ❌ | no_public_list |  |  |
| 283 | daytoday.ai | not_monitorable | ❌ | stale: feed /feed.xml found but entries are blog/news posts; newest entry is 329d old; source looks stale | 42 | 2025-11-28 |
| 284 | dechiffre.fr | not_monitorable | ❌ | stale: newest entry is 3458d old; source looks stale | 10 | 2017-05-05 |
| 285 | delv.tools | not_monitorable | ❌ | stale: feed /feed.xml found but entries are blog/news posts; newest entry is 165d old; source looks stale | 203 | 2026-05-11 |
| 286 | dev.to | not_monitorable | ❌ | not_a_directory: manual override: general developer blog feed, not a launch/listing directory | 12 | 2026-10-24 |
| 287 | directory-free.com | not_monitorable | ❌ | no_public_list |  |  |
| 288 | directory.clan.su | not_monitorable | ❌ | dead: parked / for-sale domain |  |  |
| 289 | directory.hotelposadabelen.com | not_monitorable | ❌ | no_public_list |  |  |
| 290 | directory.ldmstudio.com | not_monitorable | ❌ | false_positive: manual override: html page links are category navigation | 15 |  |
| 291 | directory.travelagent.win | not_monitorable | ❌ | no_public_list |  |  |
| 292 | directory.traveltours.review | not_monitorable | ❌ | no_public_list |  |  |
| 293 | directory32.com | not_monitorable | ❌ | no_public_list |  |  |
| 294 | directorytraveltourism.com | not_monitorable | ❌ | no_public_list |  |  |
| 295 | directoryworld.net | not_monitorable | ❌ | no_public_list |  |  |
| 296 | dizila.com | not_monitorable | ❌ | stale: newest entry is 178d old; source looks stale | 20 | 2026-04-28 |
| 297 | dmoz.ebmdattorneys.com | not_monitorable | ❌ | no_public_list |  |  |
| 298 | dokeyai.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 3 urls but no recognisable listing path |  |  |
| 299 | drovenio.app | not_monitorable | ❌ | stale: json /wp-json/wp/v2/ai_news rejected: entries are blog/news posts; newest entry is 160d old; source looks stale | 25 | 2026-05-16 |
| 300 | dtn.jp | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1008 urls but no recognisable listing path |  |  |
| 301 | dujoor.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1 urls but no recognisable listing path |  |  |
| 302 | ebay-dir.com | not_monitorable | ❌ | dead: home http 509 |  |  |
| 303 | eintrag-seo.de | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 373 urls but no recognisable listing path |  |  |
| 304 | elitesitesdirectory.com | not_monitorable | ❌ | stale: newest entry is 337d old; source looks stale | 6 | 2025-11-20 |
| 305 | en.globalsoftwareindex.com | not_monitorable | ❌ | no_public_list |  |  |
| 306 | epirus.vc | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1702 urls but no recognisable listing path |  |  |
| 307 | eposcr.eu | not_monitorable | ❌ | no_public_list |  |  |
| 308 | esearch.cdon.info | not_monitorable | ❌ | no_public_list |  |  |
| 309 | europeannavigator.eu | not_monitorable | ❌ | no_public_list |  |  |
| 310 | exactseek.com | not_monitorable | ❌ | no_public_list |  |  |
| 311 | ezinepublishing.org | not_monitorable | ❌ | no_public_list |  |  |
| 312 | fat64.net | not_monitorable | ❌ | false_positive: manual override: html page is a category navigation menu | 42 |  |
| 313 | favird.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 314 | financesonline.com | not_monitorable | ❌ | stale: newest entry is 245d old; source looks stale | 20 | 2026-02-20 |
| 315 | findbusiness.ukcleaningreviews.com | not_monitorable | ❌ | no_public_list |  |  |
| 316 | fire-directory.com | not_monitorable | ❌ | no_public_list: html /tools/new: looks like a navigation/category menu; html /sites/new: looks like a navigation/category menu |  |  |
| 317 | fmhy.net | not_monitorable | ❌ | not_a_directory: manual override: wiki change feed | 52 | 2026-10-01 |
| 318 | form:aiinfinity | not_monitorable | ❌ | form_only: ledger entry is a hosted form (Google Form/Tally), no directory domain |  |  |
| 319 | form:educatortools | not_monitorable | ❌ | form_only: ledger entry is a hosted form (Google Form/Tally), no directory domain |  |  |
| 320 | form:lachief | not_monitorable | ❌ | form_only: ledger entry is a hosted form (Google Form/Tally), no directory domain |  |  |
| 321 | form:toolsfine | not_monitorable | ❌ | form_only: ledger entry is a hosted form (Google Form/Tally), no directory domain |  |  |
| 322 | form:yourstory | not_monitorable | ❌ | form_only: ledger entry is a hosted form (Google Form/Tally), no directory domain |  |  |
| 323 | francewebdirectory.net | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 324 | freeinternetwebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 325 | freemiumtools.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 67 urls but no recognisable listing path |  |  |
| 326 | freeprwebdirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 327 | freestuff.dev | not_monitorable | ❌ | no_public_list: html /new: duplicate/generic anchor names; html /latest: duplicate/generic anchor names; html /recent/: duplicate/generic an |  |  |
| 328 | freetoprankdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 329 | freewebsubmission.com | not_monitorable | ❌ | no_public_list |  |  |
| 330 | gainweb.org | not_monitorable | ❌ | stale: newest entry is 257d old; source looks stale | 300 | 2026-02-09 |
| 331 | gamedevid.org | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 225 urls but no recognisable listing path |  |  |
| 332 | germanywebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 333 | getmagictools.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 2 urls but no recognisable listing path |  |  |
| 334 | gimpsy.com | not_monitorable | ❌ | no_public_list |  |  |
| 335 | globalsoftwareindex.com | not_monitorable | ❌ | no_public_list |  |  |
| 336 | gmawebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 337 | goseboze.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 31 urls but no recognisable listing path |  |  |
| 338 | gptdemo.net | not_monitorable | ❌ | no_public_list |  |  |
| 339 | gptforge.net | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 340 | gptshunter.com | not_monitorable | ❌ | blocked: home http 403 (anti-bot challenge); anti-bot / forbidden; no probe path accessible |  |  |
| 341 | gtawebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 342 | hackernews.com | not_monitorable | ❌ | not_a_directory: manual override: redirects to news.ycombinator.com/newest (stories, not listings) | 23 |  |
| 343 | hatena.ne.jp | not_monitorable | ❌ | no_public_list: sitemap /solution/blog/corporation/sitemap_index.xml has 47 urls but no recognisable listing path |  |  |
| 344 | hhlink.com | not_monitorable | ❌ | no_public_list |  |  |
| 345 | highrankdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 346 | hitwebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 347 | hotdirectory.net | not_monitorable | ❌ | no_public_list |  |  |
| 348 | iaboxtool.es | not_monitorable | ❌ | false_positive: manual override: comments feed | 10 | 2026-08-24 |
| 349 | idahoindex.com | not_monitorable | ❌ | no_public_list |  |  |
| 350 | iforai.com | not_monitorable | ❌ | stale: newest entry is 335d old; source looks stale | 40 | 2025-11-22 |
| 351 | imagenav.net | not_monitorable | ❌ | stale: newest entry is 185d old; source looks stale | 95 | 2026-04-22 |
| 352 | inc42.com | not_monitorable | ❌ | not_a_directory: manual override: news site feed | 24 | 2026-10-23 |
| 353 | indieblog.page | not_monitorable | ❌ | no_public_list: feed /weeklyfeed found but feed content looks like articles, not listings |  |  |
| 354 | indiehustles.com | not_monitorable | ❌ | no_public_list |  |  |
| 355 | info-listings.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 356 | insidr.ai | not_monitorable | ❌ | stale: newest entry is 519d old; source looks stale | 40 | 2025-05-22 |
| 357 | installpwa.com | not_monitorable | ❌ | no_public_list |  |  |
| 358 | inuidea.com | not_monitorable | ❌ | stale: newest entry is 144d old; source looks stale | 40 | 2026-06-01 |
| 359 | ismailblogger.com | not_monitorable | ❌ | js_only |  |  |
| 360 | italywebdirectory.net | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 361 | jeuxtrouve.net | not_monitorable | ❌ | no_public_list |  |  |
| 362 | katalog-webu.eu | not_monitorable | ❌ | no_public_list: feed /rss/rss.php found but feed content looks like articles, not listings; sitemap /sitemap.xml has 80 urls but no recognis |  |  |
| 363 | katalogstranok.sk | not_monitorable | ❌ | no_public_list |  |  |
| 364 | ki-tools-uebersicht.de | not_monitorable | ❌ | stale: newest entry is 512d old; source looks stale | 40 | 2025-05-29 |
| 365 | landing.mycloudmedia.co.uk | not_monitorable | ❌ | no_public_list |  |  |
| 366 | lfll.cn | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 3026 urls but no recognisable listing path |  |  |
| 367 | library.phygital.plus | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 4044 urls but no recognisable listing path |  |  |
| 368 | linkcentre.com | not_monitorable | ❌ | no_public_list: feed /rss found but feed content looks like articles, not listings; sitemap /sitemap.xml has 26 urls but no recognisable lis |  |  |
| 369 | linkdirectory.budgetotraveler.com | not_monitorable | ❌ | no_public_list |  |  |
| 370 | links-verteiler.de | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 377 urls but no recognisable listing path |  |  |
| 371 | linkstomy.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1 urls but no recognisable listing path |  |  |
| 372 | listedai.co | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 215 urls but no recognisable listing path |  |  |
| 373 | listyourapp.online | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 114 urls but no recognisable listing path |  |  |
| 374 | listyourtool.com | not_monitorable | ❌ | stale: newest entry is 139d old; source looks stale | 300 | 2026-06-06 |
| 375 | llmstxt.info | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 263 urls but no recognisable listing path |  |  |
| 376 | llmstxt.site | not_monitorable | ❌ | no_public_list |  |  |
| 377 | marketingwebdirectory.com | not_monitorable | ❌ | stale: short titles (name-like); newest entry is 2246d old; source looks stale | 15 | 2020-08-29 |
| 378 | marsx.dev | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 835 urls but no recognisable listing path |  |  |
| 379 | masteraifinder.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 31 urls but no recognisable listing path |  |  |
| 380 | mathi.info | not_monitorable | ❌ | no_public_list |  |  |
| 381 | mediafiredirectlink.com | not_monitorable | ❌ | not_a_directory: manual override: unclear feed content | 20 | 2026-10-16 |
| 382 | mogudh.com | not_monitorable | ❌ | stale: newest entry is 500d old; source looks stale | 300 | 2025-06-10 |
| 383 | morefunz.com | not_monitorable | ❌ | false_positive: manual override: page list, not listings | 37 |  |
| 384 | mridul.tech | not_monitorable | ❌ | stale: feed /feed.xml found but feed content looks like articles, not listings; newest entry is 143d old; source looks stale | 300 | 2026-06-02 |
| 385 | navi7.com | not_monitorable | ❌ | no_public_list |  |  |
| 386 | netmegathread.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap-index.xml has 29 urls but no recognisable listing path |  |  |
| 387 | netted.net | not_monitorable | ❌ | stale: newest entry is 610d old; source looks stale | 10 | 2025-02-20 |
| 388 | neuralchooser.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 2893 urls but no recognisable listing path |  |  |
| 389 | newsiteindex.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 390 | nextgentools.me | not_monitorable | ❌ | stale: newest entry is 279d old; source looks stale | 40 | 2026-01-17 |
| 391 | nextpedia.io | not_monitorable | ❌ | stale: newest entry is 1303d old; source looks stale | 40 | 2023-03-30 |
| 392 | nosignups.net | not_monitorable | ❌ | js_only |  |  |
| 393 | nosignuptools.com | not_monitorable | ❌ | stale: newest entry is 187d old; source looks stale | 230 | 2026-04-19 |
| 394 | note.com | not_monitorable | ❌ | not_a_directory: manual override: general blogging platform feed | 10 | 2026-10-22 |
| 395 | offpagesavvy.com | not_monitorable | ❌ | false_positive: manual override: bookmarking-site roundup article, not a listing feed | 41 |  |
| 396 | okay.directory | not_monitorable | ❌ | false_positive: manual override: sponsored/top-pick blocks, no stable listing structure | 26 |  |
| 397 | olarex.eu | not_monitorable | ❌ | no_public_list |  |  |
| 398 | ometeca.org | not_monitorable | ❌ | no_public_list |  |  |
| 399 | once.tools | not_monitorable | ❌ | no_public_list |  |  |
| 400 | onemillionscreenshots.com | not_monitorable | ❌ | no_public_list |  |  |
| 401 | onpaco.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 402 | ontoplist.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap_static.xml has 12 urls but no recognisable listing path; sitemap /sitemap_categories.xml has 314 urls but n |  |  |
| 403 | openmakers.io | not_monitorable | ❌ | stale: newest entry is 1373d old; source looks stale | 145 | 2023-01-19 |
| 404 | our-study.com | not_monitorable | ❌ | no_public_list |  |  |
| 405 | paggu.com | not_monitorable | ❌ | stale: feed /rss found but feed content looks like articles, not listings; newest entry is 3073d old; source looks stale | 15 | 2018-05-25 |
| 406 | perfectwebdirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 407 | portal.sbk-24.de | not_monitorable | ❌ | no_public_list |  |  |
| 408 | prodpapa.com | not_monitorable | ❌ | stale: newest entry is 392d old; source looks stale | 26 | 2025-09-26 |
| 409 | productselectoren.com | not_monitorable | ❌ | no_public_list |  |  |
| 410 | prolinkdirectory.com | not_monitorable | ❌ | stale: newest entry is 20751d old; source looks stale | 104 | 1969-12-31 |
| 411 | qiita.com | not_monitorable | ❌ | not_a_directory: manual override: popular-articles feed, not listings | 30 | 2026-10-23 |
| 412 | qualityinternetdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 413 | quicklinks.net | not_monitorable | ❌ | no_public_list |  |  |
| 414 | relevantsaas.com | not_monitorable | ❌ | stale: newest entry is 206d old; source looks stale | 4 | 2026-03-31 |
| 415 | rssamplifier.com | not_monitorable | ❌ | not_a_directory: manual override: API lists the vendor's own feeds, not directory listings | 91 |  |
| 416 | saasbrowser.com | not_monitorable | ❌ | false_positive: manual override: news-style page | 300 | 2026-10-20 |
| 417 | saashub.com | not_monitorable | ❌ | false_positive: manual override: html page lists comparison headlines, not products | 12 |  |
| 418 | saaspo.com | not_monitorable | ❌ | blocked: home http 403 (anti-bot challenge); anti-bot / forbidden; no probe path accessible |  |  |
| 419 | searchweb.seomarketplace.net | not_monitorable | ❌ | no_public_list |  |  |
| 420 | seekdragon.com | not_monitorable | ❌ | no_public_list |  |  |
| 421 | seekwebsites.innovasysindia.com | not_monitorable | ❌ | no_public_list |  |  |
| 422 | seofai.com | not_monitorable | ❌ | stale: json /wp-json/wp/v2/tool_comparison rejected: feed content looks like articles, not listings; newest entry is 198d old; source looks  | 40 | 2026-04-08 |
| 423 | seowebdirectory.com | not_monitorable | ❌ | dead: sitemap /sitemap.xml has 500 urls but no recognisable listing path |  |  |
| 424 | sick.tools | not_monitorable | ❌ | no_public_list: sitemap /sitemap_index.xml has 4 urls but no recognisable listing path; sitemap /sitemap.xml has 4 urls but no recognisable  |  |  |
| 425 | siliconfriendly.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 1627 urls but no recognisable listing path |  |  |
| 426 | sitepromotiondirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 427 | sites-plus.com | not_monitorable | ❌ | no_public_list |  |  |
| 428 | sitesondisplay.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 3 urls but no recognisable listing path |  |  |
| 429 | smartwebdirectory.com | not_monitorable | ❌ | no_public_list: html /tools/new: looks like a navigation/category menu; html /sites/new: looks like a navigation/category menu |  |  |
| 430 | snapmunk.com | not_monitorable | ❌ | false_positive: manual override: comments feed (startups.snapmunk.com has its own enabled source) | 100 | 2026-10-24 |
| 431 | somuch.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 510 urls but no recognisable listing path |  |  |
| 432 | sonicrun.com | not_monitorable | ❌ | no_public_list |  |  |
| 433 | sprout24.com | not_monitorable | ❌ | stale: newest entry is 248d old; source looks stale | 6 | 2026-02-17 |
| 434 | stackviv.ai | not_monitorable | ❌ | stale: newest entry is 136d old; source looks stale | 300 | 2026-06-09 |
| 435 | startupbuffer.com | not_monitorable | ❌ | blocked: home http 403 (anti-bot challenge); anti-bot / forbidden; no probe path accessible |  |  |
| 436 | startupcollections.com | not_monitorable | ❌ | stale: newest entry is 1647d old; source looks stale | 300 | 2022-04-20 |
| 437 | startuproulette.com | not_monitorable | ❌ | dead: no connection / DNS failure on https+http, apex+www |  |  |
| 438 | startuptracker.io | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 4 urls but no recognisable listing path |  |  |
| 439 | submit.biz | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 349 urls but no recognisable listing path |  |  |
| 440 | superaitools.io | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 4 urls but no recognisable listing path |  |  |
| 441 | superblogdirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 442 | taalk.com | not_monitorable | ❌ | no_public_list: feed /rss found but feed content looks like articles, not listings; sitemap /sitemap_index.xml has 1157 urls but no recognis |  |  |
| 443 | techpluto.com | not_monitorable | ❌ | stale: newest entry is 1157d old; source looks stale | 28 | 2023-08-23 |
| 444 | textlinkdirectory.com | not_monitorable | ❌ | no_public_list |  |  |
| 445 | thatsmy.ai | not_monitorable | ❌ | stale: newest entry is 219d old; source looks stale | 72 | 2026-03-18 |
| 446 | theaicorvex.com | not_monitorable | ❌ | stale: newest entry is 192d old; source looks stale | 20 | 2026-04-15 |
| 447 | thedirectory.com.ar | not_monitorable | ❌ | no_public_list |  |  |
| 448 | thejoai.com | not_monitorable | ❌ | no_public_list |  |  |
| 449 | thestartupinc.com | not_monitorable | ❌ | stale: json /wp-json/wp/v2/blog rejected: entries are blog/news posts; newest entry is 147d old; source looks stale | 10 | 2026-05-29 |
| 450 | tinystartups.co | not_monitorable | ❌ | dead: home http 525 |  |  |
| 451 | tinytools.directory | not_monitorable | ❌ | no_public_list |  |  |
| 452 | tipocode.com | not_monitorable | ❌ | no_public_list |  |  |
| 453 | toolai.io | not_monitorable | ❌ | no_public_list: sitemap /sitemap-index.xml has 875 urls but no recognisable listing path; sitemap /sitemap.xml has 875 urls but no recognisa |  |  |
| 454 | toolassistant.com | not_monitorable | ❌ | stale: newest entry is 1362d old; source looks stale | 3 | 2023-01-31 |
| 455 | toolbattles.com | not_monitorable | ❌ | stale: json /wp-json/wp/v2/elementor_snippet rejected: feed content looks like articles, not listings; json /wp-json/wp/v2/company-update re | 6 | 2023-12-11 |
| 456 | tools-ai.online | not_monitorable | ❌ | no_public_list |  |  |
| 457 | tools.so | not_monitorable | ❌ | no_public_list |  |  |
| 458 | toolsforhumans.ai | not_monitorable | ❌ | stale: newest entry is 193d old; source looks stale | 29 | 2026-04-13 |
| 459 | toptools.ai | not_monitorable | ❌ | stale: newest entry is 227d old; source looks stale | 100 | 2026-03-11 |
| 460 | totallyfreetools.com | not_monitorable | ❌ | stale: newest entry is 191d old; source looks stale | 48 | 2026-04-15 |
| 461 | trymy.app | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 243 urls but no recognisable listing path |  |  |
| 462 | turkeywebdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 463 | txtlinks.com | not_monitorable | ❌ | no_public_list |  |  |
| 464 | ukinternetdirectory.net | not_monitorable | ❌ | no_public_list |  |  |
| 465 | unamenlinea.info | not_monitorable | ❌ | no_public_list |  |  |
| 466 | usawebsitesdirectory.com | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 467 | utorr.org | not_monitorable | ❌ | no_public_list |  |  |
| 468 | velog.io | not_monitorable | ❌ | no_public_list |  |  |
| 469 | vipdaohang.cn | not_monitorable | ❌ | no_public_list |  |  |
| 470 | vipdirectory.com.ar | not_monitorable | ❌ | no_public_list: html /index.php: too few entries |  |  |
| 471 | waildworld.com | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 33 urls but no recognisable listing path |  |  |
| 472 | webdirectory-submit.com | not_monitorable | ❌ | no_public_list |  |  |
| 473 | websitesindex.medicalbillinglogic.com | not_monitorable | ❌ | no_public_list |  |  |
| 474 | webspider24.de | not_monitorable | ❌ | no_public_list: sitemap /sitemap.xml has 9911 urls but no recognisable listing path |  |  |
| 475 | websurl.com | not_monitorable | ❌ | no_public_list |  |  |
| 476 | webwiki.com | not_monitorable | ❌ | blocked: home http 403 (anti-bot challenge); anti-bot / forbidden; no probe path accessible |  |  |
| 477 | whatuseek.com | not_monitorable | ❌ | no_public_list |  |  |
| 478 | youmightnotneed.co | not_monitorable | ❌ | stale: newest entry is 130d old; source looks stale | 84 | 2026-06-15 |
