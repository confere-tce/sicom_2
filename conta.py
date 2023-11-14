import streamlit as st
# from streamlit_option_menu import option_menu
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
from  util import mensagem as msg
import enviar_email as e


def app():
    st.subheader("Conta de Usuário", divider='rainbow')

    if not st.session_state.authentication_status:
        msg.warning("Necessário Logar no Sistema")
    else:
        pass

    # hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

    # with open('config.yaml') as file:
    #     config = yaml.load(file, Loader=SafeLoader)

    # authenticator = stauth.Authenticate(
    #     config['credentials'],
    #     config['cookie']['name'],
    #     config['cookie']['key'],
    #     config['cookie']['expiry_days'],
    #     config['preauthorized']
    # )

    # modo_acesso = option_menu(
    #     None, 
    #     options=["Login", "Cadastro"], 
    #     icons=['bi-door-open', 'bi-box-arrow-in-right'], 
    #     default_index=0, 
    #     orientation="horizontal",
    #     styles={
    #         "nav-link-selected": {"background-color": "#2986cc"}, }
    # )

    # if modo_acesso == 'Login':
    #     col1,col2,col3 = st.columns([0.5,1,0.5])
    #     with col2:
    #         name, authentication_status, username = authenticator.login('Login', 'main')

    #         if authentication_status:
    #             authenticator.logout('Logout', 'main')
    #             st.write(f'Bem vindo *{name}*')
    #         elif authentication_status == False:
    #             st.error('Usuario / Senha inválidos', icon="🚨")
    #         elif authentication_status == None:
    #             st.warning("Por favor entre com usuário e senha", icon="⚠️")

    # if modo_acesso == 'Cadastro':
    #     col1,col2,col3 = st.columns([0.5,1,0.5])
    #     with col2:
    #         try:
    #             if authenticator.register_user('Cadastrar ao Sistema', preauthorization=False):

    #                 with open('config.yaml', 'w') as file:
    #                     yaml.dump(config, file, default_flow_style=False)

    #                 st.success('Cadastrado com Sucesso', icon="✅")
    #         except Exception as e:
    #             st.error(e)

    botao = st.button('enviar')
    if botao:
        e.enviar_email('ranzatti@sonner.com.br')