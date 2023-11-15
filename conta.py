import streamlit as st
from util import mensagem as msg
from ConsultasSQL import usuario

def app():
    st.subheader("Conta de Usuário", divider='rainbow')

    if not st.session_state.authentication_status:
        msg.warning("Necessário Logar no Sistema")
    else:
        if not st.session_state.ativo:
            col1, col2, col3 = st.columns([0.5,1,0.5])
            with col2:
                with st.form('ativacao'):
                    codigo_ativacao = st.text_input('Informe o Código de Ativação')
                    submitted = st.form_submit_button("Cadastrar")
                    if submitted:
                        usuario_login, email_usuario, nome_usuario, chave_acesso, usuario_ativo = usuario.get_dados_usuario(st.session_state.username)
                        if int(codigo_ativacao) == int(chave_acesso):
                            if usuario.update_codigo_ativacao(st.session_state.username):
                                st.session_state.ativo = True
                                msg.success("Código de Ativação realizado com Sucesso. Sistema liberado!")
                            else:
                                msg.error("Erro no processo de ativação de usuário, contacte o suporte técnico")
                        else:
                            msg.error(f"""
                                      Código de ativação Inválido
                                      
                                      Confira o código de ativação enviado no email: {email_usuario}
                                      """)