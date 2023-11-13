import streamlit as st

class mensagem:
    def error(mensagem):
        return st.error(mensagem, icon="🚨")

    def success(mensagem):
        return st.success(mensagem, icon="✅")

    def warning(mensagem):
        return st.success(mensagem, icon="⚠️")

