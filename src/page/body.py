import i18n

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
    # On app start, display hint to use the sidebar menu
    if config_app[ConfigName.navlink] == Options.sidebar[0]:
        return render_initial_info()
    # Display sidebar item "Data selection"
    elif config_app[ConfigName.navlink] == Options.sidebar[1]:
        return selection.render(app, config_app, config_data)
    # Display sidebar item "Bottleneck Detection"
    elif config_app[ConfigName.navlink] == Options.sidebar[2]:
        return detection.render(app, config_app, config_data)
    # Display sidebar item "Bottleneck Diagnosis"
    elif config_app[ConfigName.navlink] == Options.sidebar[3]:
        return diagnose.render(app, config_app, config_data)
    # Display sidebar item "Bottleneck Prediction"
    elif config_app[ConfigName.navlink] == Options.sidebar[4]:
        return prediction.render(app, config_app, config_data)
    # Catch any navlink error with a warning
    else:
        return render_invalid_selection()


def render_initial_info() -> html.Div:
    return html.Div(
        id="alert-no-sidebar-selected",
        children=Alert(
            i18n.t("general.body_warning_1"),
            color="secondary",
        ),
    )


def render_invalid_selection() -> html.Div:
    return html.Div(
        id="alert-invalid-sidebar-option",
        children=Alert(
            i18n.t("general.body_warning_2"),
            color="danger",
        ),
    )
