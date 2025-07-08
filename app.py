import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("C:/Users/mange/OneDrive/Desktop/dashboard_project/Dataset.csv")
df = df.dropna(subset=["Cuisines", "City", "Latitude", "Longitude"])

# Top cuisines
top_cuisines = df["Cuisines"].str.split(", ").explode().value_counts().head(3).reset_index()
top_cuisines.columns = ['Cuisine', 'Count']

# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # Dark Theme
app.title = "Restaurant Insights Dashboard"

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="🍽 Restaurant Insights Dashboard",
        color="dark", dark=True, fluid=True, className="mb-4"
    ),

    dbc.Row([
        dbc.Col([
            html.Label("🔍 Select City:", style={"color": "white"}),
            dcc.Dropdown(
                id="city-dropdown",
                options=[{'label': city, 'value': city} for city in df["City"].unique()],
                placeholder="Filter by City", multi=False
            )
        ], width=4)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🏙️ Total Cities", className="text-white"),
                html.H3(id="total-cities", className="text-white")
            ])
        ], color="dark"), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🍴 Total Restaurants", className="text-white"),
                html.H3(id="total-restaurants", className="text-white")
            ])
        ], color="dark"), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("⭐ Average Rating", className="text-white"),
                html.H3(id="avg-rating", className="text-white")
            ])
        ], color="dark"), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🗳️ Average Votes", className="text-white"),
                html.H3(id="avg-votes", className="text-white")
            ])
        ], color="dark"), width=3),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Top 3 Cuisines", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(
                figure=px.bar(top_cuisines, x='Cuisine', y='Count', color='Cuisine')
            )])
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("📈 Price Range Distribution", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="price-graph")])
        ]), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🗳️ Votes vs Ratings", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="votes-vs-rating-graph")])
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🗺️ Map (⭐ Highlights 5-Star)", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="map-graph")])
        ]), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🚚 Online Delivery Stats", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="online-delivery-pie")])
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("📅 Table Booking Stats", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="table-booking-pie")])
        ]), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("⭐ Ratings Distribution", className="text-white bg-dark"),
            dbc.CardBody([dcc.Graph(id="rating-distribution")])
        ]), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🏆 Top 10 Rated Restaurants (⭐ Highlighted)", className="text-white bg-dark"),
            dbc.CardBody([
                dash_table.DataTable(
                    id="top-table",
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'padding': '5px'},
                    style_header={'backgroundColor': '#444', 'color': 'white', 'fontWeight': 'bold'},
                    style_data={'backgroundColor': '#2c2c2c', 'color': 'white'},
                    page_size=10
                )
            ])
        ]), width=6),
    ]),

    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div([
            html.H2("📬 Get in Touch!", style={'color': '#66d9ef', 'textAlign': 'center'}),
            html.P("If you have any questions or just want to connect, feel free to reach out to me on LinkedIn or check out my GitHub!",
                   style={'fontSize': '18px', 'textAlign': 'center', 'color': '#ccc'}),
            html.P("🔗 Mangesh Ambekar", style={'fontSize': '22px', 'fontWeight': 'bold', 'textAlign': 'center', 'color': '#ffffff'}),
            html.Div([
                html.A(html.Img(src="https://www.svgrepo.com/show/448234/linkedin.svg",
                                style={'height': '50px', 'marginRight': '30px'}),
                       href="https://www.linkedin.com/in/mangeshsanjayambekar/", target="_blank"),
                html.A(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
                                style={'height': '50px'}),
                       href="https://github.com/Mangesh0101", target="_blank"),
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginTop': '10px'})
        ]), width=12)
    ])
], fluid=True)

# Callbacks
@app.callback(
    Output("total-cities", "children"),
    Output("total-restaurants", "children"),
    Output("avg-rating", "children"),
    Output("avg-votes", "children"),
    Output("price-graph", "figure"),
    Output("votes-vs-rating-graph", "figure"),
    Output("map-graph", "figure"),
    Output("online-delivery-pie", "figure"),
    Output("table-booking-pie", "figure"),
    Output("rating-distribution", "figure"),
    Output("top-table", "data"),
    Output("top-table", "columns"),
    Input("city-dropdown", "value")
)
def update_dashboard(city):
    filtered = df[df["City"] == city] if city else df

    total_cities = filtered["City"].nunique()
    total_rest = len(filtered)
    avg_rating = round(filtered["Aggregate rating"].mean(), 2)
    avg_votes = int(filtered["Votes"].mean())

    price_fig = px.histogram(filtered, x="Price range", nbins=4, title="Price Range Distribution")
    scatter_fig = px.scatter(filtered, x="Votes", y="Aggregate rating", size="Votes", color="Price range",
                             hover_data=["Restaurant Name"], title="Votes vs Ratings")

    rating_group = filtered["Aggregate rating"].apply(lambda x: "⭐ 5-Star" if x == 5.0 else "Other")
    map_fig = px.scatter_mapbox(filtered, lat="Latitude", lon="Longitude", color=rating_group,
                                hover_name="Restaurant Name", zoom=3, height=350,
                                hover_data=["City", "Cuisines"])
    map_fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 30, "l": 0, "b": 0})
    map_fig.update_layout(legend_title_text="Rating Category")

    delivery_pie = px.pie(filtered, names="Has Online delivery", title="Online Delivery Availability")
    table_pie = px.pie(filtered, names="Has Table booking", title="Table Booking Availability")
    rating_dist = px.histogram(filtered, x="Aggregate rating", nbins=20, title="Ratings Distribution")

    top10 = filtered.sort_values(by="Aggregate rating", ascending=False).head(10).copy()
    top10["Restaurant Name"] = top10.apply(
        lambda row: "⭐ " + row["Restaurant Name"] if row["Aggregate rating"] == 5.0 else row["Restaurant Name"],
        axis=1
    )
    table_data = top10[["Restaurant Name", "City", "Aggregate rating", "Votes"]].to_dict('records')
    table_cols = [{"name": i, "id": i} for i in ["Restaurant Name", "City", "Aggregate rating", "Votes"]]

    return (total_cities, total_rest, avg_rating, avg_votes,
            price_fig, scatter_fig, map_fig,
            delivery_pie, table_pie, rating_dist,
            table_data, table_cols)

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
