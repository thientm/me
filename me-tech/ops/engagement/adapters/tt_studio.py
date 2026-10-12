from adapters.base import BaseAdapter
from brain.filter import classify_comment
from brain.templates import get_template_reply
from brain.llm_reply import generate_smart_reply

class TikTokStudioAdapter(BaseAdapter):
    def __init__(self, port: int = 9333):
        super().__init__(port=port)

    def process_comments_batch(self, comments: list[dict], channel: str, dry_run: bool = False, limit_replies: int = 5) -> list[dict]:
        results = []
        replies_count = 0
        for item in comments:
            cid = item.get("id", "")
            author = item.get("author", "")
            text = item.get("text", "")
            category = classify_comment(text, channel)

            if category == "spam":
                results.append({"id": cid, "action_taken": ["skip_spam"], "reply_text": ""})
                continue

            actions = ["heart"]
            reply_text = ""
            if replies_count < limit_replies:
                if category == "greeting":
                    reply_text = get_template_reply(channel, "greeting", author=author)
                    actions.append("reply")
                    replies_count += 1
                elif category == "question":
                    reply_text = generate_smart_reply(text, channel)
                    actions.append("reply")
                    replies_count += 1

            results.append({"id": cid, "action_taken": actions, "reply_text": reply_text})
        return results

    def scan_and_engage(self, channel_name: str, ledger=None, dry_run: bool = False, limit_replies: int = 5) -> list[dict]:
        from playwright.sync_api import sync_playwright

        results = []
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{self.port}")
                ctx = browser.contexts[0]
                page = ctx.new_page()
                page.set_default_timeout(10000)

                url = "https://www.tiktok.com/tiktokstudio/comment"
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(6000)

                # Locate comment items
                cards = page.locator("div.comment-item").all()
                processed_replies = 0

                for card in cards:
                    try:
                        text_el = card.locator("p.comment-text").first
                        if not text_el.is_visible():
                            continue
                        text = text_el.inner_text().strip()
                        cid = f"tt_{channel_name}_{hash(text)}"

                        if ledger and ledger.has(cid):
                            continue

                        category = classify_comment(text, channel_name)
                        if category == "spam":
                            if ledger and not dry_run:
                                ledger.record(cid, "TikTok User", ["skip_spam"], "")
                            continue

                        actions = []
                        reply_text = ""

                        # Like / Heart
                        heart_btn = card.locator("button.like-btn").first
                        if heart_btn.is_visible():
                            if not dry_run:
                                heart_btn.click()
                                self.random_delay(2.0, 4.0)
                            actions.append("heart")

                        # Reply
                        if processed_replies < limit_replies:
                            reply_text = get_template_reply(channel_name, category) if category == "greeting" else generate_smart_reply(text, channel_name)
                            reply_btn = card.locator("button.reply-btn").first
                            if reply_btn.is_visible() and reply_text:
                                if not dry_run:
                                    reply_btn.click()
                                    self.random_delay(1.5, 3.0)
                                    input_box = card.locator("textarea").first
                                    input_box.fill(reply_text)
                                    self.random_delay(2.0, 3.5)
                                    send_btn = card.locator("button:has-text('Send')").first
                                    if not send_btn.is_visible():
                                        send_btn = card.locator("button:has-text('Gửi')").first
                                    send_btn.click()
                                    self.random_delay(2.0, 4.0)
                                actions.append("reply")
                                processed_replies += 1

                        if ledger and not dry_run:
                            ledger.record(cid, "TikTok User", actions, reply_text)
                        results.append({"id": cid, "actions": actions, "reply_text": reply_text})

                    except Exception:
                        continue

                page.close()
            except Exception as e:
                print(f"[TikTokStudioAdapter] Error: {e}")

        if ledger and not dry_run:
            ledger.save()
        return results
