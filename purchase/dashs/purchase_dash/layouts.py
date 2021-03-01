
from .app import app
from common.dashboards import  dash_utils
from stock.models import Product, ProductCategory, Supplier,Warehouse

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from django.utils.translation import gettext as _
import colorlover
# import dash_daq as daq

from .ids import *

_all_products   = list(Product.objects.get_all_products())
_all_categories = list(ProductCategory.objects.get_all_productcategory())
_all_suppliers  = list(Supplier.objects.get_all_suppliers())
_all_status     = list(Product.objects.get_all_status_of_products())
_all_warehouses = list(Warehouse.objects.get_all_warehouses())


cs12 = colorlover.scales['12']['qual']['Paired']


def filter_container():
    filter_container = html.Div([

        dbc.Row([
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_CATEGORIE_LIST_ID, DIV_CATEGORIE_LIST_ID, CHECKBOX_CATEGORIE_LIST_ID, _all_categories,
                    _('Categories'))
            ], sm=12, md=6, lg=3),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_WAREHOUSE_LIST_ID, DIV_WAREHOUSE_LIST_ID, CHECKBOX_WAREHOUSE_LIST_ID, _all_warehouses, _('Warehouses'))
            ], sm=12, md=6, lg=3),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_SUPPLIER_LIST_ID, DIV_SUPPLIER_LIST_ID, CHECKBOX_SUPPLIER_LIST_ID,_all_suppliers,
                    _('Suppliers')),
                html.Div(id="number-out"),
            ], sm=12, md=6, lg=6),
            dbc.Col([
                dash_utils.get_date_range(
                    INPUT_DATE_RANGE_ID,
                    label=_('Time horizon'),
                    year_range=2
                ),
            ], sm=12, md=6, lg=6),
        ]),

        html.Details([
            html.Summary(_('Products')),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_PRODUCT_LIST_ID, DIV_PRODUCT_LIST_ID, CHECKBOX_PRODUCT_LIST_ID, _all_products, '')
            ], sm=12, md=12, lg=12),
        ], id=DETAILS_PRODUCT_LIST_ID, open=False),


    ])
    return filter_container


def body_container():
    body_container = html.Div(
        [

            dbc.Row([
                dbc.Col([
                    dash_utils.get_mini_card_profil(MINI_CARD_SUBTITLE_BIAS_PERCENT_ID,title=_('OTIF Global'),id_subtitle=SUBTITLE_OTIF_ID,icon="fas fa-tachometer-alt"
                                            #  subtitle=
                                            #     [html.Br(),
                                            #     dbc.Col([
                                            #         dbc.Progress(
                                            #             id='400',
                                            #             striped=True,
                                            #         ),
                                            #     ])],icon="fas fa-tachometer-alt"
                                            ,subtitle='')
                ], sm=12, md=4, lg=4),
                dbc.Col([
                    dash_utils.get_mini_card_profil(MINI_CARD_SUBTITLE_MAD_ID, title=_('Number of Orders '),id_subtitle=SUBTITLE_ORDERS_ID,
                                             subtitle='', icon='fas fa-clipboard-list'),
                ], sm=12, md=4, lg=4),
                dbc.Col([
                   dash_utils.get_mini_card_profil(MINI_CARD_SUBTITLE_MAPE_ID,title=_('Number of Deliveries'),subtitle='',id_subtitle=SUBTITLE_DELIVERIES_ID,icon='fas fa-dolly')
                ], sm=12, md=4, lg=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id='forna-body-1',
                        className='shadow-lg p-12 mb-5  rounded',
                        children=[
                            html.Div(
                                id='forna-control-tabs',
                                className='control-tabs',
                                children=[
                                    dcc.Tabs(
                                        id='forna-tabs',
                                        value='what-is',
                                        children=[
                                            dcc.Tab(
                                                label=_('délai en jours  des lignes de commande par fournisseurs'),
                                                value='what-is',
                                                children=dcc.Loading(
                                                    html.Div(
                                                        [dcc.Graph(id=FIGURE_ORDERSDETAILS_BY_CUSTOMER_ID)],
                                                        className="",
                                                    )
                                                ),
                                            ),
                                        ])
                                ],
                            ),
                            dcc.Store(id='forna-custom-colors-1')
                        ]
                    ),
                ], sm=12, md=6, lg=6),
                dbc.Col([
                    dbc.Col([
                        html.Div(
                            [
                                html.Div(
                                    id='forna-control-tabs-2',
                                    className='control-tabs',
                                    children=[
                                        dcc.Tabs(
                                            id='forna-tabs-1',
                                            value='what-is',
                                            children=[
                                                dcc.Tab(
                                                    label=_('Classification des lignes de commande'),
                                                    value='what-is',
                                                    children=dcc.Loading(
                                                        html.Div(
                                                            [   
                                                                dbc.Row([
                                                                    dbc.Col([
                                                                        html.Div([
                                                                            dbc.Form(
                                                                                [
                                                                                    dbc.Row([
                                                                                        dbc.Col([
                                                                                            html.Div([
                                                                                                dbc.FormGroup(
                                                                                                    [
                                                                                                        dbc.Label("Valeur Max:",
                                                                                                                className="mr-4 my-12",
                                                                                                                style={
                                                                                                                    'margin-left': 10,
                                                                                                                },
                                                                                                                ),
                                                                                                        dbc.Input(
                                                                                                            id=INPUT_RISQUE_VALUE,
                                                                                                            type="number",
                                                                                                            value=700,
                                                                                                            style={
                                                                                                                'color': 'black',
                                                                                                                'text-align': 'center',
                                                                                                                'fontStyle': 'oblique',
                                                                                                                'fontWeight': 'bold',
                                                                                                                'margin-left': 10,
                                                                                                            }
                                                                                                        ),
                                                                                                    ],
                                                                                                    className="",
                                                                                                ),
                                                                                            ])
                                                                                        ], sm=12, md=12, lg=12),
                                                                                    ]),
                                                                                    dbc.Row([
                                                                                        dbc.Col([
                                                                                                dbc.FormGroup(
                                                                                                    [
                                                                                                        dbc.Label(
                                                                                                            "Valeur Min : ",
                                                                                                            style={
                                                                                                                'margin-left': 10,
                                                                                                            },
                                                                                                            className="mr-2"),
                                                                                                        dbc.Input(
                                                                                                            id=INPUT_ACCEPTABLE_VALUE,
                                                                                                            type="number",
                                                                                                            value=10,
                                                                                                            style={
                                                                                                                'color': 'black',
                                                                                                                'text-align': 'center',
                                                                                                                'fontStyle': 'oblique',
                                                                                                                'margin-left': 10,
                                                                                                                'fontWeight': 'bold',
                                                                                                            }
                                                                                                        ),
                                                                                                    ],
                                                                                                    className="",
                                                                                                ),
                                                                                        ], sm=12, md=12, lg=12)
                                                                                    ]),

                                                                                    dbc.Button(
                                                                                        "Calculer",
                                                                                        id=SUBMIT_VALUES,
                                                                                        color="black",
                                                                                        className="mx-3 my-3 btn btn-primary",
                                                                                        # style={
                                                                                        #     'width': '200px',
                                                                                        #     'margin-left': 60,
                                                                                        #     'margin': 30,
                                                                                        #     'color': 'black',
                                                                                        # },
                                                                                        n_clicks=0
                                                                                    ),
                                                                                ],
                                                                                inline=True,
                                                                            ),
                                                                        ]),
                                                                    ],sm=12, md=4, lg=4),
                                                                    dbc.Col([
                                                                        dcc.Graph(id=FIGURE_OTIF_ID)
                                                                    ],sm=12, md=8, lg=8),
                                                                ])
                                                            ],
                                                            className="",
                                                        )
                                                    ),
                                                ),
                                            ])
                                    ],
                                ),
                            ],
                            className="shadow-lg p-12 mb-5 bg-white rounded",
                        ),
                    ]),
                ],sm=12, md=6, lg=6),
            ]),
            dbc.Row(
                [
                    dbc.Col([
                        html.Div(
                            [
                                html.Div(
                                    id='forna-control-tabs-2',
                                    className='control-tabs',
                                    children=[
                                        dcc.Tabs(
                                            id='forna-tabs-1',
                                            value='what-is',
                                            children=[
                                                dcc.Tab(
                                                    label=_('État des lignes de commande'),
                                                    value='what-is',
                                                    children=dcc.Loading(
                                                        html.Div(
                                                            [dcc.Graph(id=FIGURE_ORDERSDETAILS_ID)],
                                                            className="",
                                                        )
                                                    ),
                                                ),
                                            ])
                                    ],
                                ),
                            ],
                            className="shadow-lg p-12 mb-5 bg-white rounded",
                        ),
                    ],sm=12, md=6, lg=6),
                    dbc.Col([
                        html.Div(
                            [
                                html.Div(
                                    id='forna-control-tabs-2',
                                    className='control-tabs',
                                    children=[
                                        dcc.Tabs(
                                            id='forna-tabs-1',
                                            value='what-is',
                                            children=[
                                                dcc.Tab(
                                                    label=_('État des commandes'),
                                                    value='what-is',
                                                    children=dcc.Loading(
                                                        html.Div(
                                                            [dcc.Graph(id=FIGURE_ORDERS_ID)],
                                                            className="",
                                                        )
                                                    ),
                                                ),
                                            ])
                                    ],
                                ),
                            ],
                            className="shadow-lg p-12 mb-5 bg-white rounded",
                        ),
                    ],sm=12, md=6, lg=6),
                ],
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )
    return body_container


layout = dash_utils.get_dash_layout(filter_container(), body_container())