import i18n
from dash import Dash, html
from dash_bootstrap_components import Nav, NavLink


def render(app: Dash, conf: dict) -> html.Div:
    return html.Div(
        id="app-sidebar-content",
        children=[
            Nav(
                id="app-sidebar-nav",
                children=[
                    render_link(conf, "app-sidebar-nav-link-select"),
                    render_link(conf, "app-sidebar-nav-link-detect"),
                    render_link(conf, "app-sidebar-nav-link-diagnose"),
                    render_link(conf, "app-sidebar-nav-link-predict"),
                ],
                pills=True,
            ),
        ],
    )


def render_link(conf: dict, link_id: str) -> NavLink:
    return NavLink(
        id=link_id,
        children=html.H4(i18n.t(f"sidebar.{link_id}")),
        href=f"/{link_id}",
        active=conf["navlink"] == link_id.split("-")[-1],
    )
