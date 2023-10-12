import i18n

from dash import Dash, html
from dash_bootstrap_components import Nav, NavLink

from ..auxiliaries.storage import ConfigName
from ..auxiliaries.options import Options


class LinkName:
    selection = f"sidebar-navlink-{Options.sidebar[1]}"
    detection = f"sidebar-navlink-{Options.sidebar[2]}"
    diagnosis = f"sidebar-navlink-{Options.sidebar[3]}"
    prediction = f"sidebar-navlink-{Options.sidebar[4]}"


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
        LinkName.selection: Options.sidebar[1],
        LinkName.detection: Options.sidebar[2],
        LinkName.diagnosis: Options.sidebar[3],
        LinkName.prediction: Options.sidebar[4],
    }
    return NavLink(
        id=navlink,
        children=[html.H4(i18n.t(f"sidebar.{navlink}"))],
        href=f"/{page_names[navlink]}",
        active=config_app[ConfigName.navlink] == navlink.split("-")[-1],
    )
