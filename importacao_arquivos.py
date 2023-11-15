import streamlit as st
import connection as conn
import os
import pandas as pd
from funcoes import *
from sqlalchemy import create_engine
from zipfile import ZipFile
from ConsultasSQL import delete
import yaml
from yaml.loader import SafeLoader
from  util import mensagem as msg


def app():
    st.subheader("Importação dos arquivos Acompanhamento Mensal (AM) e Balancete", divider='rainbow')

    if not st.session_state.authentication_status:
        msg.warning("Necessário Logar no Sistema")
    elif not st.session_state.ativo:
        msg.warning("Usuário não está ativo")
    else:

        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        engine = create_engine(config['conection']['url'])

        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        css = '''
            <style>
            [data-testid="stFileUploadDropzone"] div div::before {content:"Arraste aqui seu arquivo ou clique no botão 'Browse Files' "}
            [data-testid="stFileUploadDropzone"] div div span{display:none;}
            [data-testid="stFileUploadDropzone"] div div::after {font-size: .8em; content:"Somente arquivos formato ZIP"}
            [data-testid="stFileUploadDropzone"] div div small{display:none;}
            </style>
            '''
        st.markdown(css, unsafe_allow_html=True)

        tudoOK = True
        ano_arquivo_AM = ano_arquivo_Bal = None
        cod_municipio_AM = cod_municipio_BAL = None
        cod_orgao_AM = cod_orgao_BAL = None
        mes_AM = mes_BAL = None

        col1, col2 = st.columns(2)
        with col1:
            arquivo_AM = st.file_uploader("Arquivo AM",
                                          type=["zip"],
                                          accept_multiple_files=False )

            if arquivo_AM is not None:
                arquivo = arquivo_AM.name.split('_')

                if arquivo[0] != 'AM':
                    msg.error('Arquivo não é AM (Acompanhamento Mensal)')
                    tudoOK = False

                # pega o cod Municipio do AM
                cod_municipio_AM = arquivo[1]
                st.session_state.cod_municipio_AM = cod_municipio_AM

                # pega o orgao do AM
                cod_orgao_AM = arquivo[2]
                st.session_state.cod_orgao = cod_orgao_AM

                # pega o Mes do AM
                mes_AM = arquivo[3]
                st.session_state.mes = mes_AM

                # pegar no ano no arquivo AM
                ano_arquivo_AM = int(arquivo[4][0:4])
                st.session_state.ano = ano_arquivo_AM

            else:
                tudoOK = False

        with col2:
            arquivo_BAL = st.file_uploader("Arquivo Balancete",
                                           type=["zip"],
                                           accept_multiple_files=False)

            if arquivo_BAL is not None:
                arquivo = arquivo_BAL.name.split('_')

                if arquivo[0] != 'BALANCETE':
                    msg.error('Arquivo não é Balancete')
                    tudoOK = False

                # pega o Cod Municipio do Balancete
                cod_municipio_BAL = arquivo[1]

                # pega o orgao do BAL
                cod_orgao_BAL = arquivo[2]

                # pega o Mes do BAL
                mes_BAL = arquivo[3]

                # pegar no ano no arquivo Balancete
                ano_arquivo_Bal = int(arquivo[4][0:4])
            else:
                tudoOK = False

        # validações entre os dois arquivos
        if ano_arquivo_AM is not None and ano_arquivo_Bal is not None and ano_arquivo_AM != ano_arquivo_Bal:
            msg.error(f"O Ano do arquivo AM ({ano_arquivo_AM}) está diferente do Ano do arquivo Balancete ({ano_arquivo_Bal}) ")
            tudoOK = False

        if cod_municipio_AM is not None and cod_municipio_BAL is not None and cod_municipio_AM != cod_municipio_BAL:
            msg.error(f"O Código do Municipio do arquivo AM ({cod_municipio_AM}) está diferente do Código do Municipio do arquivo Balancete ({cod_municipio_BAL}) ")
            tudoOK = False

        if cod_orgao_AM is not None and cod_orgao_BAL is not None and cod_orgao_AM != cod_orgao_BAL:
            msg.error(f"O Código do Orgão do arquivo AM ({cod_orgao_AM}) está diferente do Código do Orgão do arquivo Balancete ({cod_orgao_BAL})")
            tudoOK = False

        if mes_AM is not None and mes_BAL is not None and mes_AM != mes_BAL:
            msg.error(f"O Mês de geração do arquivo AM ({mes_AM}) está diferente do Mês de geração do arquivo Balancete ({mes_BAL})")
            tudoOK = False

        st.divider()

        if tudoOK:
            if st.button("Processar os arquivos", type="primary"):
                
                # deletando informaçoes da tabela
                delete(ano_arquivo_Bal, st.session_state.username)

                # criando pasta temporaria e mandando o arquivo zip pra pasta
                pasta_temp = criar_pasta_temporaria()

                pasta_AM = criar_pasta_tipo_arquivo(pasta_temp, "AM")
                pasta_BAL = criar_pasta_tipo_arquivo(pasta_temp, "BAL")

                arquivo_zip_AM = os.path.join(pasta_AM, arquivo_AM.name)
                arquivo_zip_BAL = os.path.join(pasta_BAL, arquivo_BAL.name)

                with open(arquivo_zip_AM, "wb") as f:
                    f.write(arquivo_AM.getbuffer())
                f.close()

                with open(arquivo_zip_BAL, "wb") as f:
                    f.write(arquivo_BAL.getbuffer())
                f.close()

                # Descompactando o arquivo AM
                with ZipFile(arquivo_zip_AM, 'r') as zip:
                    zip.extractall(pasta_AM)

                # Descompactando o arquivo Balancete
                with ZipFile(arquivo_zip_BAL, 'r') as zip:
                    zip.extractall(pasta_BAL)

                nomes_colunas = ['seq1', 'seq2', 'seq3', 'seq4', 'seq5', 'seq6', 'seq7', 'seq8', 'seq9', 'seq10', 'seq11', 'seq12', 'seq13', 'seq14', 'seq15', 'seq16', 'seq17', 'seq18', 'seq19', 'seq20',
                                 'seq21', 'seq22', 'seq23', 'seq24', 'seq25', 'seq26', 'seq27', 'seq28', 'seq29', 'seq30', 'seq31', 'seq32', 'seq33', 'seq34', 'seq35', 'seq36', 'seq37', 'seq38', 'seq39', 'seq40']
                dtypes = {coluna: str for coluna in range(30)}

                # Carregando os arquivos AM
                my_bar_AM = st.progress(0, text="")
                indice = 1

                quantidade_arquivos = len(os.listdir(pasta_AM))

                for arquivo_csv in os.listdir(pasta_AM):
                    if arquivo_csv.upper().endswith('.CSV'):

                        my_bar_AM.progress(int(indice / quantidade_arquivos * 100), text="Processando arquivo Acompanhamento Mensal (AM)... aguarde")
                        indice += 1

                        # Pegando o nome do arquivo
                        x = arquivo_csv.rfind(".")
                        nome_arquivo = arquivo_csv[:x].upper()

                        processa = False
                        if nome_arquivo == 'AEX' or \
                                nome_arquivo == 'ALQ' or \
                                nome_arquivo == 'ANL' or \
                                nome_arquivo == 'AOB' or \
                                nome_arquivo == 'AOC' or \
                                nome_arquivo == 'AOP' or \
                                nome_arquivo == 'ARC' or \
                                nome_arquivo == 'CAIXA' or \
                                nome_arquivo == 'CTB' or \
                                nome_arquivo == 'CONCIBANC' or \
                                nome_arquivo == 'CUTE' or \
                                nome_arquivo == 'EMP' or \
                                nome_arquivo == 'EXT' or \
                                nome_arquivo == 'IDE' or \
                                nome_arquivo == 'IDERP' or \
                                nome_arquivo == 'LQD' or \
                                nome_arquivo == 'OBELAC' or \
                                nome_arquivo == 'OPS' or \
                                nome_arquivo == 'ORGAO' or \
                                nome_arquivo == 'REC' or \
                                nome_arquivo == 'RSP':
                            processa = True

                        if processa:

                            arq_completo = os.path.join(pasta_AM, arquivo_csv)

                            # Carregar o arquivo CSV em um DataFrame do Pandas
                            df = pd.read_csv(arq_completo, 
                                             delimiter=';', 
                                             encoding='latin-1',
                                             header=None, 
                                             names=nomes_colunas, 
                                             dtype=dtypes)

                            # Preencher com None para completar até 30 colunas
                            df = df.reindex(columns=[*df.columns, *range(30 - len(df.columns))])

                            # Manter apenas as 30 primeiras colunas
                            df = df.iloc[:, :30]

                            # Substituir NaN por None
                            df = df.where(pd.notna(df), None)

                            df.insert(0, 'ano', ano_arquivo_AM)
                            df.insert(0, 'arquivo', nome_arquivo)
                            df.insert(0, 'modulo', "AM")
                            df.insert(0, 'usuario', st.session_state.username)

                            df.to_sql('tce_sicom', engine, if_exists='append', index=False)

                msg.success("Arquivo ACOMPANHAMENTO MENSAL (AM) Importado com Sucesso")

                my_bar_AM.empty()

                # Carregando os arquivos Balancete
                my_bar_BAL = st.progress(0, text="")
                indice = 1

                quantidade_arquivos = len(os.listdir(pasta_BAL))

                for arquivo_csv in os.listdir(pasta_BAL):
                    if arquivo_csv.upper().endswith('.CSV'):

                        my_bar_BAL.progress(int(indice / quantidade_arquivos * 100), text="Processando arquivo Balancete... aguarde")
                        indice += 1

                        # Pegando o nome do arquivo
                        x = arquivo_csv.rfind(".")
                        nome_arquivo = arquivo_csv[:x].upper()

                        processa = False
                        if nome_arquivo == 'BALANCETE':
                            processa = True

                        if processa:
                            arq_completo = os.path.join(pasta_BAL, arquivo_csv)

                            # Carregar o arquivo CSV em um DataFrame do Pandas
                            df = pd.read_csv(arq_completo, 
                                             delimiter=';', 
                                             encoding='latin-1',
                                             header=None, 
                                             names=nomes_colunas, 
                                             dtype=dtypes)

                            # Preencher com None para completar até 30 colunas
                            df = df.reindex(columns=[*df.columns, *range(30 - len(df.columns))])

                            # Manter apenas as 30 primeiras colunas
                            df = df.iloc[:, :30]

                            # Substituir NaN por None
                            df = df.where(pd.notna(df), None)

                            df.insert(0, 'ano', ano_arquivo_Bal)
                            df.insert(0, 'arquivo', nome_arquivo)
                            df.insert(0, 'modulo', "BAL")
                            df.insert(0, 'usuario', st.session_state.username)

                            df.to_sql('tce_sicom', engine,if_exists='append', index=False)

                msg.success("Arquivo BALANCETE Importado com Sucesso.")

                # Deletando a pasta depois do processamento
                deletando_pasta(pasta_temp)

                my_bar_BAL.empty()

                st.info("Clique em Menu >> Resultado da Apuração")
