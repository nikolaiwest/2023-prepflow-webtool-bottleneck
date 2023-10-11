import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html
from dash.dcc import Graph
from dash_bootstrap_components import Card, CardBody, Accordion, AccordionItem, Alert

from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


class DetectionName:
    fig_bottleneck = "detection-figure-bottlenecks"
    acc_bottleneck = "detection-accordion-bottleneck"
    fig_buffer_level = "detection-figure-buffer-level"
    acc_buffer_level = "detection-accordion-buffer-level"
    fig_active_periods = "detection-figure-active-periods"
    acc_active_periods = "detection-accordion-active-periods"


def render(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    """
    Render the main content of the bottleneck detection.

    This function generates the main content to be displayed in the Dash web application for
    bottleneck detection. It checks if a data source has been selected and renders either
    an alert message to prompt the user to select a data source or visualizations based on
    the selected data source.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration settings for the application.
        config_data (dict): A dictionary containing configuration data, including the selected data source.

    Returns:
        html.Div: A Dash HTML div element containing the rendered content for the bottleneck analysis.

    Notes:
        - If the selected data source is the initial default option, an alert message is displayed
          to instruct the user to navigate to the "Data Selection" section and choose a data source.
        - If a valid data source is selected, the visualizations are obtained using the
          `get_detection_visualizations` function and displayed within a card.

    Example:
        To render the main content for the bottleneck analysis, you can call this function as follows:
        ```
        main_content = render(app_instance, config_app_settings, config_data_settings)
        ```
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
) -> CardBody:
    """
    Generate visualizations for bottleneck analysis.

    This function generates visualizations for bottleneck analysis, including plots for
    bottleneck states, buffer levels, and active periods. Each visualization is encapsulated
    within an AccordionItem and collectively displayed within a CardBody.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration settings for the application.
        config_data (dict): A dictionary containing configuration data.

    Returns:
        CardBody: A Dash Bootstrap Components CardBody containing the rendered visualizations.

    Example:
        To generate bottleneck analysis visualizations, you can call this function as follows:
        ```
        visualizations = get_detection_visualizations(app_instance, config_app_settings, config_data_settings)
        ```
    """

    # Return graph as accordion item
    return html.Div(
        CardBody(
            children=[
                # Render plot with current bottlenecks
                Accordion(
                    AccordionItem(
                        id=DetectionName.acc_bottleneck,
                        children=Graph(DetectionName.fig_bottleneck),
                        title="Bottlenecks",
                    ),
                    start_collapsed=False,
                ),
                # Render plot with buffer level
                Accordion(
                    AccordionItem(
                        id=DetectionName.acc_buffer_level,
                        children=Graph(DetectionName.fig_buffer_level),
                        title="Buffer level",
                    ),
                    start_collapsed=True,
                ),
                # Render plot with active periods
                Accordion(
                    AccordionItem(
                        id=DetectionName.acc_active_periods,
                        children=Graph(DetectionName.fig_active_periods),
                        title="Active periods",
                    ),
                    start_collapsed=True,
                ),
            ],
        )
    )


def plot_bottlenecks(
    df: pd.DataFrame,
    config_app: dict,
    xaxis_range: list = None,
):
    """
    Displays the bottleneck states of the selected data set.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration settings for the application.
        config_data (dict): A dictionary containing configuration data.
        xaxis_range (list, optional): The range of x-axis values for the plot. Default is None.
    """
    color_dict = {category: i for i, category in enumerate(df[df.columns[-1]].unique())}

    # Get figure from active periods
    figure = px.scatter(
        template=get_template(config_app),
        range_x=xaxis_range,
    )
    figure.add_trace(
        go.Scatter(
            x=df[df.columns[0]],  # time
            y=df[df.columns[-1]],  # bottlenecks
            mode="markers",
            marker=dict(
                size=10,
                color=df[df.columns[-1]].map(color_dict),
                colorscale="Portland",
            ),
            name="Bottlenecks",
        )
    )

    # Update ax labels
    figure.update_xaxes(title_text="Simulation time [t]")
    figure.update_yaxes(title_text="Current bottleneck station")

    # Return graph as accordion item
    return figure


def plot_buffer_level(
    df: pd.DataFrame,
    config_app: dict,
    xaxis_range: list = None,
):
    """
    Displays the buffer level of the selected data set.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration settings for the application.
        config_data (dict): A dictionary containing configuration data.
        xaxis_range (list, optional): The range of x-axis values for the plot. Default is None.
    """
    # Load data (later from path)
    df = pd.read_csv("data/buffer_10000.csv", nrows=10000)

    # Get figure from active periods
    figure = px.scatter(
        template=get_template(config_app),
        range_x=xaxis_range,
    )
    for col in df.columns[2:-1]:
        figure.add_trace(
            go.Scatter(
                x=df[df.columns[0]],  # time
                y=df[col],
                mode="lines",
                name=col,
            )
        )

    # Update ax labels
    figure.update_xaxes(title_text="Simulation time [t]")
    figure.update_yaxes(title_text="Buffer level [parts]")

    # Return graph as accordion item
    return figure


def plot_active_periods(
    df: pd.DataFrame,
    config_app: dict,
    xaxis_range: list = None,
):
    """
    Displays the active periods of the selected data set.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration settings for the application.
        config_data (dict): A dictionary containing configuration data.
        xaxis_range (list, optional): The range of x-axis values for the plot. Default is None.
    """

    # Get figure from active periods
    figure = px.scatter(
        template=get_template(config_app),
        range_x=xaxis_range,
    )
    for col in df.columns[1:-1]:
        figure.add_trace(
            go.Scatter(
                x=df[df.columns[0]],  # time
                y=df[col],
                mode="lines",
                name=col,
            )
        )

    # Update ax labels
    figure.update_xaxes(title_text="Simulation time [t]")
    figure.update_yaxes(title_text="Current active period")

    # Return graph as accordion item
    return figure


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
