import i18n
import pandas as pd

from dash import callback_context
from dash.dependencies import Input, Output, State

from ..page import body
from ..components import layout
from ..components.detection import (
    DetectionName,
    plot_bottlenecks,
    plot_buffer_level,
    plot_active_periods,
)
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
        """
        Update the application layout and user configuration based on user selections.

        This callback function handles user interactions with dropdowns to change the language and theme,
        as well as the navigation links. It updates the application layout and user configuration
        accordingly.

        Parameters:
            selected_language_en (int): Number of clicks on the English language dropdown.
            selected_language_de (int): Number of clicks on the German language dropdown.
            selected_theme_light (int): Number of clicks on the Light theme dropdown.
            selected_theme_dark (int): Number of clicks on the Dark theme dropdown.
            navlink_select (int): Number of clicks on the "Selection" navigation link.
            navlink_detect (int): Number of clicks on the "Detection" navigation link.
            navlink_diagnose (int): Number of clicks on the "Diagnosis" navigation link.
            navlink_predict (int): Number of clicks on the "Prediction" navigation link.
            config_app (dict): A dictionary containing configuration settings for the application.
            config_data (dict): A dictionary containing configuration data.

        Returns:
            tuple: A tuple containing the updated application layout and user configuration.
        """
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
        """
        Update the data source selection and the application body content based on user interactions.

        This callback function handles user interactions with buttons to change the data source selection.
        It updates the data source selection and the content of the application body accordingly.

        Parameters:
            button_default_clicked (int): Number of clicks on the "Default Data" button.
            button_simulate_clicked (int): Number of clicks on the "Simulate Data" button.
            button_upload_clicked (int): Number of clicks on the "Upload Data" button.
            config_app (dict): A dictionary containing configuration settings for the application.
            config_data (dict): A dictionary containing configuration data.

        Returns:
            tuple: A tuple containing the updated application body content and data source selection.
        """
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
        # load data
        return pd.read_csv("data/active_periods_10000.csv").to_json(orient="split")

    @app.callback(
        Output(DetectionName.fig_bottleneck, "figure"),
        Output(DetectionName.fig_buffer_level, "figure"),
        Output(DetectionName.fig_active_periods, "figure"),
        Input(DetectionName.fig_bottleneck, "relayoutData"),
        Input(DetectionName.fig_buffer_level, "relayoutData"),
        Input(DetectionName.fig_active_periods, "relayoutData"),
        State(ConfigName.app, "data"),
    )
    def update_plot_layouts(
        relayout_bottlenecks,
        relayout_buffer_level,
        relayout_active_periods,
        config_app,
    ):
        """
        Update the plot layouts after a user selection.

        This callback function is triggered when the user interacts with the plot layouts for bottleneck analysis,
        buffer levels, or active periods. It captures the user's selection, specifically the x-axis range,
        and updates the respective figures with the new x-axis range if available. If no x-axis range is provided
        or if an invalid selection is made, the figures are updated with the default x-axis range.

        Parameters:
            relayout_bottlenecks (dict): The relayoutData from the bottleneck figure.
            relayout_buffer_level (dict): The relayoutData from the buffer level figure.
            relayout_active_periods (dict): The relayoutData from the active periods figure.
            config_app (dict): A dictionary containing configuration settings for the application.
            config_data (dict): A dictionary containing configuration data.

        Returns:
            tuple: A tuple containing updated figures for bottleneck analysis, buffer levels, and active periods.

        Notes:
            - This function is used as a callback to dynamically update the plots based on user interaction.
            - It determines the x-axis range from the selected plot's relayoutData and updates all figures with
            the same x-axis range.
            - If no x-axis range is available or if an invalid selection is made, the default x-axis range is used.
        """
        # Get selection from callback context
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        try:
            # Determine the x-axis range from any of the scatter plots
            xaxis_range = None
            if selection == DetectionName.fig_bottleneck:
                x1 = relayout_bottlenecks["xaxis.range[0]"]
                x2 = relayout_bottlenecks["xaxis.range[1]"]
                xaxis_range = [x1, x2]
            elif selection == DetectionName.fig_buffer_level:
                x1 = relayout_buffer_level["xaxis.range[0]"]
                x2 = relayout_buffer_level["xaxis.range[1]"]
                xaxis_range = [x1, x2]
            elif selection == DetectionName.fig_active_periods:
                x1 = relayout_active_periods["xaxis.range[0]"]
                x2 = relayout_active_periods["xaxis.range[1]"]
                xaxis_range = [x1, x2]

            # Create new figures for all scatter plots with the same x-axis range
            figure_bottlenecks = plot_bottlenecks(config_app, xaxis_range)
            figure_buffer_level = plot_buffer_level(config_app, xaxis_range)
            figure_active_periods = plot_active_periods(config_app, xaxis_range)

        except KeyError:
            # Create new figures for all scatter plots with the same x-axis range
            figure_bottlenecks = plot_bottlenecks(config_app)
            figure_buffer_level = plot_buffer_level(config_app)
            figure_active_periods = plot_active_periods(config_app)

        return figure_bottlenecks, figure_buffer_level, figure_active_periods
