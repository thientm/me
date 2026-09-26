with open("yt.py", "r") as f:
    c = f.read()

old_type = """t = p.locator("#title-textarea #textbox").first
t.click()
p.keyboard.press("Meta+a")
p.keyboard.press("Delete")
t.type(YT_TITLE, delay=6)
p.wait_for_timeout(600)

d = p.locator("#description-textarea #textbox").first
d.click()
d.type(YT_DESC, delay=3)"""

new_type = """t = p.locator("#title-textarea #textbox").first
t.fill(YT_TITLE)
p.wait_for_timeout(600)

d = p.locator("#description-textarea #textbox").first
d.fill(YT_DESC)"""

with open("yt.py", "w") as f:
    f.write(c.replace(old_type, new_type))
print("Patched yt.py with .fill()")
