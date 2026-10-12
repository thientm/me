import time
from adapters.base import BaseAdapter
from brain.filter import classify_comment
from brain.templates import get_template_reply
from brain.llm_reply import generate_smart_reply

def parse_comment_element_mock(raw: dict) -> dict:
    return {
        "id": raw.get("id", ""),
        "author": raw.get("author", ""),
        "text": raw.get("text", ""),
        "video_title": raw.get("video_title", "")
    }

class YouTubeStudioAdapter(BaseAdapter):
    def __init__(self, port: int):
        super().__init__(port=port)

    def process_comments_batch(self, comments: list[dict], channel: str, dry_run: bool = False, limit_replies: int = 5) -> list[dict]:
        results = []
        replies_count = 0

        for item in comments:
            c = parse_comment_element_mock(item)
            cid = c["id"]
            text = c["text"]
            category = classify_comment(text, channel)

            if category == "spam":
                results.append({
                    "id": cid,
                    "action_taken": ["skip_spam"],
                    "reply_text": ""
                })
                continue

            actions = ["heart", "like"]
            reply_text = ""

            if replies_count < limit_replies:
                if category == "greeting":
                    reply_text = get_template_reply(channel, "greeting", author=c["author"])
                    actions.append("reply")
                    replies_count += 1
                elif category == "question":
                    reply_text = generate_smart_reply(text, channel, video_title=c.get("video_title", ""))
                    actions.append("reply")
                    replies_count += 1

            results.append({
                "id": cid,
                "action_taken": actions,
                "reply_text": reply_text
            })

        return results

    def scan_and_engage(self, channel_id: str, channel_name: str, ledger=None, dry_run: bool = False, limit_replies: int = 5) -> list[dict]:
        from playwright.sync_api import sync_playwright

        results = []
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{self.port}")
                ctx = browser.contexts[0]
                page = ctx.new_page()
                page.set_default_timeout(10000)

                url = f"https://studio.youtube.com/channel/{channel_id}/comments/inbox"
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(5000)

                # Locate comment cards
                cards = page.locator("ytcp-comment-thread").all()
                processed_replies = 0

                for card in cards:
                    try:
                        comment_text_el = card.locator("#content-text")
                        if not comment_text_el.is_visible():
                            continue
                        text = comment_text_el.inner_text().strip()
                        author_el = card.locator("#author-text")
                        author = author_el.inner_text().strip() if author_el.is_visible() else "Khán giả"
                        cid = f"yt_{channel_name}_{hash(text + author)}"

                        if ledger and ledger.has(cid):
                            continue

                        category = classify_comment(text, channel_name)
                        if category == "spam":
                            if ledger:
                                ledger.record(cid, author, ["skip_spam"], "")
                            continue

                        actions = []
                        reply_text = ""

                        # 1. Creator Heart
                        heart_btn = card.locator("#creator-heart-button")
                        if heart_btn.is_visible():
                            if not dry_run:
                                heart_btn.click()
                                self.random_delay(1.5, 3.0)
                            actions.append("heart")

                        # 2. Like
                        like_btn = card.locator("#like-button")
                        if like_btn.is_visible():
                            if not dry_run:
                                like_btn.click()
                                self.random_delay(1.5, 3.0)
                            actions.append("like")

                        # 3. Reply
                        if processed_replies < limit_replies:
                            if category == "greeting":
                                reply_text = get_template_reply(channel_name, "greeting", author=author)
                            else:
                                reply_text = generate_smart_reply(text, channel_name)

                            reply_btn = card.locator("#reply-button")
                            if reply_btn.is_visible() and reply_text:
                                if not dry_run:
                                    reply_btn.click()
                                    self.random_delay(1.0, 2.0)
                                    input_box = card.locator("#contenteditable-root")
                                    input_box.fill(reply_text)
                                    self.random_delay(1.5, 3.0)
                                    submit_btn = card.locator("#submit-button")
                                    submit_btn.click()
                                    self.random_delay(2.0, 4.0)
                                actions.append("reply")
                                processed_replies += 1

                        if ledger:
                            ledger.record(cid, author, actions, reply_text)
                        results.append({"id": cid, "actions": actions, "reply_text": reply_text})

                    except Exception:
                        continue

                page.close()
            except Exception as e:
                print(f"[YouTubeStudioAdapter] Error connecting or scanning: {e}")

        if ledger:
            ledger.save()
        return results
