./stop.sh
echo ""

echo "Validate chargeback model config"
echo ""
python chargeback_validator.py -m chargeback_model.yaml
echo ""

echo "Generate prometheus metric_label_config"
echo "Copy the following config and paste it in Prometheus config at path \"kafka/prometheus\""
python generate_label_config.py -m chargeback_model.yaml -c chargeback_codes.yaml
echo ""

echo "Bring up Kafka cluster"
docker compose up -d
echo ""

echo "Wait for Kafka cluster to be in running state"
sleep 30
echo ""

echo "Create sample topics"
docker exec kafka_client bash -c "kafka-topics --bootstrap-server kafka1:29092 --create --topic testTopic --partitions 6"
docker exec kafka_client bash -c "kafka-topics --bootstrap-server kafka1:29092 --create --topic demoTopic --partitions 6"
echo ""

echo "Set Kafka Client Quotas"
docker exec kafka_client bash -c "kafka-configs --bootstrap-server kafka1:29092 --alter --add-config 'producer_byte_rate=1024,consumer_byte_rate=2048,request_percentage=200' --entity-type clients --entity-default"
echo ""

echo "Wait for JMX metrics to populate"
sleep 30

echo "Produce and consume some sample data to testTopic"
docker exec kafka_client bash -c "seq 1000 | kafka-console-producer --bootstrap-server kafka1:29092 --topic testTopic --producer-property 'client.id=demoProducer'"
docker exec kafka_client bash -c "kafka-console-consumer --bootstrap-server kafka1:29092 --topic testTopic --max-messages 1000 --from-beginning --consumer-property 'client.id=demoConsumer'"
echo ""

echo "Produce and consumer some sample data to demoTopic"
docker exec kafka_client bash -c "seq 2000 | kafka-console-producer --bootstrap-server kafka1:29092 --topic demoTopic --producer-property 'client.id=testProducer'"
docker exec kafka_client bash -c "kafka-console-consumer --bootstrap-server kafka1:29092 --topic demoTopic --max-messages 1500 --from-beginning --consumer-property 'client.id=testConsumer'"
echo ""

echo "Grafana Dashboard details"
echo ""
echo "Host: http://localhost:3000"
echo "Username: admin"
echo "Password: kafka"




