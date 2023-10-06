import i18n

from dash import Dash, html
from dash_bootstrap_components import Row, Col, Card, CardImg, CardBody, Button, Alert

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
    print(config_app)
    print(config_data)
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
    def _render_default(conf: dict) -> CardBody:
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
                    [
                        Col(
                            [
                                html.H4(i18n.t("selection.selection-default-title1")),
                                html.Div(i18n.t("selection.selection-default-text1")),
                                html.H4(i18n.t("selection.selection-default-title2")),
                                html.Div(i18n.t("selection.selection-default-text2")),
                            ]
                        ),
                        Col(
                            [
                                html.Img(src=link_to_img),
                            ]
                        ),
                    ]
                )
            ],
        )

    def _render_simulate(conf: dict) -> CardBody:
        """Display the description for the default data set."""
        # pick picture according to template
        if config_app[ConfigName.theme] == Options.theme[0]:
            link_to_img = "assets/selection-simulate-data-dark.png"
        elif config_app[ConfigName.theme] == Options.theme[1]:
            link_to_img = "assets/selection-simulate-data-light.png"
        # render
        return CardBody(
            id="app-body-content-parameter-cardbody",
            children=[
                Row(
                    [
                        Col(
                            [
                                html.H4(i18n.t("selection.selection-simulate-title1")),
                                # html.Div(i18n.t("selection.selection-default-text1")),
                                html.H4(i18n.t("selection.selection-simulate-title2")),
                                # html.Div(i18n.t("selection.selection-default-text2")),
                            ]
                        ),
                        Col(
                            [
                                html.Img(src=link_to_img),
                            ]
                        ),
                    ]
                )
            ],
        )

    def _render_initial() -> html.Div:
        return html.Div(
            id="alert-no-data-source-selected",
            children=Alert(
                "Please select a data source above to get started with the bottleneck analysis.",
                color="secondary",
            ),
        )

    def _render_upload(config_app: dict) -> CardBody:
        return CardBody("PLACEHOLDER: Upload content goes here")

    if config_data[ConfigName.source] == Options.selection[1]:
        return Card(
            id="app-body-content-parameter",
            children=_render_default(config_app),
        )
    elif config_data[ConfigName.source] == Options.selection[2]:
        return Card(
            id="app-body-content-parameter",
            children=_render_simulate(config_app),
        )
    elif config_data[ConfigName.source] == Options.selection[3]:
        return Card(
            id="app-body-content-parameter",
            children=_render_upload(config_app),
        )
    else:
        return _render_initial()


def render_confirmation_button(
    app: Dash, config_app: dict, config_data: dict
) -> html.Div:
    if config_data[ConfigName.source] != Options.selection[0]:
        return Card(
            id="app-body-content-button",
            children=CardBody(
                id="app-body-content-button-card",
                children=[
                    Button(
                        id="app-body-button-data-selection",
                        children=["Save selection and proceed"],
                    ),
                ],
            ),
        )
    else:
        html.Div()
