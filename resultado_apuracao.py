import streamlit as st
import locale
from funcoes import *
from ConsultasSQL import *
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


def app():
    st.subheader("Resultado da Apuração", divider='rainbow')

    if not st.session_state.authentication_status:
        st.warning("Necessário Logar no Sistema", icon="⚠️")
    else:
        if not st.session_state.cod_municipio_AM:
            st.error("Sem Informações a serem processadas e visualizadas", icon="🚨")
        else:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

            custom_css = {
                ".ag-cell": {"text-align": "right"},
            }

            total_linhas_pagina_ag_grid = 20

            ######## DADOS BANCÁRIOS ############
            st.subheader(":red[Contas Bancárias:]")

            bancos = confereSaldoFinalBancos(
                st.experimental_user, st.session_state.ano)
            if bancos:
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Saldo Final no CTB", value=locale.currency(
                    bancos[0][0], grouping=True, symbol=False))
                col2.metric(label="Saldos Contabilizados no Balancete", value=locale.currency(
                    bancos[0][1], grouping=True, symbol=False))
                col3.metric(label="Diferença encontrada", value=locale.currency(
                    bancos[0][0] - bancos[0][1], grouping=True, symbol=False))
                style_metric_cards(background_color="back",
                                border_left_color="gray")

                if bancos[0][0] == bancos[0][1]:
                    st.success(
                        "Os valores dos arquivos CTB de Contas Bancárias do BALANCETE de Contas Bancárias são iguais", icon="✅")
                else:
                    # Exibe os dados da diferença
                    st.warning(
                        "Os valores dos arquivos CTB de Contas Bancárias do BALANCETE de Contas Bancárias são diferentes", icon="⚠️")

                    ficha = []
                    fonteRecurso = []
                    saldo_Final_CTB = []
                    saldo_Final_BAL = []
                    diferenca = []

                    valores = buscaDiferencaSaldoFinalBancos(st.experimental_user, st.session_state.ano)
                    with st.expander("Dados com diferença nos saldos finais:"):
                        for linha in valores:
                            ficha.append(str(linha[0]))
                            fonteRecurso.append('{}.{}.{}'.format(linha[1][:1], linha[1][1:4], linha[1][4:]))
                            saldo_Final_CTB.append(locale.currency(linha[2], grouping=True, symbol=False))
                            saldo_Final_BAL.append(locale.currency(linha[3], grouping=True, symbol=False))
                            diferenca.append(locale.currency(linha[2] - linha[3], grouping=True, symbol=False))

                        df = pd.DataFrame({
                            "Ficha": ficha,
                            "Fonte Recurso": fonteRecurso,
                            "Saldo Final no CTB": saldo_Final_CTB,
                            "Saldo Final no Balancete": saldo_Final_BAL,
                            "Diferença": diferenca,
                        })

                        gb = GridOptionsBuilder.from_dataframe(df)
                        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
                        gb.configure_column('Ficha', minWidth=120, maxWidth=120)
                        gb.configure_column('Fonte Recurso', minWidth=120, maxWidth=120)
                        gridoption = gb.build()

                        AgGrid(df,
                            gridOptions=gridoption,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                            custom_css=custom_css,
                            allow_unsafe_jscode=True)
            else:
                st.success(
                    "Não foram encontrados dados Saldo de Bancários para o usuário e ano fornecidos", icon="✅")

            bancos = confereSaldoFinalBancosNaoCompoe(
                st.experimental_user, st.session_state.ano)
            if bancos:
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Saldo Final no CTB não Compõe Saldo de Caixa",
                            value=locale.currency(bancos[0][0], grouping=True, symbol=False))
                col2.metric(label="Saldos Contabilizados no Balancete não Compõe Saldo de Caixa",
                            value=locale.currency(bancos[0][1], grouping=True, symbol=False))
                col3.metric(label="Diferença encontrada", value=locale.currency(
                    bancos[0][0] - bancos[0][1], grouping=True, symbol=False))
                style_metric_cards(background_color="back",
                                border_left_color="gray")

                if bancos[0][0] == bancos[0][1]:
                    st.success(
                        "Os valores dos arquivos CTB não Compõe Saldo de Caixa e Contas Bancárias não Compõe Saldo de Caixa do BALANCETE são iguais", icon="✅")
                else:
                    # Exibe os dados da diferença
                    st.warning(
                        "Os valores dos arquivos CTB não Compõe Saldo de Caixa e Contas Bancárias não Compõe Saldo de Caixa do BALANCETE são diferentes", icon="⚠️")

                    ficha = []
                    fonteRecurso = []
                    saldo_Final_CTB = []
                    saldo_Final_BAL = []
                    diferenca = []

                    valores = buscaDiferencaSaldoFinalBancosNaoCompoe(
                        st.experimental_user, st.session_state.ano)
                    with st.expander("Dados com diferença nos saldos finais:"):
                        for linha in valores:
                            ficha.append(linha[0])
                            fonteRecurso.append('{}.{}.{}'.format(
                                linha[1][:1], linha[1][1:4], linha[1][4:]))
                            saldo_Final_CTB.append(locale.currency(
                                linha[2], grouping=True, symbol=False))
                            saldo_Final_BAL.append(locale.currency(
                                linha[3], grouping=True, symbol=False))
                            diferenca.append(locale.currency(
                                linha[2] - linha[3], grouping=True, symbol=False))

                        df = pd.DataFrame({
                            "Ficha": ficha,
                            "Fonte Recurso": fonteRecurso,
                            "Saldo Final no CTB": saldo_Final_CTB,
                            "Saldo Final no Balancete": saldo_Final_BAL,
                            "Diferença": diferenca,
                        })

                        gb = GridOptionsBuilder.from_dataframe(df)
                        gb.configure_pagination(
                            paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
                        gb.configure_column('Ficha', minWidth=120, maxWidth=120)
                        gb.configure_column(
                            'Fonte Recurso', minWidth=120, maxWidth=120)
                        gridoption = gb.build()

                        AgGrid(df,
                            gridOptions=gridoption,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                            custom_css=custom_css,
                            allow_unsafe_jscode=True)
            else:
                st.success(
                    "Não foram encontrados dados de Valores que não Compõe Saldo de Caixa para o usuário e ano fornecidos", icon="✅")

            bancos = confereSaldoFinalBancosRestituiveis(
                st.experimental_user, st.session_state.ano)
            if bancos:
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Saldo Final no CTB Valores Restituíveis", value=locale.currency(
                    bancos[0][0], grouping=True, symbol=False))
                col2.metric(label="Saldos Contabilizados no Balancete Valores Restituíveis",
                            value=locale.currency(bancos[0][1], grouping=True, symbol=False))
                col3.metric(label="Diferença encontrada", value=locale.currency(
                    bancos[0][0] - bancos[0][1], grouping=True, symbol=False))
                style_metric_cards(background_color="back",
                                border_left_color="gray")

                if bancos[0][0] == bancos[0][1]:
                    st.success(
                        "Os valores dos arquivos CTB Valores Restituíveis e Contas Bancárias Valores Restituíveis do BALANCETE são iguais", icon="✅")
                else:
                    # Exibe os dados da diferença
                    st.warning(
                        "Os valores dos arquivos CTB Valores Restituíveis e Contas Bancárias Valores Restituíveis do BALANCETE são diferentes", icon="⚠️")

                    ficha = []
                    fonteRecurso = []
                    saldo_Final_CTB = []
                    saldo_Final_BAL = []
                    diferenca = []

                    valores = buscaDiferencaSaldoFinalBancosRestituiveis(
                        st.experimental_user, st.session_state.ano)
                    with st.expander("Dados com diferença nos saldos finais:"):
                        for linha in valores:
                            ficha.append(linha[0])
                            fonteRecurso.append('{}.{}.{}'.format(
                                linha[1][:1], linha[1][1:4], linha[1][4:]))
                            saldo_Final_CTB.append(locale.currency(
                                linha[2], grouping=True, symbol=False))
                            saldo_Final_BAL.append(locale.currency(
                                linha[3], grouping=True, symbol=False))
                            diferenca.append(locale.currency(
                                linha[2] - linha[3], grouping=True, symbol=False))

                        df = pd.DataFrame({
                            "Ficha": ficha,
                            "Fonte Recurso": fonteRecurso,
                            "Saldo Final no CTB": saldo_Final_CTB,
                            "Saldo Final no Balancete": saldo_Final_BAL,
                            "Diferença": diferenca,
                        })

                        gb = GridOptionsBuilder.from_dataframe(df)
                        gb.configure_pagination(
                            paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
                        gb.configure_column('Ficha', minWidth=120, maxWidth=120)
                        gb.configure_column(
                            'Fonte Recurso', minWidth=120, maxWidth=120)
                        gridoption = gb.build()

                        AgGrid(df,
                            gridOptions=gridoption,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                            custom_css=custom_css,
                            allow_unsafe_jscode=True)
            else:
                st.success(
                    "Não foram encontrados dados de Valores Restituíveis para o usuário e ano fornecidos", icon="✅")

            # Exibe Conciliacao Bancaria
            concilicacao_bancos = buscaValoresConciliacaoBancaria(
                st.experimental_user, st.session_state.ano)
            if concilicacao_bancos:
                with st.expander("Informações de Conciliação Bancária"):
                    for linha in concilicacao_bancos:
                        if linha[1] == '1':
                            st.write(
                                f"Ficha: {linha[0]} - Entradas contabilizadas e não consideradas no extrato bancário: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '2':
                            st.write(
                                f"Ficha: {linha[0]} - Saídas contabilizadas e não consideradas no extrato bancário: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '3':
                            st.write(
                                f"Ficha: {linha[0]} - Entradas não consideradas pela contabilidade: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '4':
                            st.write(
                                f"Ficha: {linha[0]} - Saídas não consideradas pela contabilidade: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        else:
                            st.write("Valor desconhecido")

            ######## DADOS EMPENHOS ############
            st.divider()

            st.subheader(":red[Valores Empenhados:]")

            empenhos = confereValoresEmpenhados(
                st.experimental_user, st.session_state.ano)
            if empenhos:
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Valores Empenhados", value=locale.currency(
                    empenhos[0][0], grouping=True, symbol=False))
                col2.metric(label="Valores Contabilizados no Balancete", value=locale.currency(
                    empenhos[0][1], grouping=True, symbol=False))
                col3.metric(label="Diferença encontrada", value=locale.currency(
                    empenhos[0][0] - empenhos[0][1], grouping=True, symbol=False))
                style_metric_cards(background_color="back",
                                border_left_color="gray")

                if empenhos[0][0] == empenhos[0][1]:
                    st.success(
                        "Os valores dos arquivos EMP e Contabilizados no Balancete são iguais", icon="✅")
                else:
                    # Exibe os dados da diferença
                    st.warning(
                        "Os valores dos arquivos EMP e Contabilizados no Balancete são diferentes", icon="⚠️")

                    funcional = []
                    fonteRecurso = []
                    saldo_EMP_AM = []
                    saldo_Final_BAL = []
                    diferenca = []

                    valores = buscaDiferencaValoresEmpenhados(
                        st.experimental_user, st.session_state.ano)
                    with st.expander("Dados com diferença nos saldos finais:"):
                        for linha in valores:
                            funcional.append(
                                f"{linha[0]}.{linha[1]}.{linha[2]}.{linha[3]}.{linha[4]}.{linha[5]}.{linha[6]}.{linha[7]}")
                            fonteRecurso.append('{}.{}.{}'.format(
                                linha[8][:1], linha[8][1:4], linha[8][4:]))
                            saldo_EMP_AM.append(locale.currency(
                                linha[9], grouping=True, symbol=False))
                            saldo_Final_BAL.append(locale.currency(
                                linha[10], grouping=True, symbol=False))
                            diferenca.append(locale.currency(
                                linha[9] - linha[10], grouping=True, symbol=False))

                        df = pd.DataFrame({
                            "Funcional": funcional,
                            "Fonte Recurso": fonteRecurso,
                            "Total Empenhado": saldo_EMP_AM,
                            "Saldo Final no Balancete": saldo_Final_BAL,
                            "Diferença": diferenca,
                        })

                        gb = GridOptionsBuilder.from_dataframe(df)
                        gb.configure_pagination(
                            paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
                        gb.configure_column(
                            'Funcional', minWidth=250, maxWidth=250)
                        gb.configure_column(
                            'Fonte Recurso', minWidth=120, maxWidth=120)
                        gridoption = gb.build()

                        AgGrid(df,
                            gridOptions=gridoption,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                            custom_css=custom_css,
                            allow_unsafe_jscode=True)
            else:
                st.error(
                    "Não foram encontrados dados para o usuário e ano fornecidos", icon="✅")

            ######## DADOS RECEITAS ############
            st.divider()

            st.subheader(":red[Valores de Receitas:]")

            receitas = confereValoresReceitas(
                st.experimental_user, st.session_state.ano)
            if receitas:
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Valores Receita", value=locale.currency(
                    receitas[0][0], grouping=True, symbol=False))
                col2.metric(label="Valores Contabilizados no Balancete", value=locale.currency(
                    receitas[0][1], grouping=True, symbol=False))
                col3.metric(label="Diferença encontrada", value=locale.currency(
                    receitas[0][0] - receitas[0][1], grouping=True, symbol=False))
                style_metric_cards(background_color="back",
                                border_left_color="gray")

                if receitas[0][0] == receitas[0][1]:
                    st.success(
                        "Os valores dos arquivos REC e Contabilizados no Balancete são iguais", icon="✅")
                else:
                    # Exibe os dados da diferença
                    st.warning(
                        "Os valores dos arquivos REC e Contabilizados no Balancete são diferentes", icon="⚠️")

                    receita = []
                    fonteRecurso = []
                    saldo_REC_AM = []
                    saldo_Final_BAL = []
                    diferenca = []

                    valores = buscaDiferencaValoresReceitas(
                        st.experimental_user, st.session_state.ano)
                    with st.expander("Dados com diferença nos saldos finais:"):
                        for linha in valores:
                            receita.append('{}.{}.{}.{}.{}.{}.{}'.format(
                                linha[0][:1], linha[0][1:2], linha[0][2:3], linha[0][3:4], linha[0][4:6], linha[0][6:7], linha[0][7:]))
                            fonteRecurso.append('{}.{}.{}'.format(
                                linha[1][:1], linha[1][1:4], linha[1][4:]))
                            saldo_REC_AM.append(locale.currency(
                                linha[2], grouping=True, symbol=False))
                            saldo_Final_BAL.append(locale.currency(
                                linha[3], grouping=True, symbol=False))
                            diferenca.append(locale.currency(
                                linha[2] - linha[3], grouping=True, symbol=False))

                        df = pd.DataFrame({
                            "Receita": receita,
                            "Fonte Recurso": fonteRecurso,
                            "Total Receita": saldo_REC_AM,
                            "Saldo Final no Balancete": saldo_Final_BAL,
                            "Diferença": diferenca,
                        })

                        gb = GridOptionsBuilder.from_dataframe(df)
                        gb.configure_pagination(
                            paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
                        gb.configure_column('Receita', minWidth=120, maxWidth=120)
                        gb.configure_column(
                            'Fonte Recurso', minWidth=120, maxWidth=120)
                        gridoption = gb.build()

                        AgGrid(df,
                            gridOptions=gridoption,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                            custom_css=custom_css,
                            allow_unsafe_jscode=True)
            else:
                st.error(
                    "Não foram encontrados dados para o usuário e ano fornecidos", icon="✅")

            st.divider()
