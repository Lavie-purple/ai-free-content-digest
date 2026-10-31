# -*- coding: utf-8 -*-
"""054 期：把 body_a 的刊头导语与摘要重排 —— 头条改成 054 期的真头条（`OXR` 免费 API）。

053 期刊头与摘要前四条是 `Mistral Large 4` / `OXR` / `AutoClaw` / `K2` / `Anthropic`，
054 期的头条顺序应为：`OXR`（免费 API）→ `AutoClaw`（两站两个数）→ `K2`（销项）→ `Anthropic Ultra`。
本脚本按「锚点定位 → 切段 → 重排」处理，不做脆弱的整串替换。
"""
import io

P = "tmp_054_body_a.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

# ---------- 定位摘要五条的正文片段 ----------
def seg(li, start_marker, end_marker=None):
    """取第 li 行里 [start_marker, end_marker) 之间的正文（不含标识部分）。"""
    l = lines[li]
    i = l.find(start_marker)
    assert i > 0, (li, start_marker, l[:120])
    if end_marker:
        j = l.find(end_marker, i)
        assert j > i, (li, end_marker)
        return l[i:j]
    return l[i:]


OXR_BODY = seg(18, "—— **一手**：`github.com/SoMarkAI/OXR`")
AC_BODY = seg(19, "—— **一手**：`autoclaw.z.ai/blog/news/M11W1/`")
K2_BODY = seg(20, "—— **一手**：`platform.moonshot.cn/docs/pricing/chat`")
AN_BODY = seg(21, "—— **一手**：`claude.com/pricing`")

# ---------- 刊头导语 ----------
NEW_LEAD = (
"**2026-10-31（周六）· 本期头条是「本报告至今第一次读到一份「免注册、免 API key、而且官方把免费额度写成了具体数字」的免费 API」—— `OXR`（`SoMark` 团队）**1.3B 开放权重文档解析模型**，官方 `Hugging Face` 模型卡里第一次出现了「**`🔥 🆓 Free API`**」段落，官方文档站更给出了一张**逐字写明额度的规则表**：`docs.somark.ai` 的 `free-tier-rules.md` 官方逐字 `Up to 500 pages of free quota per day` ／ `Up to 2000 pages of free quota per month` ／ `Daily free quota resets at 00:00 each day` ／ `Monthly free quota resets at 00:00 on the 1st of each month` —— **本报告此前读过的所有免费额度里，只有 `Google Antigravity` 的科研 6 个月档与个人 `$0/month` 档两条「明写期限」，但两条都没给数字；而 `Mistral Large 4` 的首周共享预算连数字都没有 —— 这一条是「免注册 ＋ 免 `API key` ＋ 明写数字」三件事第一次同时成立**。**同期还拿到三条硬条目**：**① `AutoClaw` 万圣节双周档 `M11W1` —— 国际站给 `80M`、国内站给 `50M`，且起始日不同（国际 `10/31`、国内 `11/2`）、积分当量不同（`8,000` vs `5,000`）—— **同一个活动在两个官方站点上就是两个活动**（新立避坑 240）；**② `Moonshot` `K2` 系列 `10/31` 停新 —— 官方定价页逐字原文终于核到**（**被追了 7 期的挂账项，本期销项** —— 且 053 期记的「四个候选文档页各命中 `0` 次」其实是「当期没读到那一段」，**不是「官方没写」**，新立避坑 243）；**③ `Anthropic` 订阅档改版 —— `Max 20x` 更名 `Ultra`、`Ultra` 取消 5 小时限制、月度 API credits 从 `$100` 翻倍到 `$200`**。另外本期完成了 `OpenRouter` 全量 `456` 条 ID 的逐条 diff（**新增 `0`、消失 `0`**）、以及 `Runware` 促销数组的逐条 diff —— **后者打破了一个连续两期的「逐条零变化」口径**：**官方把一条在售促销的 `endsAt` 从 `10/31` 延长到了 `11/30`**"
)
assert lines[2].startswith("**2026-10-31")
lines[2] = NEW_LEAD

# ---------- 摘要重排 ----------
# 第一条：OXR（原第二条），但把 `docs.somark.ai/...` 的裸路径写法改成「`docs.somark.ai` 的 `xxx.md`」
b_oxr = OXR_BODY
b_oxr = b_oxr.replace("`docs.somark.ai/en/api-reference/oxr/index.md`（`200` / `4,580` 字节）",
                      "`docs.somark.ai` 的 `oxr/index.md`（`200` / `4,580` 字节）")
b_oxr = b_oxr.replace("**`docs.somark.ai/en/documentation/free-tier-rules.md`（`200` / `1,290` 字节 —— 本期最硬的一条一手证据）**",
                      "**`docs.somark.ai` 的 `free-tier-rules.md`（`200` / `1,290` 字节 —— 本期最硬的一条一手证据）**")
b_oxr = b_oxr.replace("**官方逐字（`free-tier-rules.md` 的规则表）**：`Daily free quota | Up to 500 pages of free quota per day`、`Monthly free quota | Up to 2000 pages of free quota per month`、`Daily reset time | Daily free quota resets at 00:00 each day`、`Monthly reset time | Monthly free quota resets at 00:00 on the 1st of each month`",
                      "**官方逐字（规则表）**：`Up to 500 pages of free quota per day` ／ `Up to 2000 pages of free quota per month` ／ `Daily free quota resets at 00:00 each day` ／ `Monthly free quota resets at 00:00 on the 1st of each month`")
b_oxr = b_oxr.replace("**官方逐字（`oxr/index.md` 的 `Free API` 段）**", "**官方逐字（`Free API` 段）**")
b_oxr = b_oxr.replace("⚠️ **「免注册 + 免 API key + 明写数字」这三件事同时成立，是本报告至今第一条**",
                      "⚠️ **「免注册 ＋ 免 key ＋ 明写数字」三件事同时成立，是本报告至今第一条**")
# 追加归期说明
b_oxr += ("。⚠️ **归期如实写**：官方 `README.md` 的 `Free API` 段**首次出现于提交 `0245ee0e`"
          "（`2026-10-19T10:11:58Z`）** —— **落在 051 期窗口之前，本报告此前从未覆盖过它，"
          "本期按「首次登记的往期事件」写入**（避坑 229）")

lines[17] = ("- **本期头条（本报告至今第一次读到「免注册、免 `API key`、且官方把免费额度写成了具体数字」的免费 API）**："
              "`OXR`（`SoMark` 团队）**1.3B 开放权重文档解析模型 + 官方「免费 API」**" + b_oxr)

b_ac = AC_BODY.replace("**国际站逐字**", "**国际站逐字**")
lines[18] = ("- **本期头条之二（一个活动，两个官方站点，两个数 —— 连起始日都不同）**：`AutoClaw` 万圣节双周档 `M11W1`" + b_ac)

lines[19] = ("- **本期头条之三（被追了 7 期的挂账项，本期销项）**：`Moonshot` `K2` 系列 `10/31` 停新" + K2_BODY)

b_an = AN_BODY.replace("**对照表逐字** `Limit every 5 hours | Limited | 1x | 5x | No 5-hour limit ‡` ＋ `Limit every week | Limited | 1x | 5x | 10x`",
                       "**对照表逐字**（`Limit every 5 hours` 一行四格：`Free`=`Limited`／`Pro`=`1x`／`Max`=`5x`／`Ultra`=`No 5-hour limit ‡`）＋（`Limit every week` 一行四格：`Free`=`Limited`／`Pro`=`1x`／`Max`=`5x`／`Ultra`=`10x`）")
lines[20] = ("- **本期头条之四（`Anthropic` 订阅档改版：`Max 20x` 更名 `Ultra`、取消 5 小时限制、"
              "月度 API credits 翻倍）**" + b_an)

io.open(P, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("patched lead + summary")
