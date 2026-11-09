# -*- coding: utf-8 -*-
"""063 期：手工维护的《免费速查》数据源同步（quick_items.csv）。

本期必改的四类（062 期记忆里的「下期若新增可领额度必须同步」）：
  ① `OpenRouter` 免费档：全量模型数写成 `454`（062 期实读口径），本期实读 `461` → 改数；
  ② `OpenCode` 免费模型清单：写「`11` 项（`2026-11-05` 实读）」，本期三套口径 `12/12/13` → 改数改日期；
  ③ 新增 **`AMD Radeon Token Factory`**（本期唯一「能领」的新增；额度数字官方页读不到，按线索登记）；
  ④ 四条 `11/7`–`11/8` 已到期的活动，`状态` 由 `live` 改成 `over` ——
     速查页的问句是「**今天**还能领什么」，已过期却留在倒计时区，读者要自己去读「（已过 N 天）」才发现。
     **只改 `状态`，`截止日` / `截止说明` / `分组` 一个字不动**（分组留着，已结束区才分得清来源）。
"""
import csv
import io

P = ".workbuddy/data/quick_items.csv"
raw = io.open(P, encoding="utf-8", newline="").read()
assert "\r\n" in raw, "预期 CRLF"
head = raw.split("\r\n")[0]
assert head == "分组,名称,量,截止日,截止说明,状态,门槛", head
rows = list(csv.DictReader(io.StringIO(raw)))
assert len(rows) == 77, ("改前行数", len(rows))
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

hit = []


def one(pred, why):
    idx = [i for i, r in enumerate(rows) if pred(r)]
    assert len(idx) == 1, ("命中数不为 1", why, len(idx))
    return idx[0]


# ① OpenRouter 全量数 454 -> 461
i = one(lambda r: r["名称"] == "OpenRouter 免费档", "① OpenRouter 免费档")
assert "全量 454 个模型中 16 个零价" in rows[i]["量"], rows[i]["量"]
rows[i]["量"] = rows[i]["量"].replace("全量 454 个模型中 16 个零价", "全量 461 个模型中 16 个零价")
hit.append("① OpenRouter 454 -> 461 个模型")

# ② OpenCode 清单 11 -> 12 项 + 日期
i = one(lambda r: r["名称"] == "OpenCode 免费模型清单", "② OpenCode 清单")
assert "11 项（2026-11-05 实读" in rows[i]["量"], rows[i]["量"]
old = rows[i]["量"]
rows[i]["量"] = old.replace("11 项（2026-11-05 实读", "12 项（2026-11-09 实读")
hit.append("② OpenCode 11 -> 12 项 / 实读日 11-05 -> 11-09")

# ④ 四条已过期 -> over（只动状态列）
for key in ("AutoClaw 国内站 M11W1 万圣节档",
            "AutoClaw 国际站 M11W1",
            "MiniMax 开放平台 M3 / M2",
            "火山方舟 Agent Plan 个人版"):
    i = one(lambda r: key in r["名称"], "④ " + key)
    assert rows[i]["状态"] == "live", ("④ 状态不是 live", key, rows[i]["状态"])
    rows[i]["状态"] = "over"
    hit.append("④ %s：live -> over（截止日 %s 未改）" % (key, rows[i]["截止日"]))

# ③ 新增一条（本期唯一「能领」的新增）
assert not [r for r in rows if "AMD Radeon Token Factory" in r["名称"]], "③ 已经存在"
rows.append({
    "分组": "api",
    "名称": "AMD Radeon Token Factory 公共免费模型 API",
    "量": "免费模型每日重置（额度数字官方页读不到 · 三份来源「$1/日」与「$10/日」互相矛盾）",
    "截止日": "",
    "截止说明": "未公布（官方只写「每日重置」，未给日历日）",
    "状态": "live",
    "门槛": "注册即用、免绑卡 · 20 请求/分钟 · OpenAI / Anthropic 双兼容",
})
hit.append("③ 新增 AMD Radeon Token Factory（api / live）")

# ---- 落盘（CRLF，与表头列序一致，不写 BOM）----
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
w.writeheader()
for r in rows:
    w.writerow({k: r[k] for k in COLS})
out = "\r\n".join(buf.getvalue().rstrip("\n").split("\n")) + "\r\n"
io.open(P, "w", encoding="utf-8", newline="").write(out)

# ---- 回读 ----
disk_raw = io.open(P, encoding="utf-8", newline="").read()
d = list(csv.DictReader(io.StringIO(disk_raw)))
assert len(d) == 78, ("回读行数", len(d))
assert disk_raw.count("\r\n") == 79, ("回读 CRLF 数", disk_raw.count("\r\n"))
assert [r for r in d if r["名称"] == "OpenRouter 免费档"][0]["量"].startswith("全量 461")
assert [r for r in d if r["名称"] == "OpenCode 免费模型清单"][0]["量"].startswith("12 项（2026-11-09")
assert len([r for r in d if "AMD Radeon Token Factory" in r["名称"]]) == 1
assert len([r for r in d if r["状态"] == "over"]) == 16, ("over 行数",
                                                          len([r for r in d if r["状态"] == "over"]))
print("改前 77 行 -> 改后 %d 行（状态 over %d 条）" % (len(d), len([r for r in d if r["状态"] == "over"])))
for h in hit:
    print("  " + h)
