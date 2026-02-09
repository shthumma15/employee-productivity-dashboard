import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRfanchxIXmn54oSJ0u0w5yTft3ipRUxGpmtBy8gtUhvrAcmbDXO5wu01IT7Nsob2SvVrpIkL7oWbdt/pub?gid=1395197216&single=true&output=csv'
df = pd.read_csv(url)
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={"maxWidth": "1200px", "margin": "auto"},
    children=[
        html.H1("Employee Productivity Dashboard", style={"textAlign": "center"}),

        dcc.Dropdown(
            id="department-filter",
            options=[{"label": d, "value": d} for d in df["department"].unique()],
            value=list(df["department"].unique()),
            multi=True
        ),

        dcc.Tabs([
            dcc.Tab(label="Overtime vs Productivity", children=[
                dcc.Graph(id="scatter-plot")
            ]),
            dcc.Tab(label="Distribution", children=[
                dcc.Graph(id="box-plot")
            ]),
            dcc.Tab(label="Correlation", children=[
                dcc.Graph(id="heatmap-plot")
            ]),
            dcc.Tab(label="Trends", children=[
                dcc.Graph(id="line-plot")
            ]),
        ])
    ]
)

# Callbacks
@app.callback(
    Output("scatter-plot", "figure"),
    Output("box-plot", "figure"),
    Output("heatmap-plot", "figure"),
    Output("line-plot", "figure"),
    Input("department-filter", "value"),
)
def update_graphs(depts):

    dff = df if not depts else df[df["department"].isin(depts)]

    scatter = px.scatter(
        dff,
        x="over_time",
        y="actual_productivity",
        color="department",
        title="Overtime vs Productivity"
    )

    box = px.box(
        dff,
        x="department",
        y="actual_productivity",
        color="department",
        title="Productivity Distribution"
    ).update_layout(showlegend=False)

    corr = dff[["over_time", "incentive", "idle_time", "actual_productivity"]].corr()
    heatmap = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Matrix",
        color_continuous_scale="Viridis"
    )

    line = px.line(
        dff,
        x="date",
        y="actual_productivity",
        color="department",
        title="Productivity Trends Over Time"
    )

    return scatter, box, heatmap, line


# Run server
if __name__ == "__main__":
    app.run(debug=True)
