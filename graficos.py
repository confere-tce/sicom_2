import streamlit as st
from ConsultasSQL import *
import pandas as pd
import altair as alt
from  util import mensagem as msg

def app():
    st.subheader("Gráficos", divider='rainbow')

    if not st.session_state.authentication_status:
        msg.warning("Necessário Logar no Sistema")
    elif not st.session_state.ativo:
        msg.warning("Usuário não está ativo")        
    else: 
        # st.markdown("<style>.block-container {background-color: #fffff0; border-radius: 20px; box-shadow: 3px 3px 3px #888;}</style>", unsafe_allow_html=True)

        if not st.session_state.cod_municipio_AM:
            msg.error("Sem Informações a serem processadas e visualizadas")
        else:
            ##### EMPENHOS #####
            with st.container():

                dados = graficoEmpenhoReceita(st.session_state.username, st.session_state.ano)
                valores = [float(dados[0][0]), float(dados[0][1])]

                col1, col2, col3 = st.columns(3)
                with col1:
                    source = pd.DataFrame({
                        'Tipo': ['Empenho', 'Receita'],
                        'Valores em R$': valores
                    })

                    bar_chart = alt.Chart(source).mark_bar().encode(
                        x='Tipo',
                        y='Valores em R$:Q',
                        color=alt.Color('Tipo', scale=alt.Scale( domain=['Empenho', 'Receita'], range=['red', 'green']))
                    ).properties(
                        title='Empenho x Receitas',
                        width=300, 
                        height=300
                    )

                    st.altair_chart(bar_chart, use_container_width=True)

                with col2:
                    # st.markdown("<p style='color: red; font-weight: bold'>Empenho x Receita</p>", unsafe_allow_html=True) -> de exemplo

                    source = pd.DataFrame({
                        'Tipo': ['Empenho', 'Receita'],
                        'Valores em R$': valores
                    })

                    bar_chart = alt.Chart(source).mark_arc().encode(
                        theta="Valores em R$",
                        color="Tipo"
                    ).properties(
                        title='Empenho x Receitas',
                        width=300,
                        height=300
                    )

                    st.altair_chart(bar_chart, use_container_width=True)
                with col3:
                    source = pd.DataFrame({
                        'Tipo': ['Empenho', 'Receita'],
                        'Valores em R$': valores
                    })

                    bar_chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
                        # theta="Valores em R$",
                        # color="Tipo:N",
                        theta=alt.Theta(
                            field="Valores em R$", 
                            type="quantitative", 
                            stack=True, 
                            scale=alt.Scale(type="linear", rangeMax=1.5708, rangeMin=-1.5708)),
                        color=alt.Color('Tipo', scale=alt.Scale(
                            domain=['Empenho', 'Receita'], range=['red', 'green']))
                    ).properties(
                        title='Empenho x Receitas',
                        width=300,
                        height=300
                    )

                    st.altair_chart(bar_chart, use_container_width=True)

            # with st.container():
            #     dados = graficoEmpenhoDiarios(st.session_state.username, st.session_state.ano)

            #     dias = []
            #     valores = []

            #     i = 0
            #     for dado in dados:
            #         dias.append(dados[i][0])
            #         valores.append(float(dados[i][1]))
            #         i += 1

            #     source = pd.DataFrame({
            #         'a': dias,
            #         'b': valores
            #     })

            #     bar_chart =alt.Chart(source).mark_area().encode(
            #         x='a',
            #         y='b'
            #     )

            #     st.altair_chart(bar_chart, use_container_width=True)

            #     container_style = (
            #         "background-color: red; padding: 10px; border-radius: 10px; box-shadow: 3px 3px 3px #888;"
            #     )
            #     container = st.container()
            #     container.markdown('<p style="color: black;">This is a color container with custom styling.</p>', unsafe_allow_html=True)
            #     container.write("You can put your content here.")

            #     # You can use CSS to style the container
            #     container.style = container_style
            
