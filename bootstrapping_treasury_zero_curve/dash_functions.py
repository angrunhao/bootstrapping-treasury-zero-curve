import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

colors = {'background': '#f1e6da', 'text': '#404040'}

dateList = spotData.index

app.layout = html.Div(children = [
        html.H6(children = 'Treasury Curves',
                style = {'textAlign': 'center', 'color': colors['text']}),
        html.Div(children = "Move the slider to see the evolution of curves through time.",
                 style = {'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id = "treasury-curve"),
        html.Label("Slider"),
        dcc.Slider(id = "date-slider-input", min = 0, max = len(dateList) - 1,
                   value = 0, step = 1),
        html.Div(id = "date-output")
])

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
                    mode = "lines+markers",
                    name = "Spot"))
    fig.add_trace(go.Scatter(x = filtered_df.index, y = filtered_df["forward1"],
                    mode = "lines+markers",
                    name = "T+1 Forward"))
    fig.add_trace(go.Scatter(x = filtered_df.index, y = filtered_df["forward2"],
                    mode = "lines+markers",
                    name = "T+2 Forward"))
    fig.update_layout(plot_bgcolor = colors['background'],
                      paper_bgcolor = colors['background'],
                      font_color = colors['text'],
                      xaxis_title = "Tenor (years)",
                      yaxis_title = "Yield %")
    fig.update_yaxes(range=[ymin, ymax])
    fig.update_layout(transition_duration=0)
    
    return "Date: {}".format(dateList[date_slider_input]), fig

if __name__ == '__main__':
    app.run_server(debug=False)
