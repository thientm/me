# Omni-Integration Business Issues

## Overview
- Component: omni-integration (Kibana logging)
- Function: Đồng bộ dữ liệu gian hàng
- Updated: 2025-09-14

## Issues
- 2025-09-14: Gian hàng hết hạn hợp đồng → đồng bộ failed, retry 30p/lần until threshold → resolved

## Notes
- Retry pattern: 30 phút intervals until threshold limit
- Monitor Kibana logs for pattern detection
