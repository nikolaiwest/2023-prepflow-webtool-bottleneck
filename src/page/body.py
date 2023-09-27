from dash import Dash, html

from ..components import selection, detection, diagnose, prediction


def render(app: Dash, conf: dict, data: dict) -> html.Div:
    return html.Div(
        id="app-body-content",
        children=[
            get_body(app, conf, data),
        ],
    )


def get_body(app: Dash, conf: dict, data: dict) -> html.Div:
    if conf["navlink"] == "":
        return html.Div("Body is empty")  # place holder
    elif conf["navlink"] == "select":
        return selection.render(app, conf, data)
    elif conf["navlink"] == "detect":
        return detection.render(app, conf)
    elif conf["navlink"] == "diagnose":
        return diagnose.render(app, conf)
    elif conf["navlink"] == "predict":
        return prediction.render(app, conf)
