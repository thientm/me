#!/bin/bash
# Giám sát viên Mê Tech — launchd gọi lúc 07:40 · 11:40 · 19:40 (và chạy bù khi máy vừa thức).
#
# Vì sao nằm NGOÀI Claude: tác vụ dựng chạy trong một session Claude. Session đó treo
# (lệnh con kẹt) hoặc máy ngủ thì không lịch nào trong cùng session chen vào được.
#
#   1. khung đã đủ 3 nền tảng        -> thôi
#   2. tiến trình pipeline chạy >30' -> coi là treo, TERM rồi KILL (chỉ python/run.sh
#                                       của pipeline — KHÔNG đụng Chrome, KHÔNG pkill)
#   3. khoá .run/build.lock được chạm <20' -> job khác đang chạy, thôi (tránh hai agent
#                                       đăng hai bài). Job đang chạy phải `touch` khoá ở mỗi bước.
#   4. còn lại                       -> giữ khoá, mở Chrome nếu tắt, chạy `claude -p`
#                                       tối đa 50 phút để dựng/đăng nốt khung này
set -u
# launchd không nạp profile: tự khai PATH (node cho hook plugin) và USER/LOGNAME
# (thiếu thì `claude -p` không đọc được keychain → "Not logged in")
export PATH="/Users/thien.tm/.local/bin:/Users/thien.tm/.nvm/versions/node/v22.14.0/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export USER=thien.tm LOGNAME=thien.tm HOME=/Users/thien.tm
ME=/Users/thien.tm/Documents/me
MT=$ME/me-tech
RUN=$MT/.run
LOCK=$RUN/build.lock
LOG=$HOME/Library/Logs/metech-watchdog.log
mkdir -p "$RUN"
exec >>"$LOG" 2>&1
say() { echo "[$(date '+%d/%m %H:%M:%S')] $*"; }
notify() { osascript -e "display notification \"$1\" with title \"Mê Tech giám sát\"" >/dev/null 2>&1; }

H=$((10#$(date +%H)))
SLOT=$(( H + 1 ))
# chạy bù lúc máy thức muộn: gán về khung gần nhất đã qua giờ dựng
if   (( H >= 7  && H < 11 )); then SLOT=8
elif (( H >= 11 && H < 19 )); then SLOT=12
elif (( H >= 19 && H < 23 )); then SLOT=20
else say "ngoài giờ ($H h), không đăng 00:00–06:00"; exit 0; fi
say "── khung $(printf %02d $SLOT):00"

cd "$ME" && git pull -q --rebase --autostash || say "⚠ git pull lỗi, dùng sổ trên máy"

ST=$(python3 "$MT/ops/slot_status.py" $SLOT); RC=$?
say "sổ: $ST"
(( RC == 0 )) && exit 0

# 2 · tiến trình treo
python3 - <<'EOF'
import os, re, signal, subprocess, time
out = subprocess.run(["ps", "-axo", "pid=,etime=,command="], capture_output=True, text=True).stdout
def secs(e):
    d, _, t = e.rpartition("-"); p = [int(x) for x in t.split(":")]
    while len(p) < 3: p.insert(0, 0)
    return (int(d) if d else 0) * 86400 + p[0] * 3600 + p[1] * 60 + p[2]
stuck = []
for ln in out.splitlines():
    pid, et, cmd = ln.strip().split(None, 2)
    if "me-tech/pipeline" in cmd or re.search(r"\b(run\.sh|build\.py|post\.py|yt\.py|tt\.py|fb\.py|fb_finish\.py|capture\.py)\b", cmd):
        if "Google Chrome" in cmd or "watchdog" in cmd or cmd.split()[0].endswith("claude"): continue
        if secs(et) > 30 * 60: stuck.append((int(pid), cmd[:120]))
for pid, cmd in stuck:
    print(f"   treo >30' -> TERM {pid}: {cmd}"); os.kill(pid, signal.SIGTERM)
if stuck:
    time.sleep(10)
    for pid, _ in stuck:
        try: os.kill(pid, signal.SIGKILL); print(f"   KILL {pid}")
        except ProcessLookupError: pass
EOF

# 3 · khoá
if [[ -f $LOCK ]]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$LOCK") ))
    if (( AGE < 1200 )); then
        say "khoá còn mới ($((AGE/60))'): $(cat "$LOCK") — job khác đang chạy, không chạy song song"
        exit 0
    fi
    say "khoá $((AGE/60))' không ai chạm → coi như job chết, gỡ khoá"; rm -f "$LOCK"
fi

# 4 · tự chạy
if [[ -n ${DRY:-} ]]; then say "DRY: tới đây sẽ giữ khoá + chạy claude -p cho khung $SLOT:00 ($ST)"; exit 0; fi
echo "watchdog pid $$ · khung $SLOT:00 · $(date '+%d/%m %H:%M')" > "$LOCK"
( while sleep 240; do touch "$LOCK"; done ) & TOUCHER=$!
trap 'kill $TOUCHER 2>/dev/null; rm -f "$LOCK"' EXIT
curl -s -m 3 http://127.0.0.1:9333/json/version >/dev/null || {
    say "Chrome 9333 tắt → mở lại theo publish/README.md"
    nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        --user-data-dir="$HOME/.me-tech-browser" --remote-debugging-port=9333 \
        --no-first-run --no-default-browser-check >/dev/null 2>&1 &
    sleep 8
}
notify "Khung $(printf %02d $SLOT):00 chưa đủ bài ($ST) — giám sát viên tự chạy"

HH=$(printf %02d $SLOT)
PROMPT="[Giám sát viên Mê Tech — chạy thay tác vụ định kỳ bị lỡ/treo] Sổ đăng bài báo khung ${HH}:00 hôm nay: ${ST}.
Chế độ TỰ DUYỆT, theo đúng me-tech/AGENTS.md, chỉ làm trong me-tech/. Chrome cổng 9333 đã mở sẵn — KHÔNG pkill, KHÔNG tự mở hồ sơ bằng Playwright. Python của pipeline là .venv/bin/python (không dùng python3 hệ thống cho script đăng).
- Nếu 'partial <slug> <thiếu>': KHÔNG dựng bài mới. Chỉ đăng nốt nền tảng thiếu của đúng <slug> (python3 publish/use.py <slug>, rồi publish/*_finish.py nếu composer còn mở, không thì ../.venv/bin/python post.py --only <nền tảng>), hẹn ${HH}:00 nếu còn >20 phút, không thì đăng ngay.
- Nếu 'none': chạy daily Mê Tech đầy đủ (chọn tin, content, shot --phone, validate.py, ./run.sh, contact sheet, meta_<slug>.py, use.py, post.py). Còn >20 phút tới ${HH}:00 thì --at ${HH}:00 (TikTok lệch 30 phút), không thì đăng ngay. Trễ giờ KHÔNG phải lý do bỏ khung; chỉ dừng khi cổng an toàn hỏng không sửa được.
- Sau đó chạy yt_verify/tt_verify/fb_verify, ghi 1 dòng log (ghi rõ 'chạy bởi giám sát viên'), commit CHỈ me-tech/logs/ rồi git push (push lỗi thì ghi chú, đừng dừng).
- Không xoá video trên nền tảng. Có bản thừa thì ghi vào log để Thiện xử lý."

say "chạy claude -p (tối đa 50')"
cd "$MT"
caffeinate -i perl -e 'alarm shift; exec @ARGV' 3000 \
  claude -p "$PROMPT" --permission-mode acceptEdits \
    --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebSearch" "WebFetch" \
      "Bash(git pull:*)" "Bash(git add:*)" "Bash(git commit:*)" "Bash(git push:*)" "Bash(git status:*)" "Bash(git log:*)" "Bash(git diff:*)" \
      "Bash(./run.sh:*)" "Bash(.venv/bin/python:*)" "Bash(../.venv/bin/python:*)" "Bash(python3:*)" \
      "Bash(curl -s:*)" "Bash(ffmpeg:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(grep:*)" "Bash(head:*)" "Bash(tail:*)" "Bash(date:*)" "Bash(cd:*)" \
  --output-format text > "$RUN/last-run.txt" 2>&1
RC=$?
say "claude thoát mã $RC ($([[ $RC == 142 ]] && echo 'hết 50 phút, bị cắt' || echo 'xong'))"
ST2=$(python3 "$MT/ops/slot_status.py" $SLOT)
say "sổ sau khi chạy: $ST2"
notify "Khung ${HH}:00 sau giám sát: $ST2"
