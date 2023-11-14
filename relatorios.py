import streamlit as st
import pandas as pd
from ConsultasSQL import *
from funcoes import *
from  util import mensagem as msg


def app():
    st.subheader("Relatórios", divider='rainbow')

    if not st.session_state.authentication_status:
        msg.warning("Necessário Logar no Sistema")
    else:
        if not st.session_state.cod_municipio_AM:
            msg.error("Sem Informações a serem processadas e visualizadas")
        else:
            opcoes = ['Analítico de Despesa', 'Movimentos Por Fonte']

            relatorios = st.radio(" ", opcoes, index=0)
            
            st.divider()

            if st.button("Imprimir"):
                if relatorios == 'Analítico de Despesa':
                    dados = relatorioAnaliticoEmpenho(st.session_state.username, st.session_state.ano)

                    # Exibe os dados em uma tabela
                    if dados:
                        df = pd.DataFrame(dados, columns=['Empenho', 'Fonte\nRecurso', 'Cod.\nOper.', 'Empenhado', 'Anulado\nEmpenhado', 'Liquidado', 'Anulado\nLiquidado', 'Pago', 'Anulado\nPago'])

                        # Exibindo a tabela estilizada
                        st.write('Dados do relatório:')
                        st.dataframe(df, width=1800, height=1000)  # Ajuste o tamanho conforme necessário

                        pdf_filename = "Analítico de Despesa.pdf"

                        exportar_pdf(df, pdf_filename, formato="A4", orientacao="portrait", percentual_tabela=10, tamanho_letra=7)
                        exportar_excel(df, "Analítico de Despesa.xlsx")
                    else:
                        msg.error("Nenhum dado encontrado para os parâmetros inseridos")  
                elif relatorios == 'Movimentos Por Fonte':
                    dados = totalizaMovimentosPorFonte(st.session_state.username, st.session_state.ano)

                    # Exibe os dados em uma tabela
                    if dados:
                        df = pd.DataFrame(dados, columns=['Fonte\nRecurso', 'Receita', 'Anulação\nReceita', 'Entrada\nBanco', 'Saida\nBanco', 'Entrada\nCaixa', 'Saida\nCaixa', 'Entrada\nCUTE', 'Saida\nCUTE', 'Empenho', 'Reforço\nEmpenho', 'Aulação\nEmpenho', 'Liquidação', 'Retenção', 'Anulação\nliquidação', 'Anulação\nRetenção', 'Pagamento\nExtra', 'Anulação\nPagto Extra', 'Pagamento', 'Aulação\nPagamento', 'Outras\nBaixas', 'Anul.Outras\nBaixas', 'Inscrição\nRestos' ])
                        st.write('Dados do relatório:')
                        st.dataframe(df, width=1800, height=1000)  # Ajuste o tamanho conforme necessário

                        pdf_filename = "Movimentos Por Fonte.pdf"
                        exportar_pdf(df, pdf_filename, formato="A4", orientacao="landscape", percentual_tabela=6, tamanho_letra=5)
                        exportar_excel(df, "Movimentos Por Fonte.xlsx")
                    else:
                        msg.error("Nenhum dado encontrado para os parâmetros inseridos")