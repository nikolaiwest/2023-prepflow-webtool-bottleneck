import io
import i18n
import base64
import pandas as pd

from dash import callback_context, html
from dash.exceptions import NonExistentEventException
from dash.dependencies import Input, Output, State

from dash_bootstrap_components import Alert, Button, Tooltip

from ..page import body
from ..components import layout
from ..components.detection import (
    DetectionName,
    plot_bottlenecks,
    plot_buffer_level,
    plot_active_periods,
)
from simulation.simulation import run_simulation
from simulation.bottlenecks import Bottlenecks
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
            config_app[ConfigName.navlink] = Options.sidebar[1]
        elif selection == LinkName.detection:
            config_app[ConfigName.navlink] = Options.sidebar[2]
        elif selection == LinkName.diagnosis:
            config_app[ConfigName.navlink] = Options.sidebar[3]
        elif selection == LinkName.prediction:
            config_app[ConfigName.navlink] = Options.sidebar[4]
        return layout.create(app, config_app, config_data), config_app

    # Update data source selection based on active card
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
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]
        if selection == "app-body-button-default-data":
            config_data[ConfigName.source] = Options.selection[1]
        elif selection == "app-body-button-simulate-data":
            config_data[ConfigName.source] = Options.selection[2]
        elif selection == "app-body-button-upload-data":
            config_data[ConfigName.source] = Options.selection[3]
        return body.render(app, config_app, config_data), config_data

    # Update data store after selection button was clicked
    @app.callback(
        [
            Output(ConfigName.active_periods, "data"),
            Output(ConfigName.buffer_level, "data"),
            Output("app-body-content-button-card", "children"),
        ],
        [
            Input("app-body-button-data-selection", "n_clicks"),
            State(ConfigName.data, "data"),
            State(ConfigName.buffer_level_upload, "data"),
            State(ConfigName.active_periods_upload, "data"),
        ],
        prevent_initial_call=True,
    )
    def update_data(
        button_clicked,
        config_data,
        df_buffer_level_upload,
        df_active_periods_upload,
    ):
        selection = callback_context.triggered[0]["prop_id"].split(".")[0]

        # Check if user pressed "Continue"
        if button_clicked is not None:
            # If selected to use default data
            if config_data[ConfigName.source] == Options.selection[1]:
                # Load example data from file (limiting to 10k to minimize loading times)
                df_active_periods = pd.read_csv(
                    "data/active_periods_10000.csv"
                ).to_json(orient="split")
                df_buffer_levels = pd.read_csv(
                    "data/active_periods_10000.csv",
                ).to_json(orient="split")
                # Set confirmation alert
                confirmation = html.Div(
                    children=Alert(
                        id="alert-default-data-loaded-successfully",
                        children=i18n.t("selection.confirm-upload-default"),
                        color="success",
                    ),
                )
            # If selected to use simulation data
            if config_data[ConfigName.source] == Options.selection[2]:
                # Run simulation and set data
                scenario = {
                    "process_times": [2, 2.25, 2, 2.25, 2],
                    "simulation_time": 10000,
                    "path_buffer": "buffer.csv",
                    "path_events": "events.csv",
                    "save_results": True,
                    "capa_init": 0,
                    "capa_max": 10,
                    "capa_inf": int(1e2),
                }
                # Run
                if False:  # temporary disabled
                    run_simulation(**scenario)
                    # Load results from file
                    buffer_level = pd.read_csv("buffer.csv")
                    events = pd.read_csv("events.csv")
                    # Get active periods
                    bottlenecks = Bottlenecks(events)
                    active_periods = bottlenecks.calc_active_periods()

                df_buffer_levels = {}  # place holder
                df_active_periods = {}

                # Set confirmation alert
                confirmation = html.Div(
                    children=Alert(
                        id="alert-default-data-loaded-successfully",
                        children=i18n.t("selection.confirm-upload-simulation"),
                        color="success",
                    ),
                )

            # If selected to use custom data
            if config_data[ConfigName.source] == Options.selection[3]:
                #
                df_buffer_levels = df_buffer_level_upload
                df_active_periods = df_active_periods_upload

                # Check uploaded data
                if df_buffer_levels is None or df_active_periods is None:
                    # Set confirmation alert
                    confirmation = html.Div(
                        children=Alert(
                            id="alert-default-data-loaded-unsuccessfully",
                            children=i18n.t("selection.decline-upload-custom"),
                            color="danger",
                        ),
                    )
                else:
                    # Set confirmation alert
                    confirmation = html.Div(
                        children=Alert(
                            id="alert-default-data-loaded-successfully",
                            children=i18n.t("selection.confirm-upload-custom"),
                            color="success",
                        ),
                    )
            # Return loaded dataframes
            return df_active_periods, df_buffer_levels, confirmation

        else:
            button = Button(
                id="app-body-button-data-selection",
                children=[i18n.t("selection.confirm-and-proceed")],
            )
            return {}, {}, button

    @app.callback(
        Output(ConfigName.buffer_level_upload, "data"),
        Output("upload-buffer-level", "children"),
        Input("upload-buffer-level", "contents"),
        Input("upload-buffer-level", "filename"),
        prevent_initial_call=True,
    )
    def upload_buffer_level(
        df,
        file_name,
    ):
        if df is not None:
            _, df = df.split(",")
            df = base64.b64decode(df)
            df = pd.read_csv(io.StringIO(df.decode("utf-8")))
            return df.to_json(orient="split"), file_name
        else:
            return None, i18n.t("selection.upload-button")

    @app.callback(
        Output(ConfigName.active_periods_upload, "data"),
        Output("upload-active-periods", "children"),
        Input("upload-active-periods", "contents"),
        Input("upload-active-periods", "filename"),
        prevent_initial_call=True,
    )
    def upload_buffer_level(
        df,
        file_name,
    ):
        if df is not None:
            _, df = df.split(",")
            df = base64.b64decode(df)
            df = pd.read_csv(io.StringIO(df.decode("utf-8")))
            return df.to_json(orient="split"), file_name
        else:
            return None, i18n.t("selection.upload-button")

    # Detection: Update figures according to selected data set
    @app.callback(
        Output(DetectionName.fig_bottleneck, "figure"),
        Output(DetectionName.fig_buffer_level, "figure"),
        Output(DetectionName.fig_active_periods, "figure"),
        Input(DetectionName.fig_bottleneck, "relayoutData"),
        Input(DetectionName.fig_buffer_level, "relayoutData"),
        Input(DetectionName.fig_active_periods, "relayoutData"),
        State(ConfigName.app, "data"),
        State(ConfigName.active_periods, "data"),
        State(ConfigName.buffer_level, "data"),
    )
    def update_plot_layouts(
        relayout_bottlenecks,
        relayout_buffer_level,
        relayout_active_periods,
        config_app,
        df_active_periods,
        df_buffer_level,
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

        # Prepare data for visualization
        df_active_periods = pd.read_json(df_active_periods, orient="split")
        df_buffer_level = pd.read_json(df_buffer_level, orient="split")

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
            figure_bottlenecks = plot_bottlenecks(
                df_active_periods,
                config_app,
                xaxis_range,
            )
            figure_buffer_level = plot_buffer_level(
                df_buffer_level,
                config_app,
                xaxis_range,
            )
            figure_active_periods = plot_active_periods(
                df_active_periods,
                config_app,
                xaxis_range,
            )

        except KeyError:
            # Create new figures for all scatter plots with the same x-axis range
            figure_bottlenecks = plot_bottlenecks(df_active_periods, config_app)
            figure_buffer_level = plot_buffer_level(df_buffer_level, config_app)
            figure_active_periods = plot_active_periods(df_active_periods, config_app)

        return figure_bottlenecks, figure_buffer_level, figure_active_periods
