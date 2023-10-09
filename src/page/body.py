from dash import Dash, html
from dash_bootstrap_components import Alert

from ..components import selection, detection, diagnose, prediction
from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


def render(app: Dash, config_app: dict, config_data: dict) -> html.Div:
    return html.Div(
        id="app-body-content",
        children=[
            get_body(app, config_app, config_data),
        ],
    )


def get_body(app: Dash, config_app: dict, config_data: dict) -> html.Div:
    if config_app[ConfigName.navlink] == "Initial":
        return render_initial_info()
    elif config_app[ConfigName.navlink] == Options.sidebar[0]:
        return selection.render(app, config_app, config_data)
    elif config_app[ConfigName.navlink] == Options.sidebar[1]:
        return detection.render(app, config_app, config_data)
    elif config_app[ConfigName.navlink] == Options.sidebar[2]:
        return diagnose.render(app, config_app)
    elif config_app[ConfigName.navlink] == Options.sidebar[3]:
        return prediction.render(app, config_app)


def render_initial_info() -> html.Div:
    return html.Div(
        id="alert-no-sidebar-selected",
        children=Alert(
            "Select an option on the sidebar on the left to get started with the bottleneck analysis.",
            color="secondary",
        ),
    )
