import streamlit as st

def app():
    if st.session_state.authentication_status:
        st.subheader(f"Bem vindo {st.session_state.name.title()} ao :blue[Consuta TCE]", divider='rainbow')

    # hashed_passwords = stauth.Hasher(['123abc']).generate()
    # st.write(hashed_passwords)



    