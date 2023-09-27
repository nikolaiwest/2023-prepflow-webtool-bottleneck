import i18n

from dash import Dash, callback_context
from dash.dependencies import Input, Output, State

from ..page import body
from ..components import layout


def register(app):
    # Change language or theme based on user selection (dropdowns)
    @app.callback(
        # Update layout and user config
        Output("app-layout", "children"),
        Output("user-config", "data"),
        # Language dropdown inputs
        Input("header-dropdown-language-select-en", "n_clicks"),
        Input("header-dropdown-language-select-de", "n_clicks"),
        # Theme dropdown inputs
        Input("header-dropdown-theme-select-light", "n_clicks"),
        Input("header-dropdown-theme-select-dark", "n_clicks"),
        # Navlink selections
        Input("app-sidebar-nav-link-select", "n_clicks"),
        Input("app-sidebar-nav-link-detect", "n_clicks"),
        Input("app-sidebar-nav-link-diagnose", "n_clicks"),
        Input("app-sidebar-nav-link-predict", "n_clicks"),
        # States from config und data source
        State("user-config", "data"),
        State("data-source", "data"),
        prevent_initial_call=True,
    )
    def update_layout(
        selected_language_en,
        selected_language_de,
        selected_theme_light,
        selected_theme_dark,
        navlink_select,
        navlink_detect,
        navlink_diagnose,
        navlink_predict,
        conf,
        data,
    ):
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        print(f"User pressed: {selection} (debugging)")

        # Update conf based on language selection
        if selection == "header-dropdown-language-select-en":
            conf["language"] = "en"
            i18n.set("locale", conf["language"])
        elif selection == "header-dropdown-language-select-de":
            conf["language"] = "de"
            i18n.set("locale", conf["language"])

        # Update conf based on language selection
        elif selection == "header-dropdown-theme-select-light":
            conf["theme"] = "light"
        elif selection == "header-dropdown-theme-select-dark":
            conf["theme"] = "dark"

        # Update active sidebar based on navlink selection
        elif selection == "app-sidebar-nav-link-select":
            conf["navlink"] = "select"
        elif selection == "app-sidebar-nav-link-detect":
            conf["navlink"] = "detect"
        elif selection == "app-sidebar-nav-link-diagnose":
            conf["navlink"] = "diagnose"
        elif selection == "app-sidebar-nav-link-predict":
            conf["navlink"] = "predict"
        return layout.create(app, conf, data), conf

    @app.callback(
        Output("app-body-content", "children"),
        Output("data-source", "data"),
        Input("app-body-button-default-data", "n_clicks"),
        Input("app-body-button-simulate-data", "n_clicks"),
        Input("app-body-button-upload-data", "n_clicks"),
        State("user-config", "data"),
        State("data-source", "data"),
        prevent_initial_call=True,
    )
    def update_body_selection(
        button_default_clicked,
        button_simulate_clicked,
        button_upload_clicked,
        conf,
        data,
    ):
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        print(f"User pressed: {selection} (debugging)")

        if selection == "app-body-button-default-data":
            data["source"] = "default"
        elif selection == "app-body-button-simulate-data":
            data["source"] = "simulate"
        elif selection == "app-body-button-upload-data":
            data["source"] = "upload"
        return body.render(app, conf, data), data
