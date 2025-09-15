import psycopg2
from app.models.pydantic_models import TimeSeries, DataPoint
from app.core.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

DB_PARAMS = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}

def save_training_data(series_id: str, version: str, ts: TimeSeries):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for dp in ts.data:
        cursor.execute(
            "INSERT INTO training_data (series_id, version, timestamp, value) VALUES (%s,%s,%s,%s)",
            (series_id, version, dp.timestamp, dp.value)
        )
    conn.commit()
    cursor.close()
    conn.close()

def load_training_data(series_id: str, version: str) -> TimeSeries:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, value FROM training_data WHERE series_id=%s AND version=%s ORDER BY timestamp",
        (series_id, version)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return TimeSeries(data=[DataPoint(timestamp=r[0], value=r[1]) for r in rows])

def count_trained_series() -> int:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT series_id) FROM training_data")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result
