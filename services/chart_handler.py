import plotly.graph_objects as go
from plotly.subplots import make_subplots

import os

CHART_FOLDER = "latency_charts"
os.makedirs(CHART_FOLDER, exist_ok=True)

def plot_latency(latency_data: list[list[float]], name: str = "latency_plot"):
    if not latency_data:
        return
    # Transpose
    eou, llm, tts, total = map(list, zip(*latency_data))

    fig = go.Figure()

    fig = make_subplots(rows=2, cols=2,
        subplot_titles=["EOU Time", "LLM TTFT", "TTS TTFB", "Total Latency"])

    fig.add_trace(go.Scatter(y=eou, name="EOU"), row=1, col=1)
    fig.add_trace(go.Scatter(y=llm, name="LLM TTFT"), row=1, col=2)
    fig.add_trace(go.Scatter(y=tts, name="TTS TTFB"), row=2, col=1)
    fig.add_trace(go.Scatter(y=total, name="Total"), row=2, col=2)

    fig.update_layout(height=800, width=1000, title_text="Latency Metrics Over Time")

    idx = len(latency_data)
    fname = os.path.join(CHART_FOLDER, f"{name}_{idx:04d}.png")
    fig.write_image(fname, scale=3)