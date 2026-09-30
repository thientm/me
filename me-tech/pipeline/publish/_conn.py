"""Nối tới Chrome hồ sơ Mê Tech đang chạy sẵn ở cổng 9333.

LUẬT CỨNG — đọc trước khi sửa file này:

  Chỉ được `connect_over_cdp` vào một Chrome ĐÃ chạy sẵn.
  TUYỆT ĐỐI không `launch_persistent_context` lên ~/.me-tech-browser,
  và không `pkill` nó.

Ngày 19.09.2026 đã mất sạch phiên đăng nhập cả ba nền tảng vì phạm luật này.
Bằng chứng: bảng cookie chỉ còn 15 dòng (hồ sơ Chrome thường của Thiện có ~1,2 MB),
tức là các dòng bị XOÁ chứ không phải không giải mã được. Cùng buổi sáng đó có hai
lần `launch_persistent_context` lên đúng thư mục này (một lần còn giả lập iPhone) và
một lần `pkill`; Chrome ghi lại `exit_type: Crashed`. Hôm trước không hề khởi động
lại hồ sơ — chỉ nối CDP — nên không mất gì.

Muốn đo giao diện di động thì tạo hồ sơ vứt đi riêng, đừng đụng hồ sơ này.
"""
import sys
import urllib.request
from playwright.sync_api import sync_playwright

PORT = 9333
PROFILE = "~/.me-tech-browser"

LAUNCH = f"python3 me-tech/ops/open_chrome.py {PORT}   (chạy từ gốc repo; mở nền, không cướp chuột)"


def alive():
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
        return True
    except Exception:
        return False


def connect():
    if not alive():
        sys.exit(
            f"❌ Chrome hồ sơ Mê Tech chưa chạy ở cổng {PORT}.\n"
            f"   Mở bằng tay rồi chạy lại:\n\n   {LAUNCH}\n\n"
            "   ĐỪNG để script tự mở — tự mở bằng Playwright là mất phiên đăng nhập."
        )
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    quiet(b, b.contexts[0])
    return pw, b, b.contexts[0]


def quiet(b, ctx):
    """Chạy ngầm, không cướp chuột (30.09.2026): thu nhỏ cửa sổ Chrome và cho
    ctx.new_page() mở tab ở chế độ nền. ctx.new_page() gốc của Playwright bật
    cửa sổ lên trước mặt Thiện; Target.createTarget background=True thì không.
    Đã thử: tab nền trong cửa sổ thu nhỏ vẫn goto/click/gõ phím/chụp ảnh bình thường."""
    s = b.new_browser_cdp_session()
    for t in s.send("Target.getTargets")["targetInfos"]:
        if t["type"] == "page":
            try:
                wid = s.send("Browser.getWindowForTarget", {"targetId": t["targetId"]})["windowId"]
                s.send("Browser.setWindowBounds", {"windowId": wid, "bounds": {"windowState": "minimized"}})
            except Exception:
                pass

    def new_page():
        with ctx.expect_page() as ev:
            s.send("Target.createTarget", {"url": "about:blank", "background": True})
        return ev.value
    ctx.new_page = new_page


def require_login(ctx, which):
    """Kiểm tra đăng nhập TRƯỚC khi upload, để hỏng thì hỏng sớm và nói rõ lý do."""
    probe = {
        "youtube": ("https://studio.youtube.com/", "accounts.google.com"),
        "facebook": ("https://business.facebook.com/latest/home", "loginpage"),
        "tiktok": ("https://www.tiktok.com/tiktokstudio/upload", "/login"),
    }[which]
    p = ctx.new_page()
    p.goto(probe[0], wait_until="domcontentloaded", timeout=60000)
    p.wait_for_timeout(6000)
    if probe[1] in p.url:
        sys.exit(f"❌ {which}: hồ sơ chưa đăng nhập. Đăng nhập trong cửa sổ Chrome rồi chạy lại.")
    print(f"✅ {which}: còn đăng nhập")
    return p


def quit_browser():
    """Đóng SẠCH. Không bao giờ pkill."""
    import subprocess
    subprocess.run(["osascript", "-e", 'quit app "Google Chrome"'], check=False)


def confirm_schedule(page, fields, want):
    """Đọc LẠI giá trị ngày/giờ trên giao diện trước khi bấm nút hẹn. Trống thì dừng.

    19.09.2026: bấm Schedule trên Facebook lúc ô giờ còn trống → nền tảng tự lấy
    mốc sớm nhất (now+1h) và bài suýt lên sai khung giờ. Không bao giờ tin cú bấm;
    luôn đọc lại cái mình vừa điền.

        fields = {"giờ": "input[aria-label='hours']", ...}
        want   = {"giờ": "21", ...}
    """
    import sys
    bad = []
    for name, sel in fields.items():
        loc = page.locator(sel).first
        # Đọc NHANH rồi thôi. Để nguyên timeout mặc định 120 giây thì một ô
        # biến mất khiến hàm này treo bốn phút rồi mới chết — 21.09.2026 đã
        # mất hai lần 120 giây đúng kiểu đó. Ô không đọc được = ô TRỐNG,
        # và trống thì đằng nào cũng không được bấm.
        val = ""
        # Ba cach doc, lay cai dau tien ra chu. Facebook dung o nhap do React
        # dieu khien: `input_value()` tra ve RONG trong khi man hinh hien ro
        # "12 : 30" — chu nam o the cha. Doc thieu cach thu ba thi guard bao
        # TRONG cho mot lich da dat dung (21.09.2026 hong hai lan vi the).
        for read in (lambda: loc.input_value(timeout=6000),
                     lambda: loc.inner_text(timeout=6000),
                     lambda: loc.evaluate(
                         "e => (e.parentElement && e.parentElement.innerText) || ''")):
            try:
                val = (read() or "").replace("\u202f", " ").strip()
                if val:
                    break      # RONG khong phai la doc duoc -> thu cach sau
            except Exception:
                continue
        print(f"   {name}: {val!r}")
        if not val:
            bad.append(f"{name} không đọc được hoặc đang TRỐNG")
        elif want.get(name) and want[name].lstrip("0") not in val.replace(":", " "):
            bad.append(f"{name} là {val!r}, muốn {want[name]!r}")
    # Ô nào KHÔNG được nêu trong `want` thì chỉ bị kiểm "khác rỗng" — và ô ngày
    # thì LUÔN khác rỗng vì nền tảng điền sẵn hôm nay. 22.09.2026 cả 30 bài ảnh
    # dồn vào một ngày đúng vì lỗ này: gọi confirm_schedule mà quên đưa ngày vào
    # `want`, nên cổng gật đầu cho một ô ngày chưa ai đụng tới.
    thieu = [k for k in fields if k not in want]
    if thieu:
        bad.append("KHÔNG nêu giá trị mong muốn cho: " + ", ".join(thieu) +
                   " — ô không nêu thì chỉ bị kiểm khác rỗng, tức là không kiểm gì")
    if bad:
        sys.exit("❌ KHÔNG bấm nút hẹn giờ: " + " · ".join(bad) +
                 "\n   Điền tay trên giao diện rồi chạy lại, hoặc bỏ --at để đăng ngay.")
    print("   ✅ ngày giờ đã đúng, được phép bấm")
