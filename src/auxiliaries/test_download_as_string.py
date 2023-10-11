from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

# Create a Dash app
app = Dash(__name__)

# Create a Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("File Upload and Storage"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,  # Allow only a single file to be uploaded
        ),
        dcc.Store(id="data-storage"),  # Store uploaded file path
    ]
)


# Define callback to store the uploaded file path
@app.callback(
    Output("data-storage", "data"),
    Input("upload-data", "filename"),
    State("upload-data", "filepath"),
)
def store_uploaded_data(filename, filepath):
    if filename is None:
        raise PreventUpdate

    # Use the provided filepath as the absolute path
    return filepath


if __name__ == "__main__":
    app.run_server(debug=True)
