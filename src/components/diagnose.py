import pandas as pd
import plotly.express as px

from dash import Dash, html
from dash.dcc import Graph
from dash_bootstrap_components import Card, CardBody, Accordion, AccordionItem, Alert

from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


def render(
    app: Dash,
    config_app: dict,
    config_data,
) -> html.Div:
    """
    Render the main content of the bottleneck diagnosis.
    """
    # Check if a data source was selected yet
    if config_data[ConfigName.source] == Options.selection[0]:
        # If initial, display alert
        children = Alert(
            id="alert-detection",
            children="""Please go to "Data Selection" first and pick a data source for the bottleneck analysis.""",
            color="secondary",
        )
    else:
        # Show detection data
        children = get_visualizations(app, config_app, config_data)

    return html.Div(
        id="app-body-content-detection",
        children=[
            # Display all content on a card
            Card(id="app-body-content-detection-card", children=children)
        ],
    )


def get_visualizations(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    return html.Div(
        CardBody(
            children=[
                # Bottleneck frequency
                Accordion(
                    AccordionItem(
                        id="diagnosis-frequency-accordion",
                        children=[
                            Graph(
                                id="diagnosis-plot-grpah",
                                figure=plot_diagnosis(app, config_app, config_data),
                            )
                        ],
                        title="Bottleneck Frequency",
                    ),
                    start_collapsed=False,
                ),
                # Bottleneck severity
                Accordion(
                    AccordionItem(
                        id="diagnosis-severity-accordion",
                        children=[
                            html.Div(
                                "The bottleneck severity is a measurement to assess the degree of effect that one bottleneck situation has on the entire system."
                            )
                        ],
                        title="Bottleneck Severity",
                    ),
                    start_collapsed=True,
                ),
                # bottleneck costs
                Accordion(
                    AccordionItem(
                        id="diagnosis-costs-accordion",
                        children=[
                            html.Div(
                                "The bottleneck cost is a measurement to assess the monetary effect that a stations' bottleneck states have on the entire system."
                            )
                        ],
                        title="Bottleneck Costs",
                    ),
                    start_collapsed=True,
                ),
            ]
        )
    )


def plot_diagnosis(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> CardBody:
    """
    Generate visualizations for bottleneck diagnosis.
    """
    # Load data (later from path)
    df = pd.read_csv("data/active_periods_10000.csv", nrows=10000)
    value_counts = df["bottleneck"].value_counts()
    figure = px.bar(
        x=value_counts.index,
        y=value_counts.values,
        labels={"x": "Bottleneck", "y": "Count"},
    )
    return figure
