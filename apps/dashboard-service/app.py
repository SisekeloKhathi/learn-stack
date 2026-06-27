from flask import Flask, render_template_string, jsonify
from kafka import KafkaConsumer
import json
import os
import logging
import threading
from collections import deque
from datetime import datetime

# Configure logging
log_level = os.getenv('LOGLEVEL', 'INFO')
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'events')

# Event storage (keep last N events)
event_buffer = deque(maxlen=100)
is_running = True

def consume_and_store_events():
    """Consume events and store them in memory."""
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id='dashboard-consumer',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        logger.info(f"Dashboard consumer connected to {KAFKA_TOPIC}")
        
        for message in consumer:
            if not is_running:
                break
            try:
                event = message.value
                event['received_at'] = datetime.now().isoformat()
                event_buffer.append(event)
                logger.debug(f"Stored event: {event}")
            except Exception as e:
                logger.error(f"Error storing event: {e}")
    except Exception as e:
        logger.error(f"Consumer error: {e}")

@app.route('/')
def index():
    """Serve the dashboard."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kafka Platform Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            h1 { color: #333; }
            .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .status { padding: 10px; background-color: #e8f5e9; border-radius: 3px; margin: 10px 0; }
            .error { background-color: #ffebee; }
        </style>
        <script>
            function refreshEvents() {
                fetch('/api/events')
                    .then(response => response.json())
                    .then(data => {
                        const tbody = document.getElementById('events-tbody');
                        tbody.innerHTML = '';
                        data.events.forEach(event => {
                            const row = tbody.insertRow();
                            row.insertCell(0).textContent = event.event_id;
                            row.insertCell(1).textContent = event.message;
                            row.insertCell(2).textContent = event.value;
                            row.insertCell(3).textContent = event.timestamp;
                        });
                        document.getElementById('count').textContent = data.count;
                    })
                    .catch(error => console.error('Error:', error));
            }
            
            setInterval(refreshEvents, 5000);
            window.onload = refreshEvents;
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Kafka Platform Dashboard</h1>
            <div class="status">
                <strong>Topic:</strong> {topic}<br>
                <strong>Bootstrap Servers:</strong> {bootstrap_servers}<br>
                <strong>Events Received:</strong> <span id="count">0</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Event ID</th>
                        <th>Message</th>
                        <th>Value</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody id="events-tbody">
                    <tr><td colspan="4">Loading...</td></tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """.format(topic=KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    return render_template_string(html)

@app.route('/api/events')
def get_events():
    """API endpoint to get recent events."""
    return jsonify({
        'events': list(event_buffer),
        'count': len(event_buffer),
        'topic': KAFKA_TOPIC
    })

@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    logger.info("Starting Dashboard Service...")
    
    # Start consumer thread
    consumer_thread = threading.Thread(target=consume_and_store_events, daemon=True)
    consumer_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
        is_running = False
    finally:
        logger.info("Dashboard closed.")
