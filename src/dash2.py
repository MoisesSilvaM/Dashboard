import plotly.express as px
import plotly.graph_objects as go
import os
from src.const import detectors_out_to_table


def generate_visualizations(dO, dR, traffic):
    dfO = detectors_out_to_table(dO, traffic)
    dfR = detectors_out_to_table(dR, traffic)
    dfO = dfO.fillna(0)
    dfR = dfR.fillna(0)
    dfO_aligned, dfR_aligned = dfO.align(dfR, fill_value=0)

    time_intervals = dO['interval_id'].unique()
    figures = []
    for i, data in enumerate(time_intervals):
        # title = f"Figure {i + 1}"  # Customize title based on data or your logic
        figures.append(generate_figure(dfO_aligned[data], dfR_aligned[data], data, traffic))
    return figures


def generate_figure(dfO, dfR, name, traffic):
    inf = ''
    if traffic == "density":
        inf = "Vehicle density (veh/km)"
    elif traffic == "occupancy":
        inf = "Occupancy (%)"
    elif traffic == "timeLoss":
        inf = "Time loss due to driving slower than desired (s)"
    elif traffic == "traveltime":
        inf = "Travel time (s)"
    elif traffic == "waitingTime":
        inf = "Waiting time (s)"
    elif traffic == "speed":
        inf = "Average speed (m/s)"
    elif traffic == "speedRelative":
        inf = "Speed relative (average speed / speed limit)"
    elif traffic == "sampledSeconds":
        inf = "Sampled seconds (veh/s)"
    fig_bar_mean_votes = go.Figure()
    fig_bar_mean_votes.add_trace(go.Histogram(x=dfO, name="Without deviations"))
    fig_bar_mean_votes.add_trace(go.Histogram(x=dfR, name="With deviations"))
    fig_bar_mean_votes.update_layout(
        title_text='Distribution of the results for time interval ' + name + 'in terms of ' + traffic,  # title of plot
        xaxis_title_text=inf,  # xaxis label
        yaxis_title_text='Number of vehicles',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    fig_bar_mean_votes.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_bar_mean_votes
