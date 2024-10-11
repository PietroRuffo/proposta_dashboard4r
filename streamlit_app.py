import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
   page_title ="Dashboard 4 ERRE COSTRUZIONI",
   page_icon = ":bar_chart:",
   layout = "wide"
)
st.title("4 ERRE COSTRUZIONI :hammer_and_wrench: :bar_chart: 	:pushpin:")
st.markdown("Versione prova con dati sintetici")

@st.cache_data
def load_data(path: str):
   data = pd.read_csv(path)
   return data

#with st.sidebar:
#   st.header("Configurazione")
#   uploaded_file = st.file_uploader("Carica l'ultima versione del file .csv")
#
#if uploaded_file is None:
#   st.info("Nessun .csv sorgente è stato caricato. Fai drag and drop del .csv", icon="ℹ️")  # Using an information emoji
#   st.stop()

df = load_data("./esempio_dashboard_4r.csv")

with st.expander("Anteprima dei dati"):
   st.dataframe(df)


def plot_bottom_left():

          entrate_uscite_mensili = duckdb.sql(f"""
          
              SELECT Mese, 
                     SUM(Entrate) AS Entrate, 
                     SUM(Uscite) AS Uscite
              FROM df
              GROUP BY Mese
              ORDER BY CASE 
                           WHEN Mese = 'Gennaio' THEN 1
                           WHEN Mese = 'Febbraio' THEN 2
                           WHEN Mese = 'Marzo' THEN 3
                           WHEN Mese = 'Aprile' THEN 4
                           WHEN Mese = 'Maggio' THEN 5
                           WHEN Mese = 'Giugno' THEN 6
                           WHEN Mese = 'Luglio' THEN 7
                           WHEN Mese = 'Agosto' THEN 8
                           WHEN Mese = 'Settembre' THEN 9
                           WHEN Mese = 'Ottobre' THEN 10
                           WHEN Mese = 'Novembre' THEN 11
                           WHEN Mese = 'Dicembre' THEN 12
                       END
          """).df()

          fig = px.line(
                         entrate_uscite_mensili,
                         x='Mese',
                         y='Entrate',
                         title='Entrate vs Uscite per Mese',
                         labels={'Mese': 'Mese', 'value': 'Valore in Euro'},
                         markers=True,
                         color_discrete_sequence=["green"]
                        )
     
         # Add Uscite to the same figure
          fig.add_scatter(
                         x=entrate_uscite_mensili['Mese'], 
                         y=entrate_uscite_mensili['Uscite'], 
                         mode='lines+markers', 
                         name='Uscite', 
                         textposition="top center",
                         line=dict(color='red'),  # Set Uscite color to red
                         marker=dict(color='red')  # Set marker color to red
                          )
         # Add Entrate scatter trace with a distinct name for the legend
          fig.add_scatter(
              x=entrate_uscite_mensili['Mese'],
              y=entrate_uscite_mensili['Entrate'],
              mode='lines+markers',
              name='Entrate',  # Ensure Entrate is named for the legend
              line=dict(color='green'),  # Entrate color
              marker=dict(color='green')  # Marker color for Entrate
          )
               
         # Update layout for better visualization
          fig.update_layout(
                            yaxis_title='Valore in Euro',
                            xaxis_title='Mese',
                            legend_title='Tipo',
                            legend=dict(x=0, y=1)
         )               
          # Show the chart in Streamlit
          st.plotly_chart(fig, use_container_width=True)
     
plot_bottom_left()

def plot_bottom_right():

   count_cantieri = duckdb.sql(f"""
   WITH TEMP AS(
      SELECT ID_Cantiere, MAX(Tipo_Cantiere) AS Tipo_Cantiere
      FROM df
      GROUP BY ID_Cantiere
      )

      SELECT Tipo_Cantiere, COUNT(*) AS Totale
      FROM TEMP
      GROUP BY Tipo_Cantiere
   """).df()

   fig = px.bar(
      count_cantieri,
      x = 'Tipo_Cantiere',
      y = 'Totale',
      color='Tipo_Cantiere',
      title = 'Totale Cantieri per tipologia'
   )
   st.plotly_chart(fig, use_container_width=True)

plot_bottom_right()          
 

def plot_map():

   map_cantieri = duckdb.sql(f"""
   WITH TEMP AS(
      SELECT ID_Cantiere, MAX(Città) AS Città, MAX(Lat) as Lat, MAX(Long) as Long
      FROM df
      GROUP BY ID_Cantiere)
   
   SELECT Città, Lat, Long, COUNT(*) AS Totale_Cantieri
   FROM TEMP
   GROUP BY Città, Lat, Long
  
   """).df()

   st.write("**Copertura suolo italiano dei Cantieri**")
   st.map(map_cantieri, latitude="Lat", longitude="Long", size="Totale_Cantieri")

plot_map()

def plot_cantieri_by_city():

   map_cantieri = duckdb.sql(f"""
   WITH TEMP AS(
      SELECT ID_Cantiere, MAX(Città) AS Città, MAX(Lat) as Lat, MAX(Long) as Long
      FROM df
      GROUP BY ID_Cantiere)
   
   SELECT Città, COUNT(*) AS Totale_Cantieri
   FROM TEMP
   GROUP BY Città
  
   """).df()

   fig = px.bar(
      map_cantieri,
      x = 'Città',
      y = 'Totale_Cantieri',
      color='Totale_Cantieri',
      title = 'Totale Cantieri per Città'
   )
   st.plotly_chart(fig, use_container_width=True)

plot_cantieri_by_city() 


def plot_incidenti_by_mese():

   incidenti = duckdb.sql(f"""
   SELECT Mese, CAST(SUM(Incidenti_sul_Lavoro) AS INT) AS Totale
   FROM df
   GROUP BY Mese
  
   """).df()

   fig = px.bar(
      incidenti,
      x = 'Mese',
      y = 'Totale',
      color='Totale',
      title = 'Totale Incidenti per mese',
          category_orders={'Mese': ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']}

   )
   fig.update_traces(marker_color='red')
   st.plotly_chart(fig, use_container_width=True)

plot_incidenti_by_mese() 


#def plot_avanzamento_lavori():
#
#   avanzamento_lavori = duckdb.sql(f"""
#    SELECT ID_Cantiere, MAX(Avanzamento_percentuale) AS Stato_Avanzamento
#    FROM df
#    GROUP BY ID_Cantiere
#   """).df()
#
#   fig = px.bar(
#      avanzamento_lavori,
#      x = 'ID_Cantiere',
#      y = 'Stato_Avanzamento',
#      color='Stato_Avanzamento',
#      title = 'Stato Avanzamento in percentuale per cantiere'
#   )
#   st.plotly_chart(fig, use_container_width=True)
##
##plot_avanzamento_lavori() 

def plot_avanzamento_lavori():
    avanzamento_lavori = duckdb.sql(f"""
        SELECT ID_Cantiere, MAX(Avanzamento_percentuale) AS Stato_Avanzamento
        FROM df
        GROUP BY ID_Cantiere
    """).df()

    # Create a figure
    fig = go.Figure()

    # Set the number of gauges per row (columns in the grid)
    gauges_per_row = 3  # Adjust this value for more/less per row
    total_gauges = len(avanzamento_lavori)
    rows = (total_gauges // gauges_per_row) + 1

    # Add a gauge for each construction site with smaller sizes and conditional colors
    for i, row in avanzamento_lavori.iterrows():
        row_pos = i // gauges_per_row  # Calculate row position
        col_pos = i % gauges_per_row   # Calculate column position

        # Set gauge color based on the progress value
        gauge_color = "green" if row['Stato_Avanzamento'] >= 50 else "yellow"

        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=row['Stato_Avanzamento'],
                title={'text': f"Cantiere {row['ID_Cantiere']}", 'font': {'size': 15}},  # Smaller title text
                number={'font': {'size': 20}, 'suffix': "%"},  # Smaller value font size
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': gauge_color},
                    'borderwidth': 1,
                    'bordercolor': "grey"
                },
                # Adjust gauge size by modifying the x and y domains
                domain={
                    'x': [col_pos / gauges_per_row + 0.05, (col_pos + 1) / gauges_per_row - 0.05],
                    'y': [1 - (row_pos + 1) / rows + 0.05, 1 - row_pos / rows - 0.05]  # Added margin for spacing
                }
            )
        )

    # Adjust the layout for better visualization with smaller size
    fig.update_layout(
        title="Stato Avanzamento in percentuale per cantiere",
        height=300 * rows,  # Adjust height to create better spacing between rows
        margin=dict(t=50, b=50),
        font=dict(size=9)  # Reduce font size overall
    )

    st.plotly_chart(fig, use_container_width=True)


plot_avanzamento_lavori()
