import i18n
from pandas import DataFrame

from dash import Dash, html, dcc
from dash_bootstrap_components import (
    Row,
    Col,
    Card,
    CardImg,
    CardBody,
    Button,
    Alert,
    Table,
    Container,
)

from ..auxiliaries.options import Options
from ..auxiliaries.storage import ConfigName


class Cards:
    """Simple helper class to manage card labels."""

    image = "image"
    title = "title"
    descr = "description"
    button_id = "button_id"
    button_label = "button_label"
    button_active = "button_active"


def render(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    """Display all content for data selection."""
    # render
    return html.Div(
        id="app-body-content-selection",
        children=[
            # display of three cards for selection (default, simulate, upload)
            render_selection_options(app, config_app, config_data),
            # display of the main input for data source according to the selected option
            render_selection_details(app, config_app, config_data),
            # display of a button (for all selections)
            render_confirmation_button(app, config_app, config_data),
        ],
    )


def render_selection_options(
    app: Dash, config_app: dict, config_data: dict
) -> html.Div:
    card_label_select = {
        Cards.image: "assets/card_image_select.png",
        Cards.title: i18n.t("selection.card-select-title"),
        Cards.descr: i18n.t("selection.card-select-descr"),
        Cards.button_id: "app-body-button-default-data",
        Cards.button_label: i18n.t("selection.card-select-button"),
        Cards.button_active: config_data[ConfigName.source] == Options.selection[1],
    }

    card_label_simulate = {
        Cards.image: "assets/card_image_simulate.png",
        Cards.title: i18n.t("selection.card-simulate-title"),
        Cards.descr: i18n.t("selection.card-simulate-descr"),
        Cards.button_id: "app-body-button-simulate-data",
        Cards.button_label: i18n.t("selection.card-simulate-button"),
        Cards.button_active: config_data[ConfigName.source] == Options.selection[2],
    }

    card_label_upload = {
        Cards.image: "assets/card_image_upload.png",
        Cards.title: i18n.t("selection.card-upload-title"),
        Cards.descr: i18n.t("selection.card-upload-descr"),
        Cards.button_id: "app-body-button-upload-data",
        Cards.button_label: i18n.t("selection.card-upload-button"),
        Cards.button_active: config_data[ConfigName.source] == Options.selection[3],
    }

    return html.Div(
        id="app-body-content-selection-top",
        children=[
            Row(
                [
                    Col(render_card(app, card_label_select)),
                    Col(render_card(app, card_label_simulate)),
                    Col(render_card(app, card_label_upload)),
                ]
            ),
        ],
    )


def render_card(app: Dash, label: dict) -> html.Div:
    if label[Cards.button_active]:
        card_style = {}
        button_color = "primary"
    else:
        card_style = {"filter": "grayscale(100%)"}
        button_color = "secondary"

    return Card(
        [
            CardImg(src=label[Cards.image], top=True, style=card_style),
            CardBody(
                children=[
                    html.H4(label[Cards.title], className="card-title"),
                    html.P(label[Cards.descr], className="card-text"),
                    html.Div(
                        [
                            Button(
                                label[Cards.button_label],
                                id=label[Cards.button_id],
                                color=button_color,
                                style={"width": "100%"},
                            )
                        ],
                    ),
                ]
            ),
        ],
    )


def render_selection_details(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    def _render_initial() -> html.Div:
        return html.Div(
            id="alert-no-data-source-selected",
            children=Alert(
                "Please select a data source above to get started with the bottleneck analysis.",
                color="secondary",
            ),
        )

    def _render_default() -> CardBody:
        """Display the description for the default data set."""
        # pick picture according to template
        if config_app[ConfigName.theme] == Options.theme[0]:
            link_to_img = "assets/selection-example-data-light.png"
        elif config_app[ConfigName.theme] == Options.theme[1]:
            link_to_img = "assets/selection-example-data-dark.png"
        # render
        return CardBody(
            id="app-body-content-parameter-cardbody",
            children=[
                Row(
                    children=[
                        Col(
                            children=[
                                # Data description
                                html.H4(i18n.t("selection.default-title1")),
                                html.Div(i18n.t("selection.default-text1")),
                                dcc.Link(
                                    f""">> {i18n.t("selection.default-link1")}""",
                                    href="https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet",
                                    target="_blank",
                                ),
                            ]
                        ),
                        # Image of value stream
                        Col([html.Img(src=link_to_img)]),
                    ]
                ),
                # Reccomendations for usage
                html.H4(
                    i18n.t("selection.default-title2"),
                    style={"margin-top": "1rem"},
                ),
                html.Div(i18n.t("selection.default-text2")),
                dcc.Link(
                    f""">> {i18n.t("selection.simulation-link2")}""",
                    href=r"https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet/blob/main/WEST-E%7E1.PDF",
                    target="_blank",
                ),
            ],
        )

    def _render_simulate() -> CardBody:
        """Display the description for the default data set."""
        # pick picture according to template
        if config_app[ConfigName.theme] == Options.theme[0]:
            link_to_img = "assets/selection-simulate-data-light.png"
        elif config_app[ConfigName.theme] == Options.theme[1]:
            link_to_img = "assets/selection-simulate-data-dark.png"
        # render
        return CardBody(
            id="app-body-content-parameter-cardbody",
            children=[
                Row(
                    children=[
                        Col(
                            children=[
                                # Details of the simulation
                                html.H4(i18n.t("selection.simulation-title1")),
                                html.Div(
                                    i18n.t("selection.simulation-text1"),
                                ),
                                dcc.Link(
                                    f""">> {i18n.t("selection.simulation-link1")}""",
                                    href=r"https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet/tree/main/simulation",
                                    target="_blank",
                                ),
                            ]
                        ),
                        Col(
                            [
                                html.Img(src=link_to_img),
                            ]
                        ),
                    ]
                ),
                # Customization of the parameters
                html.H4(
                    i18n.t("selection.simulation-title2"),
                    style={"margin-top": "1rem"},
                ),
                html.Div(i18n.t("selection.simulation-text2")),
                dcc.Link(
                    f""">> {i18n.t("selection.simulation-link1")}""",
                    href=r"https://www.researchgate.net/publication/371944127_Data-driven_approach_for_diagnostic_analysis_of_dynamic_bottlenecks_in_serial_manufacturing_systems",
                    target="_blank",
                ),
                # Parameter inputs
                Row(
                    [
                        # Number of stations
                        Col(
                            children=[
                                html.H6(i18n.t("selection.simulation-param1")),
                                dcc.Input(
                                    id="input-station-number",
                                    type="number",
                                    placeholder=5,
                                ),
                            ],
                            width=3,
                        ),
                        # Simulation time
                        Col(
                            children=[
                                html.H6(i18n.t("selection.simulation-param2")),
                                dcc.Input(
                                    id="input-simulation-steps",
                                    type="number",
                                    placeholder=10000,
                                ),
                            ],
                            width=3,
                        ),
                        # Process times
                        Col(
                            children=[
                                html.H6(i18n.t("selection.simulation-param3")),
                                dcc.Input(
                                    id="input-process-times",
                                    type="text",
                                    placeholder="[2.00, 2.25, 2.00, 2.25, 2.00]",
                                ),
                            ],
                            width=3,
                        ),
                        # Buffer capacities
                        Col(
                            children=[
                                html.H6(i18n.t("selection.simulation-param4")),
                                dcc.Input(
                                    id="input-buffer-capacity",
                                    type="text",
                                    placeholder="[5.00, 5.00, 5.00, 5.00, 5.00]",
                                ),
                            ],
                            width=3,
                        ),
                    ],
                    style={"margin-top": "1rem"},
                ),
            ],
        )

    def _render_upload() -> CardBody:
        df_example1 = DataFrame(
            {
                "t": [0, 1, 2, 3, 4],
                "B0": [0, 1, 2, 3, 4],
                "B1": [0, 1, 2, 3, 4],
                "...": ["...", "...", "...", "...", "..."],
                "Bn-1": [0, 1, 2, 3, 4],
                "Bn": [0, 1, 2, 3, 4],
            }
        )
        df_example2 = DataFrame(
            {
                "S0": [0, 1, 2, 0, 4],
                "S1": [0, 0, 1, 2, 3],
                "...": ["...", "...", "...", "...", "..."],
                "Sn-1": [0, 1, 2, 3, 4],
                "Sn": [0, 1, 0, 1, 2],
                "bottleneck": [1, 1, "n", "n", 4],
            }
        )
        return CardBody(
            id="app-body-content-parameter-cardbody",
            children=[
                Row(
                    [
                        Col(
                            children=[
                                # Upload buffer level
                                html.H4(i18n.t("selection.upload-title1")),
                                html.Div(i18n.t("selection.upload-text1")),
                                Table.from_dataframe(
                                    df_example1,
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                    style={"margin-top": "1rem"},
                                ),
                                dcc.Upload(
                                    id="upload-buffer-level",
                                    children=[i18n.t("selection.upload-button")],
                                    multiple=False,
                                    accept=".csv",
                                ),
                            ],
                        ),
                        Col(
                            children=[
                                # Upload active periods
                                html.H4(i18n.t("selection.upload-title2")),
                                html.Div(i18n.t("selection.upload-text2")),
                                Table.from_dataframe(
                                    df_example2,
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                    style={"margin-top": "1rem"},
                                ),
                                dcc.Upload(
                                    id="upload-active-periods",
                                    children=[i18n.t("selection.upload-button")],
                                    multiple=False,
                                    accept=".csv",
                                ),
                            ],
                        ),
                    ]
                )
            ],
        )

    if config_data[ConfigName.source] == Options.selection[1]:
        return Card(
            id="app-body-content-parameter",
            children=_render_default(),
        )
    elif config_data[ConfigName.source] == Options.selection[2]:
        return Card(
            id="app-body-content-parameter",
            children=_render_simulate(),
        )
    elif config_data[ConfigName.source] == Options.selection[3]:
        return Card(
            id="app-body-content-parameter",
            children=_render_upload(),
        )
    else:
        return _render_initial()


def render_confirmation_button(
    app: Dash,
    config_app: dict,
    config_data: dict,
) -> html.Div:
    # If no source selected, display warning
    if config_data[ConfigName.source] == Options.selection[0]:
        return html.Div()
    elif config_data[ConfigName.source] in Options.selection[1:4]:
        return Card(
            id="app-body-content-button",
            children=CardBody(
                id="app-body-content-button-card",
                children=[
                    Button(
                        id="app-body-button-data-selection",
                        children=[i18n.t("selection.confirm-and-proceed")],
                    ),
                ],
            ),
        )
