# POS Online Service

## Dependencies
- **Kafka**: 3 instances trên production
  - Log paths: `/var/log/kafka` (production)

## Configuration
- **DB**: kol01_sandbox (dev)
- **URI**: mongodb://kol:ooF3eF7o@dc2d-ko-database-04.citigo.io:27017,dc2d-ko-database-05.citigo.io:27017,dc2d-ko-database-06.citigo.io:27017/kol01_sandbox?authSource=kol01_sandbox&replicaSet=rs0&maxPoolSize=100&readPreference=secondaryPreferred&maxStalenessSeconds=120
- **Hosts**: dc2d-ko-database-04,05,06.citigo.io:27017
- **RS**: rs0, **Pool**: 100, **Read pref**: secondaryPreferred
- **Staleness**: 120s, **Auto index**: false

## Notes
- Updated: 2025-09-25
- Critical info: Production log location cho troubleshooting
