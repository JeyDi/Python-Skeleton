import streamlit as st


def app():
    st.title("{{cookiecutter.project}} example")
    st.subheader("Streamlit template for python-skeleton")

    st.markdown(
        """
        This is a multipage template for a streamlit project and web application 
        **Streamlit** is now mature and at the 1.1.0 version! (and more)
        - Streamlit webpage: https://blog.streamlit.io/announcing-streamlit-1-0/
        - Documentation: https://docs.streamlit.io/library/get-started
        """
    )
    
    st.markdown("Feel free to setup and modify the code in the following project, if you encounter any problem with this template, please report an issue to: `python-skeleton` Github repository")

    st.image(
        "./app/static/images/sentiment_analysis.png",
        width=800,
    )
