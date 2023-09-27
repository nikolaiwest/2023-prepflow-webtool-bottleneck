from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        id="app-footer-content",
        children=[
            html.H6("Footer."),
        ],
    )