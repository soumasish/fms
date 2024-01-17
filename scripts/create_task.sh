curl -X POST http://localhost:9001/fleet/task/create/ \
-H 'Content-Type: application/json' \
-d '{"description": "New Task", "start_time": "2023-01-01T10:00:00Z"}' | jq .