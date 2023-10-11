from dash import Dash, html, dcc
from dash_bootstrap_components import Card, CardBody

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
            CardBody(
                id="app-body-content-prediction-parameter-card",
                children=[
                    html.H4("Select prediction parameter"),
                    html.Div("PARAMETER"),
                ],
            )
        ],
    )


def render_prediction_results(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    return Card(
        id="app-body-content-prediction-results",
        children=[
            CardBody(
                id="app-body-content-prediction-results-card",
                children=[
                    html.H4("Results of the bottleneck prediction"),
                    html.Div("RESULTS"),
                ],
            )
        ],
    )


def render_prediction_examples(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    return Card(
        id="app-body-content-prediction-examples",
        children=[
            CardBody(
                id="app-body-content-prediction-examples-card",
                children=[html.H4("Select prediction examples"), html.Div("EXAMPLE")],
            )
        ],
    )
