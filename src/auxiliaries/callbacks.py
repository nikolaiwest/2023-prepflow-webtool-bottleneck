import i18n
import pandas as pd

from dash import callback_context
from dash.dependencies import Input, Output, State

from ..page import body
from ..components import layout
from ..page.sidebar import LinkName
from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


def register(app):
    # Change language or theme based on user selection (dropdowns)
    @app.callback(
        # Update layout and user config
        Output("app-layout", "children"),
        Output(ConfigName.app, "data"),
        # Language dropdown inputs
        Input("header-dropdown-language-select-en", "n_clicks"),
        Input("header-dropdown-language-select-de", "n_clicks"),
        # Theme dropdown inputs
        Input("header-dropdown-theme-select-light", "n_clicks"),
        Input("header-dropdown-theme-select-dark", "n_clicks"),
        # Navlink selections
        Input(LinkName.selection, "n_clicks"),
        Input(LinkName.detection, "n_clicks"),
        Input(LinkName.diagnosis, "n_clicks"),
        Input(LinkName.prediction, "n_clicks"),
        # States from config und data source
        State(ConfigName.app, "data"),
        State(ConfigName.data, "data"),
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
        config_app,
        config_data,
    ):
        print(
            "Callback triggered: Change of navlink selection (one of four links selected)"
        )
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        # Update conf based on language selection
        if selection == "header-dropdown-language-select-en":
            config_app[ConfigName.language] = Options.language[0]
            i18n.set("locale", config_app[ConfigName.language])
        elif selection == "header-dropdown-language-select-de":
            config_app[ConfigName.language] = Options.language[1]
            i18n.set("locale", config_app[ConfigName.language])

        # Update conf based on language selection
        elif selection == "header-dropdown-theme-select-light":
            config_app[ConfigName.theme] = Options.theme[0]
        elif selection == "header-dropdown-theme-select-dark":
            config_app[ConfigName.theme] = Options.theme[1]

        # Update active sidebar based on navlink selection
        elif selection == LinkName.selection:
            config_app[ConfigName.navlink] = Options.sidebar[0]
        elif selection == LinkName.detection:
            config_app[ConfigName.navlink] = Options.sidebar[1]
        elif selection == LinkName.diagnosis:
            config_app[ConfigName.navlink] = Options.sidebar[2]
        elif selection == LinkName.prediction:
            config_app[ConfigName.navlink] = Options.sidebar[3]
        return layout.create(app, config_app, config_data), config_app

    # update data source selection based on active card
    @app.callback(
        Output("app-body-content", "children"),
        Output(ConfigName.data, "data"),
        Input("app-body-button-default-data", "n_clicks"),
        Input("app-body-button-simulate-data", "n_clicks"),
        Input("app-body-button-upload-data", "n_clicks"),
        State(ConfigName.app, "data"),
        State(ConfigName.data, "data"),
        prevent_initial_call=True,
    )
    def update_body_selection(
        button_default_clicked,
        button_simulate_clicked,
        button_upload_clicked,
        config_app,
        config_data,
    ):
        print("Callback triggered: Change of data source (one of three cards selected)")
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        if selection == "app-body-button-default-data":
            config_data[ConfigName.source] = Options.selection[1]
        elif selection == "app-body-button-simulate-data":
            config_data[ConfigName.source] = Options.selection[2]
        elif selection == "app-body-button-upload-data":
            config_data[ConfigName.source] = Options.selection[3]
        return body.render(app, config_app, config_data), config_data

    # update data after selection button was clicked
    @app.callback(
        Output(ConfigName.active_periods, "data"),
        Input("app-body-button-data-selection", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_data(
        button_clicked,
    ):
        print("Rendering for new data.")
        # load data
        return pd.read_csv("data/active_periods_10000.csv").to_json(orient="split")
