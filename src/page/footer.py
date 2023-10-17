from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        id="app-footer-content",
        children=[
            html.H6("RIF Institut for Research and Transfer e.V."),
            html.H6("Förderzeichen: 21595"),
        ],
        style={"margin": "0.5rem"},
    )
