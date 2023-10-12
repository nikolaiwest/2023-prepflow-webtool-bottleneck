from dash import Dash, html
from dash_bootstrap_components import Col, Row, DropdownMenu, DropdownMenuItem


def render(app: Dash) -> html.Div:
    return html.Div(
        id="app-header-content",
        children=[
            # Logo in column
            Col(
                id="app-header-logo",
                width=1,
                children=[html.Img(src="assets/logo.svg", height=100)],
            ),
            # Title in column
            Col(
                id="app-header-title",
                width=9,
                children=html.H1(
                    [
                        "Bottle",
                        html.Span(
                            "Next",
                            style={"color": "rgb(30, 161, 179)", "font-weight": "bold"},
                        ),
                    ]
                ),
            ),
            # Dropdowns in column
            Col(
                id="app-header-menu",
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
