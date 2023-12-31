import streamlit as st
import smtplib
import email.message

def enviar_email(nome_usuario, email_usuario, chave_acesso ):
    corpo_email = f"""
    <p>Olá <b>{nome_usuario}</b>, tudo bem?</p>

    <p>Seja bem vindo ao sistema Confere-TCE</p>
    
    Estamos enviando o código de ativação da sua conta de acesso ao sistema<br>
    
    Siga os seguinte passos:
    <ul>
        <li>Entre no sistema com seu usuário e senha</li>
        <li>Clique "Conta Usuário", irá encontrar um campo para informar o código de ativação</li>
        <li>Copie o codigo abaixo, cole no campo indicado e clique em <b>Cadastrar</b></li>

    </ul>

    Código de Ativação: <h1>{chave_acesso}</h1>

    <p>Te esperamos lá</p>

    <br>
    Favor não responder esse email.
    <br>
    Forte abraço da equipe Confere-TCE
    
    """

    email_msg = email.message.Message()
    email_msg['Subject'] = "Código de Ativação no Confere-TCE"
    email_msg['From'] = 'confere.tce@gmail.com'
    email_msg['To'] = email_usuario
    password = 'dghrtbhhpfikdxqb'
    # password = 'cdgtezrnjzgdabxk'
    email_msg.add_header('Content-Type', 'text/html')
    email_msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(email_msg['From'], password)
    s.sendmail(email_msg['From'], [email_msg['To']], email_msg.as_string().encode('utf-8'))
    # msg.success('Email enviado com sucesso!')