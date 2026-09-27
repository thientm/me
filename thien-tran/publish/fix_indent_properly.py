import re
with open("fb.py", "r") as f:
    text = f.read()

# I will find "    if pub_btn.is_visible() and pub_btn.is_enabled():" and replace everything below it up to "pub_btn.click()"
new_block = """    if pub_btn.is_visible() and pub_btn.is_enabled():
        # TỰ ĐỘNG CHUYỂN SANG PUBLIC (CÔNG KHAI) NẾU ĐANG LÀ ONLY ME/FRIENDS
        print("🔍 Đang kiểm tra quyền riêng tư (Audience)...")
        try:
            audience_btn = p.locator('div[role="button"]').filter(has_text=re.compile(r"^(Only me|Chỉ mình tôi|Friends|Bạn bè)\\\\s*(Only me|Chỉ mình tôi|Friends|Bạn bè)$", re.I)).first
            if audience_btn.is_visible():
                print("🔒 Phát hiện đang ở chế độ rêng tư, tiến hành mở Public...")
                audience_btn.click()
                p.wait_for_timeout(1500)
                public_opt = p.locator('div[role="radio"]').filter(has_text=re.compile(r"Public|Công khai", re.I)).first
                if public_opt.is_visible():
                    public_opt.click()
                    p.wait_for_timeout(1000)
                save_btn = p.get_by_role("button", name=re.compile(r"Save|Lưu", re.I)).first
                if save_btn.is_visible():
                    save_btn.click()
                    p.wait_for_timeout(1500)
                    print("✅ Đã chuyển thành công sang Public!")
        except Exception as e:
            print("⚠️ Không thể đổi quyền Public tự động (Có thể nó đã là Public sẵn). Bỏ qua.")
        print("🚀 Đang bấm Đăng (Publish)...")
        pub_btn.click()"""

# We'll just read up to line 78 and rewrite
lines = text.split("\n")
out = []
in_block = False
for l in lines:
    if l.startswith('    if pub_btn.is_visible() and pub_btn.is_enabled():'):
        out.append(new_block.replace('\\\\', '\\'))
        in_block = True
    elif in_block and l.strip() == "pub_btn.click()":
        in_block = False
    elif not in_block:
        out.append(l)

with open("fb.py", "w") as f:
    f.write("\n".join(out))
