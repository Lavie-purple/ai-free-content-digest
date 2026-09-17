# AI 免费内容与权益速递 · 期号索引

> 本文件由 `.workbuddy/build_index.py` **自动生成，请勿手工编辑**。
> 重建：`python .workbuddy/build_index.py`

共 **6 期**（2026-09-14 ~ 2026-09-17），Markdown 合计 **148495 B ≈ 145 KB**。

| 期号 | 日期 | 本期定位 | md 体积 | 表格 | 网页版 | 避坑编号 |
| --- | --- | --- | --- | --- | --- | --- |
| **001** | 2026-09-14 | AI 免费内容发布 · 免费额度 · 免费内容生成工具 | 12,619 B | 5 | — | 1–7 |
| **002** | 2026-09-14 | 复核更新版 | 18,806 B | 11 | — | 1–10 |
| **003** | 2026-09-15 | 刷新版 | 16,249 B | 11 | — | 1–11 |
| **004** | 2026-09-15 | 晚间信源扩版 | 22,062 B | 11 | — | 12–15 |
| **005** | 2026-09-16 | 分发入口专题版 | 35,071 B | 14 | 86647 B | 16–20 |
| **006** | 2026-09-17 | 匿名模型与分发入口续集 | 43,688 B | 15 | 97904 B | 21–25 |

## 台账与结构化数据（内部，不对外展示）

- **信源分级台账** `AI信息源分级清单-T0-T4.md`：182 条（T0 97 / T1 19 / T2 18 / T3 36 / T4 12）
- **截止时间表** `.workbuddy/data/deadlines.csv`：37 条（由 `extract_deadlines.py` 从最新一期重建）
- **已固化条目库** `.workbuddy/data/frozen_items.md`（防重复往期）
- **待澄清口径** `.workbuddy/data/open_questions.md`
- **信源命中统计** `.workbuddy/data/source_hits.csv`（品牌提及口径，用于筛零命中源）

## 工具链（`.workbuddy/`，均可**不传参自动取最新一期**）

| 脚本 | 作用 |
| --- | --- |
| `build_web.py` | 日报 md → 单文件网页版（自包含，0 外部引用） |
| `verify_web.py` | 编译后必跑：表格列数/行数、保真度、标签闭合、状态格 |
| `probe_layout.py` | UI 量测：表格列宽满足度 / 搜索框可用宽 / 装饰元素压字（需 Edge） |
| `audit_color.py` | 配色审计：语义色色距 + WCAG 对比度 + opacity 叠加后实测值 |
| `extract_deadlines.py` | 第四章截止表 → deadlines.csv |
| `check_deadlines.py` | 截止巡检：过期未更新 / N 天内到期（`--days` / `--today`） |
| `check_frozen.py` | 出刊前防重复：比对已固化条目库，有重复则 exit 1 |
| `build_source_hits.py` | 信源命中统计 → 回写台账 + 导出 CSV |
| `build_index.py` | 重建本索引 |

## 版本控制

远端私仓：`Lavie-purple/ai-free-content-digest`（GitHub，private）
