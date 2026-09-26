import re
with open("fb.py", "r") as f:
    c = f.read()

# Replace the overly broad Publish button regex with a strict one
old_btn = 'pub_btn = p.get_by_role("button", name=re.compile(r"Publish|Đăng", re.I)).first'
new_btn = 'pub_btn = p.get_by_role("button", name=re.compile(r"^(Post|Publish|Đăng)$", re.I)).first'

with open("fb.py", "w") as f:
    f.write(c.replace(old_btn, new_btn))
print("Patched fb.py publish button regex")
