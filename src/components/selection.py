import i18n

from dash import Dash, html
from dash_bootstrap_components import Row, Col, Card, CardImg, CardBody, Button


class Cards:
    image = "image"
    title = "title"
    descr = "description"
    button_id = "button_id"
    button_label = "button_label"
    button_active = "button_active"


def render(app: Dash, conf: dict, data: dict) -> html.Div:
    return html.Div(
        id="app-body-content-selection",
        children=[render_data_selection(app, conf, data)],
    )


def render_data_selection(app: Dash, conf: dict, data: dict) -> html.Div:
    card_label_select = {
        Cards.image: "assets/card_image_select.png",
        Cards.title: i18n.t("selection.card-select-title"),
        Cards.descr: i18n.t("selection.card-select-descr"),
        Cards.button_id: "app-body-button-default-data",
        Cards.button_label: i18n.t("selection.card-select-button"),
        Cards.button_active: data["source"] == "default",
    }

    card_label_simulate = {
        Cards.image: "assets/card_image_simulate.png",
        Cards.title: i18n.t("selection.card-simulate-title"),
        Cards.descr: i18n.t("selection.card-simulate-descr"),
        Cards.button_id: "app-body-button-simulate-data",
        Cards.button_label: i18n.t("selection.card-simulate-button"),
        Cards.button_active: data["source"] == "simulate",
    }

    card_label_upload = {
        Cards.image: "assets/card_image_upload.png",
        Cards.title: i18n.t("selection.card-upload-title"),
        Cards.descr: i18n.t("selection.card-upload-descr"),
        Cards.button_id: "app-body-button-upload-data",
        Cards.button_label: i18n.t("selection.card-upload-button"),
        Cards.button_active: data["source"] == "upload",
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
