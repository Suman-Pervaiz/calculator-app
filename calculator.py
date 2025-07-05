import streamlit as st
import math

st.set_page_config(
    page_title="Functional Calculator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'last_was_equals' not in st.session_state:
    st.session_state.last_was_equals = False


def handle_input(value):
    if value == "AC":
        st.session_state.display = "0"
        st.session_state.expression = ""
        st.session_state.last_was_equals = False
    elif value == "=":
        try:
            if st.session_state.expression:
                expr = st.session_state.expression
                expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("＋", "+").replace("^", "**")
                expr = expr.replace("π", str(math.pi)).replace("e", str(math.e))
                expr = expr.replace("√", "math.sqrt")

                result = eval(expr, {"__builtins__": None}, {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "sqrt": math.sqrt, "log": math.log10, "exp": math.exp,
                    "pi": math.pi, "e": math.e, "math": math
                })

                if isinstance(result, float):
                    result = int(result) if result.is_integer() else round(result, 10)
                    result = f"{result:g}"
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
                st.session_state.last_was_equals = True
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""
            st.session_state.last_was_equals = False
    elif value == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
        st.session_state.display = st.session_state.expression if st.session_state.expression else "0"
        st.session_state.last_was_equals = False
    elif value == "√":
        st.session_state.expression += "√("
        st.session_state.display = st.session_state.expression
        st.session_state.last_was_equals = False
    else:
        if st.session_state.last_was_equals and value in "0123456789.()":
            st.session_state.expression = value
        elif st.session_state.display == "0" or st.session_state.display == "Error":
            st.session_state.expression = value
        else:
            st.session_state.expression += value

        st.session_state.display = st.session_state.expression
        st.session_state.last_was_equals = False


# Get current theme base (light or dark)
theme = st.context.theme.type  # 'light' or 'dark'
bg_color = "#F2F2F2" if theme == "light" else "white"
text_color = "black" if theme == "light" else "black"
footer_color = "#707070" if theme == "light" else "#BBBBBB"

# --- CSS for buttons  ---
st.markdown(f"""
<style>
    div[data-testid="stButton"] > button {{
        width: 100% !important;
        height: 55px !important;
        font-weight: 600 !important;
        font-size: 24px !important;
        border-radius: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# Title and display area
st.title("🧮 Functional Calculator")
st.markdown(
    f'<div style="font-size:2.5rem;text-align:right;background-color:{bg_color};color:{text_color};padding:10px;border-radius:8px;margin-bottom:10px;">{st.session_state.display or "0"}</div>',
    unsafe_allow_html=True)

# Button layout
buttons = [
    ["AC", "(", ")", "⌫"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "＋"],
    ["0", ".", "^", "="],
    ["sin(", "cos(", "tan(", "√"],
    ["log(", "π", "e", "÷"],
]

# Render buttons
for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        with cols[i]:
            is_primary = btn in ["=", "AC"]
            if st.button(btn, type="primary" if is_primary else "secondary", key=f"btn-{btn}"):
                handle_input(btn)
                st.rerun()

# Footer
st.markdown(
    f'<div style="position: fixed; bottom: 10px; right: 20px; text-align: right;"><p style="font-size: 0.8rem; color: {footer_color};">Made by Suman Pervaiz</p></div>',
    unsafe_allow_html=True)
