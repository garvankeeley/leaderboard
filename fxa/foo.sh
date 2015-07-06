curl -v \
    -X POST \
    -H "Content-Type: application/json" \
    "https://oauth-stable.dev.lcip.org/v1/token" \
    -d '{
  "client_id": "d0f6d2ed3c5fcc3b",
  "client_secret": "3015f44423df9a5f08d0b5cd43e0cbb6f82c56e37f09a3909db293e17a9e64af",
  "code": "d7e11e6f05daf1715f2915b6b2b7c68ea305956cd1dcdc0ffc319c1383858b2c"
  }'
