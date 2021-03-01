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
from dash.dependencies import Input, Output, State
from django.db import connection
from django.db.models import Case, CharField, DateTimeField,ExpressionWrapper, F, IntegerField, Sum, Value,When,Count
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


IN_FULL_IN_TIME = 'In Full In Time'
IN_FULL_NOT_IN_TIME = 'In Full Not In Time'
PARTIALLY_DELIVERED_NOT_IN_TIME = 'Partially Delivered Not In Time'
PARTIALLY_DELIVERED_IN_TIME = 'Partially Delivered In Time'
NOT_DELIVERED = 'Not Delivered'


def calcule(x,df_recipe_detail_filtred,df_order_detail_filtred):
    
    var = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])&(df_recipe_detail_filtred['no_cumulative']>=x['no_cumulative'])].sort_values(['no_cumulative'],ascending=True).head(1)['receipt_at']
    last_date_reciption = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])].head(1)['receipt_at']
    max_reciption = 0
    max_ordred = 0
    max_by_order_product_order = df_order_detail_filtred[(df_order_detail_filtred['order']==x['order'])&(df_order_detail_filtred['product']==x['product'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    max_by_order_product_reciption = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    max_by_order_product_reciption = df_recipe_detail_filtred[(df_recipe_detail_filtred['order']==x['order'])&(df_recipe_detail_filtred['product']==x['product'])].sort_values(['no_cumulative'],ascending=False).head(1)['no_cumulative']
    if len(max_by_order_product_reciption)!=0:
        max_reciption = max_by_order_product_reciption.iloc[0]
        
    if len(max_by_order_product_order)!=0:
        max_ordred = max_by_order_product_order.iloc[0]
        
    x['rest_totle'] = max_reciption-max_ordred

    if len(last_date_reciption)!=0:
            x['last_date_reception'] = last_date_reciption.iloc[0]

    else :
        x['last_date_reception'] =  None
    
        
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
    x['In_Full_In_Time'] = 0
    x['In_Full_Not_In_Time'] = 0 
    x['Not_Delivered'] = 0
    x['Partially_Delivered_In_Time'] = 0
    x['Partially_Delivered_Not_In_Time'] = 0  
    x['Sum'] = 1
    if delta!=None:
        if delta>=0:
            x['status'] = IN_FULL_IN_TIME
            x['In_Full_In_Time'] = 1
        else :
            x['status'] = IN_FULL_NOT_IN_TIME
            x['In_Full_Not_In_Time'] = 1
    elif x['last_date_reception']!=None :
        if abs(x['rest_no_all']) == x['ordered_quantity']:
            x['status'] = NOT_DELIVERED
            x['Not_Delivered'] = 1
        elif abs(x['rest_no_all']) < x['ordered_quantity']:
            if x['last_date_reception']<=x['desired_at']:                
                x['status'] = PARTIALLY_DELIVERED_IN_TIME
                x['Partially_Delivered_In_Time'] = 1
            else :
                x['status'] = PARTIALLY_DELIVERED_NOT_IN_TIME
                x['Partially_Delivered_Not_In_Time'] = 1
    else :
        x['status'] = NOT_DELIVERED
        x['Not_Delivered'] = 1
    x['diff_days'] = delta

    print(x['diff_days'],'diff')

    
    return x

def count_values(x,value_acceptable,value_risque):

    var = x['diff_days']

    x['ok'] = 0
    x['acceptable'] = 0
    x['risque'] = 0

    if var!=None :
        if var <=0 :
            if abs(var)<=value_acceptable or var==0 :
                x['ok'] = 1
            elif  abs(var)>=value_acceptable and abs(var)<value_risque:
                x['acceptable'] = 1
            else :  
                x['risque'] = 1

    return x

def set_status_of_order(x):

    
    if x['Not_Delivered']==x['Sum']:

        x['status'] = NOT_DELIVERED

    elif x['In_Full_In_Time']==x['Sum']:

        x['status'] = IN_FULL_IN_TIME

    elif x['In_Full_In_Time']+x['In_Full_Not_In_Time']==x['Sum'] and x['In_Full_In_Time']<x['Sum'] :

        x['status'] = IN_FULL_NOT_IN_TIME

    elif x['In_Full_Not_In_Time']==0 and x['Partially_Delivered_Not_In_Time']==0 and x['In_Full_In_Time']<x['Sum'] and  x['Not_Delivered']<x['Sum']:

        x['status'] = PARTIALLY_DELIVERED_IN_TIME

    else :

        x['status'] = PARTIALLY_DELIVERED_NOT_IN_TIME


    return x
_figure_empty = _df_empty.iplot(
    asFigure=True,
    kind='bar',
    barmode='group',
    x=None,
    y=None,
    theme='white',
)

D = []
@app.callback(
    [
        Output(FIGURE_ORDERSDETAILS_BY_CUSTOMER_ID, "figure"),
        Output(FIGURE_ORDERSDETAILS_ID, "figure"),
        Output(FIGURE_OTIF_ID, "figure"),
        Output(FIGURE_ORDERS_ID, "figure"),
        Output(SUBTITLE_OTIF_ID, "children"),
        Output(SUBTITLE_DELIVERIES_ID, "children"),
        Output(SUBTITLE_ORDERS_ID, "children"),
    ],   
    [
        Input(DROPDOWN_PRODUCT_LIST_ID, "value"),
        Input(DROPDOWN_WAREHOUSE_LIST_ID, "value"),
        Input(DROPDOWN_CATEGORIE_LIST_ID, "value"),
        Input(DROPDOWN_SUPPLIER_LIST_ID, "value"),
        Input(INPUT_DATE_RANGE_ID, 'start_date'),
        Input(INPUT_DATE_RANGE_ID, 'end_date'),
        Input(SUBMIT_VALUES, 'n_clicks'),
    ],   
    [
        State(INPUT_ACCEPTABLE_VALUE,'value'),
        State(INPUT_RISQUE_VALUE,'value'),
    ]
)
def plot_figure(selected_products,selected_warehouses,selected_categories,selected_suppliers,start_date,end_date, n_clicks,value_acceptable,value_risque):
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

    colors = ['rgb(127,255,0)', 'yellow', 'red']

    qs_order_detail_filtred = OrderDetail.objects.filter(
        product__in=selected_products,
        product__category__in=selected_categories,
        order__ordered_at__gte=start_date,
        order__supplier__in=selected_suppliers,
        order__ordered_at__lte=end_date
    )

    qs_recipe_detail_filtred = ReceiptDetail.objects.filter(
        product__in=selected_products,
        status='A',
        product__category__in=selected_categories,
        warehouse__in=selected_warehouses,
        receipt__supplier__in=selected_suppliers,
        order__ordered_at__gte=start_date,
        order__ordered_at__lte=end_date
    )

    orders_count = qs_order_detail_filtred.values('order').distinct().count()

    receipts_count = qs_recipe_detail_filtred.values('receipt').distinct().count()

    count_order_details =  qs_order_detail_filtred.distinct().count()
    
    df_recipe_detail_filtred = read_frame(qs_recipe_detail_filtred)

    df_order_detail_filtred = read_frame(qs_order_detail_filtred)

    df_order_detail_filtred['no_cumulative'] = df_order_detail_filtred.sort_values(['desired_at'],ascending=True).groupby(['order','product'])['ordered_quantity'].cumsum()

    df_recipe_detail_filtred['no_cumulative'] = df_recipe_detail_filtred.sort_values(['receipt_at'],ascending=True).groupby(['order','receipt','product'])['receipted_quantity'].cumsum()

    df_recipe_detail_filtred = df_recipe_detail_filtred.sort_values(['receipt_at'],ascending=False)

    df_order_detail_filtred = df_order_detail_filtred.apply(lambda x : calcule(x,df_recipe_detail_filtred,df_order_detail_filtred),axis = 1) 

    df_order_filtred = df_order_detail_filtred.groupby(
        by=['order'],
        as_index=False
    ).agg({
        'In_Full_In_Time':'sum',
        'In_Full_Not_In_Time':'sum',
        'Not_Delivered':'sum',
        'Partially_Delivered_In_Time':'sum',
        'Partially_Delivered_Not_In_Time':'sum',
        'Sum':'sum',
    })

    df_order_filtred = df_order_filtred.apply(lambda x : set_status_of_order(x),axis = 1) 

    df = df_order_detail_filtred.groupby(['order','product']).first().reset_index()

    fig_pie = _figure_empty

    if n_clicks>0 and value_acceptable!=None and value_risque!=None:

        df_order_detail_filtred = df_order_detail_filtred.apply(lambda x : count_values(x,value_acceptable,value_risque),axis = 1) 

        ok_value_count = df_order_detail_filtred['ok'].sum()

        acceptable_value_count = df_order_detail_filtred['acceptable'].sum()

        risque_value_count = df_order_detail_filtred['risque'].sum()

        labels = ['0<valeur<'+str(value_acceptable),str(value_acceptable)+'<value<'+str(value_risque),str(value_risque)+'<value']

        values = [ok_value_count, acceptable_value_count,risque_value_count]

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values,pull=[0.1, 0.2, 0.2, 0.2])])

    if value_acceptable!=None and value_risque!=None:

        df_order_detail_filtred = df_order_detail_filtred.apply(lambda x : count_values(x,value_acceptable,value_risque),axis = 1) 

        ok_value_count = df_order_detail_filtred['ok'].sum()

        acceptable_value_count = df_order_detail_filtred['acceptable'].sum()

        risque_value_count = df_order_detail_filtred['risque'].sum()

        labels = ['0<valeur<'+str(value_acceptable),str(value_acceptable)+'<value<'+str(value_risque),str(value_risque)+'<value']

        values = [ok_value_count, acceptable_value_count,risque_value_count]

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values,pull=[0.1, 0.2, 0.2, 0.2])])


    else : 
        fig_pie = _figure_empty

    fig_pie.update_traces(hoverinfo='label+percent+value', textinfo='value', hole=.4,marker=dict(colors=colors))
    
    figure_pie_order = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])

    figure_pie_order_detail = make_subplots(rows=1, cols=1, specs=[[{'type': 'domain'}]])
    
    if df_order_detail_filtred.size!=0 :

        df_for_pie_graph = df_order_detail_filtred

        df_order_detail_filtred = df_order_detail_filtred[df_order_detail_filtred['diff_days'].notnull()]

        df_order_detail_filtred = df_order_detail_filtred.sort_values(['diff_days'],ascending=False)

        df_order_detail_filtred = df_order_detail_filtred.reset_index(drop=True)

        df_order_detail_filtred.index = df_order_detail_filtred.index + 1
    
        tseries = df_order_detail_filtred['diff_days']

        color = (tseries > 0).apply(lambda x: 'g' if x else 'r')
        
        otif_df = df_for_pie_graph['status'].value_counts()

        otif = 0
        
        if count_order_details!=0:

            otif = (otif_df['In Full In Time']/count_order_details)*100

            otif = round(otif,3)

        figure = df_order_detail_filtred.iplot(
            asFigure=True,
            kind='bar',
            barmode='group',
            y=['diff_days'],
            theme='white',
            showlegend= False,
            title='',
            xTitle=_('lignes de commande'),
            yTitle=_('délai en jours'),
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
                showlegend=True,
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

        figure_pie_order_detail.add_trace(
            go.Pie(
                labels=df_for_pie_graph['status'],
                pull=[0.1, 0.2, 0.2, 0.2],
                name="",
                marker={
                    # 'colors' : [{ 
                    #     NOT_DELIVERED:'#ff0000',
                    #     IN_FULL_IN_TIME:'#ff5050'
                    # }],
                    'colors': [
                        'yellow',
                        'yellow',
                        'yellow',
                        'yellow',
                        'yellow',
                    ]
                },
            )
        , 1, 1)

        figure_pie_order.add_trace(
            go.Pie(
                labels=df_order_filtred['status'],
                pull=[0.1, 0.2, 0.2, 0.2],
                name="",
                marker={
                    'colors' : [{ 
                        '10':'#ff0000',
                        '9':'#ff5050'
                    }],
                    # 'colors': [
                    #     'red',
                    #     'rgb(0, 200, 0)',
                    #     'rgb(0,255,0)',
                    #     'rgb(255, 230, 0)',
                    #     'rgb(255, 132, 0)',
                    # ]
                },
            )
        , 1, 1)
    else :
        
        figure = _figure_empty

    figure_pie_order.update_traces(hole=.4, hoverinfo="label+percent+name+value") 
    figure_pie_order_detail.update_traces(hole=.4, hoverinfo="label+percent+name+value") 
    figure.update_layout(
        autosize=True,
        yaxis=dict(
            tickmode="array",
        )
    )
    return figure,figure_pie_order_detail,fig_pie,figure_pie_order,str(otif)+'%',receipts_count,orders_count


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
