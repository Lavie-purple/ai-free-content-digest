# -*- coding: utf-8 -*-
"""059 期记忆落盘：对 `.workbuddy/memory/automations/<id>/memory.md` **追加**。

⚠️ 054 期纪律⑥：这个文件只能追加，不能覆盖写。本脚本先查重、已写过就退出。
⚠️ 059 期纪律：写完必须重新读回落盘文件再断言（不校验内存结果）。
"""
import io, os, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(WS, ".workbuddy", "memory", "automations",
                   "256c1349-ea4a-4721-9c5d-14067699f1f1", "memory.md")

HEAD = "## 2026-11-05 第 059 期"

SEC = HEAD + """（`Kimi K3.1 Pro` 权重公开 ＋ `OpenRouter` 两个 `:free` 整批摘下 ＋ 第一次「`4.2` 行数不变、成员换一个」）

- **状态**：成功。**窗口 = 058 期截止 11/4 16:48 → 本期截止 11/5 12:35（北京），`19.8` 小时**；美西换算：起 美西 `11/4 00:48 PT`、止 美西 `11/4 20:35 PT` —— **完全落在美西 `11/4` 一个日历日内**（057 期单日 `17.1h`、058 期跨两日历日 `31.7h`，本期是「单日 + 长窗口」）。
- **规模**：目标 `284` / 落盘 `223` / `200` 共 `190` / `000` 共 `57`（`20.1%`）；解析 `3,121` 条、窗口内 `118` 条。

### 头条
- **⚠️ `Kimi K3.1 Pro` 权重已公开（058 期那句「完整模型权重将于 11 月 4 日前发布」已兑现）** —— `hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro` `200` / `7,428` 字节；`createdAt` = `lastModified` = `2026-11-02T04:13:51Z`、`gated:false`、`private:false`、`license:other`（`kimi-k3.1-pro`）、`112` 个文件 / `96` 个 `safetensors` 分片；官方组织清单 `19 → 20` 个模型；仓库卡 `2.8T` 总参 / `104B` 激活 / `93` 层。**但官方文档页那句承诺逐字未改**（`740,462` 字节、命中 `3` 次）。**判定：只写事实、不写「是否按期」** —— 兑现时刻落在观测盲区（`11/4 16:49` 不可见 → `11/5 12:36` 可见），精度 `19.8h` 比承诺窗更粗。
- **⚠️ `OpenRouter` 两个 `:free` 整批摘下** —— 全量 `455 → 454`、零价 `18 → 16`、`:free` `14 → 12`；消失 `thinkingmachines/inkling:free` 与 `inkling-small:free`；**付费版 `inkling`（`$1`/`$4.05`）与 `inkling-small`（`$0.45`/`$1.2`）原价原上下文一字未动**；新增 `ricursiveai/ripple-65b-preview`（北京 `11/5 03:03`、付费）。**三条证据闭合**：`/llms.txt` `404`（10 字节 `Not Found`）、`/endpoints` `200` 但 `endpoints: []`、`announcements` 全文 `inkling` 命中 `0`。**免费变体上下文 `1,048,576` > 付费版 `524,288`** —— 摘掉免费档让读者同时失去「价格」与「上下文」两样。
- **`stealth/crouton-alpha` 第 `3` 天仍在**（`created 1793669930`、`pricing` `0/0`、`1,048,576` 上下文、`llms.txt` `4,021` 字节逐字节相同），**并且 `opencode.ai/docs/zen` 新增 `Crouton Alpha Free`（`crouton-alpha-free`），免费清单 `10 → 11`** —— 同一个隐身模型扩散到第二个站。
- **`Runware` 促销数组 `14 → 18`** —— 新增 `klingai-video-4-0-flash-launch-promo`（`11/10`）、`krea-3-launch-promo`（`11/10`）、`minimax-h3-max-november-promo`（`11/15`）、`pruna-p-video-2-pro-replace-launch-promo`（`11/19`）；`pruna-p-video-2-pro-avatar` 的 `endsAt` 恰为基准日当天（`11/5`）。

### 目录与同值记账
- **`freellm.net` 四计数器 `535/296/31/454` 与字节数 `171,340` 三期同值**，`Latest free LLM API model update` 仍 `2026-10-27`（连续第 `8` 期）。**本期起改口径：不再用它交叉验证 `OpenRouter`** —— 它已经比真值慢至少一期，拿它校验会让「本期目录没变」变成假结论。
- **`Antigravity` 定价页 `137,595` 逐字节相同** —— ⚠️ 但第一次落盘只有 `12,408` 字节（见工程坑①）。
- **`Ollie` 告别信 `39,747 → 35,662`**（少掉的是 `Next.js` 构建块，三处关键逐字未变）＋ 定价页 `41,791` 逐字节相同；**距今 `1` 天**。
- **商汤 `sensetime.com/cn/news` 现在读到 `2026/11/03` 的 `SenseNova 6.8 Flash` 正式版发布条目**（`6.8 Flash` 命中 `8` 次），**但该页 `限时` / `免费` 各 `0` 命中**；`token-plan` `20,820` 与 `xiaohuanxiong` `158,318` 逐字节相同。
- **`AXON` `20,111` 逐字节相同**，仍无许可证与版本号（连续第 `2` 期）。

### 本期纠错 1 条（对 058 期）
1. **058 期「`sensetime.com/cn/news` 无 `6.8 Flash` 发布条目」这个结论无法回溯** —— 058 期没把那一页存进 `tmp_058/`；本期同页读到 `11/03` 的条目，**却判不出是「页面后来上架」还是「上期漏读」**。**处置：本期起把「零命中」结论涉及的页面全部入档**（新立避坑 260）。

### 本期新增避坑 260–263
260 **「零命中」的结论必须连同归档件一起留下** —— 没有留档的零命中，下一期无法区分「页面变了」与「上次读错了」；
261 **`HF` 的 `createdAt` 是「建仓时间」，不是「公开时间」** —— 匿名列表接口不返回私有仓库，所以「建仓」与「公开」可以隔两天；**「这个模型什么时候放出来的」只有「两次观测的差集」能答，精度等于观测间隔**；
262 **同一个 API 家族的不同端点，计数可能不一致** —— `?author=moonshotai` 给 `likes 277`、`/api/models/moonshotai/Kimi-K3.1-Pro` 给 `579`、`downloads` 两边都是 `797`。**引用计数必须写明端点，同段落不许混用**；
263 **传输被截断会伪造出「页面变小」，而且伪造得非常像** —— `antigravity.google/pricing` 首抓 `12,408` 字节、三处关键逐字全 `0`、剥标签只剩 `1,028` 字符，**看起来就是「页面改成 JS 外壳」**；但文件断在 `.button-primary:disabled{…on-disable` 中间、**没有收尾标记**，重抓即回到 `137,595`。

### 规模与对账
- 表体 **218** 行 ＝ 058 期 `217` ＋ 补入 `1`（`Vercel Labs` `fx`）− 移出 `0`；`4.1` = `55` / `4.2` = `42`（**出 `1` 进 `1`**：`AXON` 毕业进总账、`fx` 进入）；常驻未变 `121`；**总账 `163`**；极速视图 `76` 条（`75 → 76`）。
- 色标 ⚪2/🔴5/🟢149/🟡22/🟠7/⚠14/空19 = 218；`classify()` crit5/live166/over2/pending23/unclear16/switch6 = 218。
- `check_deadlines` **A21+B15+C0+D175+E7=218** —— **`A +2`（`Figma`、`Kimi` 两条 `T+0` 跨日）与 `B −2` 是同一件事的两面；`D +1` 正是补入的那一行**。
- **⚠️ 本报告第一次出现「`4.2` 行数完全不变（`42 → 42`）、但成员换了一个」** —— **只看 `42 = 42` 会得出「本期没有常驻变化」，而事实是一条毕业、一条进来**（与 058 期「`B` 桶 `17 → 17` 但成员换了 `1` 个」同一条纪律，只是这次落在 `4.2` 上）。

### 本期实测的工程坑（详见 ENGINEERING.md §十·35）
- **① ⚠️ `slim_table.py` 只保留状态列「第一句边界」→ 追加在尾部的当期事实会被裁掉** —— 本期第一次跑完整条流水线后，`Kimi K3.1 Pro` 行的 `112` 个文件 / `license: other` / 两个 `:free` 的 ID **全部消失**（`set_status` 之前的写法是 `append_note`）。**修法：改成 `set_status()` 整体改写状态列，让当期事实成为「第一句边界」**；`gen_table059.py` 里显式注明原因。**这与 054 期「流通量被裁」是同一条纪律的第三次变形 —— 不是数字写错、是数字被裁。**
- **② `set_status` 的字段数计算踩了一次 `Counter({3: 206, 2: 12})`** —— `row.strip().rstrip("|").split("|")` 得到 `4` 段（首段为空串），索引应为 `cells[1] / cells[2]`；修正后 `Counter({3: 218})`。
- **③ `patch059_status.py` 的匹配键要用「块内短键」** —— 商汤 `6.8` 那条一开始用带「正式版发布：办…」的长串，实际块内文本是「现在读得到」，断言当场失败。
- **④ `check_frozen` 的 🔴 高危第六次由「说明性措辞」触发** —— 脚注写「不是本期**新增**的错」，`新增` 落进 `NEW_PAT` → `3` 条高危。**改成「不是本期才出现的偏差」→ 🔴 `0`**（处置照旧：改措辞、不放宽守卫）。
- **⑤ `prune_table.py` 的相对路径坑第二次发作** —— 这次移出 `0` 条，所以只留下一个**只有表头**的根目录 `data/deadline_archive.md`；**已删除该幽灵目录**（真档在 `.workbuddy/data/`，未被触碰）。**下次必须在仓库根调用或显式 `--archive`。**
- **⑥ 附录 `原文` 里的指针标签停在上期** —— `第四章表体明细附录.md` 的 059 段里 `[附录 058](details.html)` 出现 `55` 处（`058` 段里同位置是 `[附录 057]`，属历史惯例）。**本期起在附录 059 段内重贴为 `[附录 059]`** —— 链接目标本来就都是 `details.html`，只有标签是旧的，但读者会以为点到了别期。

### 守卫
- `lint_table --strict` **CLEAN（R1–R4 全 0）**；`verify_web` **ALL GREEN（14 表 / 97 状态格 / 缺失片段 0）**；`build_site.sh` **两守卫 ALL GREEN**（`quick.html` `76` 条 / `43,013 B`、`index.html` 同字节、`archive.html` 收录 `59` 期）；`check_frozen` 🔴 **0**（引用 `30`）。
- `probe_mobile` 四档（320/360/375/414）：**与 058 期逐项同值**（文档宽 `1343`、`320` 档溢出元素 `41` 个、`375`/`414` 档 `0` 个、13 张表「容器可横滑」）—— **非本期回归**。

### 发布
- **未核到 / 受阻**：`mistral.ai` 全站连续第 `20` 次 `000`；`platform.reflection.ai` 连续第 `22` 期 `403`；`platform.openai.com/docs/models` 连续第 `13` 期 `403`；`next.opera.com/web-ai/` 连续第 `10` 期 `451`；`antigravity.google/models` 连续第 `8` 期 `404`；`docs.somark.ai/free-tier-rules.md` 连续第 `5` 期 `404`。
- **下一轮强制动作（20 条，见 059 期第四章脚注③）**；**最紧的五条**：① `Ollie` `11/6` 关停（`1` 天）＋ 核 `Free` 档是否一并停服 ② `Kimi K3.1 Pro` 自定义许可 `kimi-k3.1-pro` 允不允许商用 ＋ `Highspeed` 版有没有同步放权重 ③ 两个下架的 `inkling:free` 会不会回归（**若回归就是第一次「下架可逆」**）④ `stealth/crouton-alpha` 第 `4` 天是否还在 ＋ `OpenCode` 那份 `crouton-alpha-free` 会不会先消失 ⑤ `freellm.net` 更新日若仍停在 `2026-10-27` → 正文直接写「该站已停止维护该字段」。
"""

# ---- 查重 ----
with io.open(MEM, encoding="utf-8") as f:
    old = f.read()
if HEAD in old:
    print("本期内容已写过，断言退出（不覆盖）")
    sys.exit(0)

lines_before = len(old.splitlines())
with io.open(MEM, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n" + SEC)

# ---- 读回落盘复核 ----
with io.open(MEM, encoding="utf-8") as f:
    disk = f.read()
assert HEAD in disk, "059 段落未落盘"
assert disk.count(HEAD) == 1, "059 段落重复"
assert disk.startswith(old), "追加破坏了原有内容（前缀不一致）"
lines_after = len(disk.splitlines())
assert lines_after > lines_before + 10, ("追加行数异常", lines_before, lines_after)
print("已追加：%d → %d 行（+%d）" % (lines_before, lines_after, lines_after - lines_before))
