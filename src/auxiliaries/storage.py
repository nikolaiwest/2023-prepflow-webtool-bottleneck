from dash import dcc

DEFAULT_CONFIG = {
    "language": "en",
    "theme": "light",
    "navlink": "",
}

DATA_SOURCE = {
    "source": "default",
}


def register_user_config() -> dcc.Store:
    return dcc.Store(
        id="user-config",
        data=DEFAULT_CONFIG,
        storage_type="memory",
    )


def register_data_source() -> dcc.Store:
    return dcc.Store(
        id="data-source",
        data=DATA_SOURCE,
        storage_type="local",
    )
