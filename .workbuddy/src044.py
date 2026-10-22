# -*- coding: utf-8 -*-
"""044 期：台账新增 5 条一手源 + 同步三处手写括号计数。
⚠️ 034/036 期纪律：改计数用 rindex("（") 精确切分；「加行」与「加行加对节」是两件事。
⚠️ 改完必须跑 audit_src036.py 逐节核对「括号数 vs 实际行数」。
"""
import io
import re

P = "AI信息源分级清单-T0-T4.md"

# ---- 本期新增 5 条（均为本轮实际取料的一手源）----
NEW = {
 "模型与开源": [
  "| **🆕 `OpenRouter` 官方 API 目录** | https://openrouter.ai/api/v1/models | — | **免费清单的第一手判据（本报告第一次把「官方 API 目录」当判据）**。**044 期首次取用：468 全量 / 21 零价 / 18 带 `:free` 后缀**；**差额 3 个为 `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free`（路由器）** —— **「零价」与「带 `:free`」是两个口径，不可互换**（避坑 161）。**⚠️ 目录与模型页均无 `limited time` / `until`** → **限免时长只认官方公告页**（避坑 191） | 044 | 1 |",
  "| **🆕 `Hugging Face` `RecursiveSI` 组织页** | https://huggingface.co/RecursiveSI/flint | — | **本期新增免费档的权重一手**。**`apache-2.0` + `gated: false` + `createdAt` 2026-10-21 14:20:58 UTC + `lastModified` 14:24:03 + `downloads: 0`**；**tags 含 `region:us`**；**另有 `int4` / `int4-gguf` / `nvfp4-gguf` 三个衍生仓库**。**⚠️ `downloads: 0` 不等于没人用**（发布不足一天）；**⚠️ `region:us` 是地域标记，需与平台限免口径分开看** | 044 | 1 |",
 ],
 "官方一手 · 国外": [
  "| **🆕 `OpenAI` 公告 `Patch the Planet`** | https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/ | — | **本期唯一的「三种免费形态同篇并存」样本**。**逐字三层**：`We’re sharing`（`PHP` 版本检查 `Codex` skill，**`Apache-2.0`、可自取**）/ `$1 billion` subsidized `Daybreak access` through `Daybreak for Frontline Defenders`（**定向补贴、对象是资源有限的机构、官方未给截止日**）/ `subscriptions for all maintainers through Codex for OSS`（**身份权益、需申请**）。**⚠️ 全页无 `free` 一词**；**⚠️ 官方自认 `safeguards ... can also block legitimate security work`**（避坑 185）。**⚠️ 取料坑：真实 slug 是本条 URL，`/index/patch-the-planet/` 抓到的是 6 月旧文** | 044 | 1 |",
  "| **🆕 `vLLM` 官方仓库（`Humming`）** | https://github.com/vllm-project/humming | — | **第二个「框架开源」样本**。**`Apache-2.0`、284 stars / 58 forks、created 2026-02-11、pushed 2026-10-21 05:54 UTC**；**README 逐字 `SM75+` / `Requires only PyTorch and NVCC` / `package size is only 100+KB` / `Supports both Dense GEMM and MoE GEMM`**。**⚠️ 判据分工：框架开源看「能不能跑起来、依赖什么硬件」，不是「能不能下载、许可是什么」** —— **避坑 189 的许可五层不适用于框架** | 044 | 1 |",
  "| **🆕 `Anthropic` 官方资源页（`Claude Duet`）** | https://claude.com/resources/articles/claude-duet | — | **「官方没说免费」这条路线的第一个完整样本**。**逐字 `included in Pro and Max plans and uses the same usage limits as the rest of Claude` / `starting with Pro and Max users in the US` / `available by waitlist today` / `Its background checks count toward those limits`**。**⚠️ 全篇无 `free` 字样 → 官方无免费额度**（避坑 195 三步法）；**⚠️ `Team`/`Enterprise` 公告未说明** | 044 | 1 |",
 ],
}

# ---- 计数同步：标题 + 增量 ----
COUNTS = [
 ("## T0 · 根节点（161）", 5),
 ("### 模型与开源（33）", 2),
 ("### 官方一手 · 国外（49）", 3),
]

VERSION_NOTE = (
 "；就地更新至 **2026-10-22（044 期，条目数 272 → 277；**T0 模型与开源 +2**（**`OpenRouter` 官方 API 目录** —— "
 "**免费清单的第一手判据，本报告第一次拿官方 API 目录当准绳：468 全量 / 21 零价 / 18 带 `:free`，与第三方转录站的 `20` 条三个数各不相同**；"
 "**`Hugging Face` `RecursiveSI` 组织页** —— **本期新增免费档的权重一手：`apache-2.0` + `gated: false` + `downloads: 0` + `region:us` 标签**）"
 "/ **T0 官方一手 · 国外 +3**（**`OpenAI` 公告 `Patch the Planet`** —— **同一篇公告里三层「免费」并存（`We’re sharing` 的 Apache-2.0 工具 / "
 "`$1 billion` 面向资源有限机构的定向补贴 / `Codex for OSS` 维护者身份权益），且全页无 `free` 一词**；"
 "**`vLLM` 官方仓库 `Humming`** —— **第二个「框架开源」样本，`SM75+` 硬件门槛是必写字段**；"
 "**`Anthropic` 官方资源页 `Claude Duet`** —— **「官方没说免费」这条路线的第一个完整样本**）→ **T0 合计 161 → 166**"
 "（**论文与预印本 12、官方一手 · 国内 28、政策与监管 22、评测与榜单 17 均不变**）、**T1 19、T2 18、T3 41、T4 33 均不变**）→ **全表 272 → 277 条**；"
 "**手写计数三处同步**（`## T0 · 根节点（161→166）`、`### 模型与开源（33→35）`、`### 官方一手 · 国外（49→52）`）—— "
 "**站点首页「信源 N 条」= 五个 `## T\d …（N）` 标题求和**；"
 "**本期就地更新 1 行**：**`freellm.net`**（**`No Credit Card` 由 `425+` 变 `425` —— 口径表述变化，两期不可相减**；"
 "**新增两个从未登记的面板字段 `Models Tracked 510` 与 `Free & Online 301`**；**其 `:free` 清单本期缺 `recursive/flint-v1.0:free`**，"
 "**是「转录源会滞后于官方目录」的具体样本**）；"
 "**044 期另逐条核对用户随任务提供的 T0–T4 补充清单**：**与台账逐条比对无新增项、无缺项，故不产生条目增删**"
 "（**其中 T0=97 / T1=19 / T2=18 / T3=36 / T4=12 = 182 条是分级清单的原始基线，与台账当前 277 条不是同一口径、不可相减**））**）"
)


def main():
    t = io.open(P, encoding="utf-8", newline="").read()
    assert "\r\n" not in t, "台账不是 LF 行尾，先查清再改"
    L = t.split("\n")

    for sec, rows in NEW.items():
        hi = None
        for i, x in enumerate(L):
            if x.strip().startswith("### " + sec):
                hi = i
                break
        assert hi is not None, sec
        last = None
        for j in range(hi + 1, len(L)):
            if L[j].startswith("##"):
                break
            if L[j].startswith("|"):
                last = j
        assert last is not None, sec
        L = L[:last + 1] + rows + L[last + 1:]

    t = "\n".join(L)

    for head, delta in COUNTS:
        assert t.count(head) == 1, (head, t.count(head))
        i = t.rindex(head)
        m = re.search(r"（(\d+)）", t[i:i + len(head)])
        assert m, head
        old = int(m.group(1))
        s = i + m.start(1)
        e = i + m.end(1)
        t = t[:s] + str(old + delta) + t[e:]

    # 版本行追加本期说明
    key = "**用途**：为「AI 免费内容与权益速递」日报提供扫描路由。"
    assert t.count(key) == 1
    t = t.replace(key, VERSION_NOTE + "\n" + key)

    io.open(P, "w", encoding="utf-8", newline="\n").write(t)
    print("ledger updated")


if __name__ == "__main__":
    main()
