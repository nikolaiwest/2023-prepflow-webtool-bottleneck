from dash import Dash, html, dcc, callback_context
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import random

# Create a Dash app
app = Dash(__name__)

# Generate some random data for the scatter plots

# Generate some random data for the scatter plots
random.seed(42)
data1 = {
    "x": [random.randint(1, 100) for _ in range(100)],
    "y": [random.randint(1, 100) for _ in range(100)],
}
df1 = pd.DataFrame(data1)
data2 = {
    "x": [random.randint(1, 100) for _ in range(100)],
    "y": [random.randint(1, 100) for _ in range(100)],
}
df2 = pd.DataFrame(data2)
data3 = {
    "x": [random.randint(1, 100) for _ in range(100)],
    "y": [random.randint(1, 100) for _ in range(100)],
}
df3 = pd.DataFrame(data3)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Linked Scatter Plots"),
        dcc.Graph(id="scatter-plot-1", config={"displayModeBar": False}),
        dcc.Graph(id="scatter-plot-2", config={"displayModeBar": False}),
        dcc.Graph(id="scatter-plot-3", config={"displayModeBar": False}),
    ]
)


# Define callback function to update all the plots when any of them is zoomed
@app.callback(
    [
        Output("scatter-plot-1", "figure"),
        Output("scatter-plot-2", "figure"),
        Output("scatter-plot-3", "figure"),
    ],
    [
        Input("scatter-plot-1", "relayoutData"),
        Input("scatter-plot-2", "relayoutData"),
        Input("scatter-plot-3", "relayoutData"),
    ],
    prevent_initial_call=True,
)
def update_plots(relayoutData1, relayoutData2, relayoutData3):
    selection = callback_context.triggered[0]["prop_id"].split(".")[0]

    # Determine the x-axis range from any of the scatter plots
    try:
        xaxis_range = None
        if selection == "scatter-plot-1":
            print("1")
            x1 = relayoutData1["xaxis.range[0]"]
            x2 = relayoutData1["xaxis.range[1]"]
            xaxis_range = [x1, x2]
        elif selection == "scatter-plot-2":
            print("1")
            x1 = relayoutData2["xaxis.range[0]"]
            x2 = relayoutData2["xaxis.range[1]"]
            xaxis_range = [x1, x2]
        elif selection == "scatter-plot-3":
            print("1")
            x1 = relayoutData3["xaxis.range[0]"]
            x2 = relayoutData3["xaxis.range[1]"]
            xaxis_range = [x1, x2]
        print(xaxis_range)

        # Create new figures for all scatter plots with the same x-axis range
        fig1 = px.scatter(
            df1, x="x", y="y", title="Scatter Plot 1", range_x=xaxis_range
        )
        fig2 = px.scatter(
            df2, x="x", y="y", title="Scatter Plot 2", range_x=xaxis_range
        )
        fig3 = px.scatter(
            df3, x="x", y="y", title="Scatter Plot 3", range_x=xaxis_range
        )

    except KeyError:
        # Create new figures for all scatter plots with the same x-axis range
        fig1 = px.scatter(df1, x="x", y="y", title="Scatter Plot 1")
        fig2 = px.scatter(df2, x="x", y="y", title="Scatter Plot 2")
        fig3 = px.scatter(df3, x="x", y="y", title="Scatter Plot 3")

    return fig1, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug=True)
