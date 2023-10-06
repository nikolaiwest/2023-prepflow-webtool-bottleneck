import pandas as pd
import plotly.express as px

from dash import Dash, html
from dash.dcc import RangeSlider, Graph
from dash_bootstrap_components import Card, CardBody, Accordion, AccordionItem, Table


def render(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    return html.Div(
        id="app-body-content-detection",
        children=[
            # Display all content on a card
            Card(
                id="app-body-content-detection-card",
                children=[
                    CardBody(
                        [
                            # render sider
                            html.H4("🔽 Select interval"),
                            html.Div("some text"),
                            render_slider(app, config_app, config_data),
                            html.Hr(),
                            # render bottlenecks
                            render_bottlenecks(app, config_app, config_data),
                            # render buffer level
                            render_buffer_level(app, config_app, config_data),
                            # render active periods
                            render_active_periods(app, config_app, config_data),
                        ]
                    )
                ],
            )
        ],
    )


def render_slider(app, conf, data):
    marks = {i: str(i) for i in range(0, 10001, 1000)}
    return RangeSlider(
        id="slider1",
        min=0,
        max=10000,
        step=100,
        value=[0, 100],
        marks=marks,
    )


def render_bottlenecks(app: Dash, conf: dict, data: dict) -> html.Div:
    """Displays the bottleneck states of the selected data set."""

    # Load data (later from path)
    df = pd.read_csv("data/active_periods_10000.csv", nrows=10000)

    # Get figure
    figure = px.scatter(
        df,
        x="S1",
        y="bottleneck",
    )

    # Return graph as accordion item
    return html.Div(
        Accordion(
            AccordionItem(
                id="app-body-detection-accordion-bottleneck",
                children=Graph(id="detection-figure-bottlenecks", figure=figure),
                title="Bottlenecks",
            ),
            start_collapsed=False,
        )
    )


def render_buffer_level(app: Dash, conf: dict, data: dict) -> html.Div:
    """Displays the buffer level of the selected data set."""

    # Load data (later from path)
    df = pd.read_csv("data/buffer_10000.csv", nrows=10000)

    # Get figure
    figure = px.scatter(
        df,
        x="B1",
        y="t",
    )

    # Return graph as accordion item
    return html.Div(
        Accordion(
            AccordionItem(
                id="app-body-detection-accordion-buffer-level",
                children=Graph(id="detection-figure-buffer-level", figure=figure),
                title="Buffer level",
            ),
            start_collapsed=False,
        )
    )


def render_active_periods(app: Dash, conf: dict, data: dict) -> html.Div:
    """Displays the active periods of the selected data set."""
    # Load data (later from path)
    df = pd.read_csv("data/active_periods_10000.csv", nrows=10000)

    # Get figure
    figure = px.scatter(
        df,
        x="S1",
        y="bottleneck",
    )

    # Return graph as accordion item
    return html.Div(
        Accordion(
            AccordionItem(
                id="app-body-detection-accordion-active-periods",
                children=Graph(id="detection-figure-active-periods", figure=figure),
                title="Active periods",
            ),
            start_collapsed=False,
        )
    )
