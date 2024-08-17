import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit.components.v1 import html
ga_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KYT9QJN6FW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-KYT9QJN6FW');
</script>
"""

html(ga_code, height=0)
# Configurar estilos CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .header {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 30px;
            color: #F4E1C1;
            background-color:  #6D5843;
            padding: 20px;
            text-align: center;
        }
        .sidebar {
            background-color: #F4E1C1;
            color: white;
            padding: 20px;
        }
        .sidebar .nav-item {
            padding: 10px;
            cursor: pointer;
        }
        .sidebar .nav-item:hover {
            background-color: #A0522D;
        }
        .section {
            background-color: #F4E1C1;
            padding: 20px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #1f77b4;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 24px;
            margin-top: 0;
        }
        .section p {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 16px;
            color: #333;
        }
        .guardian-selectbox label,
        .guardian-dateinput label {
            color: #1f77b4;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .css-1aumxhk {
            color: #1f77b4;
        }
        .css-1b7ax4k {
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

# Crear una función para cargar los datos
@st.cache_data
def cargar_datos(file_path):
    datos = pd.read_csv(file_path, )
    
    datos['bestsellers_date'] = pd.to_datetime(datos['bestsellers_date'], format='%Y-%m-%d')
    datos['published_date'] = pd.to_datetime(datos['published_date'], format='%Y-%m-%d')
    datos['month'] = datos['bestsellers_date'].dt.month
    datos['month'] = datos['month'].map({
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo",
        6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre",
        11: "Noviembre", 12: "Diciembre"
    })
    datos['year'] = datos['bestsellers_date'].dt.year
    return datos

# Cargar datos
ruta= 'Datos/datos2013-2023.csv'
datos = cargar_datos(ruta)


# Función para aplicar filtros
def aplicar_filtros(datos, list=None, years=None, mes=None, autor=None, publisher=None):
    datos_filtros = datos
    if list:
        datos_filtros = datos_filtros[datos_filtros['list_name'] == list]
    if years:
        datos_filtros = datos_filtros[datos_filtros['year'].isin(years)]
    if mes:
        datos_filtros = datos_filtros[datos_filtros['month'].isin(mes)]
    if autor:
        datos_filtros = datos_filtros[datos_filtros['author'].isin(autor)]
    if publisher:
        datos_filtros = datos_filtros[datos_filtros["publisher"].isin(publisher)]
    return datos_filtros

# Función para graficar
def mejores_libros(data, group_by, title):
    if not data.empty:  
        titulos = data.groupby(group_by + ['title']).size().reset_index(name='count').sort_values(by='count', ascending=False)
        titulos= titulos.head(20)
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=titulos, x='title', y='count', ax=ax, palette='viridis')
        ax.set_title(title, fontsize=20, color='#052962')
        ax.set_ylabel('Número de veces en el ranking', fontsize=14, color='#052962')
        ax.set_xlabel('Título', fontsize=14, color='#052962')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12, color='#052962')
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=12, color='#052962')
        st.pyplot(fig)
    else:
        st.write("No hay datos disponibles para los filtros seleccionados.")


# Menú lateral
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    page = st.radio('Navegar a', ['Home','Libros', 'Autores', 'Editoriales', ], index=0)
    st.markdown('</div>', unsafe_allow_html=True)
    
if page=="Home":
    st.markdown('<div class="header">Página principal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    
    st.title("¡Explora el Mundo de los Libros Más Vendidos!")
    st.image('descarga-34-1.png.webp')
    st.markdown("""
    ### ¡Sumérgete en el universo de los libros que están dejando huella!

    ¿Sabías que hay libros que están rompiendo récords en todo el mundo? Esta app te invita a descubrir cuáles son esos libros y quiénes están detrás de ellos. No importa si eres un lector empedernido o solo estás buscando algo interesante para leer, aquí encontrarás algo que te atrapará.

    ### ¿Qué puedes hacer aquí?

    - **Descubre autores que están en el top**: ¿Te has preguntado qué hace que un autor sea tan popular? Aquí puedes explorar cuántas veces han aparecido en las listas de los más vendidos y en qué categorías.

    - **Explora las editoriales que marcan tendencia**: ¿Alguna vez te has preguntado quién está detrás de los libros que todos están leyendo? Aquí puedes ver qué editoriales están liderando el mercado.

    - **Encuentra libros que no te querrás perder**: ¿Quieres saber qué libros han capturado la atención de todos? Navega por títulos que han estado en la cima y descubre nuevas lecturas.

    - **Visualizaciones que te cuentan una historia**: Con gráficos interactivos y fáciles de entender, podrás ver de un vistazo qué está pasando en el mundo de los libros. Desde tendencias a sorpresas, todo está aquí.

    ### ¿Cómo empezar?
    1. **Primeramente haz clic en el simbolo > en la esquina izqquierda superior de la pantalla**: te mostrará las diferentes categorías en las que puedes explorar
    2. **Selecciona un autor, editorial o libro**: Usa los menús desplegables para elegir sobre qué quieres saber más.
    3. **Aplica filtros**: Puedes filtrar por año y mes para ver lo que te interesa de verdad.
    4. **Explora los gráficos**: Los datos se mostrarán en gráficos súper visuales para que descubras patrones y novedades de un solo vistazo.
    5. **Descubre tu próxima lectura**: Encuentra libros que quizás no conocías pero que están en todas partes.

    ### ¿Para quién es esta aplicación?

    - **Curiosos**: Si siempre has querido saber qué es lo que hace que ciertos libros y autores sean tan populares, esta app es para ti.
    - **Nuevos lectores**: Si estás buscando algo que leer pero no sabes por dónde empezar, aquí descubrirás libros que todo el mundo está leyendo.
    - **Lectores de toda la vida**: Si ya tienes tus autores favoritos pero quieres descubrir más sobre ellos, explora y encuentra nuevas joyas literarias.

    ¡Atrévete a explorar el mundo de los libros más vendidos y descubre qué es lo que todos están leyendo ahora mismo!
    """)

if page == 'Libros' :
    
    st.markdown('<div class="header">📚 Book Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2>Libros más vendidos</h2>', unsafe_allow_html=True)
    
    libros = sorted(datos["year"].unique())
    years_seleccionado = st.multiselect("Elige uno o más años", libros, default=libros)
    mes = None
    if years_seleccionado:
        if st.checkbox('Filtrar por mes'):
            mes = st.multiselect("Elige un mes", ["Enero", 'Febrero', "Marzo", 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])
    
    list_escoger = st.selectbox('Selecciona la lista', sorted(datos['list_name'].unique()))
    
    
    datos_filtrados = aplicar_filtros(datos, list=list_escoger, years=years_seleccionado, mes=mes)
        
    if not datos_filtrados.empty:
            mejores_libros(datos_filtrados, ['month'], 'Libros más vendidos')
            dataframe=datos_filtrados.drop(columns=['price','list_name_encoded'])
            st.write(dataframe)
    else:
            st.write("No hay datos disponibles para los filtros seleccionados.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == 'Autores':
    st.markdown('<div class="header">📚 Book Analysis - Autores</div>', unsafe_allow_html=True)
    st.markdown('<div class="section ">', unsafe_allow_html=True)
    st.markdown('<h2>Autores más populares</h2>', unsafe_allow_html=True)
    c1,c4,c5=st.columns(3)
    c2,c3=st.columns(2)
    if "libros1" not in st.session_state:
        st.session_state.libros1= False
    if c1.button('Libros por autor',use_container_width=3):
        st.session_state.libros1=True
    if st.session_state.libros1:
        with st.spinner('cargando'):
            st.markdown('<h2>Libros por autor</h2>', unsafe_allow_html=True)

            titulos=sorted([author for author in datos['author'].unique() if isinstance(author, str)])

            selec_authors=st.selectbox('Elige a un autor',titulos,index=None)
            
            years= datos['year'].unique()
            selec_years=None
            selec_month=None
            if selec_authors:
                if st.checkbox('Filtrar por año'):
                    selec_years=st.multiselect('elige un ano',sorted(years),default=years)
                    if selec_years:
                        if st.checkbox('filtrar por mes'):
                            selec_month=st.multiselect("elige un mes",["Enero", 'Febrero', "Marzo", 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])
            datos_filtrados=aplicar_filtros(datos,years=selec_years,mes=selec_month)
            datos_filtrados=datos_filtrados[datos_filtrados['author']==selec_authors]
            dataframe=datos_filtrados.drop(columns=['price','list_name_encoded'])
            st.write(dataframe)
            grafica=datos_filtrados.groupby(['month','year','list_name','rank','title']).size().reset_index(name='count').sort_values(by='count',ascending=False)
           
            mejores_libros(datos_filtrados,['month'],'libros más vendidos')
            fig = px.scatter(grafica, x='count', y='list_name', title=f'Listas donde aparece {selec_authors}', labels={'rank': 'Ranking', 'title': 'Título'})
            st.plotly_chart(fig)
            fig = px.scatter(grafica, x='rank', y='title', title=f'rankink de los libros de {selec_authors}', labels={'rank': 'Ranking', 'title': 'Título'})
            st.plotly_chart(fig)
    
    if 'show_authors' not in st.session_state:
        st.session_state.show_authors = False
    
    if c2.button('Comparar autores más populares por lista',use_container_width=6):
        st.session_state.show_authors = True
    
    if st.session_state.show_authors:
        with st.spinner('Cargando datos...'):
            st.markdown('<h2>Comparar autores más populares por lista</h2>', unsafe_allow_html=True)

            lista = st.selectbox('Selecciona la lista', (datos['list_name'].unique()))
            filrados_datos = aplicar_filtros(datos, list=lista)
            available_authors = (filrados_datos['author'].unique())
            
            varios_autores = st.multiselect('Selecciona los autores', available_authors)

            if varios_autores:
                filrados_datos = aplicar_filtros(datos, list=lista, autor=varios_autores)
                
                grouped_data = filrados_datos.groupby(['year', 'author']).size().reset_index(name='count').sort_values(by='count' ,ascending=False)
                
                fig = px.bar(
                    grouped_data, 
                    x='year', 
                    y='count', 
                    color='author',
                    barmode='group',
                    title='Número de Bestsellers por Autor y Año'
                )
                fig.update_layout(xaxis_title='Año', yaxis_title='Número de Bestsellers')
                st.plotly_chart(fig)
                st.write(filrados_datos)
            else:
                st.write("Selecciona al menos un autor.")
            st.markdown('<div class="section">', unsafe_allow_html=True)
    
   
    
    if 'compararbestsellers' not in st.session_state:
        st.session_state.compararbestsellers=False
    if c3.button('Comparar autores por cantidad de bestsellers',use_container_width=4):
        st.session_state.compararbestsellers=True
    if st.session_state.compararbestsellers:
        with st.spinner('cargando....'):
    # Filtros adicionales
            
            st.markdown('<h2>Comparar autores por cantidad de bestsellers</h2>', unsafe_allow_html=True)
            
            
            autores_disponibles_c3 = sorted([autor for autor in datos['author'].unique() if isinstance(autor, str)])
            filtro_autor = st.multiselect('Selecciona los autores', autores_disponibles_c3,help="Puede seleccionar más de uno")
            filtro_year= None
            filtro_mes=None
            if filtro_autor:
                if st.checkbox('Filtrar por años'):
                    filtro_year = st.multiselect("Elige uno o más años", sorted([year for year in datos['year'].unique() if pd.notna(year)]),key='hola')
                    if st.checkbox('Filtrar por mes'):
                    
                        filtro_mes = st.multiselect("Elige uno o más meses", ["Enero", 'Febrero', "Marzo", 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

            if st.button(':green[Mostrar resultados]'):
                filtered_data = aplicar_filtros(datos, years=filtro_year, mes=filtro_mes, autor=filtro_autor)
                    
                if not filtered_data.empty:
                    grouped_data = filtered_data.groupby(['year', 'author']).size().reset_index(name='count')
                    fig = px.bar(
                        grouped_data, 
                        x='year', 
                        y='count', 
                        color='author',
                        barmode='group',
                        title='Número de Bestsellers por Autor y Año (Filtro Adicional)'
                    )
                    
                    fig.update_layout(xaxis_title='Año', yaxis_title='Número de Bestsellers')
                    st.plotly_chart(fig)
                    st.write(filtered_data.drop(columns=['price','list_name_encoded']))
                else:
                    st.warning("No hay datos disponibles para los filtros seleccionados.")
                st.markdown('<div class="section">', unsafe_allow_html=True)
    if "freclistas" not in st.session_state:
        st.session_state.freclistas=False
    if c4.button("Autores frecuentes por lista",use_container_width=4):
        st.session_state.freclistas=True
    if st.session_state.freclistas:
        with st.spinner("Cargando..."):
            st.markdown('<h2>Autores frecuentes por listas</h2>', unsafe_allow_html=True)

            years_multiselect= st.multiselect("Elige uno o más años", sorted([year for year in datos['year'].unique() if pd.notna(year)]),key="diferente")
            mes_multi = None
            if years_multiselect:
                if st.checkbox('Filtrar por mes'):
                    mes_multi = st.multiselect("Elige un mes", ["Enero", 'Febrero', "Marzo", 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

            selec_list = st.selectbox('Selecciona la lista', sorted(datos['list_name'].unique()))

            datos_filtrados = aplicar_filtros(datos, list=selec_list, years=years_multiselect, mes=mes_multi)
            
            if not datos_filtrados.empty:
                grouped_data = datos_filtrados.groupby([ 'author']).size().reset_index(name='count').head(10)
                top_authors = grouped_data.sort_values(by='count', ascending=False).head(10)
                fig = px.bar(
                    grouped_data, 
                    x='author', 
                    y='count', 
                    color='author',
                    barmode='group',
                    
                    title='Autores con más Bestsellers por Año'
                )
                fig.update_layout(xaxis_title='Año', yaxis_title='Número de Bestsellers')
                # st.plotly_chart(fig)
                
                fig = px.pie(
                        top_authors, 
                        values='count', 
                        names='author', 
                        title='Proporción de Bestsellers por Autor',
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                st.plotly_chart(fig)
                dataframe=datos_filtrados.drop(columns=['price',"list_name_encoded"])
                st.write(dataframe)

            else:
                    st.error("No hay datos disponibles para los filtros seleccionados.")
            st.markdown('<div class="section">', unsafe_allow_html=True)
    if "boton" not in st.session_state:
        st.session_state.boton=False
    if c5.button("Editoriales por autores",use_container_width=4):
        st.session_state.boton=True
    if st.session_state.boton:
        with st.spinner("Cargando..."):
            
            st.markdown('<h2>Editoriales por autores</h2>', unsafe_allow_html=True)

            autores_disponibles = sorted([autor for autor in datos['author'].unique() if isinstance(autor, str)])
            

            autores = st.selectbox('Selecciona los autores', autores_disponibles,key='MaS')
            

            
            if autores:
                author_data = datos[datos['author'] == autores]
                
                
                editorials_by_year = author_data.groupby(['year', 'publisher'])['title'].nunique().reset_index(name='count')

                if not editorials_by_year.empty:
                    fig = px.bar(
                        editorials_by_year,
                        x='year',
                        y='count',
                        color='publisher',
                    
                        title=f'Editoriales en las que ha publicado {autores} a lo largo de los años',
                        barmode='stack'
                    )
                    fig.update_layout(xaxis_title='Año', yaxis_title='Número de Publicaciones')
                    st.plotly_chart(fig)
                    fig = px.area(
                        editorials_by_year,
                        x='year',
                        y='count',
                        color='publisher',
                        title=f'Editoriales en las que ha publicado {autores} a lo largo de los años',
                        labels={'count': 'Número de Publicaciones', 'publisher': 'Editorial'},
                        
                        
                    )
                    fig.update_layout(xaxis_title='Año', yaxis_title='Número de Publicaciones')
                    st.plotly_chart(fig)

                else:
                    st.write(f"No se encontraron datos de publicaciones para {autores}.")
                st.markdown('<div class="section ">', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                            
        
    

elif page == 'Editoriales':
    st.markdown('<div class="header">📚 Book Analysis - Editoriales</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2>Editoriales más populares</h2>', unsafe_allow_html=True)
    st.write('editoriales')
    listas= datos['list_name'].unique()
    editoriales=datos['publisher'].unique()
    publisher=st.selectbox('selecciona una editorial',editoriales)
    editoriales_filtradas=datos[datos['publisher']==publisher]
    editorialgrafica=editoriales_filtradas.groupby(['year',"list_name"]).size().reset_index(name='count')


   

    fig = px.bar(
    editorialgrafica, 
    x='year', 
    y='count', 
    color='list_name',
    title=f'Apariciones de {publisher} en diferentes listas a lo largo del tiempo',
    labels={'count': 'Número de Apariciones', 'list_name': 'Lista', 'year': 'Año'},
    barmode='stack')
    st.plotly_chart(fig)
    success_by_list = editoriales_filtradas.groupby(['list_name']).size().reset_index(name='count')
    fig = px.bar(success_by_list, x='list_name', y='count', color='list_name', title=f'Éxito por Lista de {publisher}')
    st.plotly_chart(fig)
    listas_selct=st.selectbox('elige una lista',listas)

    edi_data= datos[datos['list_name']==listas_selct]
    publishers_count = edi_data['publisher'].value_counts().reset_index()
    publishers_count.columns = ['publisher', 'count']
    fig = px.bar(publishers_count.head(10), x='publisher', y='count', title=f'Editoriales con más libros en la lista {listas_selct}')
    st.plotly_chart(fig)
    fig = px.scatter(editoriales_filtradas, x='rank', y='title', title=f'Posiciones en listas para {publisher}', labels={'rank': 'Ranking', 'title': 'Título'})
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

