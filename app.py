import i18n

from dash import Dash

from src.components import layout
from src.auxiliaries import callbacks
from src.auxiliaries.storage import DEFAULT_CONFIG, DATA_SOURCE


def main() -> None:
    i18n.set("locale", DEFAULT_CONFIG["language"])
    i18n.load_path.append("locale")

    # New app
    app = Dash(__name__, suppress_callback_exceptions=True)

    # Set static title and create layout
    app.title = "PrEPFlow-Webtool"
    app.layout = layout.create(app, DEFAULT_CONFIG, DATA_SOURCE)

    # Register callbacks
    callbacks.register(app)

    # Run app
    app.run(port=8051, debug=True)


if __name__ == "__main__":
    main()
