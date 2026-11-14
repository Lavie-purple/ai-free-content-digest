import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, ".workbuddy", "memory", "automations",
                 "256c1349-ea4a-4721-9c5d-14067699f1f1", "memory.md")
A = os.path.join(ROOT, ".workbuddy", "mem068_section.md")

s = io.open(P, encoding="utf-8").read()
a = io.open(A, encoding="utf-8").read()

assert "## \u7b2c 068 \u671f" not in s, "already appended"
before = len(s)

s2 = s.rstrip("\n") + "\n\n" + a.strip("\n") + "\n"
io.open(P, "w", encoding="utf-8", newline="\n").write(s2)

# read back
chk = io.open(P, encoding="utf-8").read()
assert "## \u7b2c 068 \u671f" in chk, "not landed"
assert len(chk) == len(s2), "length mismatch"
assert chk.startswith(s.rstrip("\n")), "prefix changed"
assert "\r" not in chk, "CR found"

print("ok | before %d -> after %d (+%d)" % (before, len(chk), len(chk) - before))
print("lines", chk.count("\n"))
