from dash import Dash, html


def render(app: Dash, conf: dict) -> html.Div:
    return html.Div(
        id="app-body-content-diagnosis",
        children=[""],
    )
