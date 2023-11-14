import streamlit as st
import smtplib
import email.message
from  util import mensagem as msg
from ConsultasSQL import usuario

def enviar_email(username):
    print(username)

    usuario_login, email_usuario, nome_usuario, chave_acesso = usuario.get_dados_usuario(username)
    print('3')

    corpo_email = f"""
    <p>Olá <b>{nome_usuario}</b>, tudo bem?</p>

    <p>Seja bem vindo ao sistema Confere-TCE</p>
    
    Estamos enviando o código de ativação da sua conta de acesso ao sistema<br>
    
    Siga os seguinte passos:
    <ul>
        <li>Entre no sistema com seu usuário e senha</li>
        <li>Clique "Conta Usuário", irá encontrar um campo para informar o código de ativação</li>
        <li>Copie o codigo abaixo, cole no campo indicado e clique em Salvar</li>

    </ul>

    Código de Ativação: <h1>{chave_acesso}</h1>

    <br>
    <p>Te esperamos lá</p>

    Forte abraço da equipe Confere-TCE
    
    """

    email_msg = email.message.Message()
    email_msg['Subject'] = "Código de Ativação no Confere-TCE"
    email_msg['From'] = 'ranzatti@gmail.com'
    # email_msg['To'] = 'ranzatti@sonner.com.br'
    email_msg['To'] = email_usuario
    password = 'cdgtezrnjzgdabxk'
    email_msg.add_header('Content-Type', 'text/html')
    email_msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(email_msg['From'], password)
    s.sendmail(email_msg['From'], [email_msg['To']], email_msg.as_string().encode('utf-8'))
    msg.success('Email enviado com sucesso!')