import sys, re
with open("yt.py", "r") as f:
    c = f.read()

# Replace the previous bad fix with the working one
old_nav = """create_btn = p.get_by_test_id("create-icon")
if create_btn.count():
    create_btn.first.click()
    p.wait_for_timeout(2000)
    p.locator("tp-yt-paper-item").filter(has_text="Upload videos").first.click()"""

new_nav = """create_btn = p.get_by_role("button", name=re.compile(r"create", re.I))
if create_btn.count():
    create_btn.first.click()
    p.wait_for_timeout(2000)
    p.locator("tp-yt-paper-item").filter(has_text=re.compile(r"upload", re.I)).first.click()"""

with open("yt.py", "w") as f:
    f.write(c.replace(old_nav, new_nav))
print("Patched yt.py again")
