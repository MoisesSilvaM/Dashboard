import plotly.express as px
import plotly.graph_objects as go
from src.const import detectors_out_to_table
from src.dash4 import generate_visualizations as generate_visualizations4


def generate_visualizations(dO, dR, VO, VR, traffic, vehicle):
    dfO = detectors_out_to_table(dO, traffic)
    dfR = detectors_out_to_table(dR, traffic)
    dfO = dfO.fillna(0)
    dfR = dfR.fillna(0)
    dfO_aligned, dfR_aligned = dfO.align(dfR, fill_value=0)

    time_intervals = dO['interval_id'].unique()
    fig1 = generate_figure1(dfO_aligned, dfR_aligned, time_intervals[-1], traffic)
    fig2 = generate_figure2(dfO_aligned, dfR_aligned, traffic)
    fig3 = generate_figure3(dfO_aligned, dfR_aligned, time_intervals[-1], traffic)
    fig4 = generate_visualizations4(VO, VR, vehicle)
    return fig1, fig2, fig3, fig4


def generate_figure1(dfO, dfR, name, traffic):
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
    fig_bar_mean_votes.add_trace(go.Histogram(x=dfO[name], name="Without deviations"))
    fig_bar_mean_votes.add_trace(go.Histogram(x=dfR[name], name="With deviations"))
    fig_bar_mean_votes.update_layout(
        title_text='Distribution of the results for time interval ' + name + ' in terms of ' + traffic,  # title of plot
        xaxis_title_text=inf,  # xaxis label
        yaxis_title_text='Number of vehicles',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    fig_bar_mean_votes.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_bar_mean_votes


def generate_figure2(dfO, dfR, traffic):
    inf = ''
    if traffic == "density":
        inf = "Difference in terms of vehicle density (veh/km)"
    elif traffic == "occupancy":
        inf = "Difference in terms of occupancy (%)"
    elif traffic == "timeLoss":
        inf = "Difference in terms of time loss (s)"
    elif traffic == "traveltime":
        inf = "Difference in terms of travel time (s)"
    elif traffic == "waitingTime":
        inf = "Difference in terms of waiting time (s)"
    elif traffic == "speed":
        inf = "Difference in terms of average speed (m/s)"
    elif traffic == "speedRelative":
        inf = "Difference in terms of speed relative (average speed / speed limit)"
    elif traffic == "sampledSeconds":
        inf = "Difference in terms of sampled seconds (veh/s)"
    df = dfR - dfO
    fig2 = px.strip(df, orientation="h")
    fig2.update_layout(template='plotly_dark', font=dict(color='yellow'))
    fig2.update_layout(
        title_text='Difference of streets with and without deviations in terms of ' + traffic,  # title of plot
        xaxis_title_text=inf,  # xaxis label
        yaxis_title_text='Time intervals',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    return fig2


def generate_figure3(dfO, dfR, name, traffic):
    dO = dfO.loc[:,
         [name]]

    dR = dfR.loc[:,
         [name]]
    df = dO.merge(dR, left_index=True, right_index=True, how="left")
    value_x = name + '_x'
    value_y = name + '_y'
    df['diff'] = df[value_y].sub(df[value_x], axis=0)
    df = df.sort_values(by=['diff'], ascending=False).head(15)
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
    fig_bar = px.bar(df, y='diff', x=df.index, orientation='v',
                     color='diff', text='diff',
                     title='15 most impacted steets in terms of ' + inf + ' comparing with and without deviations for time interval ' + name,
                     labels={'id': 'Id of the street', 'diff': 'Difference'}
                     )
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar.update_layout(template='plotly_dark', font=dict(color='yellow'))
    return fig_bar
