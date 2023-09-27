from dash import Dash, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components import Row, Col

from src.page import header, sidebar, body, footer
from src.auxiliaries import storage


def create(app: Dash, conf: dict, data: dict) -> html.Div:
    return html.Div(
        id="app-layout",
        children=[
            # Initialize stores
            storage.register_user_config(),
            storage.register_data_source(),
            # Set Theme
            get_stylesheet(conf),
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
                        id="app-sidebar", width=3, children=[sidebar.render(app, conf)]
                    ),
                    # Body in column
                    Col(
                        id="app-body", width=9, children=[body.render(app, conf, data)]
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


def get_stylesheet(conf: dict) -> html.Link:
    if conf["theme"] == "light":
        theme = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/flatly/bootstrap.min.css"
    if conf["theme"] == "dark":
        theme = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/darkly/bootstrap.min.css"

    return html.Link(id="theme-stylesheet", rel="stylesheet", href=theme)
