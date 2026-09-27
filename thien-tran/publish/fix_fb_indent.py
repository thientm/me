with open("fb.py", "r") as f:
    lines = f.readlines()

out = []
for i, l in enumerate(lines):
    if l.startswith("    # TỰ ĐỘNG CHUYỂN") or l.startswith("    print(\"🔍") or l.startswith("    try:") or l.startswith("    except") or l.startswith("    #"):
        if i >= 80 and not l.startswith("        "):
            l = "    " + l
    out.append(l)

with open("fb.py", "w") as f:
    f.writelines(out)
print("Patched indentation")
