from kafka import KafkaProducer
import json
import os
import time
import logging
from datetime import datetime

# Configure logging
log_level = os.getenv('LOGLEVEL', 'INFO')
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'events')

def create_producer():
    """Create and return a Kafka producer."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        logger.info(f"Producer created successfully. Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        logger.error(f"Failed to create producer: {e}")
        raise

def produce_events(producer, topic, count=10):
    """Produce sample events to Kafka."""
    try:
        for i in range(count):
            event = {
                'event_id': i,
                'timestamp': datetime.now().isoformat(),
                'message': f'Sample event #{i}',
                'value': i * 100
            }
            
            future = producer.send(topic, value=event)
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Event {i} sent to topic '{topic}' partition {record_metadata.partition} at offset {record_metadata.offset}")
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Failed to produce events: {e}")
        raise

if __name__ == '__main__':
    logger.info("Starting Producer Service...")
    
    try:
        producer = create_producer()
        
        # Produce events continuously
        while True:
            logger.info("Producing batch of events...")
            produce_events(producer, KAFKA_TOPIC, count=5)
            logger.info("Batch complete. Waiting 30 seconds before next batch...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if producer:
            producer.close()
        logger.info("Producer closed.")
