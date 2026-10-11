# -*- coding: utf-8 -*-
"""031 期记忆回写（D）：自动化 memory 的发布回写记录。"""
import io

P = ".workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"

TEXT = """
### 发布回写 · 第 031 期（2026-10-11 同日第二期）

- **commit**：`0e22aa8`（**25 files changed, 3,662 insertions(+), 318 deletions(-)**；
  **新增 13 个文件** —— md / html / **11 个脚本**：`gen_table031.py` / `inject031.py` / `addfoot031.py` /
  `fix031_wording.py` / `fix031_pitrange.py` / `fix031_dup.py` / `update_ledger031.py` / `update_frozen031.py` /
  `update_questions031.py` / `write_mem031_a.py` / `write_mem031_b.py` / `write_mem031_c.py`）。
- **push**：`dd6ba87..0e22aa8  main -> main` 成功（**内联凭据助手路线第七次生效**；`token len=40`、
  `api.github.com/user` → **200**；`-c credential.helper=` 清空 + 内联 `!f(){...}` + **`export GH_TOK`** 四要点全按
  `ENGINEERING.md` §九 执行）。
- **远端核实**：① API `repos/Lavie-purple/ai-free-content-digest/commits/main` →
  **sha `0e22aa88aa8ca6411667d4c8a1433d8ea056442e`，与本地 `git rev-parse HEAD` 完全一致**；
  ② `pages/builds/latest` **本轮连续 6 次 404**（**019 / 022 期同样的间歇性 404**）→ **按 §九 的降级路径直接抓线上页比对**，
  不卡在轮询上；③ 带 `?t=<ts>` 抓线上（`https://lavie-purple.github.io/ai-free-content-digest/`）：
  **`index.html` 30,223 B / md5 `e3d7dafb415d9f5da34ad5eb3558f884` 与本地 `cmp` 逐字节一致**（`http=200`）；
  **031 单期页 244,252 B / md5 `4b216d98d59104c83b6966fc398afea4` 与本地逐字节一致**（`http=200`）；
  **线上首页已显示「第 031 期」**，**信源数 `229`**。
- **交付物留档**：md **138,773 B / md5 `c7b757c582e073d5bb0d0b3c42e72e37` / 15 表 / 避坑 138–141**；
  html **244,252 B / md5 `4b216d98d59104c83b6966fc398afea4`**；`index.html` **30,223 B / md5 `e3d7dafb…`**；
  `INDEX.md` 31 期；台账 **229 条**；`frozen_items` **330 条**（**031 首登 12 条**）；`open_questions` **21 条**（**新增 Q21**）。
- ⚠️ **本轮三条新工程教训（已进 `ENGINEERING.md`）**：
  ① **`build_index.py` 的 `pit_range()` 用 `^##+[^\\n]*避坑`，正文里任何 `### …避坑…` 小标题都会抢先命中** ——
  031 期 `### 4. …「运维避坑」` 把「避坑 138–141」挤掉，索引显示「避坑—」；**改措辞（→「运维风险」）而非放宽守卫**；
  ② **`frozen_items.md` 的关键词必须是报告里的原样连续子串** —— 关键词含反引号时 `关键词 in 行` 静默失配，
  **重复登记不会报 🔴**（031 期 `Google SynthID Detector` 即此情形，已改为 `SynthID Detector`）；
  ③ **「就地更新」脚本要按行首前缀定位，不要只靠「唯一子串」** —— `Qwen-Image-2.1-Turbo`（029）与
  `Qwen-Image-2.1`（010）两行结尾逐字相同 → `rep()` 命中 1→2 断言失败；改用 `append_row(prefix, add)`。
- ⚠️ **本轮另有一条「计数与明细同源」的复发**：报告第八章原写 `## T0 · 根节点（123→129）`，
  **而 T0 六个子节只加了 5 条（+4 +1），总数 223 → 229 是 +6（另一条在 T4）** —— **129 与 229 自相矛盾**。
  **根因：正文括号里的数字是手写的、没跟表体行数对账**。**处置：改正文数字 + 在 `update_ledger031.py` 里加
  「六个子节求和 = T0 标题数字」与「五个 `## T\\d` 标题求和 = 全表」两道收尾断言。**
  **下一期起：台账正文里凡是出现「（N→M）」这种增量表述，必须当场用表体行数验一遍。**
- **下一轮强制动作**：① **10/12 00:00 北京 AutoClaw 第二期开跑 / 10/12 17:00 张江三券截止** → 回扫是否如期；
  ② **10/14 GPT-5.5 下线进入 3 天窗口 → 升为摘要最高优先级运维项**，同时排 **10/23 `o4-mini`**；
  ③ **10/15 Step 5 权重是否如期开放（许可证是否公布）+ Magnific One 促销 / CorelDRAW 券到期**；
  ④ **Step 5「渠道免费一周」是否到期**；⑤ **ZCode 月度安全审计报告连续第 5 期未见**；
  ⑥ **Q21 首次回核**：Cloudflare 收购 Deno 后三条时间线的具体日期 + `celld` / `workerd` 合流计划；
  ⑦ **`Drex 1.5` 的许可证是否再次变更**（新设「许可证变更追踪位」第一次留档）。
"""

old = io.open(P, encoding="utf-8").read()
io.open(P, "w", encoding="utf-8", newline="\n").write(old.rstrip("\n") + "\n" + TEXT)
print("自动化 memory 已追加 031 期发布回写  +%d B" % len(TEXT.encode("utf-8")))
