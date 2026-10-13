"""CLI utility for Telegram notifications."""
import argparse
import sys
from ops.telegram import client, notifier, config

def main():
    parser = argparse.ArgumentParser(description="Personal OS Telegram Notification CLI")
    parser.add_argument("--test", type=str, help="Send a test message")
    parser.add_argument("--crypto", action="store_true", help="Send mock/sample Crypto Review notification")
    parser.add_argument("--pipeline", action="store_true", help="Send sample Pipeline Status notification")
    parser.add_argument("--alert", type=str, help="Send alert message")
    parser.add_argument("--source", type=str, default="System Monitor", help="Alert source name")
    parser.add_argument("--dry-run", action="store_true", help="Print message to console without sending")

    args = parser.parse_args()

    if not config.is_configured() and not args.dry_run:
        print("⚠️ Warning: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing in .env.")
        print("Please check your .env configuration.")

    if args.test:
        print(f"Sending test message: {args.test}")
        res = client.send_message(args.test, dry_run=args.dry_run)
        print("Result:", res)
        sys.exit(0 if res.get("ok") else 1)

    elif args.crypto:
        print("Sending sample Crypto Review notification...")
        res = notifier.notify_crypto_review(
            tts_vnd=512_500_000,
            btc_price=84_140,
            sol_price=113.0,
            p2p_rate=25_895,
            floor_vnd=500_000_000,
            action_note="Ưu tiên xả toàn bộ SOL ra USDT để khóa rủi ro.",
            dry_run=args.dry_run
        )
        print("Result:", res)
        sys.exit(0 if res.get("ok") else 1)

    elif args.pipeline:
        print("Sending sample Pipeline Status notification...")
        res = notifier.notify_pipeline_status(
            slot="12:00",
            channel="Mê Tech",
            slug="quinnipiac-ai-trust-crisis",
            gates={"Gate 1 (Script)": True, "Gate 2 (Audio)": True, "Render": True, "Publish": True},
            next_slot="20:00 (Kênh 3)",
            dry_run=args.dry_run
        )
        print("Result:", res)
        sys.exit(0 if res.get("ok") else 1)

    elif args.alert:
        print(f"Sending alert notification: {args.alert}")
        res = notifier.notify_alert(
            source=args.source,
            error_msg=args.alert,
            action_needed="Kiểm tra logs hệ thống tại terminal.",
            dry_run=args.dry_run
        )
        print("Result:", res)
        sys.exit(0 if res.get("ok") else 1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
