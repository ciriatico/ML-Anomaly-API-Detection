from prometheus_client import Counter, Histogram

# Training metrics
train_requests = Counter("train_requests_total", "Total number of training requests")
train_duration = Histogram("train_duration_seconds", "Time spent training models")

# Prediction metrics
predict_requests = Counter("predict_requests_total", "Total number of prediction requests")
predict_duration = Histogram("predict_duration_seconds", "Time spent on prediction")
