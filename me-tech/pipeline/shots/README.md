# Ảnh dẫn nguồn — ĐẦU VÀO, không phải đầu ra

Ảnh chụp trang gốc cho trạm `mode: "shot"`. Để ở đây chứ **không** để trong
`render/shots/`: `render/` nằm trong `.gitignore`, nên ảnh để đó là mất — và mất
ảnh thì **không dựng lại được bài cũ**. 21.09.2026 phát hiện `render/shots/` đã
rỗng, tức là bài `hacktron-openai` không dựng lại được nữa.

Chụp:

```bash
cd pipeline
.venv/bin/python capture.py <url> shots/<tên>.png --phone
```

**Luôn `--phone`.** Chụp khổ máy tính rồi thu vào khung 1080 thì chữ thân bài chỉ
còn ~5 px thật trên điện thoại — đó là ảnh trang trí, không phải trích dẫn.
