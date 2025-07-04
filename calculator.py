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
                expr = expr.replace("√", "sqrt")
                result = eval(expr, {"__builtins__": None}, {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "sqrt": math.sqrt, "log": math.log10, "exp": math.exp,
                    "pi": math.pi, "e": math.e
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
    elif value == "√":
        st.session_state.expression += "√("
        st.session_state.display = st.session_state.expression
    else:
        if st.session_state.last_was_equals:
            if value in "0123456789.":
                st.session_state.expression = value
                st.session_state.display = value
            else:
                st.session_state.expression += value
                st.session_state.display = st.session_state.expression
            st.session_state.last_was_equals = False
        else:
            if st.session_state.display == "0" or st.session_state.display == "Error":
                if value in "0123456789.":
                    st.session_state.expression = value
                    st.session_state.display = value
                else:
                    st.session_state.expression += value
                    st.session_state.display = st.session_state.expression
            else:
                st.session_state.expression += value
                st.session_state.display = st.session_state.expression


# CSS styling
st.markdown("""
<style>
    /* Common button styles */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 55px !important;
        font-weight: 900 !important;
        font-size: 30px !important;
    }

    /* Primary button styling */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:active {
        background-color: #ff4b4b !important;
        color: white !important;
    }

    /* Default (light mode) display box */
    .display-box {
        font-size: 2rem;
        text-align: right;
        background: #f2f2f2;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: black !important;
    }

    /* DARK MODE specific styling */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stButton"] > button {
            color: white !important;
        }
        .display-box {
            background: #f2f2f2 !important;
            color: black !important; /* Text ko black krta ha sirf dark mode k liye */
        }
    }
</style>
""", unsafe_allow_html=True)



# Title and display area
st.title("🧮 Functional Calculator")
st.markdown(f'<div style="font-size:2rem;text-align:right;background:#f2f2f2;padding:5px;border-radius:6px;margin-bottom:10px;">{st.session_state.display}</div>', unsafe_allow_html=True)

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
            if btn in ["=", "AC"]:
                if st.button(btn, type="primary"):
                    handle_input(btn)
                    st.rerun()
            else:
                if st.button(btn):
                    handle_input(btn)
                    st.rerun()

# Footer
st.markdown('<p style="text-align:right">Made by Suman Pervaiz</p>', unsafe_allow_html=True)