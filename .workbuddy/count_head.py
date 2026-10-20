# -*- coding: utf-8 -*-
import io, re, sys
sys.path.insert(0, ".workbuddy")
import importlib.util
spec = importlib.util.spec_from_file_location("bsh", ".workbuddy/build_source_hits.py")
bsh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bsh)
for tag, P in [("HEAD(035后)", ".workbuddy/tmp_ledger_head.md"), ("当前(036)", "AI信息源分级清单-T0-T4.md")]:
    t = io.open(P, encoding="utf-8").read()
    rows = bsh.parse_sources(t)
    print("%s : build_source_hits 行数 = %d" % (tag, len(rows)))
