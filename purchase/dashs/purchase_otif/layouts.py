
from .app import app
from common.dashboards import  dash_utils
from stock.models import Product, ProductCategory, Supplier,Warehouse
from purchase.models import OrderDetail, ReceiptDetail,Order

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from django.utils.translation import gettext as _
import colorlover
import dash_table 
# import dash_daq as daq

from .ids import *

_all_products   = list(Product.objects.get_all_products())
_all_categories = list(ProductCategory.objects.get_all_productcategory())
_all_suppliers  = list(Supplier.objects.get_all_suppliers())
_all_status     = list(Product.objects.get_all_status_of_products())
_all_warehouses = list(Warehouse.objects.get_all_warehouses())
_all_orders     = list(Order.objects.get_all_orders())
_all_order_types = list(Order.objects.get_all_order_type_of_orders())
_all_incoterms  = list(Order.objects.get_all_incoterm_of_orders())


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
                    DROPDOWN_ORDER_LIST_ID, DIV_ORDER_LIST_ID, CHECKBOX_ORDER_LIST_ID, _all_orders, _('Orders'))
            ], sm=12, md=6, lg=3),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_ORDER_TYPE_LIST_ID, DIV_ORDER_TYPE_LIST_ID, CHECKBOX_ORDER_TYPE_LIST_ID, _all_order_types, _('Order Type'))
            ], sm=12, md=6, lg=3),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_INCOTERM_LIST_ID, DIV_INCOTERM_LIST_ID, CHECKBOX_INCOTERM_LIST_ID, _all_incoterms, _('Incoterm'))
            ], sm=12, md=6, lg=3),
        ]),
        dbc.Col([
            dash_utils.get_date_range(
                INPUT_DATE_RANGE_ID,
                label=_('Time horizon'),
                year_range=2
            ),
        ], sm=12, md=6, lg=6),
        html.Details([
            html.Summary(_('Suppliers')),
            dbc.Col([
                dash_utils.get_filter_dropdown(
                    DROPDOWN_SUPPLIER_LIST_ID, DIV_SUPPLIER_LIST_ID, CHECKBOX_SUPPLIER_LIST_ID,_all_suppliers, ''),
        ], sm=12, md=12, lg=12),
        ], id=DROPDOWN_SUPPLIER_LIST_ID, open=False),

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

            dbc.Row(
                [
                    dbc.Col([
                        html.Div(
                            id='forna-body-1',
                            className='shadow-lg p-12 mb-5  rounded',
                            children=[
                                html.Div(
                                    id='forna-control-tabs',
                                    className='control-tabs',
                                    children=[
                                        html.Div([
                                            html.Div([
                                                dcc.Loading(
                                                        html.Div(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col([
                                                                        dcc.Graph(id=FIGURE_ORDERSDETAILS_ID)
                                                                    ],sm=12, md=6, lg=6),
                                                                    dbc.Col([
                                                                        dcc.Graph(id=FIGURE_PIE_ORDERDETAIL_ID)

                                                                    ],sm=12, md=6, lg=6)     
                                                                ])

                                                            ],
                                                            className="",
                                                        )
                                                )
                                            ], className='card-body')
                                        ], className='card shadow '),

                                    ],
                                ),
                                dcc.Store(id='forna-custom-colors-1')
                            ]
                        ),
                    ], sm=12, md=12, lg=12),
                    dbc.Col([
                        html.Div(
                            id='forna-body-1',
                            className='shadow-lg p-12 mb-5  rounded',
                            children=[
                                html.Div(
                                    id='forna-control-tabs',
                                    className='control-tabs',
                                    children=[
                                        html.Div([
                                            html.Div([
                                                dcc.Loading(
                                                        html.Div(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col([
                                                                        dcc.Graph(id=FIGURE_ORDERS_ID)
                                                                    ],sm=12, md=6, lg=6),
                                                                    dbc.Col([
                                                                        dcc.Graph(id=FIGURE_PIE_ORDER_ID)

                                                                    ],sm=12, md=6, lg=6)     
                                                                ])
                                                            ],
                                                            className="",
                                                        )
                                                )
                                            ], className='card-body')
                                        ], className='card shadow '),

                                    ],
                                ),
                                dcc.Store(id='forna-custom-colors-1')
                            ]
                        ),
                    ], sm=12, md=12, lg=12),
                ],
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )
    return body_container


layout = dash_utils.get_dash_layout(filter_container(), body_container())