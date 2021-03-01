import multiprocessing as mp
import resource
import cufflinks as cf
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from common.dashboards import dash_utils
from dash.dependencies import Input, Output
from django.db import connection
from django.db.models import Case, CharField, DateTimeField,ExpressionWrapper, F, IntegerField, Sum, Value,When
from django.utils.translation import gettext as _
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from stock.models import Customer,Delivery,OrderDetail,Product,ProductCategory
from .app import app  
import plotly.express as px
from .ids import *


_df_empty = pd.DataFrame(columns=[])

nameSwap = {'not_delivered': 'Not Delivered','Partially Delivered In Time': 'hello!','Partially Delivered Not In Time': 'hello!','Delivered In Time':'hi!','Delivered Not In Time':'hi!'}

def customLegend(fig, nameSwap):

    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                fig.data[i].name = nameSwap[fig.data[i].name]
    return(fig)

_figure_empty = _df_empty.iplot(
    asFigure=True,
    kind='bar',
    barmode='group',
    x=None,
    y=None,
    theme='white',
)
@app.callback(

    Output(FIGURE_ORDERSDETAILS_BY_CUSTOMER_ID, "figure"),
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_CUSTOMER_LIST_ID, "value"),
        Input(DROPDOWN_ABC_LIST_ID, "value"),
        Input(DROPDOWN_FMR_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
    ]
)
def plot_OrderDetails_by_customer_figure(selected_products, selected_categories,selected_customers,selected_abc,selected_fmr,start_date,end_date):
    """[function that return figure that give status of all orderDetails that made by the filtered customer ]

    Args:
        selected_products ([list[int]]): [description]
        selected_categories ([list[int]]): [description]
        selected_customers ([list[int]]): [description]
        selected_abc ([list[int]]): [description]
        selected_fmr ([list[int]]): [description]
        start_date ([date]): [description]
        end_date ([date]): [description]

    Returns:
        [Figure]: [figure that give status of all orderDetails]
    """

    qs = OrderDetail.objects.get_orderdetails_status_by_customer(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)
    
    df = pd.DataFrame.from_records(qs)
    
    df = df.rename(
            {
                'not_delivered': 'Not Delivered',
                'partially_delivered_in_time': 'Partially Delivered In Time',
                'partially_delivered_not_in_time': 'Partially Delivered Not In Time',
                'delivered_in_time': 'Delivered In Time',
                'delivered_not_in_time': 'Delivered Not In Time',
        },axis=1
    )
    
    
    if df.size!=0:
        
        figure = df.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['customer__reference'],
            y=['Not Delivered', 'Partially Delivered In Time','Partially Delivered Not In Time', 'Delivered In Time', 'Delivered Not In Time'],
            colors= [
                'rgb(255, 0, 0)',
                'rgb(0, 255, 0)',
                'rgb(255, 230, 0)',
                'rgb(0,200,0)',
                'rgb(255, 132, 0)',
            ],
            theme='white',
            title=_('Statut of order Details'),
            xTitle=_('customer'),
            yTitle=_('Number of Order Details'),
        )
        
    else :
        
        figure = _figure_empty
        
    figure.update_layout(
        autosize=True,
        yaxis=dict(
            tickmode="array",
        )
    )
    return figure



@app.callback(
    Output(FIGURE_OTIF_ID, "figure"),
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_CUSTOMER_LIST_ID, "value"),
        Input(DROPDOWN_ABC_LIST_ID, "value"),
        Input(DROPDOWN_FMR_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
    ]
)
def plot_otif_by_date_figure(selected_products, selected_categories, selected_customers,selected_abc,selected_fmr, start_date,end_date):
    """return figure that give the otif by order date made by customer 

    Args:
        selected_products ([list[int]]): [description]
        selected_categories ([list[int]]): [description]
        selected_customers ([list[int]]): [description]
        selected_abc ([list[int]]): [description]
        selected_fmr ([list[int]]): [description]
        start_date ([list[int]]): [description]
        end_date ([list[int]]): [description]

    Returns:
        [figure]: [otif figure]
    """

    qs = OrderDetail.objects.get_orderdetails_status_by_order_date(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)
    
    df = pd.DataFrame.from_records(qs)
    
    # def otif to calcul the otif for each row in data frame
    def otif(row):
        sum = row['not_delivered'] + row['partially_delivered_in_time'] + row['partially_delivered_not_in_time'] + row['delivered_in_time'] + row['delivered_not_in_time']
        if sum != 0:
            return (row['delivered_in_time'] / sum) * 100
        else:
            return 0

    if df.size !=0:
        
        df['OTIF'] = df.apply(
            lambda row: otif(row),
        axis=1)
        
        df = df.rename(
            {
                'not_delivered': 'Not Delivered',
                'partially_delivered_in_time': 'Partially Delivered In Time',
                'partially_delivered_not_in_time': 'Partially Delivered Not In Time',
                'delivered_in_time': 'Delivered In Time',
                'delivered_not_in_time': 'Delivered Not In Time',
            },axis=1
        )
        df =  df.sort_values('order__ordered_at',ascending = True)

        figure = df.iplot(
            asFigure=True,
            x=['order__ordered_at'],
            y=['OTIF'],
            theme='white',
            title=_('OTIF by Ordered Date'),
            xTitle=_('Ordered Date'),
            yTitle=_('OTIF in %'),
        )
        
        figure.update_traces(
            type="scatter",
            mode="lines+markers",
            line=dict(shape="spline", smoothing=1.3),
            marker=dict(
                symbol="diamond-open",
                size=7,
            ),
        )
    else :
        figure = _figure_empty    
    figure.update_xaxes(
            tickformat = '%d %B %Y',
    )
    figure.update_layout(
        autosize=True,
        yaxis=dict(
            tickmode="array",
        )
    )
    return figure

@app.callback(

    Output(FIGURE_ORDERSDETAILS_ID, "figure"),
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_CUSTOMER_LIST_ID, "value"),
        Input(DROPDOWN_ABC_LIST_ID, "value"),
        Input(DROPDOWN_FMR_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
    ]
)
def plot_count_status_of_order_details_by_date_figure(selected_products, selected_categories, selected_customers, selected_abc,selected_fmr, start_date,end_date):
    """[return figure that give the number of Order Detail by statut in each ordred date]

    Args:
        selected_products ([list[int]]): [description]
        selected_categories ([list[int]]): [description]
        selected_customers ([list[int]]): [description]
        selected_abc ([list[int]]): [description]
        selected_fmr ([list[int]]): [description]
        start_date ([list[int]]): [description]
        end_date ([list[int]]): [description]

    Returns:
        [figure]: [order detail figure]
    """


    qs = OrderDetail.objects.get_orderdetails_status_by_order_date(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)
    
    df = pd.DataFrame.from_records(qs)

    df = df.rename(
        {
            'not_delivered': 'Not Delivered',
            'partially_delivered_in_time': 'Partially Delivered In Time',
            'partially_delivered_not_in_time': 'Partially Delivered Not In Time',
            'delivered_in_time': 'Delivered In Time',
            'delivered_not_in_time': 'Delivered Not In Time',
        },axis=1
    )
    
    figure = df.iplot(
        asFigure=True,
        kind='bar',
        barmode='group',
        x=['order__ordered_at'],
        y=['Not Delivered', 'Partially Delivered In Time','Partially Delivered Not In Time', 'Delivered In Time', 'Delivered Not In Time'],
        colors= [
            'rgb(255, 0, 0)',
            'rgb(0, 255, 0)',
            'rgb(255, 230, 0)',
            'rgb(0,200,0)',
            'rgb(255, 132, 0)',
        ],
        theme='white',
        title=_('Order Details by date'),
        xTitle=_('date'),
        yTitle=_('Number of Order Details'),
    )
    
    figure = customLegend(fig=figure,nameSwap=nameSwaps)

    figure.update_xaxes(
        tickformat = '%d %B %Y',
    )

    figure.update_layout(
        autosize=True,
        yaxis=dict(
            tickmode="array",
        )
    )
        
        
    figure = figure

    return figure

@app.callback(

    Output(FIGURE_ORDERS_ID, "figure"),
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_CUSTOMER_LIST_ID, "value"),
        Input(DROPDOWN_ABC_LIST_ID, "value"),
        Input(DROPDOWN_FMR_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
    ]
)
def plot_count_status_of_order_by_order_date_figure(selected_products, selected_categories, selected_customers, selected_abc,selected_fmr, start_date,end_date):
    """[return figure that show the number of orders by status in each date ]

    Args:
        selected_products ([list[int]]): [description]
        selected_categories ([list[int]]): [description]
        selected_customers ([list[int]]): [description]
        selected_abc ([list[int]]): [description]
        selected_fmr ([list[int]]): [description]
        start_date ([list[int]]): [description]
        end_date ([list[int]]): [description]

    Returns:
        [figure]: [order detail figure]
    """

    qs = OrderDetail.objects.get_order_status_by_order_date(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)
    
    df = read_frame(qs)
    
    if df.size!=0 :
        
        df = df.groupby(
            by=['order__ordered_at'],
            as_index=False
        ).agg({
            'order_partially_delivered_not_in_time':'sum',
            'order_delivered_in_time':'sum',
            'order_delivered_not_in_time':'sum',
            'order_partially_delivered_in_time':'sum',
            'order_not_delivered':'sum',
        })
        
        df = df.rename(
            {
                'order_not_delivered': 'Order Not Delivered',
                'order_partially_delivered_in_time': 'Order Partially Delivered In Time',
                'order_partially_delivered_not_in_time': 'Order Partially Delivered Not In Time',
                'order_delivered_in_time': 'Order Delivered In Time',
                'order_delivered_not_in_time': 'Order Delivered Not In Time',
            },axis=1
        )
        
        figure = df.iplot(
            asFigure=True,
            kind='bar',
            barmode='stack',
            x=['order__ordered_at'],
            y=[
                'Order Partially Delivered Not In Time',
                'Order Delivered In Time',
                'Order Delivered Not In Time',
                'Order Partially Delivered In Time',
                'Order Not Delivered'
            ],
            colors= [
                    'rgb(255, 230, 0)',
                    'rgb(0, 200, 0)',
                    'rgb(255, 132, 0)',
                    'rgb(0,255,0)',
                    'rgb(255, 0, 0)',
            ],
            theme='white',
            title=_('Number of Orders by Date'),
            xTitle=_('Ordered Date'),
            yTitle=_('Number of Orders'),
        )
        
        figure.update_xaxes(
                tickformat = '%d %B %Y',
        )
        
    else:
        figure = _figure_empty

    return figure
#
#
# @app.callback(

#     [
#         Output(FIGURE_PIE_ORDERDETAIL_ID, "figure"),
#         Output(FIGURE_PIE_ORDER_ID, "figure"),
#         Output(SUBTITLE_DELIVERIES_ID, 'children'),
#         Output(SUBTITLE_ORDERS_ID, 'children'),
#         Output(SUBTITLE_OTIF_ID, 'children'),
#     ],
#     [
#         Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
#         Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
#         Input(DROPDOWN_CUSTOMER_LIST_ID, "value"),
#         Input(DROPDOWN_ABC_LIST_ID, "value"),
#         Input(DROPDOWN_FMR_LIST_ID, "value"),
#         Input(INPUT_DATE_RANGE_ID, 'start_date'),
#         Input(INPUT_DATE_RANGE_ID, 'end_date'),
#     ]
# )
# def plot_statuts_of_orders_and_orderdetails_pie_figures(selected_products, selected_categories, selected_customers, selected_abc,selected_fmr,
#                                     start_date, end_date):

#     qs_orderdetails_filtred = OrderDetail.objects.get_orderdetails_by_filters(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)

#     Number_of_deliveries  = qs_orderdetails_filtred.values('order__delivery').distinct()
    
#     Number_of_deliveries  = Number_of_deliveries.count()
       
#     qs_order = OrderDetail.objects.get_order_status(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)
    
#     df_data_order = read_frame(qs_order)

#     Number_of_orders = len(df_data_order.index)
    
#     if df_data_order.size!=0:
#         df_data_order = df_data_order.rename(
#             {
#                 'order_not_delivered': 'Order Not Delivered',
#                 'order_partially_delivered_in_time': 'Order Partially Delivered In Time',
#                 'order_partially_delivered_not_in_time': 'Order Partially Delivered Not In Time',
#                 'order_delivered_in_time': 'Order Delivered In Time',
#                 'order_delivered_not_in_time': 'Order Delivered Not In Time',
                
#             },axis=1
#         )
#         df_data_order = df_data_order.agg({
#             'Order Not Delivered': 'sum',
#             'order_delivered_in_time':'sum',
#             'order_partially_delivered_in_time':'sum',
#             'order_partially_delivered_not_in_time': 'sum',
#             'order_delivered_not_in_time': 'sum',
#         }).reset_index()
        

    
#     qs_order_details = OrderDetail.objects.get_sum_of_orderdetails_by_status(selected_products, selected_categories, selected_fmr, selected_abc, [selected_customers], start_date=start_date, end_date=end_date)

#     df_data_orderdetails = read_frame(qs_order_details)

#     labels = df_data_orderdetails.index
#     values = df_data_orderdetails.values
#     if df_data_orderdetails.size!=0:
#         # Show the pie graph that gives the number status of all order details made by the customer  
#         df_data_orderdetails = df_data_orderdetails.rename(
#             {
#                 'not_delivered': 'Not Delivered',
#                 'partially_delivered_in_time': 'Partially Delivered In Time',
#                 'partially_delivered_not_in_time': 'Partially Delivered Not In Time',
#                 'delivered_in_time': 'Delivered In Time',
#                 'delivered_not_in_time': 'Delivered Not In Time',
#             },axis=1
#         ).reset_index()
        
        
#         df_data_orderdetails = df_data_orderdetails.agg({
#             'Not Delivered': 'sum',
#             'Delivered In Time': 'sum',
#             'Partially Delivered In Time': 'sum',
#             'Partially Delivered Not In Time': 'sum',
#             'Delivered Not In Time': 'sum',
#         }).reset_index()

#         sum_all = df_data_orderdetails[0][0]+df_data_orderdetails[0][1]+df_data_orderdetails[0][2]+df_data_orderdetails[0][3]+df_data_orderdetails[0][4]

#         if sum_all!=0:

#             OTIF = (df_data_orderdetails[0][1]/sum_all)*100

#         else:
#             OTIF = 0

#         OTIF = round(OTIF, 1)
        
#     else :
#         OTIF = 0

#     figure_pie_orderDetail = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
#     figure_pie_order =  make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])

#     if df_data_order.size!=0:
        
#         ## Show the pie graph that gives the number status of all order  made by the customer  
        
#         figure_pie_order.add_trace(
#             go.Pie(
#                 labels=df_data_order['index'],
#                 values=df_data_order[0],
#                 pull=[0.1, 0.2, 0.2, 0.2],
#                 name="",
#                 marker={
#                     'colors': [
#                         'red',
#                         'rgb(0, 200, 0)',
#                         'rgb(0,255,0)',
#                         'rgb(255, 230, 0)',
#                         'rgb(255, 132, 0)',
#                     ]
#                 },
#             )
#         , 1, 1)
        
#     else :
        
#         figure_pie_order
        
#     if df_data_orderdetails.size!=0:
        
#         figure_pie_orderDetail.add_trace(
#             go.Pie(
#                 labels=df_data_orderdetails['index'],
#                 values=df_data_orderdetails[0],
#                 pull=[0.1, 0.2, 0.2, 0.2],
#                 name="",
#                 marker={
#                     'colors': [
#                         'red',
#                         'rgb(0, 200, 0)',
#                         'rgb(0,255,0)',
#                         'rgb(255, 230, 0)',
#                         'rgb(255, 132, 0)',
#                     ]
#                 },
#             )
#         , 1, 1)
#     else :
        
#         figure_pie_orderDetail
        
#     figure_pie_orderDetail.update_traces(hole=.4, hoverinfo="label+percent+name")
#     figure_pie_order.update_traces(hole=.4, hoverinfo="label+percent+name")
    

#     return figure_pie_orderDetail,figure_pie_order,Number_of_deliveries,Number_of_orders,str(OTIF)+'%'


dash_utils.select_all_callbacks(
    app, DROPDOWN_PRODUCT_LIST_ID, DIV_PRODUCT_LIST_ID, CHECKBOX_PRODUCT_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_CUSTOMER_LIST_ID, DIV_CUSTOMER_LIST_ID, CHECKBOX_CUSTOMER_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_ABC_LIST_ID, DIV_ABC_LIST_ID, CHECKBOX_ABC_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_FMR_LIST_ID, DIV_FMR_LIST_ID, CHECKBOX_FMR_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_CATEGORIE_LIST_ID, DIV_CATEGORIE_LIST_ID, CHECKBOX_CATEGORIE_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_STATUT_LIST_ID, DIV_STATUT_LIST_ID, CHECKBOX_STATUT_LIST_ID)
