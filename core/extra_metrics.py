# core/extra_metrics.py
import plotly.graph_objs as go


def extra_metrics_graph(signals: dict, mc: dict, rl: dict) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="RL Reward",
            x=["RL Score"],
            y=[rl["rl_reward"]],
            marker=dict(opacity=0.7),
        )
    )

    fig.add_trace(
        go.Box(
            name="Monte Carlo Spread",
            q1=[mc["mc_p05"]],
            median=[mc["mc_mean"]],
            q3=[mc["mc_p95"]],
            boxpoints="outliers",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        font=dict(size=10, color="#e8f5ff"),
        margin=dict(l=20, r=10, t=12, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="rgba(255,255,255,0.08)",
            font_size=10,
            font_color="#e8f5ff",
            bordercolor="rgba(0,242,255,0.35)",
        )
    )

    fig.update_traces(
        hovertemplate="%{x}<br>%{y}<extra></extra>",
        hoverlabel=dict(
            bgcolor="rgba(255,255,255,0.10)",
            bordercolor="rgba(0,242,255,0.65)",
            font_size=11,
        ),
    )

    fig.update_layout(
        hoverdistance=20,
        spikedistance=12,
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1.4,
            spikecolor="rgba(0,242,255,0.85)",
        ),
        yaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1.4,
            spikecolor="rgba(255,0,212,0.85)",
        ),
    )
    return fig
