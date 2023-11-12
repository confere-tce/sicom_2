import streamlit as st
from streamlit_option_menu import option_menu
from funcoes import *
import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
import home
import conta
import importacao_arquivos
import relatorios
import resultado_apuracao
import graficos
from ConsultasSQL import criaView, usuario

# from streamlit_extras.app_logo import add_logo

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Consulta TCE"
)

criaView()

# escondendo os botoes e menus padrao de tela
hide_menu = """
    <style>
    #MainMenu{
        visibility: hidden;
    }

    .stDeployButton{
        visibility: hidden;
    }

    footer{
        visibility: hidden;
    }

    .bi-chat-text-fill {
        font-family: "Arial", sans-serif;
    }

    .menu-title {
        color: red;
    }

    </style>
    """
st.markdown(hide_menu, unsafe_allow_html=True)

# add_logo(
#     "https://www.tce.mg.gov.br/Content/images/logo-tcemg.png"
# )

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        def login():
            # with open('config.yaml') as file:
            #     config = yaml.load(file, Loader=SafeLoader)

            # authenticator = stauth.Authenticate(
            #     config['credentials'],
            #     config['cookie']['name'],
            #     config['cookie']['key'],
            #     config['cookie']['expiry_days']
            # )

            config = credenciais()

            authenticator = stauth.Authenticate(
                config['credentials'],
                'random_cookie_name',
                'random_signature_key',
                30
            )

            name, authentication_status, username = authenticator.login('Login', 'main')

            if authentication_status:
                authenticator.logout('Logout', 'main')
            elif authentication_status == False:
                st.error('Usuario / Senha inválidos', icon="🚨")

        def login2():
            # with open('config.yaml') as file:
            #     config = yaml.load(file, Loader=SafeLoader)

            # authenticator = stauth.Authenticate(
            #     config['credentials'],
            #     config['cookie']['name'],
            #     config['cookie']['key'],
            #     config['cookie']['expiry_days'],
            #     config['cookie']['expiry_days']
            # )

            config = usuario.credenciais()

            authenticator = stauth.Authenticate(
                config['credentials'],
                'random_cookie_name',
                'random_signature_key',
                30
            )

            modo_acesso = 'Login'
            if not st.session_state.authentication_status:
                modo_acesso = option_menu(
                    None, 
                    options=["Login", "Cadastro"], 
                    icons=['bi-door-open', 'bi-box-arrow-in-right'], 
                    # orientation="horizontal",
                    styles={
                        "nav-link": {"font-size": "13px"},
                        "nav-link-selected": {"font-size": "13px", "background-color": "#2986cc"}, }
                )

            if modo_acesso == 'Login':
                name, authentication_status, username = authenticator.login('Login', 'main')

                if authentication_status:
                    authenticator.logout('Logout', 'main')
                elif authentication_status == False:
                    st.error('Usuario / Senha inválidos', icon="🚨")

            if modo_acesso == 'Cadastro':
                try:
                    with st.form('formLogin'):
                        st.subheader(':green[Cadastrar]')
                        email = st.text_input('Email:') 
                        username = st.text_input('Usuário:') 
                        name = st.text_input('Nome:') 
                        password = st.text_input('Senha:') 
                        confirm_password = st.text_input('Confirmar Senha:') 
                        podeCadastrar = True

                        submitted = st.form_submit_button("Registrar")
                        if submitted:
                            #validação email
                            if email:
                                if usuario.validar_email(email):
                                    if usuario.get_user_email(email):
                                        st.error('Email Já Cadastrado', icon="🚨")
                                        podeCadastrar = False
                                else:
                                    st.error('Email Inválido', icon="🚨")
                                    podeCadastrar = False
                            else: 
                                st.error('Informe o Email', icon="🚨")
                                podeCadastrar = False

                            #Validação usuario
                            if username:
                                if usuario.get_user(username):
                                    st.error('Usuário Já Cadastrado', icon="🚨")
                                    podeCadastrar = False
                            else:
                                st.error('Informe o Usuário', icon="🚨")
                                podeCadastrar = False

                            #Validação Password
                            if password != confirm_password:
                                st.error('Senha e Confirma Senha Inválidos', icon="🚨")
                                podeCadastrar = False

                            if podeCadastrar:
                                password_decoded = stauth.Hasher([password]).generate()
                                if usuario.insere_users(email, username, name, password_decoded[0]):
                                    st.success('Cadastrado com Sucesso. Entre em Login e acesse o Sistema', icon="✅")
                                else:
                                    st.error('Erro no cadastro', icon="🚨")

                    # if authenticator.register_user('Cadastrar', preauthorization=False):

                    #     with open('config.yaml', 'w') as file:
                    #         yaml.dump(config, file, default_flow_style=False)

                        
                except Exception as e:
                    st.error(e)

        with st.sidebar:
            app = option_menu(None,
                options=['Home', 'Importação de Arquivo', 'Resultado da Apuração', 'Relatórios', 'Gráficos', 'Conta Usuário'],
                icons=['bi-house', 'bi-activity','bi-archive', 'bi-book', 'bi-bar-chart', 'bi-person'],
                # default_index=0,
                # styles= {"nav-link-selected": {"background-color": "#2986cc"}, }
                # styles={
                #     "container": {"padding": "5!important", "background-color": '#16537e'},
                #     "icon": {"color": "white", "font-size": "23px"},
                #     "nav-link": {"color": "white", "font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#2986cc"},
                #     "nav-link-selected": {"background-color": "#2986cc"}, }
            )

            ###### painel da impportação #####
            if 'cod_municipio_AM' not in st.session_state:
                st.session_state.cod_municipio_AM = None
                st.session_state.cod_orgao = None
                st.session_state.mes = None
                st.session_state.ano = None
                st.experimental_user = None
                
            if st.session_state.cod_municipio_AM:
                st.experimental_user = st.session_state.username if 'username' in st.session_state else None
                texto = f"""
                    :red[Dados de Importação:] \n
                    Código Município: {st.session_state.cod_municipio_AM} \n
                    Código Orgão: {st.session_state.cod_orgao} \n
                    Mês: {st.session_state.mes} ({meses_extenso[int(st.session_state.mes)-1].capitalize()})\n
                    Ano: {st.session_state.ano} \n
                    Usuário: {st.experimental_user}
                """
                st.sidebar.info(texto)

            ###### Login do Sistema #####
            login2()
            #### ate aqui ####

        if app == "Home":
            home.app()
        if app == "Importação de Arquivo":
            importacao_arquivos.app()
        if app == "Resultado da Apuração":
            resultado_apuracao.app()
        if app == 'Relatórios':
            relatorios.app()
        if app == 'Gráficos':
            graficos.app()
        if app == "Conta Usuário":
            conta.app()

    run()