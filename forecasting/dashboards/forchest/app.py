from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

app = DjangoDash('Forchest', add_bootstrap_links=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
