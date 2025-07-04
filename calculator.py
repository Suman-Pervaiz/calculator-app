import streamlit as st
import math

st.set_page_config(
    page_title="Functional Calculator",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🧮"
)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'last_was_equals' not in st.session_state:
    st.session_state.last_was_equals = False


def handle_input(value):
#calculation logic
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
                # Use math.sqrt directly for safety
                expr = expr.replace("√(", "math.sqrt(")
                # Safely evaluate the expression
                result = eval(expr, {"__builtins__": None, "math": math})
                if isinstance(result, float):
                    result = round(result, 10)
                    result = int(result) if result.is_integer() else result
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
                st.session_state.last_was_equals = True
        except Exception:
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
        if st.session_state.last_was_equals and value not in "×÷−＋^":
            st.session_state.expression = value
            st.session_state.display = value
        elif st.session_state.display == "0" and value not in "×÷−＋^.()":
            st.session_state.expression = value
            st.session_state.display = value
        elif st.session_state.display == "Error":
            st.session_state.expression = value
            st.session_state.display = value
        else:
            st.session_state.expression += value
            st.session_state.display = st.session_state.expression
        st.session_state.last_was_equals = False


# CSS styling for buttons light&dark mode
st.markdown("""
<style>
    /* --- General Button Styles --- */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 60px !important;
        font-weight: 600 !important;
        font-size: 24px !important;
        border-radius: 10px !important;
    }

    /* --- Display Area Style (Height Reduced) --- */
    .calculator-display {
        font-size: 2.5rem !important;
        text-align: right !important;
        background-color: #E0E0E0 !important;
        color: #0E0E10 !important;
        padding: 5px 15px !important; /* <--- YAHAN CHANGE KIYA HAI (10px se 5px) */
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        overflow-x: auto;
        white-space: nowrap;
    }

    /* --- Styles for Primary Buttons (AC, =) --- */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #ff6b6b !important;
    }

    /* --- Dark Mode Specific Styles --- */
    body[data-theme="dark"] {
        background-color: #0E1117;
    }

    /* Style for NORMAL buttons in DARK mode */
    body[data-theme="dark"] div[data-testid="stButton"] > button:not([kind="primary"]) {
        background-color: #262730 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    body[data-theme="dark"] div[data-testid="stButton"] > button:not([kind="primary"]):hover {
        background-color: #3a3b42 !important;
        border-color: #666666 !important;
    }

    /* --- Light Mode Specific Styles --- */
    /* Style for NORMAL buttons in LIGHT mode */
    body[data-theme="light"] div[data-testid="stButton"] > button:not([kind="primary"]) {
        background-color: #FFFFFF !important;
        color: #262730 !important;
        border: 1px solid #E0E0E0 !important;
    }
    body[data-theme="light"] div[data-testid="stButton"] > button:not([kind="primary"]):hover {
        background-color: #F0F2F6 !important;
        border-color: #d0d0d0 !important;
    }

    /* --- Footer Styles --- */
    .footer {
        text-align: right;
    }
    body[data-theme="light"] .footer {
        color: gray !important;
    }
    body[data-theme="dark"] .footer {
        color: #FAFAFA !important;
    }

</style>
""", unsafe_allow_html=True)

# favicon
st.title("🧮 Functional Calculator")
st.markdown(f'<div class="calculator-display">{st.session_state.display}</div>', unsafe_allow_html=True)

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
            key = f"btn-{btn}"
            if btn in ["=", "AC"]:
                if st.button(btn, type="primary", key=key, on_click=handle_input, args=(btn,)):
                    pass
            else:
                if st.button(btn, key=key, on_click=handle_input, args=(btn,)):
                    pass

# Footer
st.markdown('<p class="footer">Made by Suman Pervaiz</p>', unsafe_allow_html=True)