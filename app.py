import i18n

from dash import Dash

from src.components import layout
from src.auxiliaries import callbacks
from src.auxiliaries.storage import CONFIG_APP, CONFIG_DATA


def main() -> None:
    """Main function to run the dash app for BottleNext."""
    # Initialize language settings
    i18n.set("locale", CONFIG_APP["user_language"])
    i18n.load_path.append("locale")

    # Create new app
    app = Dash(__name__, suppress_callback_exceptions=True)

    # Set static title and create layout
    app.title = "PrEPFlow-Webtool"
    app.layout = layout.create(app, CONFIG_APP, CONFIG_DATA)

    # Register additional callbacks
    callbacks.register(app)

    # Run app
    app.run(port=8051, debug=True)


if __name__ == "__main__":
    main()
