import i18n

from dash import Dash, html
from dash_bootstrap_components import Nav, NavLink

from ..auxiliaries.storage import ConfigName


class LinkName:
    selection = "sidebar-navlink-selection"
    detection = "sidebar-navlink-detection"
    diagnosis = "sidebar-navlink-diagnosis"
    prediction = "sidebar-navlink-prediction"


def render(app: Dash, config_app: dict, config_data) -> html.Div:
    return html.Div(
        id="sidebar-content",
        children=[
            # Put links on dbc.Nav
            Nav(
                id="sidebar-nav",
                children=[
                    # Data selection
                    render_link(config_app, LinkName.selection),
                    # Bottleneck detection
                    render_link(config_app, LinkName.detection),
                    # Bottleneck diagnosis
                    render_link(config_app, LinkName.diagnosis),
                    # Bottleneck prediction
                    render_link(config_app, LinkName.prediction),
                    # debug
                    html.Div(
                        [
                            html.Div(render_dict(config_app)),
                            html.Hr(),
                            html.Div(render_dict(config_data)),
                        ]
                    ),
                ],
                pills=True,
            ),
        ],
    )


def render_dict(d: dict):
    r = []
    for k, v in d.items():
        r += [html.H5(k), html.H6(v)]
    return r


def render_link(config_app: dict, navlink: str) -> NavLink:
    # Get dict to display the page names for each navlink
    page_names = {
        LinkName.selection: "data-selection",
        LinkName.detection: "bottleneck-detection",
        LinkName.diagnosis: "bottleneck-diagnosis",
        LinkName.prediction: "bottleneck-prediction",
    }
    return NavLink(
        id=navlink,
        children=[html.H4(i18n.t(f"sidebar.{navlink}"))],
        href=f"/{page_names[navlink]}",
        active=config_app[ConfigName.navlink] == navlink.split("-")[-1],
    )
