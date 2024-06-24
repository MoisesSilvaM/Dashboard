import plotly.express as px


# Define visualizations
def generate_visualizations(VO, VR, traffic):
    traffic_indicator = "tripinfo_" + traffic
    VO = VO.loc[:,
         ['tripinfo_id',
          traffic_indicator]]

    VR = VR.loc[:,
         ['tripinfo_id',
          traffic_indicator]]

    fig_bar_language = generate_fig1(VO, VR, traffic, traffic_indicator)
    return fig_bar_language


def generate_fig1(VO, VR, traffic, traffic_indicator):
    VO['id'] = VO['tripinfo_id']
    VO['id'] = VO['id'].astype(str)
    VO = VO.set_index('tripinfo_id')
    VR = VR.set_index('tripinfo_id')
    df = VO.merge(VR, left_index=True, right_index=True, how="left")
    value_x = traffic_indicator + '_x'
    value_y = traffic_indicator + '_y'

    df['diff'] = df[value_y].sub(df[value_x], axis=0)
    df["diff"] = df["diff"].fillna(value=0)
    df[value_x] = df[value_x].fillna(value=0)
    df[value_y] = df[value_y].fillna(value=0)

    df = df.sort_values(by=['diff'], ascending=False).head(15)
    value = ''
    if traffic == 'duration':
        value = 'duration (s)'
    if traffic == 'timeLoss':
        value = 'time loss (s)'
    if traffic == 'waitingTime':
        value = 'waiting time (s)'
    fig_bar = px.bar(df, y='diff', x='id', orientation='v',
                     color='diff', text='diff',
                     title='15 most impacted vehicles in terms of ' + value + ' comparing with and without deviations',
                     labels={'id': 'Id of the vehicles', 'diff': 'Difference in seconds'}
                     )
    if traffic == 'routeLength':
        value = 'route length (m)'
        fig_bar = px.bar(df, y='diff', x='id', orientation='v',
                         color='diff', text='diff',
                         title='15 most impacted vehicles in terms of ' + value + ' comparing with and without deviations',
                         labels={'id': 'Id of the vehicles', 'diff': 'Difference in meters'}
                         )

    fig_bar.update_traces(texttemplate='%{text}(s)', textposition='outside')
    if traffic == 'routeLength':
        fig_bar.update_traces(texttemplate='%{text}(m)', textposition='outside')

    fig_bar.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_bar
