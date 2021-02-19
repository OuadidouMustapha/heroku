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
from stock.models import Product,ProductCategory
from purchase.models import OrderDetail,ReceiptDetail
from .app import app  
from datetime import datetime
import plotly.express as px
from .ids import *


_df_empty = pd.DataFrame(columns=[])

nameSwap = {'not_delivered': 'Not Delivered','Partially Delivered In Time': 'hello!','Partially Delivered Not In Time': 'hello!','Delivered In Time':'hi!','Delivered Not In Time':'hi!'}


FULINTIME = 'Full In Time'
FULNOTINTIME = 'Full Not In Time'
NOTDELIVERED = 'Not Delivered '



def calcule(x,reception_df,orders_df):
    
    var = reception_df[(reception_df['O']==x['O'])&(reception_df['P']==x['P'])&(reception_df['no_cumulative']>=x['no_cumulative'])].sort_values(['no_cumulative'],ascending=True).head(1)['RDate']
    
    max_reciption = 0
    max_ordred = 0
    max_by_order_product_order = orders_df[(orders_df['O']==x['O'])&(orders_df['P']==x['P'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    max_by_order_product_reciption = reception_df[(reception_df['O']==x['O'])&(reception_df['P']==x['P'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    if len(max_by_order_product_reciption)!=0:
        max_reciption = max_by_order_product_reciption.iloc[0]
        
    if len(max_by_order_product_order)!=0:
        max_ordred = max_by_order_product_order.iloc[0]
        
    x['rest_totle'] = max_reciption-max_ordred
    
        
    if x['no_cumulative']<=max_reciption:
        x['rest'] = 0
    else :
        x['rest'] = max_reciption - x['no_cumulative']
         
         
    if x['no_cumulative']<=max_reciption:
        x['rest_no_all'] = 0
        
    else :
        
        if abs(max_reciption - x['no_cumulative'])>x['Q'] :
            
            x['rest_no_all'] = - x['Q']
            
        elif max_reciption==0:
            x['rest_no_all'] = - x['Q']
            
        else :
            x['rest_no_all'] = max_reciption - x['no_cumulative']
            
    if len(var)!=0:
        x['date_full'] = var.iloc[0]

    else :
        x['date_full'] =  None
    if  x['DDate']!=None and x['date_full']!=None:
        
        delta = x['DDate'] - x['date_full']
        delta = delta.days
         
    else :
        delta = None
        
    if delta!=None:
        
        if delta>=0:
            x['status'] = FULINTIME
        else :
            x['status'] = FULNOTINTIME
    else :
        x['status'] = NOTDELIVERED
        
    x['diff_days'] = delta
    return x


_figure_empty = _df_empty.iplot(
    asFigure=True,
    kind='bar',
    barmode='group',
    x=None,
    y=None,
    theme='white',
)
@app.callback(
    [
        Output(FIGURE_ORDERSDETAILS_BY_CUSTOMER_ID, "figure"),
        Output(FIGURE_ORDERS_ID, "figure"),
        Output(FIGURE_PIE_ORDERDETAIL_ID, "figure"),
        Output(FIGURE_OTIF_ID, "figure"),
    ],   
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_WAREHOUSE_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_SUPPLIER_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
    ]
)
def plot_OrderDetails_by_date_figure(selected_products,selected_warehouses,selected_categories,selected_suppliers,start_date,end_date):
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

    qs_order_detail_filtred = OrderDetail.objects.filter(
        product__in=selected_products,
        product__category__in=selected_categories,
        order__ordered_at__gte=start_date,
        order__ordered_at__lte=end_date
    )

    qs_recipe_detail_filtred = ReceiptDetail.objects.filter(
        product__in=selected_products,
        status='A',
        product__category__in=selected_categories,
        warehouse__in=selected_warehouses,
        order__ordered_at__gte=start_date,
        order__ordered_at__lte=end_date
    )

    df_recipe_detail_filtred = read_frame(qs_recipe_detail_filtred)

    df_order_detail_filtred = read_frame(qs_order_detail_filtred)


    orders_df['no_cumulative'] = orders_df.sort_values(['DDate'],ascending=True).groupby(['O','P'])['Q'].cumsum()

    reception_df['no_cumulative'] =reception_df.sort_values(['RDate'],ascending=True).groupby(['O','R','P'])['Q'].cumsum()
    reception_df = reception_df.sort_values(['RDate'],ascending=False)


    orders_df= orders_df.apply(lambda x : calcule(x,reception_df,orders_df),axis = 1) 


    df = orders_df.groupby(['O','P']).first().reset_index()


    print(df)
    
    figure_pie_order = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    
    if orders_df.size!=0 :
        
        figure = orders_df.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['DDate'],
            y=['diff_days'],
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

        figure_order = df.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['DDate'],
            y=['rest_totle'],
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

        fig = orders_df.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['DDate'],
            y=['rest_no_all'],
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
        figure_pie_order.add_trace(
            go.Pie(
                labels=orders_df['status'],
                pull=[0.1, 0.2, 0.2, 0.2],
                name="",
                marker={
                    'colors': [
                        'red',
                        'rgb(0, 200, 0)',
                        'rgb(0,255,0)',
                        'rgb(255, 230, 0)',
                        'rgb(255, 132, 0)',
                    ]
                },
            )
        , 1, 1)
        
    else :
        
        figure = _figure_empty
    figure_pie_order.update_traces(hole=.4, hoverinfo="label+percent+name+value") 
    figure.update_layout(
        autosize=True,
        yaxis=dict(
            tickmode="array",
        )
    )
    return figure,figure_pie_order,fig,figure_order


dash_utils.select_all_callbacks(
    app, DROPDOWN_PRODUCT_LIST_ID, DIV_PRODUCT_LIST_ID, CHECKBOX_PRODUCT_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_SUPPLIER_LIST_ID, DIV_SUPPLIER_LIST_ID, CHECKBOX_SUPPLIER_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_WAREHOUSE_LIST_ID, DIV_WAREHOUSE_LIST_ID, CHECKBOX_WAREHOUSE_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_CATEGORIE_LIST_ID, DIV_CATEGORIE_LIST_ID, CHECKBOX_CATEGORIE_LIST_ID)

dash_utils.select_all_callbacks(
    app, DROPDOWN_STATUT_LIST_ID, DIV_STATUT_LIST_ID, CHECKBOX_STATUT_LIST_ID)
