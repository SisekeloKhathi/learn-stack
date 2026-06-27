from kafka import KafkaConsumer
import json
import os
import logging

# Configure logging
log_level = os.getenv('LOGLEVEL', 'INFO')
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'events')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'consumer-group-1')

def create_consumer():
    """Create and return a Kafka consumer."""
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        logger.info(f"Consumer created successfully. Topic: {KAFKA_TOPIC}, Group: {KAFKA_GROUP_ID}")
        return consumer
    except Exception as e:
        logger.error(f"Failed to create consumer: {e}")
        raise

def consume_events(consumer):
    """Consume and process events from Kafka."""
    try:
        logger.info("Starting to consume events...")
        for message in consumer:
            try:
                event = message.value
                logger.info(f"Received event: {event}")
                # Process event here
                process_event(event)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error consuming events: {e}")
        raise

def process_event(event):
    """Process a received event."""
    try:
        event_id = event.get('event_id')
        message = event.get('message')
        value = event.get('value')
        logger.info(f"Processing - ID: {event_id}, Message: {message}, Value: {value}")
    except Exception as e:
        logger.error(f"Failed to process event: {e}")

if __name__ == '__main__':
    logger.info("Starting Consumer Service...")
    
    try:
        consumer = create_consumer()
        consume_events(consumer)
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if consumer:
            consumer.close()
        logger.info("Consumer closed.")
