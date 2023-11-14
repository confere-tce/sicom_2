import streamlit as st

def app():
    if st.session_state.authentication_status:
        st.subheader(f"Bem vindo {st.session_state.name.title()} ao :blue[Consuta TCE]", divider='rainbow')

    st.write(st.session_state.authentication_status )
    st.write(st.session_state.name )
    st.write(st.session_state.username )
    st.write(st.session_state.cod_municipio_AM )
    st.write(st.session_state.cod_orgao )
    st.write(st.session_state.mes )
    st.write(st.session_state.ano )

    # hashed_passwords = stauth.Hasher(['123abc']).generate()
    # st.write(hashed_passwords)