from pandas import DataFrame
from dash.dcc import Store

from .options import Options


class ConfigName:
    # Name for Store id's
    app = "user-config-app"
    data = "user-config-data"
    buffer_level = "data-buffer-level"
    buffer_level_upload = "data-buffer-level-upload"
    machine_states = "data-machine-states"
    active_periods = "data-active-periods"
    active_periods_upload = "data-active-periods-upload"
    # Name for dict keys (app)
    theme = "user_theme"
    navlink = "user_navlink"
    language = "user_language"
    # Name for dict keys (data)
    source = "data-source"


# Get dict with default values for app configuration
CONFIG_APP = {
    ConfigName.language: Options.language[0],
    ConfigName.theme: Options.theme[0],
    ConfigName.navlink: Options.sidebar[0],
}

# Get dict with default values for data configuration
CONFIG_DATA = {
    ConfigName.source: Options.selection[0],
    "sim_process_times": [],
    "sim_buffer_capacity": [],
    "path_to_buffer_levles": "",
    "path_to_machine_states": "",
}


def register_config_app() -> Store:
    """Registers a dcc.Store object to save user selections, such as language or theme, during an app session."""
    # Return store to layout
    return Store(
        id=ConfigName.app,
        data=CONFIG_APP,
        storage_type="session",
    )


def register_config_data() -> Store:
    """Registers a dcc.Store object to save user selections, such as the data selection, during an app session."""
    # Return store to layout
    return Store(
        id=ConfigName.data,
        data=CONFIG_DATA,
        storage_type="session",
    )


# dcc.Store for the bottleneck analysis:


def register_data_buffer_level() -> Store:
    """Registers a dcc.Store object to save buffer level data as a serialized json object."""
    # Get empty dataframe to initialize
    df = DataFrame({}).to_json(orient="split")
    return Store(
        id=ConfigName.buffer_level,
        data=df,
        storage_type="session",
    )


def register_data_machine_states() -> Store:
    """Registers a dcc.Store object to save machine state data as a serialized json object."""
    # Get empty dataframe to initialize
    df = DataFrame({}).to_json(orient="split")
    return Store(
        id=ConfigName.machine_states,
        data=df,
        storage_type="session",
    )


def register_data_active_periods() -> Store:
    """Registers a dcc.Store object to save active period data as a serialized json object."""
    # Get empty dataframe to initialize
    df = DataFrame({}).to_json(orient="split")
    return Store(
        id=ConfigName.active_periods,
        data=df,
        storage_type="session",
    )


# dcc.Store to handle intermediary uploaded user data:
def register_data_buffer_level_upload() -> Store:
    """Registers a dcc.Store object to save buffer level data as a serialized json object."""
    # Get empty dataframe to initialize
    df = DataFrame({}).to_json(orient="split")
    return Store(
        id=ConfigName.buffer_level_upload,
        data=df,
        storage_type="session",
    )


def register_data_active_periods_upload() -> Store:
    """Registers a dcc.Store object to save active period data as a serialized json object."""
    # Get empty dataframe to initialize
    df = DataFrame({}).to_json(orient="split")
    return Store(
        id=ConfigName.active_periods_upload,
        data=df,
        storage_type="session",
    )
