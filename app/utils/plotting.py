import matplotlib.pyplot as plt
import io
from fastapi import Response

def plot_timeseries(ts, model, series_id, version) -> Response:
    timestamps = [dp.timestamp for dp in ts.data]
    values = [dp.value for dp in ts.data]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(timestamps, values, label="Training Data", marker="o")
    ax.axhline(model.mean, color="green", linestyle="--", label="Mean")
    ax.axhline(model.mean + 3 * model.std, color="red", linestyle="--", label="Mean+3σ")
    ax.set_title(f"Series: {series_id}, Version: {version}")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Value")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")
