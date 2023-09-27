from dash import Dash, html
from dash_bootstrap_components import Col, DropdownMenu, DropdownMenuItem


def render(app: Dash) -> html.Div:
    return html.Div(
        id="app-header-content",
        children=[
            # Title in column
            Col(
                id="app-header-title-col",
                width=10,
                children=[html.H1("BottleNext", id="app-header-title")],
            ),
            # Dropdowns in column
            Col(
                id="app-header-menu-col",
                width=2,
                children=[render_dropdown_language(), render_dropdown_theme()],
            ),
        ],
    )


def render_dropdown_language() -> DropdownMenu:
    return DropdownMenu(
        id="header-dropdown-language",
        label="🌐",
        className="dropdown",
        children=[
            DropdownMenuItem(
                "🇬🇧 English",
                "header-dropdown-language-select-en",
                n_clicks=0,
            ),
            DropdownMenuItem(
                "🇩🇪 German",
                "header-dropdown-language-select-de",
                n_clicks=0,
            ),
        ],
    )


def render_dropdown_theme() -> DropdownMenu:
    return DropdownMenu(
        id="header-dropdown-theme",
        label="🌗",
        className="dropdown",
        children=[
            DropdownMenuItem(
                "🌕 Light",
                "header-dropdown-theme-select-light",
                n_clicks=0,
            ),
            DropdownMenuItem(
                "🌑 Dark",
                "header-dropdown-theme-select-dark",
                n_clicks=0,
            ),
        ],
    )
