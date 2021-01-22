
from .app import app
from common.dashboards import  dash_utils
from stock.models import Product, ProductCategory, Customer

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from django.utils.translation import gettext as _
import colorlover
import dash_daq as daq

from .ids import *

_all_products   = list(Product.objects.get_all_products())
_all_categories = list(ProductCategory.objects.get_all_productcategory())
_all_customers  = list(Customer.objects.get_all_customers())
_all_status     = list(Product.objects.get_all_status_of_products())


cs12 = colorlover.scales['12']['qual']['Paired']


def filter_container():
    filter_container = html.Div([

        dbc.Row([
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_CATEGORIE_LIST_ID, DIV_CATEGORIE_LIST_ID, CHECKBOX_CATEGORIE_LIST_ID, _all_categories,
                    'Categories')
            ], sm=12, md=6, lg=4),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_STATUT_LIST_ID, DIV_STATUT_LIST_ID, CHECKBOX_STATUT_LIST_ID, _all_status, 'Status')
            ], sm=12, md=6, lg=4),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_CUSTOMER_LIST_ID, DIV_CUSTOMER_LIST_ID, CHECKBOX_CUSTOMER_LIST_ID, _all_customers,
                    'Customers',select_all=False,multi=False),
                html.Div(id="number-out"),
            ], sm=12, md=6, lg=4),
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
                    dash_utils.get_mini_card(MINI_CARD_SUBTITLE_BIAS_PERCENT_ID,title='OTIF Global',
                                             subtitle=
                                             
                                                dbc.Col([
                                                    dbc.Progress(
                                                        id='400',
                                                        striped=True,
                                                    ),
                                                ]),

                                            )
                ], sm=12, md=4, lg=4),
                dbc.Col([
                    dash_utils.get_mini_card(MINI_CARD_SUBTITLE_MAD_ID, title='Number of Orders ',
                                             subtitle='', icon='fas fa-clipboard-list'),
                ], sm=12, md=4, lg=4),
                dbc.Col([
                    dash_utils.get_mini_card(MINI_CARD_SUBTITLE_MAPE_ID,title='Number of Deliveries',subtitle='',icon='fas fa-dolly')
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
                                                label='Customers',
                                                value='what-is',
                                                children=dcc.Loading(
                                                    html.Div(
                                                        [dcc.Graph(id=FIGURE_CUSTOMER_ID)],
                                                        className="",
                                                    )
                                                ),
                                            ),
                                            dcc.Tab(
                                                label='OTIF',
                                                value='Product',
                                                children=html.Div(
                                                    className='control-tab',
                                                    children=[
                                                        html.Div(
                                                            className='app-controls-block',
                                                            children=dcc.Loading(
                                                                html.Div(
                                                                    [dcc.Graph(id=FIGURE_OTIF_ID)],
                                                                    className="",
                                                                )
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ])
                                ],
                            ),
                            dcc.Store(id='forna-custom-colors-1')
                        ]
                    ),
                ], sm=12, md=6, lg=6),

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
                                                label='OrdersDetails by Date',
                                                value='what-is',
                                                children=dcc.Loading(
                                                    html.Div(
                                                        [dcc.Graph(id=FIGURE_ORDERSDETAILS_ID)],
                                                        className="",
                                                    )
                                                ),
                                            ),
                                            dcc.Tab(
                                                label='Orders',
                                                value='Product-at',
                                                children=html.Div(
                                                    className='control-tab',
                                                    children=[
                                                        html.Div(
                                                            className='app-controls-block',
                                                            children=dcc.Loading(
                                                                html.Div(
                                                                    [dcc.Graph(id=FIGURE_ORDERS_ID)],
                                                                    className="",
                                                                )
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ])
                                ],
                            ),
                        ],
                        className="shadow-lg p-12 mb-5 bg-white rounded",
                    ),
                ], sm=12, md=6, lg=6),
            ]),


            html.Div(
                [
                    dcc.Loading(
                        html.Div(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Graph(id=FIGURE_PIE_ORDERDETAIL_ID)
                                    ], sm=12, md=6, lg=6),
                                    dbc.Col([
                                        dcc.Graph(id=FIGURE_PIE_ORDER_ID)
                                    ], sm=12, md=6, lg=6)
                                ])
                            ],
                            className="pretty_container",
                        ),
                    ),
                ],
                className="shadow-lg p-12 mb-5 bg-white rounded",
            ),

        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )
    return body_container


layout = dash_utils.get_dash_layout(filter_container(), body_container())