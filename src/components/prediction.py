from dash import Dash, html, dcc
from dash_bootstrap_components import Card, CardBody, CardImg, Row, Col, Button

import i18n
from pickle import load
from pandas import DataFrame, read_csv
from plotly.subplots import make_subplots
from plotly.graph_objects import Figure, Scatter

from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


def render(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    """Display all content for bottleneck prediction."""
    return html.Div(
        id="app-body-content-prediction",
        children=[
            # Display card with selection for model parameter
            render_prediction_parameter(app, config_app, config_data),
            # Display the results of the bottleneck prediction
            render_prediction_results(app, config_app, config_data),  # CONDITIONAL
            # Display an example selector (from test) to evaluate the prediction
            render_prediction_examples(app, config_app, config_data),  # CONDITIONAL
        ],
    )


def render_prediction_parameter(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    return Card(
        id="app-body-content-prediction-parameter",
        children=[
            # Card image
            CardImg(src="assets/card_image_prediction.png", top=True),
            # Card body
            CardBody(
                id="app-body-content-prediction-parameter-card",
                children=[
                    Row(
                        [  # Description
                            Col(
                                [
                                    html.H4(i18n.t("prediction.parameter-title")),
                                    html.Div(
                                        i18n.t("prediction.parameter-description")
                                    ),
                                ],
                                width=9,
                            ),
                            # Inputs
                            Col(
                                [
                                    html.H6(i18n.t("prediction.modelling-param1")),
                                    dcc.Input(
                                        id="input-parameter-input-steps",
                                        type="number",
                                        placeholder=60,
                                    ),
                                    html.H6(i18n.t("prediction.modelling-param2")),
                                    dcc.Input(
                                        id="input-parameter-prediction-horizon",
                                        type="number",
                                        placeholder=30,
                                    ),
                                ],
                                width=3,
                            ),
                        ]
                    ),
                    html.Div(
                        id="run-bottleneck-prediction-body",
                        children=Button(
                            id="run-bottleneck-prediction",
                            children=[i18n.t("prediction.button-run-prediction")],
                            style={"width": "100%", "margin-top": "1rem"},
                        ),
                    ),
                ],
            ),
        ],
    )


def render_prediction_results(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    # Load results from file for faster visualization
    df = read_csv("data/results.csv", delimiter=";")

    return Card(
        id="app-body-content-prediction-results",
        children=[
            CardBody(
                id="app-body-content-prediction-results-card",
                children=[
                    # Header
                    html.H4(i18n.t("prediction.results-title")),
                    # Description
                    html.Div(i18n.t("prediction.results-description")),
                    # Plot
                    # Plot
                    dcc.Graph(
                        id="prediction-results-plot",
                        figure=get_results(df, config_app),
                    ),
                ],
            )
        ],
    )


def render_prediction_examples(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    # Read the CSV file

    x_test, y_test, predictions = load_data(path="data/", name="results")

    return Card(
        id="app-body-content-prediction-examples",
        children=[
            CardBody(
                id="app-body-content-prediction-examples-card",
                children=[
                    # Header
                    html.H4(i18n.t("prediction.examples-title")),
                    # Description
                    html.Div(i18n.t("prediction.examples-description")),
                    # Input
                    dcc.Input(
                        id="input-parameter-example-sample",
                        type="number",
                        placeholder=13,
                    ),
                    # Plot
                    dcc.Graph(
                        id="prediction-results-plot",
                        figure=get_example(config_app, x_test, y_test, predictions, 13),
                    ),
                ],
            )
        ],
    )


def get_results(df: DataFrame, config_app: dict) -> Figure:
    # Create the figure object
    fig = Figure()
    fig.update_layout(template=get_template(config_app))
    # Add traces to the figure
    fig.add_trace(
        Scatter(
            x=df["prediction_horizon"],
            y=df["benchmark_random"],
            name="benchmark_random",
        )
    )
    fig.add_trace(
        Scatter(
            x=df["prediction_horizon"],
            y=df["benchmark_naiveM2"],
            name="benchmark_naiveM2",
        )
    )
    fig.add_trace(
        Scatter(
            x=df["prediction_horizon"],
            y=df["benchmark_naiveM4"],
            name="benchmark_naiveM4",
        )
    )
    fig.add_trace(
        Scatter(
            x=df["prediction_horizon"],
            y=df["benchmark_last"],
            name="benchmark_last",
        )
    )
    # fig.add_trace(
    #    Scatter(
    #        x=df["prediction_horizon"],
    #        y=df["prediction_4_60"],
    #        name="prediction_4_60",
    #    )
    # )
    fig.add_trace(
        Scatter(
            x=df["prediction_horizon"],
            y=df["prediction_5_60"],
            name="prediction_5_60",
        )
    )

    # Update layout
    fig.update_layout(
        title="Four Benchmark and two Predictions",
        xaxis_title="Prediction Horizon",
        yaxis_title="Ratio of correct predictions",
        yaxis_tickformat=".4f",  # Format y-axis as float with 2 decimal places
    )

    return fig


def get_example(config_app, x_test, y_test, y_pred, sample_number):
    x_slice = x_test[sample_number]
    y_slice = y_test[sample_number]
    y_pred_slice = y_pred[sample_number]

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        shared_xaxes=True,
        horizontal_spacing=0.05,
        vertical_spacing=0.05,
        subplot_titles=(
            "Buffer level (training)",
            "",
            "Bottlenecks (training)",
            "Truth and predictions",
        ),
    )
    fig.update_layout(template=get_template(config_app))

    # Add a line trace for each column in the slice to the top-left subplot
    col_names = ["B1", "B2", "B3", "B4"]
    for i in range(x_slice.shape[1] - 1):  # subtract 1 to exclude the last column
        fig.add_trace(
            Scatter(y=x_slice[:, i], mode="lines", name=col_names[i]),
            row=1,  # add to first row
            col=1,  # add to first column
        )

    # Add a line trace for the last column in x_test to the bottom-left subplot
    fig.add_trace(
        Scatter(
            y=x_slice[:, -1],  # select the last column
            mode="lines",
            name="Bottlenecks (y_train)",
        ),
        row=2,  # add to second row
        col=1,  # add to first column
    )

    # Add a line trace for y_test to the bottom-right subplot
    fig.add_trace(
        Scatter(
            y=y_slice,
            mode="lines",
            name="Bottlenecks (y_test)",
        ),
        row=2,  # add to second row
        col=2,  # add to second column
    )

    # Add a line trace for the prediction to the bottom-right subplot
    fig.add_trace(
        Scatter(
            y=y_pred_slice,
            mode="lines",
            name="LSTM-Prediction",
        ),
        row=2,  # add to second row
        col=2,  # add to second column
    )

    # Update layout
    fig.update_layout(
        height=800,
        title_text=f"Comparison of prediction and truth for sample {sample_number}",
    )

    fig.update_yaxes(row=1, col=1)
    fig.update_yaxes(
        row=2,
        col=1,
        range=[-0.5, 4.5],
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["S1", "S2", "S3", "S4", "S5"],
    )
    fig.update_yaxes(
        row=2,
        col=2,
        range=[-0.5, 4.5],
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["S1", "S2", "S3", "S4", "S5"],
    )

    return fig


def get_template(config_app: dict) -> str:
    """
    Get the template for visualizations based on the application theme.

    Parameters:
        config_app (dict): A dictionary containing configuration settings for the application.

    Returns:
        str: The template name for visualizations based on the application theme.
    """
    theme_colors = {
        "light": "plotly_white",
        "dark": "plotly_dark",
    }
    return theme_colors[config_app[ConfigName.theme]]


def load_data(path: str, name: str) -> object:
    file = open(f"{path}{name}.pkl", "rb")
    return load(file)
