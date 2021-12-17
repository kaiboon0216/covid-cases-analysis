import streamlit as st 
import numpy as np
import pandas as pd
import altair as alt 
from streamlit_folium import folium_static
import folium
from matplotlib import dates
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from PIL import Image 
import altair as alt 
import folium
import geopandas as gp
#EDA code
cases_mysia_url = 'cases_malaysia.csv'
df_cases_mysia = pd.read_csv(cases_mysia_url)
test_mysia_url = 'tests_malaysia.csv'
df_test_mysia = pd.read_csv(test_mysia_url)
clusters_url = 'clusters.csv'
df_clusters = pd.read_csv(clusters_url)
cases_state_url = 'cases_state.csv'
df_cases_state = pd.read_csv(cases_state_url)
test_state_url = 'tests_state.csv'
df_test_state = pd.read_csv(test_state_url)

t = pd.DataFrame(df_test_mysia.isna().sum(),columns =['Testing_Malaysia missing value'])
t1 = pd.DataFrame(df_test_state.isna().sum(),columns =['Testing_state missing value'])
t2 = pd.DataFrame(df_cases_mysia.isna().sum(),columns =['Cases_Malaysia missing value'])
t3 = pd.DataFrame(df_cases_state.isna().sum(),columns =['Cases_State missing value'])
t4 = pd.DataFrame(df_clusters.isna().sum(),columns =['Cluster missing value'])

df_msia=df_cases_mysia.merge(df_test_mysia, left_on=['date'], right_on=['date'], how='left')
df_state=df_cases_state.merge(df_test_state, left_on=['date','state'], right_on=['date','state'], how='left')

df_msia.fillna(0,inplace=True)
df_state.fillna(0,inplace=True)

df_msia["year_month"] = pd.to_datetime(df_msia["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
df_state["year_month"] = pd.to_datetime(df_state["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
df_msia["month"] = pd.to_datetime(df_msia["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%m'))
df_msia["year"] = pd.to_datetime(df_msia["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y'))
df_state["month"] = pd.to_datetime(df_state["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%m'))
df_state["year"] = pd.to_datetime(df_state["date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y'))
df_clusters["a_month"] = pd.to_datetime(df_clusters["date_announced"], format='%Y-%m-%d').apply(lambda x: x.strftime('%m'))
df_clusters["a_year"] = pd.to_datetime(df_clusters["date_announced"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y'))
df_clusters["a_year_month"] = pd.to_datetime(df_clusters["date_announced"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))

#-------------------------------------------------------------------------------------------------------------------------------------------#
st.set_page_config(layout="wide")
question1 = '<p style="font-family:Time-New-Roman; font-size: 24px;">Question 1 -EDA</p>' 
st.markdown(question1, unsafe_allow_html=True)

t = pd.DataFrame(df_test_mysia.isna().sum(),columns =['missing value'])
t1 = pd.DataFrame(df_test_state.isna().sum(),columns =['missing value'])
t2 = pd.DataFrame(df_cases_mysia.isna().sum(),columns =['missing value'])
t3 = pd.DataFrame(df_cases_state.isna().sum(),columns =['missing value'])
t4 = pd.DataFrame(df_clusters.isna().sum(),columns =['missing value'])


title1 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Missing values</p>' 
st.markdown(title1, unsafe_allow_html=True)
text1 = '<p style="font-family:Time-New-Roman;  font-size: 15px;">\nMost of the dataset does not have missing values, only the cases_malaysia dataset contains a lot of missing values in the cluster category column. Below is the output:</p>'
st.markdown(text1, unsafe_allow_html=True)   

left_column, right_column ,right_mid ,t_column= st.columns([4,4,2,3])
with left_column:
    text5 = '<p style="font-family:Time-New-Roman;font-size: 13px;">Cluster dataset</p>' 
    st.markdown(text5, unsafe_allow_html=True)
    t4 
         
with right_column:
    text3 = '<p style="font-family:Time-New-Roman;font-size: 13px;">Cases in State of Malaysia dataset</p>' 
    st.markdown(text3, unsafe_allow_html=True)
    t2
with right_mid:
    text = '<p style="font-family:Time-New-Roman; font-size: 13px;">Testing in Malaysia dataset</p>' 
    st.markdown(text, unsafe_allow_html=True)
    t
    text2 = '<p style="font-family:Time-New-Roman;  font-size: 13px;">Testing in State of Malaysia dataset</p>' 
    st.markdown(text2, unsafe_allow_html=True)
    t1   
with t_column: 
    text4 = '<p style="font-family:Time-New-Roman;  font-size: 13px;">Cases in Malaysia dataset</p>' 
    st.markdown(text4, unsafe_allow_html=True)
    t3  
    
title2 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Relationship between recovered cases and new cases every day.</p>' 
st.markdown(title2, unsafe_allow_html=True)


left_column, right_column= st.columns([5,2])
with left_column:
    df2 = pd.DataFrame(data = df_msia, columns = ['date','cases_new','cases_recovered'])
    df2 = df2.melt('date', var_name='type',  value_name='vals')
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="date", y="vals", hue='type', data=df2)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_cases_mysia['date'].unique()[0]+" to "+df_cases_mysia['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False)
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
    
with right_column:
    text2 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Based on the line plot above, we can see that both cases have kept increasing since 2020-01-25 until now. We can see that the recovered cases will increase after the day the new cases increase.</p>'
    st.markdown(text2, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    sum_my =pd.DataFrame(data = df_msia,columns = ['year_month','cases_new','cases_recovered'])
    sum_my = sum_my.melt('year_month', var_name='type',  value_name='values')
    sum_my =sum_my.groupby(['year_month','type']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="year_month", y="values", hue='type', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)    
    
with right_column:
    text3 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">To view the line plot more clearly, there is a line plot that shows the relationship between recovered cases and new cases per month. Based on the plot below, we know that August 2021 has the highest number of new cases and recovered cases. Besides, the recovered cases will increase after the month that the new cases increase.</p>'
    st.markdown(text3, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    sum_my = df_msia.loc[df_msia['year']=='2020']
    sum_my =pd.DataFrame(data = sum_my,columns = ['year_month','cases_new','cases_recovered'])
    sum_my = sum_my.melt('year_month', var_name='type',  value_name='values')
    sum_my =sum_my.groupby(['year_month','type']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="year_month", y="values", hue='type', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)    
    
with right_column:
    text4 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Since the data of cases from 2020 cannot be viewed clearly, below present the graph that only shows the relationship between recovered cases and new cases in 2020. In this graph, we observed that the cases start to increase slightly during the MCO and decreasing slowly until the RMCO phase 1 and it increase rapidly during the RMCO phase 2 which is in September 2020.</p>'
    st.markdown(text4, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    sum_my = df_msia.loc[df_msia['year']=='2021']
    sum_my =pd.DataFrame(data = sum_my,columns = ['year_month','cases_new','cases_recovered'])
    sum_my = sum_my.melt('year_month', var_name='type',  value_name='values')
    sum_my =sum_my.groupby(['year_month','type']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="year_month", y="values", hue='type', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)   
    
with right_column:
    text5 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Besides, In the graph that only shows the cases data in 2021, we observe that the cases are slightly decreasing in March of 2021 but start increasing during April of 2021 and increase rapidly in June of 2021. Fortunately, the cases in September of 2021 are decreasing very rapidly based on our observation.</p>'
    st.markdown(text5, unsafe_allow_html=True)

title3 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Relationship between local cases and import cases every day.</p>' 
st.markdown(title3, unsafe_allow_html=True)

left_column, right_column= st.columns([2,5])
with left_column:
    text6 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In this line plot, we observe that the number of imported cases does not affect the new cases of Malaysia every day, only the local cases are increasing until now. To see more clearly the imported cases data, we had plotted a line graph that only presents the imported cases. </p>'
    st.markdown(text6, unsafe_allow_html=True) 

with right_column:
    #relationship between recovered cases, import cases
    df_msia['cases_local'] = df_msia['cases_new'] - df_msia['cases_import']
    df2 = pd.DataFrame(data = df_msia, columns = ['date','cases_import','cases_local'])
    df2 = df2.melt('date', var_name='type',  value_name='vals')
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="date", y="vals", hue='type', data=df2)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_cases_mysia['date'].unique()[0]+" to "+df_cases_mysia['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False) 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)


left_column, right_column= st.columns([2,5])
with left_column:
    text6_1 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;"> In this line plot, we know that the highest number of the imported cases is just only 70+ cases per day. As a Malaysian, we know that Malaysia is restricted tourism from other countries since 2020 March, only some can visit Malaysia for some reason like work and study, etc after 14 days of quarantine. So, the imported cases do not affect the new cases of Malaysia.</p>'
    st.markdown(text6_1 , unsafe_allow_html=True)

with right_column:
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="date", y="cases_import", data=df_msia)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_cases_mysia['date'].unique()[0]+" to "+df_cases_mysia['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False) 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)


title4 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Outliers of new cases, recovered cases, and new cases in the pandemic</p>' 
st.markdown(title4, unsafe_allow_html=True)

text7 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Below is the boxplot of the recovered cases, new cases, and import cases in the whole timeline of the pandemic. Based on the boxplot below, we found that there are a lot of upper outliers in these boxplots. These 3 boxplots are skewed to the right. New cases and recovered cases have a very wide range which is 0 to 25000, but import cases boxplot only in 0- 70 range which is not a wide range.</p>'
st.markdown(text7, unsafe_allow_html=True)

left_column,middle_column, right_column = st.columns(3)
with left_column:
    plt.figure(figsize=(10,3))
    g=sns.boxplot(df_msia['cases_new'])
    g.set(xlabel=None) 
    g.set(ylabel="New Cases")
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
with middle_column:
    plt.figure(figsize=(10,3))
    g=sns.boxplot(df_msia['cases_recovered'])
    g.set(xlabel=None) 
    g.set(ylabel="Recovered Cases") 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
with right_column:
    plt.figure(figsize=(10,3))
    g=sns.boxplot(df_msia['cases_import'])
    g.set(xlabel=None) 
    g.set(ylabel="Import Cases") 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

title5 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-align: justify;text-decoration: underline">Comparison between 2020 and 2021</p>' 
st.markdown(title5, unsafe_allow_html=True)

left_column, right_column= st.columns(2)
with left_column:
    sum_my =pd.DataFrame(data = df_msia,columns= ['year_month','cases_new','year','month'])
    sum_my =sum_my.groupby(['year_month','year','month']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="month", y="cases_new", hue='year', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text8 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">This graph presents that the new cases of 2021 are highly more than the cases from 2020 especially the new cases in August of 2020 and 2021. New cases from all the months of 2021 are more than new cases for the whole year of 2020. Based on the observation, we maybe will estimate that the new cases of 2021 will still increase after September, it is because the new cases of 2020 increase a lot since September.</p>'
    st.markdown(text8, unsafe_allow_html=True)

left_column, right_column= st.columns(2)
with left_column:
    sum_my =pd.DataFrame(data = df_msia ,columns = ['year_month','cases_import','year','month'])
    sum_my =sum_my.groupby(['year_month','year','month']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="month", y="cases_import", hue='year', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text9 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">The graph above shows that the comparison of the imported cases between 2020 and 2021. In this graph, we know that the import cases are decreasing after the MCO in March 2020 and do increase slightly only after April 2020. In 2021, the imported cases are floating and it increases rapidly in June 2021 and it seems to decrease rapidly in September 2021.</p>'
    st.markdown(text9, unsafe_allow_html=True)



left_column, right_column= st.columns(2)
with left_column:
    sum_my =pd.DataFrame(data = df_msia ,columns = ['year_month','cases_recovered','year','month'])
    sum_my =sum_my.groupby(['year_month','year','month']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=1000)
    g=sns.lineplot(x="month", y="cases_recovered", hue='year', data=sum_my)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text10 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">Besides, there is a graph showing the recovered cases in 2020 and 2021. We observe that the recovered cases in 2021 are highly more than the recovered cases in 2020 which is the same as the new cases in 2020 and 2021. So, we conclude that the higher the new cases, the higher the recovered cases based on the observation in these graphs.</p>'
    st.markdown(text10, unsafe_allow_html=True)

title6 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-align: justify;text-decoration: underline">Comparison of the cases between every state in Malaysia</p>' 
st.markdown(title6, unsafe_allow_html=True)

plt.figure(figsize=(20,8))
plt.xticks(rotation=30)
g =sns.lineplot(x="date", y="cases_new", hue='state', data=df_state)
g.set(xticklabels=[])  
g.set(xlabel='Date from '+df_state['date'].unique()[0]+" to "+df_state['date'].unique()[-1]) 
g.set(ylabel='Cases')  
g.tick_params(bottom=False) 
g=st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(g)

text11 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Based on the line graph above shows that the new cases in every state of Malaysia by day. It seems very messy because Malaysia contains 13 states and 3 wilayah but we found that Selangor has the highest number of cases in almost 60% of the timeline of the Malaysia pandemic but it decreases in this time and was replaced by Sarawak. Sarawak has increased rapidly in this time. To see more clearly, a graph that shows the news cases in every state of Malaysia by month is created.</p>'
st.markdown(text11, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    sumdf=df_state.groupby(['year_month','state']).sum()
    plt.figure(figsize=(20,8))
    plt.xticks(rotation=30)
    g=sns.lineplot(x="year_month", y="cases_new", hue='state', data=sumdf)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text12 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In this graph, we can see that Sarawak has lead with the highest number of new cases in September 2020 and it take place by Selangor in November 2020. Then, both states have a switchback in September 2021. During the switchback of both states, we can know that the cases of Selangor are decreasing at an incredible speed.</p>'
    st.markdown(text12, unsafe_allow_html=True)

plt.figure(figsize=(30,10))
plt.xticks(rotation=30)
g =sns.lineplot(x="date", y="cases_import", hue='state', data=df_state)
g.set(xticklabels=[])  
g.set(xlabel='Date from '+df_state['date'].unique()[0]+" to "+df_state['date'].unique()[-1]) 
g.set(ylabel='Cases')  
g.tick_params(bottom=False)
g=st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(g)

text13 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">Next, a graph that presents the imported cases in every state of Malaysia by day is shown. In this graph, we observe that Negeri Sembilan has the highest imported cases in one day through the whole timeline of the Malaysia pandemic. Besides, Johor and W.P. Kuala Lumpur are slightly high on the imported cases in the latest. It is because Johor and W.P. Kuala Lumpur has the main airport in Malaysia and the action control in Malaysia is started to loosen gradually at this time. </p>'
st.markdown(text13, unsafe_allow_html=True)


left_column, right_column= st.columns([5,2])
with left_column:
    sumdf=df_state.groupby(['year_month','state']).sum()
    plt.figure(figsize=(25,5))
    plt.xticks(rotation=30)
    g=sns.lineplot(x="year_month", y="cases_import", hue='state', data=sumdf)
    g.set(xlabel='Month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text14 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">Then, The imported cases in every state of Malaysia by month is created into a graph and it shows that the total imported case in June 2020 is increasing rapidly especially in W.P. Kuala Lumpur. Based on this graph, we can know that overall of the imported cases in 2021 are higher than the imported cases in 2020. </p>'
    st.markdown(text14, unsafe_allow_html=True)

plt.figure(figsize=(30,5))
plt.xticks(rotation=30)
g =sns.lineplot(x="date", y="cases_recovered", hue='state', data=df_state)
g.set(xticklabels=[])  
g.set(xlabel='Date from '+df_state['date'].unique()[0]+" to "+df_state['date'].unique()[-1]) 
g.set(ylabel='Cases')  
g.tick_params(bottom=False)
g=st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(g)

text15 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">Based on the graph that shows the recovered cases in every state of Malaysia by day, we have the same observation with the new cases in every state of Malaysia which is Selangor is the highest position in the whole timeline of Malaysia pandemic and it is replaced by Sarawak in the latest date. It is because of the conclusion that we have done above: “The higher the new cases, the higher the recovered cases. </p>'
st.markdown(text15, unsafe_allow_html=True)

text16 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">But there is a very interesting observation is the overall recovered cases in Selangor are still higher than in Sarawak. It is because the average of the recovered cases in Selangor is higher than in Sarawak. The observation is based on the graph below. </p>'
st.markdown(text16, unsafe_allow_html=True)

sumdf=df_state.groupby(['year_month','state']).sum()
plt.figure(figsize=(20,5))
plt.xticks(rotation=1000)
g=sns.lineplot(x="year_month", y="cases_recovered", hue='state', data=sumdf)
g.set(xlabel='Month') 
g.set(ylabel='Cases')
g=st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(g)

sum_my =pd.DataFrame(data = df_state,columns = ['cases_new','state'])
sum_my =sum_my.groupby(['state']).sum()



df_map = gp.read_file('msia-states.json')
m = folium.Map([4.602973124617278, 108.64564992244625], zoom_start=5.5)
df_map['Cases'] = [sum_my.cases_new[0],sum_my.cases_new[1],sum_my.cases_new[2],sum_my.cases_new[13],
          sum_my.cases_new[14],sum_my.cases_new[3],sum_my.cases_new[4] ,sum_my.cases_new[5] ,
          sum_my.cases_new[6],sum_my.cases_new[7],sum_my.cases_new[8],sum_my.cases_new[15],
          sum_my.cases_new[9],sum_my.cases_new[10],sum_my.cases_new[11],sum_my.cases_new[12]]
bins = list(df_map["Cases"].quantile([0, 0.5, 0.75, 0.95, 1]))

states = folium.Choropleth(
    geo_data=df_map, 
    data=df_map,
    key_on="feature.properties.name_1",
    columns=['name_1',"Cases"],
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Cases",
    bins=bins,
    reset=True,
    ).add_to(m)

states.geojson.add_child(folium.features.GeoJsonTooltip(fields=['name_1', 'Cases'],aliases=['State: ','Cases: ']))

folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Water Color').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)
folium.LayerControl().add_to(m)
folium_static(m)

make_map_responsive= """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)

text17 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Above shown a map that presents the total number of cases in every state of Malaysia. Based on the map we can see that Selangor is the most serious state in this pandemic and followed by Kuala Lumpur, Sarawak, and Johor. In this map, only total cases from W.P. Labuan and Perlis do not more than 10 thousand cases, and other states are more than 10 thousand unfortunately. </p>'
st.markdown(text17, unsafe_allow_html=True)

title7 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Outliers in every state of Malaysia</p>' 
st.markdown(title7, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    plt.figure(figsize=(20,5))
    plt.xticks(rotation=30)
    g=sns.boxplot(y="cases_new", x='state', data=df_state)
    g.set(xlabel='State') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text18 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">We have been plotting the recovered cases, new cases, and import cases graph by states of Malaysia. The first graph shows that the new cases in every state in Malaysia, we can see that Selangor has the highest number of upper outliers and followed by Sarawak. The average range of the state is less than 4 thousand cases. Based on the graph above, we know that all the states have a lot of outliers.</p>'
    st.markdown(text18, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    plt.figure(figsize=(20,5))
    plt.xticks(rotation=30)
    g=sns.boxplot(y="cases_recovered", x='state', data=df_state)
    g.set(xlabel='State') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text19 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Besides, the graph is followed by the recovered cases graph. In this graph, Selangor still has the highest number of upper outliers but is followed by Pulau Pinang with an outlier of nearly 8 thousand recovered cases and Sabah with an outlier of nearly 6 thousand recovered cases. The average range of the states is the same as the new cases graph which is less than 4 thousand cases. </p>'
    st.markdown(text19, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    plt.figure(figsize=(20,5))
    plt.xticks(rotation=30)
    g=sns.boxplot(y="cases_import", x='state', data=df_state)
    g.set(xlabel='State') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text20 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">The last boxplot graph is the import cases graph. In this graph, Negeri Sembilan has the highest outliers which are import 70 cases but Johor, Selangor, and W.P. Kuala Lumpur have the higher number of import cases since the median of these states is higher than other states. </p>'
    st.markdown(text20, unsafe_allow_html=True)

title8 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Relationship between new cases and covid testing</p>' 
st.markdown(title8, unsafe_allow_html=True)


left_column, right_column= st.columns([5,2])
with left_column:
    df_msia['total_covid_test']=df_msia['rtk-ag']+df_msia['pcr']
    testcovid = pd.DataFrame(data = df_msia, columns = ['date','cases_new','total_covid_test'])
    testcovid = testcovid.melt('date', var_name='type',  value_name='vals')
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="date", y="vals", hue='type', data=testcovid)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_cases_mysia['date'].unique()[0]+" to "+df_cases_mysia['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False)
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text21 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In this graph, we want to investigate that the relationship between the covid testing and new cases. Based on the information from the graph, we know that the higher number of covid testing, the higher number of new cases. It is because we can observe that the latest case is increased and the covid testing is also increasing. </p>'
    st.markdown(text21, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    df_msia['total_covid_test']=df_msia['rtk-ag']+df_msia['pcr']
    testcovid = pd.DataFrame(data = df_msia, columns = ['year_month','cases_new','total_covid_test'])
    testcovid = testcovid.melt('year_month', var_name='type',  value_name='vals')
    testcovid =testcovid.groupby(['year_month','type']).sum()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="year_month", y="vals", hue='type', data=testcovid)
    g.set(xlabel='month') 
    g.set(ylabel='Cases') 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text22 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">To view the information more clearly, the graph has been plotted with month. In this graph, our observation has been proved, especially the case in August 2021. We can see that the covid testing in August is very high and the cases in August have increased. </p>'
    st.markdown(text22, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    df_test_state['total_covid_test']=df_test_state['rtk-ag']+df_test_state['pcr']
    plt.figure(figsize=(30,10))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="date", y="total_covid_test", hue='state', data=df_test_state)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_test_state['date'].unique()[0]+" to "+df_test_state['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False)
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text23 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Besides, the graph below shows the number of testing in every state of Malaysia. This graph also proved our observation because Selangor, Johor, and Sarawak have higher cases in Malaysia and we can observe that the number of covid testing in these states is higher than in other states.</p>'
    st.markdown(text23, unsafe_allow_html=True)

title9 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-align: justify;text-decoration: underline">Comparison of the covid testing method</p>' 
st.markdown(title9, unsafe_allow_html=True)

left_column, right_column= st.columns([5,2])
with left_column:
    testcovid = pd.DataFrame(data = df_msia, columns = ['date','rtk-ag','pcr'])
    testcovid = testcovid.melt('date', var_name='type',  value_name='vals')
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="date", y="vals", hue='type', data=testcovid)
    g.set(xticklabels=[])  
    g.set(xlabel='Date from '+df_cases_mysia['date'].unique()[0]+" to "+df_cases_mysia['date'].unique()[-1]) 
    g.set(ylabel='Cases')  
    g.tick_params(bottom=False) 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text24 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In the graph that we have shown above, we know that there are 2 methods of covid testing in Malaysia which are RTK-AG and PCR. At the beginning of this pandemic, PCR is started to use as the method for the covid testing and followed by RTK-AG after the pandemic has been happening for some days. Based on this graph, we can see that the RTK-AG is used slightly more than PCR at the latest time.</p>'
    st.markdown(text24, unsafe_allow_html=True)


title10 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-align: justify;text-decoration: underline">Cluster in Malaysia</p>' 
st.markdown(title10, unsafe_allow_html=True)

cluster_2020=df_clusters.loc[df_clusters['a_year']=='2020']
cluster_2021=df_clusters.loc[df_clusters['a_year']=='2021']
cluster_count_2021 =df_clusters['a_year'].loc[df_clusters['a_year']=='2021'].count()
cluster_count_2020 =df_clusters['a_year'].loc[df_clusters['a_year']=='2020'].count()
cluster_active_2021 = cluster_2021['status'].loc[cluster_2021['status']=='active'].count()
cluster_active_2020 = cluster_2020['status'].loc[cluster_2020['status']=='active'].count()
cluster_ended_2021 = cluster_2021['status'].loc[cluster_2021['status']=='ended'].count()
cluster_ended_2020 = cluster_2020['status'].loc[cluster_2020['status']=='ended'].count()
cluster_active = df_clusters['status'].loc[df_clusters['status']=='active'].count()
cluster_ended = df_clusters['status'].loc[df_clusters['status']=='ended'].count()


left_column, right_column= st.columns(2)
with left_column:
    data = {'Type': ['Cluster(Active)', 'Cluster(Ended)'], 'Total': [cluster_active,cluster_ended]}  
    sum_df =pd.DataFrame(data = data,columns = ['Type','Total'])
    plt.figure(figsize=(20,3))
    plt.ticklabel_format(style='plain')
    g=sns.barplot(x='Total',y='Type',data=sum_df)
    g.set(xlabel='Type') 
    g.set(ylabel='Total')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    text25 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Based on the bar plot above, we can see that most of the clusters in Malaysia are already ended, only left about 1450 clusters that are still active in Malaysia. To look more closely, the bar plot has been separated into 2 which are the cluster in 2020 and 2021. </p>'
    st.markdown(text25, unsafe_allow_html=True)


left_column, right_column= st.columns(2)
with left_column:
    count = df_clusters.groupby(['category','a_year_month']).count()
    data = {'Type': ['Cluster Active', 'Cluster Ended','Total Cluster'], 'Total': [cluster_active_2021,cluster_ended_2021,cluster_count_2021]}  
    sum_df =pd.DataFrame(data = data,columns = ['Type','Total'])
    plt.figure(figsize=(20,3))
    plt.ticklabel_format(style='plain')
    g=sns.barplot(x='Total',y='Type',data=sum_df)
    g.set(xlabel='Type') 
    g.set(ylabel='Total') 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
    

with right_column:
    text26 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In the bar plot that shows the cluster in 2020, we know that there is no more active cluster in 2020 that is active until now. 500 and more clusters in 2020 have been ended successfully.</p>'
    st.markdown(text26, unsafe_allow_html=True)

left_column, right_column= st.columns(2)
with left_column:
    data = {'Type': ['Cluster Active', 'Cluster Ended','Total Cluster'], 'Total': [cluster_active_2020,cluster_ended_2020,cluster_count_2020]}  
    sum_df =pd.DataFrame(data = data,columns = ['Type','Total'])
    plt.figure(figsize=(20,3))
    plt.ticklabel_format(style='plain')
    g=sns.barplot(x='Total',y='Type',data=sum_df)
    g.set(xlabel='Type') 
    g.set(ylabel='Total')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
    

with right_column:
    text27 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Besides, In the bar plot that shows the cluster in 2021, we know that there are about 1500 clusters are still active in 2021, and more than half of the clusters, 3000+ clusters have been ended.</p>'
    st.markdown(text27, unsafe_allow_html=True)

plt.figure(figsize=(30,10))
plt.xticks(rotation=30)
g =sns.lineplot(x="a_year_month", y="cluster", hue='category', data=count)
g=st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(g)

text28= '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">The cluster has been differentiated into a few types of clusters such as community, detention centre, education, high risk, import, religious, and workplace. Below shows the number of these clusters in the whole pandemic. In this graph, we can know that the workplace cluster has the highest number of clusters every month in this pandemic and it is followed by the community cluster. Fortunately, other categories are not as high as the cluster that we explain before, they are just not more than 100 clusters every month.</p>'
st.markdown(text28, unsafe_allow_html=True)

title11 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-decoration: underline">Comparison of the cluster in 2020 and 2021</p>' 
st.markdown(title11, unsafe_allow_html=True)


left_column, right_column = st.columns(2)
with left_column:
    cluster = df_clusters.loc[df_clusters['a_year']=='2021']
    cluster= cluster.groupby(['a_year_month','a_year','a_month']).count()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="a_month", y="cluster", data=cluster)
    g.set(xlabel='month') 
    g.set(ylabel='Cases') 
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)

with right_column:
    cluster = df_clusters.loc[df_clusters['a_year']=='2020']
    cluster= cluster.groupby(['a_year_month','a_year','a_month']).count()
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=30)
    g =sns.lineplot(x="a_month", y="cluster", data=cluster)
    g.set(xlabel='month') 
    g.set(ylabel='Cases')
    g=st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(g)
text29 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Based on the line graph above, we know that the highest number of clusters in 2020 is only 140 but the highest number of clusters in 2021 is more than 1 thousand clusters. This is unfortunate information. The number of clusters in 2021 has been increasing rapidly from April 2021 but in 2020 the number of clusters increase in September 2020.</p>'
st.markdown(text29, unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------#
df_test_state.drop(['total_covid_test'], axis=1,inplace=True)
state_list =['Johor','Kedah','Kelantan','Melaka','Negeri Sembilan','Pahang','Pulau Pinang','Perak','Perlis','Sabah','Sarawak','Selangor','Terengganu','W.P. Kuala Lumpur','W.P. Labuan','W.P. Putrajaya']
statedf =[]
statedf=[]
johor=df_cases_state[df_cases_state['state']=='Johor'].reset_index()
pahang=df_cases_state[df_cases_state['state']=='Pahang'].reset_index()
for x in state_list:
    statedf.append(df_cases_state[df_cases_state['state']==x].reset_index())
PahangDf =pd.DataFrame()
JohorDf =pd.DataFrame()
Johor_test =pd.DataFrame()
Pahang_test =pd.DataFrame()
for i in statedf:
    PahangDf[i['state'].loc[0]] = pahang.corrwith(i,axis =0)
    JohorDf[i['state'].loc[0]] = johor.corrwith(i,axis =0)
statedf=[]
johor_test=df_test_state[df_test_state['state']=='Johor'].reset_index()
pahang_test=df_test_state[df_test_state['state']=='Pahang'].reset_index()
for x in state_list:
    statedf.append(df_test_state[df_test_state['state']==x].reset_index())
for i in statedf:
    Johor_test[i['state'].loc[0]] = johor_test.corrwith(i,axis =0)
    Pahang_test[i['state'].loc[0]] = pahang_test.corrwith(i,axis =0)
Pahang_test =Pahang_test.T
Johor_test =Johor_test.T
PahangDf =PahangDf.T
JohorDf =JohorDf.T
Pahang = pd.merge(PahangDf,Pahang_test, left_index=True, right_index=True)
Johor = pd.merge(JohorDf,Johor_test, left_index=True, right_index=True)

text30 = '<p style="font-family:Time-New-Roman; font-size: 24px;">Question 2 -Correlation of Pahang and Johor with other states in Malaysia</p>'
st.markdown(text30, unsafe_allow_html=True)
left_column, right_column= st.columns(2)
with left_column:
    text29 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-align: justify;text-decoration: underline">Correlation of Pahang.</p>'
    st.markdown(text29, unsafe_allow_html=True)
    Pahang.drop(['index_x','index_y'], axis=1,inplace=True)
    Pahang

with right_column:
    text29 = '<p style="font-family:Time-New-Roman; font-size: 18px;text-align: justify;text-decoration: underline">Correlation of Johor.</p>'
    st.markdown(text29, unsafe_allow_html=True)
    Johor.drop(['index_x','index_y'], axis=1,inplace=True)
    Johor

text29 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">The first table shows that the correlation between Pahang and other states in Malaysia. In the first column which is cases_import, we can observe that the average correlation value is not high. The top 3 correlation value is 0.2542, 0.2249, and 0.1618 which are Perak, Kedah, and Perlis. Next, the top 3 correlation value in the cases_new column is from Kedah, Terengganu, and Perak which are 0.9351, 0.9209, and 0.9169. In the cases_recovered column, its first 3 high correlation value is 0.9293, 0.8906, and 0.8702: Kedah, Perak, and Selangor. Then, Selangor, Negeri Sembilan, and Sabah are the top 3 correlation value: 0.5752, 0.5401, and 0.5174 in rtk-ag column. Last is the pcr column and the top 3 correlation values are Johor, Kedah, and Terengganu which are 0.6390, 0.6165, and 0.5584. The overall correlation of Kedah is the best because most of the columns of Kedah have a high correlation, only the rtk-ag column.</p>'
st.markdown(text29, unsafe_allow_html=True)

text29 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">The second table is showing the correlation between Johor and other states in Malaysia. In the cases_import column, Pulau Pinang, Kedah, and Perak are the top 3 high correlation values which are 0.1814, 0.1428, and 0.1185. Then, Pulau Pinang, Perak, and Terengganu with correlation values: 0.9316, 0.9305, and 0.9202 are the 3 high correlation values in the cases_new column. In the third column which is the cases_recovered column, Perak, Kedah, and Kelantan with 0.8389, 0.8171, and 0.8130 correlation values are the best correlation values in the cases_recovered column. Besides, Perak, Kedah, and Terengganu have the top 3 correlation values in the rtk-ag column which are 0.7744, 0.7605, and 0.7323. The last column is the pcr column. Its 3 high correlation values are 0.8281, 0.8085, and 0.7767 which are Pulau Pinang, Kedah, and Perlis. Based on the top 3 correlation values from all columns, we have concluded that the overall correlation of Perak is more correlate with Johor.</p>'
st.markdown(text29, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------------------#

text30 = '<p style="font-family:Time-New-Roman; font-size: 24px;">Question 3</p>'
st.markdown(text30, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">Feature Selection</p>'
st.markdown(text31, unsafe_allow_html=True)

text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">In this section, we are focusing on extracting the features (independent variables) that strongly contribute to the daily cases of Pahang, Kedah, Selangor and Johor. We used two datasets which are cases_malaysia.csv and cases_states.csv provided by the Ministry of Health Malaysia. </p>'
st.markdown(text32, unsafe_allow_html=True)
text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">According to Worldometers [1], the Incubation period of Covid19 is between 2-14 days and the possible outliers range falls between 0-27 days, therefore, we create a new dataframe from the cases_states.csv to store the records of daily cases from each states from 1 day before until 1 month before. After that, we  merge this dataframe with cases_malaysia.csv and cases_states.csv and perform the feature selection using Boruta and Recursive Feature Elimination (RFE). The sample of the merged dataframe is shown below: </p>'
st.markdown(text32, unsafe_allow_html=True)
df_test_state = pd.read_csv('df_merge_together.csv')
df_test_state
text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">Boruta</p>'
st.markdown(text31, unsafe_allow_html=True)

text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Below are the top 30 important features generated by the Boruta Algorithm for Pahang, Kedah, Selangor and Johor.</p>'
st.markdown(text32, unsafe_allow_html=True)
with st.expander(" The top 30 important features of Boruta"):
    left_column, right_column= st.columns(2)
    with left_column:
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Johor</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('boruta_johor.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Kedah</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('boruta_kedah.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df

    with right_column:
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Pahang</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('boruta_pahang.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Selangor</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('boruta_selangor.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df

text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">From the tables above, we can see that PCR, cases Kelantan 2 day before and cases KL 4 days before are among the top 3 features that contribute to daily cases of Pahang. On the other hand, PCR, cases Kelantan 1 week before and cases Pahang 2 week before are among the top 3  features that contribute to daily cases of Kedah. Moreover, cases Labuan 1 day before, cluster religious and cases Labuan 5 days before are among the top 3 features that contribute to daily cases of Selangor.Furthermore, cases KL 3 day before, cluster detention Centre and cases Labuan  3 week before are among the top 3 features that contribute to daily cases of Johor. It’s very interesting to find out that PCR, cases Kelantan, cases KL and cases Labuan appeared many times in the top 3 features of Pahang, Kedah, Selangor and Johor. </p>'
st.markdown(text32, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">RFE</p>'
st.markdown(text31, unsafe_allow_html=True)

text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">Below are the top 30 important features generated by the RFE algorithm for Pahang, Kedah, Selangor and Johor.</p>'
st.markdown(text32, unsafe_allow_html=True)
with st.expander(" The top 30 important features of RFE"):
    left_column, right_column= st.columns(2)
    with left_column:
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Johor</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('rfe_johor.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Kedah</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('rfe_kedah.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df

    with right_column:
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Pahang</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('rfe_pahang.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df
        text31 = '<p style="font-family:Time-New-Roman;font-size: 18px;text-decoration: underline">Selangor</p>'
        st.markdown(text31, unsafe_allow_html=True)
        df = pd.read_csv('rfe_selangor.csv')
        df.rename( columns={'Unnamed: 0':'No'}, inplace=True )
        df


text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">From the tables above, we can see that the RFE model seems to be overfitted in all 4 states and produced a lot of important features. For example Kedah state, the top 30 features produced by RFE contain 193 variables(due to the same ranking), while the total number of variables in the dataframe is 194, this means almost all the variables are important and the model cannot select important features from the variables.</p>'
st.markdown(text32, unsafe_allow_html=True)
text32 = '<p style="font-family:Time-New-Roman; font-size: 15px;text-align: justify;">As we compare the output of both Boruta and RFE algorithms, we can conclude that Robuta performs better than the RFE as Boruta can clearly differentiate the important features from the variables. Therefore, we will use the top 30 ranking feature indicated by Robuta for each state respectively to train our model in question 4 and drop other variables which are not important.</p>'
st.markdown(text32, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------------------#


text30 = '<p style="font-family:Time-New-Roman; font-size: 24px;">Question 4</p>'
st.markdown(text30, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">Classification and Regression model</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">In this section, we are focusing on comparing the regression and classification models to see which model performs better in predicting the daily cases for Pahang, Kedah, Selangor and Johor. </p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">Regression Model</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">We use 5 regression models which are Linear Regression, Decision Tree Regression, Random Forest Regression, Bayesian Linear Regression and Support Vector Regression to predict the daily cases of 4 states. The performance of each regression model is shown at the table below.</p>'
st.markdown(text31, unsafe_allow_html=True)

im = Image.open("regression_report.jpeg")
st.image(im, width=1350)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">From the table above, we can see that for predicting daily cases in Selangor, Bayesian Linear Regression and Linear Regression performed the best out of other regression model with the R2 score of 0.974 and 0.973 and MAE of 147.651 and 150.837 respectively. On the other hand, for predicting daily cases in Pahang, Random Forest Regression performed the best out of other regression models with the R2 score of 0.91 and MAE of 26.0737. Moreover, for predicting daily cases in Kedah, Support Vector Regression and Random Forest Regression performed the best out of other regression with the R2 score of 0.958 and 0.957 and MAE of 49.214 and 46.268 respectively. Lastly, for predicting daily cases in Johor, Decision Tree Regression and Random Forest Regression performed the best out of other regression models with the R2 score of 0.91 and 0.905 and MAE of 87.827 and 77.820. Support Vector Regression performed quite badly in this case as it only achieved the R2 score of 0.746 and MAE of 117.422. In short, for predicting daily cases in Selangor, Pahang, Kedah and Johor, we found out that Random Forest Regression was the best performing model in 3 out of 4 states, while Bayesian Linear Regression, Linear Regression, Support Vector Regression and Decision Tree Regression were the best performing model in 1 out of 4 states.</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;">Classification Model</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">Before we fit our data into the classification model, we need to discretize the dependent variable and group it into categorical data as its original data type is integer. Therefore, we created 4 new columns and named them severity scores for daily cases of each state. Below is how we set the severity score for the daily cases of each state:</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">1. Let x = No. daily cases for each state</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">2. If  x <= 100,severity score class = 1</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">3. If 100 < x <= 500, severity score class = 2</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">4. If 500 < x <= 1000, severity score class = 3</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">5. If 1000 < x <= 2000, severity score class = 4</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">6. If x > 2000, severity score class = 5</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">We use 5 classification models which are Decision Tree Classifier, Random Forest Classifier, Support Vector Machine, Naive Bayes and KNN to predict the daily cases of 4 states. The performance of each classification model is shown below. </p>'
st.markdown(text31, unsafe_allow_html=True)

im = Image.open("classification_report.jpeg")
st.image(im, width=1350)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">From the table above, we can see that for predicting daily cases in Selangor, KNN performed the best out of  other classification models with the precision, recall, F1-score and accuracy of 0.89, 0.89, 0.89 and 0.89 respectively. On the other hand, for predicting daily cases in Pahang, KNN performed the best out of  other classification models with the precision, recall, F1-score and accuracy of 0.96, 0.95, 0.95 and 0.95 respectively. Moreover, for predicting daily cases in Kedah, Random Forest Classifier performed the best out of other classification models with the precision, recall, F1-score and accuracy of 0.92,0.92,0.92 and 0.92 respectively. Lastly, for predicting daily cases in Johor, Random Forest Classifier performed the best out of other classification models with the precision, recall, F1-score and accuracy of 0.87,0.97,0.86 and 0.87 respectively. Support Vector Machine performed not that good in this case as it only achieved the precision, recall, F1-score and accuracy of 0/76,0.79,0.77 and 0.79 respectively. In short, for predicting daily cases in Selangor, Pahang, Kedah and Johor, we found out that KNN and Random Forest Classifier were the best performing models in 2 out of 4 states respectively.</p>'
st.markdown(text31, unsafe_allow_html=True)

with st.expander("Confusion matrics of Selangor"):
    left_column,left_mid,mid,right_mid, right_column= st.columns(5)
    with left_column:
        im = Image.open("selangor_dtc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Decision Tree Classifier  </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with left_mid:
        im = Image.open("selangor_knn.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">K-nearest neightbour </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with mid:
        im = Image.open("selangor_nb.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Naive Bayes </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_mid:
        im = Image.open("selangor_rfc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Random Forest Classifier </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_column:
        im = Image.open("selangor_svm.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;;">Support Vector Machines </p>'
        st.markdown(text31, unsafe_allow_html=True)

    
with st.expander("Confusion matrics of Pahang"):
    left_column,left_mid,mid,right_mid, right_column= st.columns(5)
    with left_column:
        im = Image.open("pahang_dtc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Decision Tree Classifier  </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with left_mid:
        im = Image.open("pahang_knn.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">K-nearest neightbour </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with mid:
        im = Image.open("pahang_nb.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Naive Bayes </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_mid:
        im = Image.open("pahang_rfc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Random Forest Classifier </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_column:
        im = Image.open("pahang_svm.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;;">Support Vector Machines </p>'
        st.markdown(text31, unsafe_allow_html=True)
    
    
with st.expander("Confusion matrics of Johor"):
    left_column,left_mid,mid,right_mid, right_column= st.columns(5)
    with left_column:
        im = Image.open("johor_dtc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Decision Tree Classifier  </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with left_mid:
        im = Image.open("johor_knn.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">K-nearest neightbour </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with mid:
        im = Image.open("johor_nb.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Naive Bayes </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_mid:
        im = Image.open("johor_rfc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Random Forest Classifier </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_column:
        im = Image.open("johor_svm.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;;">Support Vector Machines </p>'
        st.markdown(text31, unsafe_allow_html=True)
    
with st.expander("Confusion matrics of Kedah"):
    left_column,left_mid,mid,right_mid, right_column= st.columns(5)
    with left_column:
        im = Image.open("kedah_dtc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Decision Tree Classifier  </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with left_mid:
        im = Image.open("kedah_knn.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">K-nearest neightbour </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with mid:
        im = Image.open("kedah_nb.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Naive Bayes </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_mid:
        im = Image.open("kedah_rfc.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;">Random Forest Classifier </p>'
        st.markdown(text31, unsafe_allow_html=True)
    with right_column:
        im = Image.open("kedah_svm.jpeg")
        st.image(im, width=250)
        text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: center;;">Support Vector Machines </p>'
        st.markdown(text31, unsafe_allow_html=True)
    
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;">Overall conclusion of question 4 :</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify;">In a nutshell, we cannot compare the performance of classification and regression models directly because the output of two models are different. Classification model produces a categorical output, while the regression model produces a numerical output. For predicting the daily cases in Selangor, Pahang, Kedah and Johor, Random Forest Regression performed the best among other regression models while Random Forest Classifier and KNN performed the best among other classification models.It really depends what type of output we want before deciding which model to use. If we want to predict the number of covid cases in a state, then choose the regression model. If we want to predict the category of covid cases in a state, then choose the classification model. Based on the results we obtained from the training, we suggest using the Random Forest Regression model for regression model and Random Forest Classifier or KNN for classification model in predicting the daily cases of a state.</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 24px;"> Reference.</p>'
st.markdown(text31, unsafe_allow_html=True)
text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;text-align: justify"> [1] Coronavirus incubation period: Worldometer. (n.d.). Retrieved September 21, 2021, from https://www.worldometers.info/coronavirus/coronavirus-incubation-period/.</p>'
st.markdown(text31, unsafe_allow_html=True)

text31 = '<p style="font-family:Time-New-Roman;font-size: 15px;"> Done by : Chang Kai Boon (1181101282),Soe Zhao Hong (1181101614).</p>'
st.markdown(text31, unsafe_allow_html=True)