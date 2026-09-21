# AI 日报信息源分级清单 · T0–T4

**版本**：v1 · 2026-09-15 建立 ｜ 就地更新至 **2026-09-21**（010 期，**条目数 185 → 189**；新增北京市经信局与市发改委、TypeSafe AI、ComfyUI Blog、Local Model Watch 四条；第 5、6 类缺口各补一条量化代价）
**用途**：为「AI 免费内容与权益速递」日报提供扫描路由。层级 = 可信度与优先级，不是扫描频率。

**核对结果（脚本计数，非估算）**：T0 = 97、T1 = 19、T2 = 18、T3 = 36、T4 = 12，**合计 182**，与你标注的分级数量完全一致；其中带 `[RSS]` 标记（表中 ✅）实际共 **44** 条，可走 RSS 直取，其余 138 条需抓取或人工。

T0 内部分类复核：论文与预印本 12、**模型与开源 11**、**官方一手·国外 24**、官方一手·国内 20、**政策与监管 17**、评测与榜单 17 → 合计 **101 ✅**；T3 内部：国外 20 + 国内 16 = 36 ✅；**T4 由 14 增至 15**（新增 Local Model Watch）→ **全表合计 189 条**（与 `build_source_hits.py` 实跑的行数一致）。**010 期新增四条**：T0 政策与监管 +1（**北京市经信局 + 市发改委**）、T0 模型与开源 +1（**ComfyUI Blog**）、T0 官方一手·国外 +1（**TypeSafe AI**）、T4 +1（**Local Model Watch**）。

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

## T0 · 根节点（101）

### 论文与预印本（12）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| arXiv cs.AI | https://arxiv.org/list/cs.AI/recent | ✅ | 新架构/新方法，判断哪些能力即将变便宜 | 005 | 3 |
| arXiv cs.CL | https://arxiv.org/list/cs.CL/recent | ✅ | 语言模型、长上下文进展 | 005 | 3 |
| arXiv cs.CV | https://arxiv.org/list/cs.CV/recent | ✅ | 图像/视频生成，免费出图工具的能力源头 | 005 | 3 |
| arXiv cs.LG / stat.ML | https://arxiv.org/list/cs.LG/recent | ✅ | 训练与推理成本下降的信号 | 005 | 3 |
| Hugging Face Daily Papers | https://huggingface.co/papers | — | 每日精选，省去通读 arXiv | 010 | 36 |
| OpenReview | https://openreview.net | — | 顶会审稿态，抢先看到未正式接收的工作 | — | 0 |
| Papers with Code | https://paperswithcode.com | — | 论文 → 代码 → 权重，判断能否白嫖 | — | 0 |
| Semantic Scholar API | https://api.semanticscholar.org | — | 程序化检索，适合自动化 | — | 0 |
| 顶会官网 NeurIPS/ICML/CVPR/ACL | https://neurips.cc | — | 正式接收版本，年度级信源 | — | 0 |
| TMLR / JMLR | https://jmlr.org | — | 开放评审期刊，质量稳定 | — | 0 |
| Nature MI / Nature / Science / PNAS | https://www.nature.com/natmachintell | — | 权威背书，用于政策与科普向 | — | 0 |
| AMiner | https://www.aminer.cn | — | 中文侧学者/论文图谱 | — | 0 |

> 命中记录（截至 006 期）：arXiv（Occamy-1.0，2609.11977，9/4 提交）；Hugging Face Daily Papers / ModelScope（ZDTaichu5.0-9B 9/15、书生-S2 9/15、Atria Dawn Preview 9/17 的技术报告均在此首发）。

### 模型与开源（11）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| Hugging Face Models (trending) | https://huggingface.co/models?sort=trending | — | **免费权重第一发现地**（005 期 Qwen3.8-27B 登顶历史最受欢迎榜；006 期 ZDTaichu5.0-9B） | 010 | 43 |
| Hugging Face Blog | https://huggingface.co/blog | ✅ | 平台政策变动（免费层、推理供应商） | 010 | 34 |
| Hugging Face Spaces | https://huggingface.co/spaces | — | 免费在线 Demo，可直接试模型 | 010 | 34 |
| ModelScope 魔搭 | https://modelscope.cn/models | — | 国内权重镜像，下载快；**006 期 ZDTaichu5.0-9B、Atria Dawn Preview、书生-S2 的一手发布页** | 010 | 18 |
| GitHub Trending | https://github.com/trending | — | 开源工具热度，判断哪些值得进报告 | 010 | 26 |
| GitHub Releases (各项目 atom) | https://docs.github.com/en/rest/releases | ✅ | 版本号级更新，抓"免费额度调整" | 010 | 22 |
| OpenRouter Models | https://openrouter.ai/models | — | 一个 Key 试几百个模型，免费档清单。**⚠️ 006 期起升级为 T0 级发布地**：匿名/隐身模型（Ox Alpha、Union Alpha）**只在这里有规格、条款与实时性能数据**，模型厂商官网查不到。查条款认 `Stealth Model Terms` | 010 | 69 |
| Gitee AI / GitCode | https://ai.gitee.com | — | 国内开源托管 | — | 0 |
| 始智AI wisemodel | https://wisemodel.cn | — | 国内模型社区 | — | 0 |
| 硅基流动 SiliconFlow 模型广场 | https://siliconflow.cn/models | — | 免费/低价推理，常驻免费额度来源。**010 期旁证**：硅基流动完成 B+ 轮二期及 C 轮融资，2026 年内累计近 29 亿元（中国互联网投资基金 / 国新基金 / 中国移动链长基金） | 005 | 2 |
| 🆕 ComfyUI Blog（blog.comfy.org） | https://blog.comfy.org/ | ✅ | **权重「落地可用」的第一现场**：新模型进 ComfyUI 的那一天会写清**权重路径、显存门槛、量化版本与工作流文件**，这些是厂商发布稿与媒体稿都不写的。**010 期首次命中**——Qwen-Image-2.1 的 7B / 原生 RGBA / 2K / 10 图参考与 Comfy Cloud 试用路径全部出自这里 | 010 | 19 |

### 官方一手 · 国外（24）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| OpenAI News | https://openai.com/news | ✅ | 定价与免费档变动 | 010 | 65 |
| OpenAI Research | https://openai.com/research | — | 能力边界 | 010 | 65 |
| Anthropic News | https://www.anthropic.com/news | ✅ | Claude 免费档、速率 | 010 | 33 |
| Anthropic Engineering | https://www.anthropic.com/engineering | — | Agent 工程实践 | 010 | 33 |
| Google DeepMind Blog | https://deepmind.google/discover/blog | ✅ | Gemini 系列 | 006 | 2 |
| Google AI Blog | https://blog.google/technology/ai/ | ✅ | 产品侧免费入口（AI Studio、NotebookLM） | 010 | 52 |
| Google Research Blog | https://research.google/blog/ | ✅ | 论文一手 | 010 | 9 |
| Meta AI Blog | https://ai.meta.com/blog/ | ✅ | Llama 系列权重 | — | 0 |
| Microsoft AI Blog | https://blogs.microsoft.com/ai/ | ✅ | Copilot / GitHub Models 免费档 | — | 0 |
| Microsoft Research | https://www.microsoft.com/en-us/research/blog/ | — | 研究向 | — | 0 |
| NVIDIA Blog | https://blogs.nvidia.com/ | ✅ | **NIM 免费模型池**（本期：78+ 免费模型） | 004 | 1 |
| Mistral AI News | https://mistral.ai/news | — | Le Chat 免费层 | 010 | 10 |
| xAI News | https://x.ai/news | — | Grok 定价 | — | 0 |
| Cohere Blog | https://cohere.com/blog | — | 免费 1,000 次/月 | 010 | 5 |
| Midjourney | https://www.midjourney.com/showcase | — | 图像，免费档稀缺 | 008 | 1 |
| Runway | https://runwayml.com/news | — | 视频，一次性积分陷阱源 | 008 | 13 |
| Perplexity Blog | https://www.perplexity.ai/hub/blog | — | 免费搜索额度 | 005 | 6 |
| Cursor Changelog | https://cursor.com/changelog | — | 编辑器免费档 | 009 | 2 |
| Cognition (Devin) | https://cognition.ai/blog | — | Agent 产品 | — | 0 |
| Apple Machine Learning Research | https://machinelearning.apple.com/research | — | 端侧模型，本地免费路线 | — | 0 |
| AWS Machine Learning Blog | https://aws.amazon.com/blogs/machine-learning/ | — | 云侧免费层 | — | 0 |
| IBM Research | https://research.ibm.com/blog | — | 企业级 | 010 | 9 |
| Stability AI | https://stability.ai/news | — | 开源图像权重 | — | 0 |
| 🆕 TypeSafe AI（typesafe.ai / console.typesafe.ai） | https://typesafe.ai/ | — | **「决策模型」这一新形态的第一发布地**：Jev 的开放状态、免费额度、定价与适用边界只在自家页与帮助文档里。**010 期首次命中**——「全面开放、无需候补、注册送 $5、输出免费、端到端 70–500ms」全部出自这里（第三方媒体只转述了「送 1.2 亿 token」这一层） | 010 | 29 |

> 本期命中：NVIDIA Blog（9/3 宣布收购 Hugging Face，$129.3 亿）。

### 官方一手 · 国内（20）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| DeepSeek 研究与动态 | https://www.deepseek.com/zh/news | — | **全免费路线**，V4.1 Flash（9/10 多模态 + MIT） | 010 | 129 |
| 阿里云百炼·新模型发布 | https://help.aliyun.com/zh/model-studio/models | — | 免费额度规则（**只认 help 页，不认活动页**） | 007 | 3 |
| 阿里 Qwen 官方博客 | https://qwen.ai/blog | — | Qwen 开源权重 | 010 | 234 |
| 月之暗面 Kimi | https://platform.moonshot.cn/docs | — | 免费额度、上下文 | 010 | 3 |
| 智谱 GLM | https://docs.bigmodel.cn/cn/guide/start/model-overview | — | **GLM-4.7-Flash 永久免费**、夜间限免 | 008 | 22 |
| MiniMax | https://www.minimaxi.com/news | — | 海螺视频免费次数 | 010 | 26 |
| 火山引擎 / 豆包 | https://www.volcengine.com/docs | — | 日均 200 万 Token、高校 1 亿 | 005 | 4 |
| 字节 Seed 团队 | https://seed.bytedance.com/ | — | Seedance / Seedream，即梦免费额度来源 | 010 | 40 |
| 百度文心 | https://cloud.baidu.com/doc/index.html | — | 文心 4.0 全月免费、Comate 限免 | 010 | 57 |
| 腾讯混元 | https://hunyuan.tencent.com/ | — | Hy3 / Hy4 限免窗口 | 010 | 36 |
| 腾讯研究院 | https://www.tisi.org/ | — | 行业判断 | — | 0 |
| 讯飞星火 | https://xfyun.cn/doc/ | — | Spark Lite 永久免费、X2.5 开源 | 008 | 15 |
| 小米 MiMo | https://www.xiaomiev.com/ | — | MiMo Code 免注册 | 005 | 4 |
| 华为云 / 盘古 | https://www.huaweicloud.com/product/pangu.html | — | 盘古免费试用 | — | 0 |
| 面壁智能 MiniCPM | https://www.minicpm.cn/ | — | 端侧开源 | 008 | 4 |
| 阶跃星辰 | https://www.stepfun.com/ | — | Step 系列 | 010 | 28 |
| 快手可灵 (Kling) | https://klingai.com/ | — | **66 积分/天**免费视频主力 | — | 0 |
| 智源研究院 BAAI | https://www.baai.ac.cn/ | — | FlagEval 榜单、开源 | 008 | 2 |
| 昆仑万维 / 零一万物 | https://www.singularis.ltd/ | — | 开源权重 | — | 0 |
| 蚂蚁 / 美团 / 京东 AI | https://www.antgroup.com/news/media | — | CatPaw 等新产品免费额度 | — | 0 |

> 本期命中：讯飞（X2.5-1.7B/4B，9/1 开源 Apache-2.0）、DeepSeek（V4.1 Flash 9/10 发布）。

### 政策与监管（17）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| 国家网信办 | https://www.cac.gov.cn | — | 生成式 AI 备案、合规红线 | — | 0 |
| 工业和信息化部 | https://www.miit.gov.cn | — | 产业政策 | — | 0 |
| 国家数据局 | https://www.nda.gov.cn | — | 数据要素 | — | 0 |
| 中国信通院 CAICT | https://www.caict.ac.cn | — | 白皮书、标准 | — | 0 |
| 巨潮资讯网 cninfo | https://www.cninfo.com.cn | — | 上市公司 AI 相关公告 | — | 0 |
| IT 桔子 | https://www.itjuzi.com | — | 融资与新产品 | — | 0 |
| 国家企业信用信息公示系统 | https://www.gsxt.gov.cn | — | 主体核验（防骗） | — | 0 |
| SEC EDGAR 全文检索 | https://www.sec.gov/cgi-bin/srqsb?text=artificial+intelligence | — | 海外厂商披露 | — | 0 |
| EU AI Act 官方 | https://artificialintelligenceact.eu/ | — | 生效时间表 | — | 0 |
| EUR-Lex | https://eur-lex.europa.eu/ | — | 法规原文 | — | 0 |
| UK AI Safety Institute | https://www.aisi.gov.uk/ | — | 安全评估 | — | 0 |
| NIST AI | https://www.nist.gov/topics/artificial-intelligence | — | 标准与框架 | — | 0 |
| US Federal Register | https://www.federalregister.gov | — | 美国行政规则 | — | 0 |
| The White House OSTP | https://www.whitehouse.gov/ostp/ | — | 政策取向 | — | 0 |
| OECD.AI / UNESCO | https://oecd.ai/ | — | 国际比较 | — | 0 |
| 🆕 加州州长办公室（governor.ca.gov） | https://www.gov.ca.gov/ | — | **州级前沿 AI 监管行政令的第一发布地**（2026-09-18 签署：两个月内给出紧急关断机制、实验室驻场第三方审计、更新"关键事件"定义的建议）。**009 期首次命中**，也是本清单里第一个"**州级**"政策源——此前只有联邦（白宫 / NIST / Federal Register） | 010 | 1 |
| 🆕 北京市经济和信息化局 + 北京市发展和改革委员会（ncsti.gov.cn） | https://www.ncsti.gov.cn/ | — | **「词元经济」作为独立政策对象的第一个省级发布地**——《北京市加快词元经济发展的行动方案（2026—2028 年）》（9/15 印发、9/18 发布），**六大维度十条举措**，含**词元工厂分级评价标准**（模型适配数量 / 词元吞吐速度 / 首字延迟 / 缓存命中率 / PUE）、**词元质量评测体系**、**算力与词元金融工具**。**010 期首次命中**；与 005 期的「地方政府词元券」相比是**层级跃升（区级 → 市级）**，且首次给出**行业基线数据**（国内日均词元调用量两年增长超千倍、国内超半数词元生产集中在北京、豆包单家年调用量突破 180 万亿） | 010 | 3 |

> 本期命中：成都市政府门户（词元券征求意见稿）——**注意：地方词元券类信源未列入本清单，建议补 T0 政策节的"地方政府门户"聚合项**。**009 期新增：加州州长办公室（前沿 AI 监管行政令）。**

### 评测与榜单（17）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| LMArena Leaderboard | https://lmarena.ai/leaderboard | — | 文本综合排名 | — | 0 |
| LMArena Image Arena | https://lmarena.ai/leaderboard/image | — | 图像排名 | — | 0 |
| LMArena Video Arena | https://lmarena.ai/leaderboard/video | — | 视频排名 | — | 0 |
| LMArena WebDev Arena | https://lmarena.ai/leaderboard/webdev | — | 前端/网页生成 | — | 0 |
| Artificial Analysis | https://artificialanalysis.ai/ | — | 性价比、吞吐、延迟 | 010 | 11 |
| llm-stats.com | https://llm-stats.com/ | — | 多榜聚合 | — | 0 |
| LiveBench | https://livebench.ai/ | — | 防污染评测 | — | 0 |
| SWE-bench Verified | https://www.swebench.com/ | — | 代码 Agent | 006 | 1 |
| Terminal-bench | https://www.tbench.ai/leaderboards/terminal-bench | — | 终端 Agent | 006 | 6 |
| OSWorld | https://os-world.github.io/ | — | 计算机使用 | — | 0 |
| Epoch AI | https://epoch.ai/ | — | 算力与趋势 | 008 | 6 |
| Vals AI | https://www.vals.ai/ | — | Agent 评测 | — | 0 |
| Scale SEAL Leaderboard | https://scale.com/leaderboard | — | 企业级评测 | 010 | 2 |
| OpenCompass 司南 | https://opencompass.org.cn/ | — | 中文开源评测 | — | 0 |
| SuperCLUE | https://www.superclue.ai/ | — | 中文综合 | — | 0 |
| 智源 FlagEval | https://flageval.baai.ac.cn/ | — | 多模态评测 | — | 0 |
| C-Eval / CMMLU | https://cevalbenchmark.com/ | — | 中文知识 | — | 0 |

---

## T1 · 社区与社交（19）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| X / Twitter | https://x.com | — | 最快信号，需交叉验证 | 004 | 1 |
| Reddit r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA/ | ✅ | 本地/免费模型实测，**翻车预警第一现场** | 010 | 3 |
| Reddit r/MachineLearning | https://www.reddit.com/r/MachineLearning/ | ✅ | 论文讨论 | 010 | 2 |
| Reddit r/artificial | https://www.reddit.com/r/artificial/ | ✅ | 泛 AI 新闻 | 010 | 2 |
| Reddit r/OpenAI / r/ClaudeAI / r/singularity | https://www.reddit.com/r/singularity/ | ✅ | 产品体验 | 010 | 2 |
| Reddit r/StableDiffusion | https://www.reddit.com/r/StableDiffusion/ | ✅ | 出图工具实测 | 010 | 2 |
| Hacker News | https://news.ycombinator.com/ | — | 技术圈热点 | 010 | 51 |
| HN 关键词 RSS (hnrss.org) | https://hnrss.org/newest?q=AI | ✅ | **可程序化订阅的 AI 关键词流** | — | 0 |
| 知乎 · AI 话题 | https://www.zhihu.com/topic/19556664/hot | — | 中文深度讨论 | — | 0 |
| 掘金 · 人工智能 | https://juejin.cn/ai | — | 开发者实践 | — | 0 |
| 微信公众号（AI 类） | https://mp.weixin.qq.com/ | — | 厂商首发渠道之一 | 003 | 1 |
| 微博（AI 官方账号+话题） | https://s.weibo.com/ | — | 国内厂商公告 | 010 | 2 |
| B 站（发布会+测评） | https://www.bilibili.com/ | — | 发布会回放、实测 | — | 0 |
| 小红书（AI 工具玩法） | https://www.xiaohongshu.com/ | — | **发布玩法 + 平台原生 AI 生态（RED Skill / Builder Hub）** | 010 | 79 |
| Bluesky | https://bsky.app/ | — | 研究者聚集地 | — | 0 |
| LinkedIn | https://www.linkedin.com/ | — | 企业级动态 | 004 | 3 |
| LessWrong | https://www.lesswrong.com/ | ✅ | 理性主义视角长文 | — | 0 |
| AI Alignment Forum | https://www.alignmentforum.org/ | ✅ | 对齐研究 | — | 0 |
| V2EX / 少数派 | https://sspai.com/ | — | 工具玩家实测 | — | 0 |

---

## T2 · Newsletter（18）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| Import AI (Jack Clark) | https://importai.substack.com/ | ✅ | 政策 + 技术双视角 | — | 0 |
| The Batch (DeepLearning.AI) | https://www.deeplearning.ai/the-batch/ | — | 周更综述 | — | 0 |
| The Rundown AI | https://www.therundown.ai/ | ✅ | 日更，产品向 | — | 0 |
| TLDR AI | https://tldr.tech/ai | — | 极简日更 | — | 0 |
| Ben's Bites | https://www.bensbites.co/ | — | 日更 | — | 0 |
| Latent Space | https://www.latent.space/ | — | 深度访谈 | 010 | 2 |
| Ahead of AI (Raschka) | https://magazine.sebastianraschka.com/ | ✅ | 技术细节讲得最清楚 | 007 | 3 |
| AI Snake Oil | https://www.aisnakeoil.com/ | ✅ | **祛魅视角**，避坑素材来源 | — | 0 |
| Simon Willison's Blog | https://simonwillison.net/ | ✅ | 实操、本地模型 | 010 | 3 |
| The Sequence | https://thesequence.substack.com/ | ✅ | 企业级 | — | 0 |
| Interconnects | https://www.interconnects.ai/ | — | 训练与推理经济学 | — | 0 |
| Stratechery | https://stratechery.com/ | ✅ | 商业战略 | — | 0 |
| Last Week in AI | https://lastweekin.ai/ | — | 周更汇总 | — | 0 |
| The Neuron | https://www.theneurondaily.com/ | — | 日更 | — | 0 |
| 宝玉的博客 | https://baoyu.io/blog | ✅ | **中文翻译一手料**，海外信息落地最快 | — | 0 |
| Founder Park AI 速递 | https://www.founderparks.com/ | — | 中文日更 | — | 0 |
| 机器之心 SOTA! | https://sota.jiqizhixin.com/ | — | 模型/SOTA 追踪 | — | 0 |
| 硅星人 | https://www.guixingren.com/ | — | 出海与商业视角 | — | 0 |

---

## T3 · 媒体（36）

### 国外（20）

| 信源 | 地址 | RSS | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- |
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/ | ✅ | — | 0 |
| The Verge AI | https://www.theverge.com/ai-artificial-intelligence | ✅ | — | 0 |
| VentureBeat AI | https://venturebeat.com/category/ai/ | ✅ | — | 0 |
| MIT Technology Review AI | https://www.technologyreview.com/topic/artificial-intelligence/ | ✅ | — | 0 |
| Ars Technica | https://arstechnica.com/ai/ | ✅ | — | 0 |
| Wired AI | https://www.wired.com/tag/ai/ | ✅ | — | 0 |
| The Information | https://www.theinformation.com/ | — | — | 0 |
| Reuters AI | https://www.reuters.com/technology/artificial-intelligence/ | — | — | 0 |
| Bloomberg / FT / WSJ AI | https://www.bloomberg.com/ai | — | — | 0 |
| The Decoder | https://the-decoder.com/ | ✅ | 009 | 3 |
| Artificial Intelligence News | https://www.artificialintelligence-news.com/ | ✅ | — | 0 |
| MarkTechPost | https://www.marktechpost.com/ | — | 010 | 5 |
| IEEE Spectrum | https://spectrum.ieee.org/artificial-intelligence | — | — | 0 |
| Quanta Magazine | https://www.quantamagazine.org/ | ✅ | — | 0 |
| ZDNet AI / SiliconANGLE | https://www.zdnet.com/topic/artificial-intelligence/ | — | — | 0 |
| The Register | https://www.theregister.com/ai/ | — | — | 0 |
| Business Insider / Axios / Semafor | https://www.axios.com/technology/ai | — | — | 0 |
| Nature / Science news | https://www.nature.com/subjects/machine-learning | — | — | 0 |
| Tom's Hardware / ServeTheHome | https://www.tomshardware.com/tech-industry/artificial-intelligence | — | — | 0 |
| The Economist / Rest of World | https://restofworld.org/series/ai/ | — | — | 0 |

### 国内（16）

| 信源 | 地址 | RSS | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- |
| 机器之心 | https://www.jiqizhixin.com/ | ✅ | — | 0 |
| 量子位 | https://www.qbitai.com/ | ✅ | — | 0 |
| 新智元 | https://www.7wake.com/ | — | — | 0 |
| AI 科技评论（雷峰网） | https://www.leiphone.com/category/aikeji | ✅ | — | 0 |
| InfoQ · AI 前线 | https://www.infoq.cn/topic/AI | ✅ | — | 0 |
| 36 氪 · AI 频道 | https://36kr.com/channel/ai | — | — | 0 |
| 晚点 LatePost | https://www.latepost.com/ | — | — | 0 |
| 极客公园 | https://www.geekpark.net/ | — | — | 0 |
| 钛媒体 / TMTPost | https://www.tmtpost.com/ | — | — | 0 |
| 爱范儿 | https://www.ifanr.com/ | — | 010 | 1 |
| 品玩 PingWest | https://www.pingwest.com/ | — | — | 0 |
| 虎嗅 | https://www.huxiu.com/ | — | 008 | 4 |
| CSDN / 开源中国 / 掘金 | https://juejin.cn/ | — | — | 0 |
| 阿里云 / 腾讯云开发者社区 | https://developer.aliyun.com/ | — | 003 | 1 |
| Datawhale / PaperWeekly / AI TIME | https://www.datawhale.cn/ | — | — | 0 |
| 智源社区 / 将门创投 | https://hub.baai.ac.cn/ | — | — | 0 |

---

## T4 · 聚合器与工具（15）

| 信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数 |
| --- | --- | --- | --- | --- | --- |
| RSSHub | https://docs.rsshub.app/ | — | **把无 RSS 的源变成 RSS**（微博/B站/小红书/知乎都靠它） | — | 0 |
| Inoreader / Feedly / FreshRSS | https://www.inoreader.com/ | — | 统一阅读与去重 | — | 0 |
| HN Algolia API | https://hn.algolia.com/api | — | 程序化检索 HN 历史 | — | 0 |
| Google Alerts | https://www.google.com/alerts | — | 关键词邮件推送 | 010 | 52 |
| GitHub Actions 定时抓取 | https://docs.github.com/en/actions | — | **自动化骨架** | 010 | 22 |
| daily.dev | https://daily.dev/ | — | 开发者信息流 | 008 | 8 |
| AI-HOT（168 信源分级）· 主理人「数字生命卡兹克」 | https://aihot.virxact.com/ · **新域名 https://aihot.news/** | — | **T4 里用途最高的一条**：按天归档 + 精确到分钟的时间戳、每条带 **AI 评分（0–100）+ 推荐理由**、标注**「另有 N 家信源报道」**（天然跨源交叉）、按主题频道追溯（`/topics/trends`）、条目永久链接 `aihot.news/items/<id>` 可跳原文。用法：**当每日扫描的入口层**，再由它跳去 T0 原文定事实。⚠️ 它的"AI 评分"是**模型打分，不是事实核查**，结论仍须回 T0。**⚠️ 能力边界（010 期第六次逐期计数确认，视为定论）：它不覆盖"限时免费额度/权益"类条目**——006 期 6 条里额度相关仅 1 条、007 期 14 条里同样仅 1 条（Codex 额度节省工作流）、**008 期 9/19 的 10 条里额度相关为 0 条**、**009 期（9/19 的 10 条 + 9/20 至 14:40 的 2 条）额度相关为 0 条**、**010 期（9/19 全天 10 条 + 9/20 全天 4 条 + 9/21 至 09:20 的 2 条）额度相关仍为 0 条**。**权益类信息必须走 T0 帮助中心 + 垂直免费额度站 + 平台方创作者招募稿，AIHOT 不能替代**。它的可用输出是"**免费内容生成工具**"与"**厂商发布事件**"这两类。**008 期补充一条正面证据**：ZCode 逆向贴（评分 86）与 OpenRouter 图像模型成本实测（评分 70）都是先在这一层被高分条目带出来的——**它的强项是"当日技术事件"，弱项是"当日商业权益"**。**009 期再补两条**：① **正面**——Step 5 Preview（挂 2 家）、Gemini 越界（**挂 8 家**，跨源数最高）都是先在这一层被带出来的；② **⚠️ 新增的结构性观察（重要）——它的当日条目是"滚动发布"的，且日间分布不均**：9/18 全天 7 条、9/19 全天 10 条、**9/20 至 14:40 只有 2 条**（本期头条 Step 5 出现在 9/20 10:20）。**这意味着"某天条目少"只等于"到那个时点还没出"，而"出刊时点"会直接决定内容完整性**——报告必须写明扫描截止时点，关键条目宁可等当天中午再定稿（见 009 期避坑 40）。**010 期新增第三条结论（重要）：「当日条数」这个指标本身不该被引用为「新闻密度」**——010 期扫描截止 09:20 时当日仅 2 条，**但这不代表 9/21 没有新闻，只代表「到 09:20 为止出了 2 条」**；反证是 009 期的头条 Step 5 Preview 出现在 10:20，**若 009 期也按 09:20 定稿就会整个漏掉**。**处置：刊头固定标注扫描截止时点；跨源计数时把「当日条数」排除在外。** 010 期正面证据：**Google 确认 Gemini 在 Irregular 测试中访问 3 家真实公司系统**（评分 78，**首次把四家实验室的同类事故并置**）与 **ChatGPT `__obi` 跨站 Cookie 独立流量取证**（评分 76）均出自这一层 | 010 | 56 |
| 🆕 OVHcloud AI Endpoints | https://endpoints.ai.cloud.ovh.net | — | **免注册匿名档免费 API**（OpenAI 兼容、9 个开源模型、匿名 2 RPM、欧盟托管 GDPR 合规、冷启动 5–10 秒）。**009 期首次命中**——「匿名档」这一类免费 API 形态的第一条硬样本 | 010 | 17 |
| 🆕 LLM7.io | https://llm7.io | — | **匿名档免费 API**：10 RPM / 60 req·hr，**注册后 120 RPM**；含 gemini-3.1-flash-lite、DeepSeek-V4-Flash-0731 等 6 个模型；小型独立供应商、无 SLA。**009 期首次命中** | 010 | 22 |
| RadarAI | https://radarai.top/ | — | 中文聚合 | — | 0 |
| AITOP100 | https://aitop100.cn/ | — | 中文榜单 | — | 0 |
| BestBlogs.dev | https://www.bestblogs.dev/ | — | 优质博客聚合 | — | 0 |
| Ground News / Particle | https://ground.news/ | — | 立场偏差对比 | 010 | 2 |
| Product Hunt AI | https://www.producthunt.com/topics/artificial-intelligence | ✅ | **新工具首发**，免费档信息最早出现地 | — | 0 |
| 🆕 Local Model Watch（localmodelwatch.tsuchitsuchi.com） | https://localmodelwatch.tsuchitsuchi.com/ | — | **开源模型与推理栈的逐周总账**：把同一周的新模型（含各家量化 / 衍生版）与推理层版本（ggml / llama.cpp / llamafile / SGLang / Unsloth / koboldcpp / ComfyUI / LocalAI）**合并成一张表、同事件去重**。**010 期首次命中**——本期「免费开源内容资产」一节的多数条目（Intern-S2-397B-GGUF、WeVisDoc、Realtime-Venus、Needle 3、Splash Engine、Ternary-Bonsai 三档分发）都出自它。**它补的是本清单的一个结构性缺口：没有人逐周统计「哪些权重真的能下载」** | 010 | 4 |

---

## 清单缺口（本期实际取料但清单里没有的源）

以下各类在 004–010 期实际贡献了硬信息，建议补进清单。
（**计数修正**：005 期此处写"这 4 类"，但表内实列 5 行；006 期修正为 6 类；007 期新增第 7 类；**008 期新增第 8 类**；**009 期维持 8 类，第 8 类被显著扩容**；**010 期维持 8 类，第 5、6 类各补一条本期的量化代价**。）

| 缺口 | 建议补入层级 | 说明 |
| --- | --- | --- |
| **上海人工智能实验室（书生 / InternLM）** | T0 官方一手·国内 | 004 期即提出、006 期仍未进清单（已建议三期）。Atria Dawn Preview 744B MIT、书生-S2 均出自这里，并在魔搭同步放出 |
| **免费额度垂直追踪站**：freellm.net（484+ 免费模型、228 条实时验证）、aifree.dev、tokennav.cc/free、**FreeLLMAPI（freellmapi.co）** | T4 聚合器 | 权益类日报的核心弹药库，目前只能靠 T3 媒体转述。**注意其时效性同样以天计**（006 期发现多篇 9 月"免费 API 汇总"仍写 GLM-4-Flash、5000 万 DeepSeek 额度）。**009 期价值最高的一期**：**两家新免费 API 供应商（OVHcloud AI Endpoints、LLM7.io）的全部规格、限速与「Last Updated 2026-09-19」日期，只有这一类源在逐日核对**；**OpenRouter 免费模型数量出现 23 / 35+ / 511+ 三个口径**也说明只有这一层在做实时清点；Adobe Firefly 免费额度取消（2026 Q1）同样只有这一层在记。**010 期第三次贡献「官方不会写、媒体不会报」的结构性事实**：FreeLLMAPI 的《The State of Free LLM APIs (2026)》给出 **22+ 供应商 / 316+ 免费模型端点**、**SambaNova 已整体下线免费档**、**Vercel AI Gateway 现需绑卡**，以及**本报告本期最有用的一条判别框架——「一次性注册礼」vs「月度循环额度」**（后者才可能进长期方案，前者只能当一次性评测券）；同层还贡献了多模型家族的**多供应商供给度**（Llama 9 / Gemma 9 / Qwen 7 / Nemotron 7 / GPT-OSS 6 / Mistral 5 / DeepSeek 4 / GLM 4），这是「做可替换设计」的量化依据 |
| **什么值得买 / All Agent 百科** 等中文权益清单 | T4 聚合器 | 国内限时福利的**唯一系统整理方**，虽然要降级标注口径 |
| **地方政府门户 / 经信部门**（成都、杭州、深圳龙岗、武汉江夏等） | T0 政策与监管 | 词元券是 004 期最大额度来源（单主体年最高 200 万），006 期杭州 Token 卡亦出自市级口径；清单目前只有中央级部委 |
| **内容平台官方创作者中心 / 开发者文档**（抖音 AI 工坊、小红书开发者文档、B站 Toy、腾讯吐司、微信公众号后台、**快手 AI 互动内容招募**、**小红书 Cura**） | T0 官方一手·国内 | 005 期"AI 免费内容发布"线的全部关键事实出自这里；006 期再增硬证据——**快手的首批创作者招募、B站 Toy 的 2956 万体验量口径，全部出自平台方**；**007 期第三次验证：抖音"AI 工坊"三区结构与"小红书 Cura"同样出自平台方/平台活动现场**；**008 期第四次验证（也是强度最高的一次）：抖音「新赛道计划」与「星图商单三分法」全部出自 2026 抖音创作者大会现场，巨量 AI 工作台 / 即创 2.0 出自巨量引擎 CAEG 大会，讯飞 AStudio 与 Qoder 两项福利全部出自各自官方页**；**009 期第五次验证：抖音创作者大会收官口径的三条计划（新面孔 / 新标杆 / 新赛道）与全部生态数据、快手公益 × 可灵「看见微光」大赛的奖金与评审权重、DeepSeek API 的峰谷时段定义，全部出自平台/厂商自己的页面或现场**——而**同一件事在第三方整理稿里出现了三组互不相同的数字**（见 009 期避坑 36）。**"发布线"与"额度线"的事实源已经稳定落在这一层，T3 媒体只提供转述与解读**。免费分发政策（沙箱权限、审核规则、激励）必须以官方文档为准。**⚠️ 010 期缺口未被正面回应，而代价第一次被量化地看到了**：**抖音「新赛道计划」连续第三期没有报名入口与细则**、**快手「AI 互动内容」连续第二期未公布激励**；**缺口不被填上的结果是它被第三方整理稿填充，而这批稿子本期自证不可靠**（AI 短剧扶持出现第四版数字，且同一篇稿子内部就有「15 亿保底」与「300 万+ 精品剧」两个不同量纲的基金口径）。**结论：这一层不是「锦上添花的补充源」，是「防止用错数字的必需源」** |
| 🆕 **AI 短剧 / 漫剧扶持政策与地方产业政策聚合源** | T4 聚合器 + T0 政策与监管（**双挂**） | **007 期新识别**。这类内容**总量大、更新快、主要形态是自媒体整理稿**——007 期引用的单篇稿一次性摊开八大平台 + 十余省市数字（抖音 500 万、腾讯火龙 200% 分账、芒果 300 万阶梯奖…），但**既无核验日期，也不区分投资/保底/分账/奖金/基金的性质**（这五者性质完全不同）。**需要一个只做"政策事实"的源，与媒体解读分层**；在补入之前，所有此类数字一律标「媒体整理」。**008 期再增一条判断依据**：本期同一篇自媒体整理稿里**同时给出"平台加码"与"行业回调"两组相反数字**（快手 200 万奖金池 / 视频号 40% 分成 vs 一分钟 5,000→几百元、90% 公司倒闭）——**说明这类稿本身在做"两边一起报"的综述，阅读时不能只摘一半**（见 008 期避坑 34）。**⚠️ 009 期从"刚需"升级为"高频出错源"**：同一件事出现了**第二篇独立整理稿（第三个版本）**，且与第一篇**没有一个数字相同**——抖音扶持被写成"2 亿专项基金 / S+ 单部 360 万保底 / 漫剧 6,000 元每分钟"，快手被写成"**磁力新剧计划** S 级全资 200 万/部 / 个人最高 1 万元启动激励 / **合作方 99% 分成**"，而第一篇写的是"分成 90% 归创作者"。**关键教训（已升格为 009 期避坑 36）：这类稿会把"基金规模 / 单部保底 / 单部上限 / 奖金池 / 分成比例"五种性质不同的东西混在同一段里，任何把两种相加的说法都是错的**——008 期的"快手 200 万奖金池"与 009 期的"快手 200 万/部全资"就是典型的两口不同的锅 |
| 🆕 **Agent Harness / 模型托管平台官方页**（**OpenCode**、**Cline**、**Cloudflare Workers AI**、**OpenRouter 模型页与 Stealth Model Terms**） | T0 官方一手 + T1 社区 | 006 期头条 **Union Alpha 的全部一手事实出自这里**——它不在任何模型厂商官网上，只在**托管方**的模型页与条款里（且同一模型在 OpenCode 与 OpenRouter 的条款不同）。清单"模型与开源"目前只覆盖 HF / ModelScope / GitHub，**缺托管与 Harness 这一层**，而这层正是当下免费 API 的第一发布地。**008 期结论加强**：Union Alpha 的**认领声明只存在于厂商 X 账号**（@unionalphaai），**不在任何模型厂商官网、不在任何新闻稿**；同理 **ZCode 的官方说明只存在于智谱开发者社群（BigModel 社群）**——**"厂商的一手声明正在从官网迁到社群与 X"**，这一类源的价值本期达到最高。**010 期新增一条硬证据**：**Step 5 Preview 的免费权益是「分段触发」的**（注册赠 99 元套餐 + **首次登录** 15 天 + **完成首次 API 调用**再 15 天 + 每邀请 1 人再 15 天、邀请部分最多 45 天），**这些规则只写在厂商自己的活动页里**——第三方教程只转述了「免费一个月」，**漏掉了「首调才能激活第二个 15 天」和「邀请最高 45 天」**。**这类「分段触发 + 阶梯邀请」的权益规则，是媒体转述丢失最严重的一类信息**，也是 010 期避坑 44 的来源 |
| 🆕 **安全厂商与逆向 / 取证社区**（火绒、FreeBuf、**Linux.do / V2EX 技术版**、以及独立逆向长文博主） | T1 社区与社交（主）+ T3 媒体（辅） | **008 期新识别**。本期最重的一条风险事件（**ZCode 静默上传完整 Git 历史**）的**全部一手取证出自这一层**：`~/.zcode` 目录体积异常 → 拆 `app.asar` → 还原「取凭证 → tar.gz 打包 → AES-256-CTR 加密 → RSA-OAEP 包裹密钥 → HTTP 表单直传阿里云 OSS」的完整链路 → 给出可复现的取证数字（42,411 文件 / 313MB / `.git` 占 86.6% / 失败重试 564 次）。**这一层的特点是"可复现、带命令、带数字"，与媒体转述有明确分层**——厂商无从否认，只回应答与否。清单 T1 目前只有 X / Reddit / HN / 知乎 / 掘金等通用社区，**缺"终端安全与逆向取证"这个专业社区**，而 AI 桌面客户端的风险事件未来只会更多。**⚠️ 009 期显著扩容（建议改名为「AI 工具的数据越界与安全事件取证源」）**：本期三条同周事件分别来自**三个不同的地方**——① **逆向社区**（ZCode，`app.asar` 拆包 + 流量取证）；② **WSJ 独家调查**（**Gemini 越出测试环境入侵三家公司**，且 **Google 的披露是被媒体问出来的**，非主动）；③ **攻击者自己的公开复盘**（3 人团队接管 OpenAI 员工账户：含模型分工、**token 成本不到 $3,000**、**通过提交 PR 证明漏洞**）。**这三种来源都不在科技媒体的日常覆盖范围内**——这一类源从 008 期的"需要"升级为本期的"每期必查"。**⚠️ 010 期出现该缺口的「反向价值」（建议正式改名为「AI 工具的数据越界与安全事件取证源」）**：**同一个事件的「指控报道」与「回撤报道」来自不同层级**——**WSJ 独家（T3 媒体）**给出「Gemini 自主越出测试环境入侵三家公司」的叙事，而**修正来自 T1/T2 的技术复盘与 MarkTechPost 的四家并置**（指出研究者引导了漏洞复现、标题夸大，且 Anthropic / OpenAI / Meta / Google 四家的同类披露**出自同一家第三方评估方 Irregular**）。**结论：这一类缺口的价值不在于「更快拿到指控」，而在于「能不能在 48 小时内拿到技术侧的复核」——只订阅 T3 的人会停在错误版本上**（010 期避坑 43） |

---

> **维护规则**：本清单只增不减。信源失效时改标注为「⚠️ 失效（YYYY-MM-DD）」并保留条目，不做删除——保持可追溯。
