# mapping-recovery (Deprecated)

## Overview
- Description: Golang service để scan và fix data mapping lỗi
- Owner: Lý Ngọc Hùng - KV Retail
- Updated: 2025-10-24

## Status
- **Deprecated**: Đã bỏ từ 2025-10-24
- **Replacement**: omni-mapping-product-service-v2
- **Reason**: Consolidate mapping logic vào một service

## Previous Function
- Scan mapping errors
- Recovery data mapping
- Fix product mapping issues
- Handle KV retail mapping

## Configuration (Historical)
- **Language**: Golang
- **Function**: Background job để chạy recovery
- **Usage**: Manual trigger khi có mapping errors

## Migration Notes
- Business logic cần migrate sang omni-mapping-product-service-v2
- Code cũ có thể reference để implement lại functionality
- Contact: Lý Ngọc Hùng for legacy code access

## Issues Handled
- Product mapping errors với KV retail
- Data consistency issues
- Recovery patterns cho failed mappings

## Notes
- Service này không còn được sử dụng
- Nếu có lỗi mapping hiện tại → fix trong omni-mapping-product-service-v2
- Không nên sử dụng service cũ vì có thể outdated
