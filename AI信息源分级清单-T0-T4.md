# AI 日报信息源分级清单 · T0–T4

**版本**：v1 · 2026-09-15 建立 ｜ 就地更新至 **2026-09-17**（006 期，条目数不变，只改标注与缺口）
**用途**：为「AI 免费内容与权益速递」日报提供扫描路由。层级 = 可信度与优先级，不是扫描频率。

**核对结果（脚本计数，非估算）**：T0 = 97、T1 = 19、T2 = 18、T3 = 36、T4 = 12，**合计 182**，与你标注的分级数量完全一致；其中带 `[RSS]` 标记（表中 ✅）实际共 **44** 条，可走 RSS 直取，其余 138 条需抓取或人工。

T0 内部分类复核：论文与预印本 12、模型与开源 10、官方一手·国外 23、官方一手·国内 20、政策与监管 15、评测与榜单 17 → 合计 97 ✅；T3 内部：国外 20 + 国内 16 = 36 ✅。

---

## 扫描路由规则（怎么用这套清单）

| 层级 | 定位 | 日报中的用法 | 扫描建议 |
| --- | --- | --- | --- |
| **T0 根节点** | 一手事实：论文、模型权重、厂商公告、政策原文、榜单原始分 | **只用 T0 定「有没有这回事」**。凡额度、截止日、协议，必须有 T0 或厂商官方文档背书 | 每日全量标题扫描 + 关键词过滤 |
| **T1 社区社交** | 早期信号、实测体感、翻车预警 | 用 T1 **发现线索**，回到 T0 求证后才能写进报告 | 每日抽样，重点 r/LocalLLaMA、HN、知乎 |
| **T2 Newsletter** | 已消化的综述与判断 | 用来**查漏**，看别人这周提了什么我没覆盖 | 每日扫标题，命中再读 |
| **T3 媒体** | 二手报道、中文落地信息 | **只当线索源**。媒体口径一律降级标注（例："公开报道"而非"官方"） | 每日扫国内 16 家 |
| **T4 聚合器** | 降噪、去重、补漏 | 用聚合器做**交叉验证**：一条权益若聚合器与 T0 冲突，以 T0 为准 | 每次出刊前跑一遍 |

**三条硬规则**：
1. **分级 ≠ 可信度排序的唯一依据**。T0 里的厂商博客同样是公关稿，额度类信息要认**帮助中心/定价页**，不认博客。
2. **中文媒体（T3 国内）必须标注口径**：`【官方】` / `【公开报道】` / `【社区口径】`，不得混写。
3. **权益类信息有 24–72 小时衰减期**。出刊时一律写明"核验于 YYYY-MM-DD"，过期的直接在截止时间表标 ⚪ 并移到"已结束"，不删条目（保留可追溯）。

---

## T0 · 根节点（97）

### 论文与预印本（12）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| arXiv cs.AI | https://arxiv.org/list/cs.AI/recent | ✅ | 新架构/新方法，判断哪些能力即将变便宜 |
| arXiv cs.CL | https://arxiv.org/list/cs.CL/recent | ✅ | 语言模型、长上下文进展 |
| arXiv cs.CV | https://arxiv.org/list/cs.CV/recent | ✅ | 图像/视频生成，免费出图工具的能力源头 |
| arXiv cs.LG / stat.ML | https://arxiv.org/list/cs.LG/recent | ✅ | 训练与推理成本下降的信号 |
| Hugging Face Daily Papers | https://huggingface.co/papers | — | 每日精选，省去通读 arXiv |
| OpenReview | https://openreview.net | — | 顶会审稿态，抢先看到未正式接收的工作 |
| Papers with Code | https://paperswithcode.com | — | 论文 → 代码 → 权重，判断能否白嫖 |
| Semantic Scholar API | https://api.semanticscholar.org | — | 程序化检索，适合自动化 |
| 顶会官网 NeurIPS/ICML/CVPR/ACL | https://neurips.cc | — | 正式接收版本，年度级信源 |
| TMLR / JMLR | https://jmlr.org | — | 开放评审期刊，质量稳定 |
| Nature MI / Nature / Science / PNAS | https://www.nature.com/natmachintell | — | 权威背书，用于政策与科普向 |
| AMiner | https://www.aminer.cn | — | 中文侧学者/论文图谱 |

> 命中记录（截至 006 期）：arXiv（Occamy-1.0，2609.11977，9/4 提交）；Hugging Face Daily Papers / ModelScope（ZDTaichu5.0-9B 9/15、书生-S2 9/15、Atria Dawn Preview 9/17 的技术报告均在此首发）。

### 模型与开源（10）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| Hugging Face Models (trending) | https://huggingface.co/models?sort=trending | — | **免费权重第一发现地**（005 期 Qwen3.8-27B 登顶历史最受欢迎榜；006 期 ZDTaichu5.0-9B） |
| Hugging Face Blog | https://huggingface.co/blog | ✅ | 平台政策变动（免费层、推理供应商） |
| Hugging Face Spaces | https://huggingface.co/spaces | — | 免费在线 Demo，可直接试模型 |
| ModelScope 魔搭 | https://modelscope.cn/models | — | 国内权重镜像，下载快；**006 期 ZDTaichu5.0-9B、Atria Dawn Preview、书生-S2 的一手发布页** |
| GitHub Trending | https://github.com/trending | — | 开源工具热度，判断哪些值得进报告 |
| GitHub Releases (各项目 atom) | https://docs.github.com/en/rest/releases | ✅ | 版本号级更新，抓"免费额度调整" |
| OpenRouter Models | https://openrouter.ai/models | — | 一个 Key 试几百个模型，免费档清单。**⚠️ 006 期起升级为 T0 级发布地**：匿名/隐身模型（Ox Alpha、Union Alpha）**只在这里有规格、条款与实时性能数据**，模型厂商官网查不到。查条款认 `Stealth Model Terms` |
| Gitee AI / GitCode | https://ai.gitee.com | — | 国内开源托管 |
| 始智AI wisemodel | https://wisemodel.cn | — | 国内模型社区 |
| 硅基流动 SiliconFlow 模型广场 | https://siliconflow.cn/models | — | 免费/低价推理，常驻免费额度来源 |

### 官方一手 · 国外（23）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| OpenAI News | https://openai.com/news | ✅ | 定价与免费档变动 |
| OpenAI Research | https://openai.com/research | — | 能力边界 |
| Anthropic News | https://www.anthropic.com/news | ✅ | Claude 免费档、速率 |
| Anthropic Engineering | https://www.anthropic.com/engineering | — | Agent 工程实践 |
| Google DeepMind Blog | https://deepmind.google/discover/blog | ✅ | Gemini 系列 |
| Google AI Blog | https://blog.google/technology/ai/ | ✅ | 产品侧免费入口（AI Studio、NotebookLM） |
| Google Research Blog | https://research.google/blog/ | ✅ | 论文一手 |
| Meta AI Blog | https://ai.meta.com/blog/ | ✅ | Llama 系列权重 |
| Microsoft AI Blog | https://blogs.microsoft.com/ai/ | ✅ | Copilot / GitHub Models 免费档 |
| Microsoft Research | https://www.microsoft.com/en-us/research/blog/ | — | 研究向 |
| NVIDIA Blog | https://blogs.nvidia.com/ | ✅ | **NIM 免费模型池**（本期：78+ 免费模型） |
| Mistral AI News | https://mistral.ai/news | — | Le Chat 免费层 |
| xAI News | https://x.ai/news | — | Grok 定价 |
| Cohere Blog | https://cohere.com/blog | — | 免费 1,000 次/月 |
| Midjourney | https://www.midjourney.com/showcase | — | 图像，免费档稀缺 |
| Runway | https://runwayml.com/news | — | 视频，一次性积分陷阱源 |
| Perplexity Blog | https://www.perplexity.ai/hub/blog | — | 免费搜索额度 |
| Cursor Changelog | https://cursor.com/changelog | — | 编辑器免费档 |
| Cognition (Devin) | https://cognition.ai/blog | — | Agent 产品 |
| Apple Machine Learning Research | https://machinelearning.apple.com/research | — | 端侧模型，本地免费路线 |
| AWS Machine Learning Blog | https://aws.amazon.com/blogs/machine-learning/ | — | 云侧免费层 |
| IBM Research | https://research.ibm.com/blog | — | 企业级 |
| Stability AI | https://stability.ai/news | — | 开源图像权重 |

> 本期命中：NVIDIA Blog（9/3 宣布收购 Hugging Face，$129.3 亿）。

### 官方一手 · 国内（20）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| DeepSeek 研究与动态 | https://www.deepseek.com/zh/news | — | **全免费路线**，V4.1 Flash（9/10 多模态 + MIT） |
| 阿里云百炼·新模型发布 | https://help.aliyun.com/zh/model-studio/models | — | 免费额度规则（**只认 help 页，不认活动页**） |
| 阿里 Qwen 官方博客 | https://qwen.ai/blog | — | Qwen 开源权重 |
| 月之暗面 Kimi | https://platform.moonshot.cn/docs | — | 免费额度、上下文 |
| 智谱 GLM | https://docs.bigmodel.cn/cn/guide/start/model-overview | — | **GLM-4.7-Flash 永久免费**、夜间限免 |
| MiniMax | https://www.minimaxi.com/news | — | 海螺视频免费次数 |
| 火山引擎 / 豆包 | https://www.volcengine.com/docs | — | 日均 200 万 Token、高校 1 亿 |
| 字节 Seed 团队 | https://seed.bytedance.com/ | — | Seedance / Seedream，即梦免费额度来源 |
| 百度文心 | https://cloud.baidu.com/doc/index.html | — | 文心 4.0 全月免费、Comate 限免 |
| 腾讯混元 | https://hunyuan.tencent.com/ | — | Hy3 / Hy4 限免窗口 |
| 腾讯研究院 | https://www.tisi.org/ | — | 行业判断 |
| 讯飞星火 | https://xfyun.cn/doc/ | — | Spark Lite 永久免费、X2.5 开源 |
| 小米 MiMo | https://www.xiaomiev.com/ | — | MiMo Code 免注册 |
| 华为云 / 盘古 | https://www.huaweicloud.com/product/pangu.html | — | 盘古免费试用 |
| 面壁智能 MiniCPM | https://www.minicpm.cn/ | — | 端侧开源 |
| 阶跃星辰 | https://www.stepfun.com/ | — | Step 系列 |
| 快手可灵 (Kling) | https://klingai.com/ | — | **66 积分/天**免费视频主力 |
| 智源研究院 BAAI | https://www.baai.ac.cn/ | — | FlagEval 榜单、开源 |
| 昆仑万维 / 零一万物 | https://www.singularis.ltd/ | — | 开源权重 |
| 蚂蚁 / 美团 / 京东 AI | https://www.antgroup.com/news/media | — | CatPaw 等新产品免费额度 |

> 本期命中：讯飞（X2.5-1.7B/4B，9/1 开源 Apache-2.0）、DeepSeek（V4.1 Flash 9/10 发布）。

### 政策与监管（15）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| 国家网信办 | https://www.cac.gov.cn | — | 生成式 AI 备案、合规红线 |
| 工业和信息化部 | https://www.miit.gov.cn | — | 产业政策 |
| 国家数据局 | https://www.nda.gov.cn | — | 数据要素 |
| 中国信通院 CAICT | https://www.caict.ac.cn | — | 白皮书、标准 |
| 巨潮资讯网 cninfo | https://www.cninfo.com.cn | — | 上市公司 AI 相关公告 |
| IT 桔子 | https://www.itjuzi.com | — | 融资与新产品 |
| 国家企业信用信息公示系统 | https://www.gsxt.gov.cn | — | 主体核验（防骗） |
| SEC EDGAR 全文检索 | https://www.sec.gov/cgi-bin/srqsb?text=artificial+intelligence | — | 海外厂商披露 |
| EU AI Act 官方 | https://artificialintelligenceact.eu/ | — | 生效时间表 |
| EUR-Lex | https://eur-lex.europa.eu/ | — | 法规原文 |
| UK AI Safety Institute | https://www.aisi.gov.uk/ | — | 安全评估 |
| NIST AI | https://www.nist.gov/topics/artificial-intelligence | — | 标准与框架 |
| US Federal Register | https://www.federalregister.gov | — | 美国行政规则 |
| The White House OSTP | https://www.whitehouse.gov/ostp/ | — | 政策取向 |
| OECD.AI / UNESCO | https://oecd.ai/ | — | 国际比较 |

> 本期命中：成都市政府门户（词元券征求意见稿）——**注意：地方词元券类信源未列入本清单，建议补 T0 政策节的"地方政府门户"聚合项**。

### 评测与榜单（17）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| LMArena Leaderboard | https://lmarena.ai/leaderboard | — | 文本综合排名 |
| LMArena Image Arena | https://lmarena.ai/leaderboard/image | — | 图像排名 |
| LMArena Video Arena | https://lmarena.ai/leaderboard/video | — | 视频排名 |
| LMArena WebDev Arena | https://lmarena.ai/leaderboard/webdev | — | 前端/网页生成 |
| Artificial Analysis | https://artificialanalysis.ai/ | — | 性价比、吞吐、延迟 |
| llm-stats.com | https://llm-stats.com/ | — | 多榜聚合 |
| LiveBench | https://livebench.ai/ | — | 防污染评测 |
| SWE-bench Verified | https://www.swebench.com/ | — | 代码 Agent |
| Terminal-bench | https://www.tbench.ai/leaderboards/terminal-bench | — | 终端 Agent |
| OSWorld | https://os-world.github.io/ | — | 计算机使用 |
| Epoch AI | https://epoch.ai/ | — | 算力与趋势 |
| Vals AI | https://www.vals.ai/ | — | Agent 评测 |
| Scale SEAL Leaderboard | https://scale.com/leaderboard | — | 企业级评测 |
| OpenCompass 司南 | https://opencompass.org.cn/ | — | 中文开源评测 |
| SuperCLUE | https://www.superclue.ai/ | — | 中文综合 |
| 智源 FlagEval | https://flageval.baai.ac.cn/ | — | 多模态评测 |
| C-Eval / CMMLU | https://cevalbenchmark.com/ | — | 中文知识 |

---

## T1 · 社区与社交（19）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| X / Twitter | https://x.com | — | 最快信号，需交叉验证 |
| Reddit r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA/ | ✅ | 本地/免费模型实测，**翻车预警第一现场** |
| Reddit r/MachineLearning | https://www.reddit.com/r/MachineLearning/ | ✅ | 论文讨论 |
| Reddit r/artificial | https://www.reddit.com/r/artificial/ | ✅ | 泛 AI 新闻 |
| Reddit r/OpenAI / r/ClaudeAI / r/singularity | https://www.reddit.com/r/singularity/ | ✅ | 产品体验 |
| Reddit r/StableDiffusion | https://www.reddit.com/r/StableDiffusion/ | ✅ | 出图工具实测 |
| Hacker News | https://news.ycombinator.com/ | — | 技术圈热点 |
| HN 关键词 RSS (hnrss.org) | https://hnrss.org/newest?q=AI | ✅ | **可程序化订阅的 AI 关键词流** |
| 知乎 · AI 话题 | https://www.zhihu.com/topic/19556664/hot | — | 中文深度讨论 |
| 掘金 · 人工智能 | https://juejin.cn/ai | — | 开发者实践 |
| 微信公众号（AI 类） | https://mp.weixin.qq.com/ | — | 厂商首发渠道之一 |
| 微博（AI 官方账号+话题） | https://s.weibo.com/ | — | 国内厂商公告 |
| B 站（发布会+测评） | https://www.bilibili.com/ | — | 发布会回放、实测 |
| 小红书（AI 工具玩法） | https://www.xiaohongshu.com/ | — | **发布玩法 + 平台原生 AI 生态（RED Skill / Builder Hub）** |
| Bluesky | https://bsky.app/ | — | 研究者聚集地 |
| LinkedIn | https://www.linkedin.com/ | — | 企业级动态 |
| LessWrong | https://www.lesswrong.com/ | ✅ | 理性主义视角长文 |
| AI Alignment Forum | https://www.alignmentforum.org/ | ✅ | 对齐研究 |
| V2EX / 少数派 | https://sspai.com/ | — | 工具玩家实测 |

---

## T2 · Newsletter（18）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| Import AI (Jack Clark) | https://importai.substack.com/ | ✅ | 政策 + 技术双视角 |
| The Batch (DeepLearning.AI) | https://www.deeplearning.ai/the-batch/ | — | 周更综述 |
| The Rundown AI | https://www.therundown.ai/ | ✅ | 日更，产品向 |
| TLDR AI | https://tldr.tech/ai | — | 极简日更 |
| Ben's Bites | https://www.bensbites.co/ | — | 日更 |
| Latent Space | https://www.latent.space/ | — | 深度访谈 |
| Ahead of AI (Raschka) | https://magazine.sebastianraschka.com/ | ✅ | 技术细节讲得最清楚 |
| AI Snake Oil | https://www.aisnakeoil.com/ | ✅ | **祛魅视角**，避坑素材来源 |
| Simon Willison's Blog | https://simonwillison.net/ | ✅ | 实操、本地模型 |
| The Sequence | https://thesequence.substack.com/ | ✅ | 企业级 |
| Interconnects | https://www.interconnects.ai/ | — | 训练与推理经济学 |
| Stratechery | https://stratechery.com/ | ✅ | 商业战略 |
| Last Week in AI | https://lastweekin.ai/ | — | 周更汇总 |
| The Neuron | https://www.theneurondaily.com/ | — | 日更 |
| 宝玉的博客 | https://baoyu.io/blog | ✅ | **中文翻译一手料**，海外信息落地最快 |
| Founder Park AI 速递 | https://www.founderparks.com/ | — | 中文日更 |
| 机器之心 SOTA! | https://sota.jiqizhixin.com/ | — | 模型/SOTA 追踪 |
| 硅星人 | https://www.guixingren.com/ | — | 出海与商业视角 |

---

## T3 · 媒体（36）

### 国外（20）

| 信源 | 地址 | RSS |
| --- | --- | --- |
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/ | ✅ |
| The Verge AI | https://www.theverge.com/ai-artificial-intelligence | ✅ |
| VentureBeat AI | https://venturebeat.com/category/ai/ | ✅ |
| MIT Technology Review AI | https://www.technologyreview.com/topic/artificial-intelligence/ | ✅ |
| Ars Technica | https://arstechnica.com/ai/ | ✅ |
| Wired AI | https://www.wired.com/tag/ai/ | ✅ |
| The Information | https://www.theinformation.com/ | — |
| Reuters AI | https://www.reuters.com/technology/artificial-intelligence/ | — |
| Bloomberg / FT / WSJ AI | https://www.bloomberg.com/ai | — |
| The Decoder | https://the-decoder.com/ | ✅ |
| Artificial Intelligence News | https://www.artificialintelligence-news.com/ | ✅ |
| MarkTechPost | https://www.marktechpost.com/ | — |
| IEEE Spectrum | https://spectrum.ieee.org/artificial-intelligence | — |
| Quanta Magazine | https://www.quantamagazine.org/ | ✅ |
| ZDNet AI / SiliconANGLE | https://www.zdnet.com/topic/artificial-intelligence/ | — |
| The Register | https://www.theregister.com/ai/ | — |
| Business Insider / Axios / Semafor | https://www.axios.com/technology/ai | — |
| Nature / Science news | https://www.nature.com/subjects/machine-learning | — |
| Tom's Hardware / ServeTheHome | https://www.tomshardware.com/tech-industry/artificial-intelligence | — |
| The Economist / Rest of World | https://restofworld.org/series/ai/ | — |

### 国内（16）

| 信源 | 地址 | RSS |
| --- | --- | --- |
| 机器之心 | https://www.jiqizhixin.com/ | ✅ |
| 量子位 | https://www.qbitai.com/ | ✅ |
| 新智元 | https://www.7wake.com/ | — |
| AI 科技评论（雷峰网） | https://www.leiphone.com/category/aikeji | ✅ |
| InfoQ · AI 前线 | https://www.infoq.cn/topic/AI | ✅ |
| 36 氪 · AI 频道 | https://36kr.com/channel/ai | — |
| 晚点 LatePost | https://www.latepost.com/ | — |
| 极客公园 | https://www.geekpark.net/ | — |
| 钛媒体 / TMTPost | https://www.tmtpost.com/ | — |
| 爱范儿 | https://www.ifanr.com/ | — |
| 品玩 PingWest | https://www.pingwest.com/ | — |
| 虎嗅 | https://www.huxiu.com/ | — |
| CSDN / 开源中国 / 掘金 | https://juejin.cn/ | — |
| 阿里云 / 腾讯云开发者社区 | https://developer.aliyun.com/ | — |
| Datawhale / PaperWeekly / AI TIME | https://www.datawhale.cn/ | — |
| 智源社区 / 将门创投 | https://hub.baai.ac.cn/ | — |

---

## T4 · 聚合器与工具（12）

| 信源 | 地址 | RSS | 对本报告的用途 |
| --- | --- | --- | --- |
| RSSHub | https://docs.rsshub.app/ | — | **把无 RSS 的源变成 RSS**（微博/B站/小红书/知乎都靠它） |
| Inoreader / Feedly / FreshRSS | https://www.inoreader.com/ | — | 统一阅读与去重 |
| HN Algolia API | https://hn.algolia.com/api | — | 程序化检索 HN 历史 |
| Google Alerts | https://www.google.com/alerts | — | 关键词邮件推送 |
| GitHub Actions 定时抓取 | https://docs.github.com/en/actions | — | **自动化骨架** |
| daily.dev | https://daily.dev/ | — | 开发者信息流 |
| AI-HOT（168 信源分级）· 主理人「数字生命卡兹克」 | https://aihot.virxact.com/ · **新域名 https://aihot.news/** | — | **T4 里用途最高的一条**：按天归档 + 精确到分钟的时间戳、每条带 **AI 评分（0–100）+ 推荐理由**、标注**「另有 N 家信源报道」**（天然跨源交叉）、按主题频道追溯（`/topics/trends`）、条目永久链接 `aihot.news/items/<id>` 可跳原文。用法：**当每日扫描的入口层**，再由它跳去 T0 原文定事实。⚠️ 它的"AI 评分"是**模型打分，不是事实核查**，结论仍须回 T0 |
| RadarAI | https://radarai.top/ | — | 中文聚合 |
| AITOP100 | https://aitop100.cn/ | — | 中文榜单 |
| BestBlogs.dev | https://www.bestblogs.dev/ | — | 优质博客聚合 |
| Ground News / Particle | https://ground.news/ | — | 立场偏差对比 |
| Product Hunt AI | https://www.producthunt.com/topics/artificial-intelligence | ✅ | **新工具首发**，免费档信息最早出现地 |

---

## 清单缺口（本期实际取料但清单里没有的源）

以下各类在 004–006 期实际贡献了硬信息，建议补进清单。
（**计数修正**：005 期此处写"这 4 类"，但表内实列 5 行；006 期修正为 6 类。）

| 缺口 | 建议补入层级 | 说明 |
| --- | --- | --- |
| **上海人工智能实验室（书生 / InternLM）** | T0 官方一手·国内 | 004 期即提出、006 期仍未进清单（已建议三期）。Atria Dawn Preview 744B MIT、书生-S2 均出自这里，并在魔搭同步放出 |
| **免费额度垂直追踪站**：freellm.net（484+ 免费模型、228 条实时验证）、aifree.dev、tokennav.cc/free | T4 聚合器 | 权益类日报的核心弹药库，目前只能靠 T3 媒体转述。**注意其时效性同样以天计**（006 期发现多篇 9 月"免费 API 汇总"仍写 GLM-4-Flash、5000 万 DeepSeek 额度） |
| **什么值得买 / All Agent 百科** 等中文权益清单 | T4 聚合器 | 国内限时福利的**唯一系统整理方**，虽然要降级标注口径 |
| **地方政府门户 / 经信部门**（成都、杭州、深圳龙岗、武汉江夏等） | T0 政策与监管 | 词元券是 004 期最大额度来源（单主体年最高 200 万），006 期杭州 Token 卡亦出自市级口径；清单目前只有中央级部委 |
| **内容平台官方创作者中心 / 开发者文档**（抖音 AI 工坊、小红书开发者文档、B站 Toy、腾讯吐司、微信公众号后台、**快手 AI 互动内容招募**） | T0 官方一手·国内 | 005 期"AI 免费内容发布"线的全部关键事实出自这里；006 期再增硬证据——**快手的首批创作者招募、B站 Toy 的 2956 万体验量口径，全部出自平台方**，而清单 T3 只有媒体转述。免费分发政策（沙箱权限、审核规则、激励）必须以官方文档为准 |
| 🆕 **Agent Harness / 模型托管平台官方页**（**OpenCode**、**Cline**、**Cloudflare Workers AI**、**OpenRouter 模型页与 Stealth Model Terms**） | T0 官方一手 + T1 社区 | 006 期头条 **Union Alpha 的全部一手事实出自这里**——它不在任何模型厂商官网上，只在**托管方**的模型页与条款里（且同一模型在 OpenCode 与 OpenRouter 的条款不同）。清单"模型与开源"目前只覆盖 HF / ModelScope / GitHub，**缺托管与 Harness 这一层**，而这层正是当下免费 API 的第一发布地 |

---

> **维护规则**：本清单只增不减。信源失效时改标注为「⚠️ 失效（YYYY-MM-DD）」并保留条目，不做删除——保持可追溯。
