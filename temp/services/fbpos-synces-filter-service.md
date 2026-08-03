# fbpos-synces-filter-service

## Overview
- Description: Service lọc message Kafka cho Facebook POS sync
- Type: Message filtering service

## Functionality
- Nhận message từ: SyncEs topic
- Lọc theo: kênh bán Facebook
- Gửi message sang: topic khác

## Configuration
- Input topic: SyncEs
- Filter criteria: Facebook channel
- Output topic: [to be defined]

## Notes
- Updated: 2025-09-29
