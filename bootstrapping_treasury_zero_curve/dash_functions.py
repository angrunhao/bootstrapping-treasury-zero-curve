import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

colors = {'background': '#ece5df', 'text': '#404040'}

dateList = spotData.index

animatedButton = [{"args": [None, {"frame": {"duration": 100, "redraw": False},
                                   "fromcurrent": True, "transition": {"duration": 10,
                                                                       "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"},
                  {"args": [[None], {"frame": {"duration": 0, "redraw": False},
                            "mode": "immediate", "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"}]
animatedSlider = [{"active": 0, "yanchor": "top", "xanchor": "left", "currentvalue": {"font": {"size": 20},
                                                                                      "prefix": "Day: ",
                                                                                      "visible": True,
                                                                                      "xanchor": "right"},
                   "transition": {"duration": 10, "easing": "cubic-in-out"}, "pad": {"b": 10, "t": 50},
                   "len": 0.9, "x": 0.1, "y": 0, "steps": [{"args": [[day], {"frame": {"duration": 100, "redraw": False},
                                                                     "mode": "immediate", "transition": {"duration": 10}}],
                                                            "label": day, "method": "animate"} for day in range(1, len(spotData))]}]
animatedFig = go.Figure(data = [go.Scatter(x = spotData.iloc[0].index, y = spotData.iloc[0].values, line = {"color": "rgb(67,67,67)"}, mode = "lines", name = "Spot"),
                                go.Scatter(x = forwardData.iloc[0].index, y = forwardData.iloc[0].values, line = {"color": "rgb(0,38,77)"}, mode = "lines", name = "T+1 Forward"),
                                go.Scatter(x = forwardData.iloc[0].index, y = forwardData.iloc[1].shift(1).values, line = {"color": "rgb(0,64,128)"}, mode = "lines", name = "T+2 Forward")],
                        layout = go.Layout(yaxis = dict(range=[ymin, ymax], autorange=False),
                                           title = "From 2/1/2019 - 31/12/2019", plot_bgcolor = colors['background'],
                                           updatemenus = [dict(type = "buttons", buttons = animatedButton,
                                                               x = 0.1, xanchor = "right", y = 0, yanchor = "top",
                                                               direction = "left", pad = {"r": 10, "t": 87}, showactive = False)],
                                           sliders = animatedSlider),
                        frames = [go.Frame(data = [go.Scatter(x = spotData.iloc[i].index, 
                                                              y = spotData.iloc[i].values,
                                                              line = {"color": "rgb(67,67,67)"}, mode = "lines"),
                                                   go.Scatter(x = forwardData.iloc[i].index, 
                                                              y = forwardData.iloc[i].values,
                                                              line = {"color": "rgb(0,38,77)"}, mode = "lines"),
                                                   go.Scatter(x = forwardData.iloc[i].index, 
                                                              y = forwardData.iloc[i + 1].shift(1).values,
                                                              line = {"color": "rgb(0,64,128)"}, mode = "lines")],
                                           name = i, traces = [0,1,2]) \
                                 for i in range(1, len(spotData) - 1)])


app.layout = html.Div(children = [
        html.H6(children = 'Treasury Curves',
                style = {'textAlign': 'center', 'color': colors['text']}),
        html.Div(children = "Hit the play button to observe curve evolution in 2019.",
                 style = {'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id = "animted-fig", figure = animatedFig),
        html.Br(),
        html.H6(children = 'Snapshots in time',
                style = {'textAlign': 'center', 'color': colors['text']}),
        html.Div(children = "Move the slider to see a snapshot of curves in 2019.",
                 style = {'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id = "treasury-curve"),
        html.Div(id = "date-output"),
        dcc.Slider(id = "date-slider-input", min = 0, max = len(dateList) - 1,
                   value = 0, step = 1)])

@app.callback([Output(component_id = "date-output", component_property = "children"),
               Output(component_id = "treasury-curve", component_property = "figure")],
              [Input(component_id = "date-slider-input", component_property = "value")])
def plot_output(date_slider_input):
    
    filtered_df = pd.concat([spotData.loc[dateList[date_slider_input]], 
                             forwardData.loc[dateList[date_slider_input]],
                             forwardData.loc[dateList[date_slider_input + 1]].shift(1)], 
                            axis = 1)
    filtered_df.columns = ["spot", "forward1", "forward2"]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = filtered_df.index, y = filtered_df["spot"],
                    mode = "lines+markers", line = {"color": "rgb(67,67,67)"},
                    name = "Spot"))
    fig.add_trace(go.Scatter(x = filtered_df.index, y = filtered_df["forward1"],
                    mode = "lines+markers", line = {"color": "rgb(0,38,77)"},
                    name = "T+1 Forward"))
    fig.add_trace(go.Scatter(x = filtered_df.index, y = filtered_df["forward2"],
                    mode = "lines+markers", line = {"color": "rgb(0,64,128)"},
                    name = "T+2 Forward"))
    fig.update_layout(plot_bgcolor = colors['background'],
                      #paper_bgcolor = colors['background'],
                      font_color = colors['text'],
                      xaxis_title = "Tenor (years)",
                      yaxis_title = "Yield %")
    fig.update_yaxes(range=[ymin, ymax])
    fig.update_layout(transition_duration=0)
    
    return "Slider Date: {}".format(dateList[date_slider_input]), fig

if __name__ == '__main__':
    app.run_server(debug=False)
