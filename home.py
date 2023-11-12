import streamlit as st

def app():
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if not st.session_state.authentication_status:
        st.subheader("Bem vindo ao :blue[Consuta TCE]", divider='rainbow')
    else:
        st.subheader(f"Bem vindo {st.session_state.name.title()} ao :blue[Consuta TCE]", divider='rainbow')

    # hashed_passwords = stauth.Hasher(['123abc']).generate()
    # st.write(hashed_passwords)