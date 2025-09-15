# Time Series Anomaly Detection API

A FastAPI-based microservice for detecting anomalies in time series data. The API provides endpoints for training models on historical data and making real-time predictions with comprehensive monitoring and tracking capabilities.

## Features

- **Time Series Anomaly Detection**: Train models on historical data and detect anomalies in real-time using a statistical approach (mean ± 3σ threshold)
- **Model Versioning**: Support for multiple model versions per time series with automatic versioning
- **Visualization Tool**: Plot training data with anomaly detection boundaries (optional enhancement)
- **Redis Caching**: Fast model storage and retrieval using Redis
- **PostgreSQL Storage**: Persistent storage for training data and metadata
- **MLflow Integration**: Experiment tracking and model management
- **Prometheus Metrics**: Real-time monitoring and performance metrics
- **Grafana Dashboards**: Visual monitoring of API performance
- **Containerized Deployment**: Full Docker Compose setup
- **Concurrent Processing**: Handle multiple training and prediction requests simultaneously

## Architecture

The system consists of the following components:

- **FastAPI Application**: Core API service
- **Redis**: Model caching and session storage
- **PostgreSQL**: Training data and metadata persistence
- **MLflow**: Model versioning and experiment tracking
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- At least 4GB of available RAM
- Ports 3000, 5000, 5432, 6379, 8000, 9090 available

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd anomaly-detection-api
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Verify deployment**
   ```bash
   # Check if all services are running
   docker-compose ps
   
   # Test the health check endpoint
   curl http://localhost:8000/healthcheck
   ```

### Service Endpoints

Once deployed, the following services will be available:

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Metrics**: http://localhost:8000/metrics

## API Usage

### Training a Model

Train an anomaly detection model on historical time series data:

**Endpoint**: `POST /fit/{series_id}`

**Sample Request**:
```bash
curl -X POST "http://localhost:8000/fit/sensor_001" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamps": [1640995200, 1640998800, 1641002400, 1641006000, 1641009600],
    "values": [23.5, 24.1, 22.8, 25.3, 23.9]
  }'
```

**Sample Response**:
```json
{
  "series_id": "sensor_001",
  "version": "v1.0.0",
  "points_used": 5
}
```

### Making Predictions

Detect anomalies in real-time data points:

**Endpoint**: `POST /predict/{series_id}`

**Sample Request** (using latest model version):
```bash
curl -X POST "http://localhost:8000/predict/sensor_001" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "1641013200",
    "value": 45.2
  }'
```

**Sample Request** (using specific model version):
```bash
curl -X POST "http://localhost:8000/predict/sensor_001?version=v1.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "1641013200",
    "value": 45.2
  }'
```

**Sample Response**:
```json
{
  "anomaly": true,
  "model_version": "v1.0.0"
}
```

### Health Check

Check the system status and performance metrics:

**Endpoint**: `GET /healthcheck`

**Sample Request**:
```bash
curl http://localhost:8000/healthcheck
```

**Sample Response**:
```json
{
  "series_trained": 5,
  "inference_latency_ms": {
    "avg": 12.5,
    "p95": 23.1
  },
  "training_latency_ms": {
    "avg": 156.7,
    "p95": 287.3
  }
}
```

### Visualization

Generate plots showing training data and anomaly detection boundaries:

**Endpoint**: `GET /plot`

**Sample Request**:
```bash
curl "http://localhost:8000/plot?series_id=sensor_001&version=v1.0.0"
```

This endpoint returns a visualization of:
- Historical training data points
- Anomaly detection thresholds (mean ± 3σ)
- Model boundaries and statistics
- Time series trends and patterns

The plot helps visualize how the model learned from the training data and what constitutes normal vs. anomalous behavior for the specific time series.

## Algorithm Details

The system uses a statistical approach for anomaly detection:

- **Training**: Calculates mean (μ) and standard deviation (σ) from historical data
- **Prediction**: Classifies a point as anomalous if: `value > μ + 3σ`
- **Model Type**: Simple statistical model optimized for real-time inference
- **Threshold**: 3-sigma rule (99.7% of normal data falls within this range)

This approach provides fast, interpretable anomaly detection suitable for various time series applications including sensor monitoring, system metrics, and business KPIs.

### Training Data
- **timestamps**: Array of Unix timestamps (integers)
- **values**: Array of numerical values corresponding to each timestamp
- Arrays must be of equal length

### Prediction Data
- **timestamp**: Unix timestamp as string
- **value**: Numerical value to check for anomaly

## Model Versioning

The API supports multiple model versions per time series:

- Each training operation creates a new model version
- Predictions can use the latest version (default) or specify a version
- Model versions are automatically managed and stored in Redis
- Training metadata is tracked in MLflow

## Monitoring

### Grafana Dashboards

Access Grafana at http://localhost:3000 (admin/admin) to view:
- Training request metrics
- Prediction request metrics  
- Average response times
- System performance indicators

### Prometheus Metrics

Available metrics at http://localhost:8000/metrics:
- `train_requests_total`: Total training requests
- `predict_requests_total`: Total prediction requests
- `train_duration_seconds`: Training duration histogram
- `predict_duration_seconds`: Prediction duration histogram

### MLflow Tracking

View experiment tracking at http://localhost:5000:
- Model parameters and metrics
- Training duration and performance
- Model artifacts and versions

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 5000, 5432, 6379, 8000, 9090 are available
2. **Memory issues**: Ensure at least 4GB RAM is available
3. **Model not found**: Train a model before making predictions

### Logs

View service logs:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs api
docker-compose logs redis
docker-compose logs postgres
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

## Development

### Project Structure

```
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── training.py
│   │       ├── prediction.py
│   │       └── plot.py
│   ├── models/
│   │   ├── anomaly_model.py
│   │   └── pydantic_models.py
│   ├── storage/
│   │   └── redis_storage.py
│   ├── db/
│   │   └── postgres.py
│   ├── core/
│   │   └── metrics.py
│   └── utils/
│       └── plotting.py
├── grafana/
│   └── provisioning/
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml
└── README.md
```

### Environment Variables

The following environment variables are configurable:

- `REDIS_HOST`: Redis hostname (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `POSTGRES_HOST`: PostgreSQL hostname (default: postgres)
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `POSTGRES_DB`: Database name (default: ml)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `MLFLOW_TRACKING_URI`: MLflow tracking URI (default: http://mlflow:5000)

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please check the logs and ensure all services are running correctly. The API documentation is available at http://localhost:8000/docs for interactive testing.