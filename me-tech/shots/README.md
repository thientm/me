# Ảnh dẫn nguồn — đầu vào của bài đang dựng, chỉ để trên máy

Ảnh chụp trang gốc cho trạm `mode: "shot"`. Từ 25.09.2026 ảnh **không commit**
(`*.png` trong `.gitignore`): một bài dựng → đăng trọn trên một máy, đăng xong là
hết giá trị. Xem `me-tech/AGENTS.md` mục "Chạy trên nhiều máy".

Chụp:

```bash
cd pipeline
.venv/bin/python capture.py <url> shots/<tên>.png --phone
```

**Luôn `--phone`.** Chụp khổ máy tính rồi thu vào khung 1080 thì chữ thân bài chỉ
còn ~5 px thật trên điện thoại — đó là ảnh trang trí, không phải trích dẫn.
