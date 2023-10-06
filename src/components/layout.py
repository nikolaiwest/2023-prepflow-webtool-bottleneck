from dash import Dash, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components import Row, Col

from src.page import header, sidebar, body, footer
from src.auxiliaries import storage


def create(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    """
    Create the main layout for the Dash application.

    Parameters:
        app (Dash): The Dash application instance.
        config_app (dict): A dictionary containing configuration parameters for the application.
        config_data (dict): A dictionary containing configuration data for the application.

    Returns:
        html.Div: The main layout of the Dash application, including header, sidebar, body, and footer.

    This function sets up the layout structure for a Dash application, including the initialization of
    configuration values and data objects using dcc.Store components. It also includes the rendering
    of the header, sidebar, body, and footer components.

    Example usage:
        app_layout = create(app, config_app, config_data)
    """
    return html.Div(
        id="app-layout",
        children=[
            # Initialize config values in dcc.Store
            storage.register_config_app(),
            storage.register_config_data(),
            # Initialize data objects as serialized json from df
            storage.register_data_buffer_level(),
            storage.register_data_machine_states(),
            storage.register_data_active_periods(),
            # Set Theme
            get_stylesheet(config_app),
            # Render header
            html.Div(
                id="app-header",
                children=[header.render(app)],
            ),
            # Render sidebar and body on Row
            html.Div(
                id="app-content",
                children=[
                    # Sidebar in column
                    Col(
                        id="app-sidebar",
                        width=3,
                        children=[sidebar.render(app, config_app, config_data)],
                    ),
                    # Body in column
                    Col(
                        id="app-body",
                        width=9,
                        children=[body.render(app, config_app, config_data)],
                    ),
                ],
            ),
            # Render footer
            html.Div(
                id="app-footer",
                children=[footer.render(app)],
            ),
        ],
    )


def get_stylesheet(config_app: dict) -> html.Link:
    """Simple helper function to set the theme according to user selection."""
    if config_app["user_theme"] == "light":
        theme = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/flatly/bootstrap.min.css"
    if config_app["user_theme"] == "dark":
        theme = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/darkly/bootstrap.min.css"
    return html.Link(id="theme-stylesheet", rel="stylesheet", href=theme)
