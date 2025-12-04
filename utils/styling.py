import streamlit as st

def set_theme():
    """
    Sets the Streamlit page theme by injecting custom CSS and a JavaScript
    snippet to toggle themes. It also returns the appropriate Plotly template.
    """
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    # Define Plotly templates for themes
    theme_plotly_template = {
        "light": "plotly_white",
        "dark": "plotly_dark",
    }

    # Load custom CSS
    with open("styles.css", "r") as f:
        css = f.read()

    # JavaScript to set the data-theme attribute on the body
    js = f"""
    <script>
        function setTheme(theme) {{
            document.body.setAttribute('data-theme', theme);
        }}
        setTheme('{st.session_state.theme}');
    </script>
    """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(js, unsafe_allow_html=True)

    return theme_plotly_template[st.session_state.theme]
