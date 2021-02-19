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



def calcule(x,df_recipe_detail_filtred,df_order_detail_filtred):
    
    var = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])&(df_recipe_detail_filtred['no_cumulative']>=x['no_cumulative'])].sort_values(['no_cumulative'],ascending=True).head(1)['receipt_at']
    
    max_reciption = 0
    max_ordred = 0
    max_by_order_product_order = df_order_detail_filtred[(df_order_detail_filtred['order']==x['order'])&(df_order_detail_filtred['product']==x['product'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    max_by_order_product_reciption = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
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
        
        if abs(max_reciption - x['no_cumulative'])>x['ordered_quantity'] :
            
            x['rest_no_all'] = - x['ordered_quantity']
            
        elif max_reciption==0:
            x['rest_no_all'] = - x['ordered_quantity']
            
        else :
            x['rest_no_all'] = max_reciption - x['no_cumulative']
            
    if len(var)!=0:
        x['date_full'] = var.iloc[0]

    else :
        x['date_full'] =  None
    if  x['desired_at']!=None and x['date_full']!=None:
        
        delta = x['desired_at'] - x['date_full']
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
        Output(FIGURE_ORDERSDETAILS_ID, "figure"),
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


    df_order_detail_filtred['no_cumulative'] = df_order_detail_filtred.sort_values(['desired_at'],ascending=True).groupby(['order','product'])['ordered_quantity'].cumsum()

    df_recipe_detail_filtred['no_cumulative'] = df_recipe_detail_filtred.sort_values(['receipt_at'],ascending=True).groupby(['order','receipt','product'])['receipted_quantity'].cumsum()
    df_recipe_detail_filtred = df_recipe_detail_filtred.sort_values(['receipt_at'],ascending=False)

    df_order_detail_filtred = df_order_detail_filtred.apply(lambda x : calcule(x,df_recipe_detail_filtred,df_order_detail_filtred),axis = 1) 


    df = df_order_detail_filtred.groupby(['order','product']).first().reset_index()

    
    figure_pie_order = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    
    if df_order_detail_filtred.size!=0 :


        df_order_detail_filtred = df_order_detail_filtred[df_order_detail_filtred['diff_days'].notnull() ]
        df_order_detail_filtred = df_order_detail_filtred.reset_index(drop=True)
        df_order_detail_filtred.index =df_order_detail_filtred.index + 1

    
        tseries = df_order_detail_filtred['diff_days']
        color = (tseries > 0).apply(lambda x: 'g' if x else 'r')
        print(df_order_detail_filtred)
        figure = df_order_detail_filtred.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            y=['diff_days'],
            theme='white',
            title=_('Statut of order Details'),
            xTitle=_('customer'),
            yTitle=_('Number of Order Details'),
        )

        figure.add_trace(go.Scatter(
                x=[df_order_detail_filtred[df_order_detail_filtred['diff_days']==df_order_detail_filtred['diff_days'].min()].index.tolist()[0]],
                y=[df_order_detail_filtred['diff_days'].min()],
                mode="markers",
                showlegend=False,
                marker=dict(color="yellow",size=10)
            )
        )
        figure.add_trace(go.Scatter(
                x=[df_order_detail_filtred[df_order_detail_filtred['diff_days']==df_order_detail_filtred['diff_days'].max()].index.tolist()[0]],
                y=[df_order_detail_filtred['diff_days'].max()],
                mode="markers",
                showlegend=False,
                marker=dict(color="lightgreen",size=10)
            )
        )

        figure.add_trace(go.Scatter(
                x=[-1,max(df_order_detail_filtred.index.tolist())+1],
                y=[df_order_detail_filtred['diff_days'].mean(),df_order_detail_filtred['diff_days'].mean()],
                mode="lines",
                showlegend=False,
                line = dict(color='firebrick', width=4, dash='dot')
            )
        )


        figure_order = df.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['desired_at'],
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

        fig = df_order_detail_filtred.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            x=['desired_at'],
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
                labels=df_order_detail_filtred['status'],
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
    return figure,figure_pie_order


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
