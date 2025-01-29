up:
	docker-compose up
	
down:
	docker-compose down

connector:
	curl -X POST -H "Content-Type: application/json" --data @./configs/connector/debezium-connector.json  http://localhost:8083/connectors