import streamlit as st
import time
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="Umbrella Corp | Red Queen OS",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)



URL_BACKGROUND = "https://live.staticflickr.com/65535/52680915588_6b80520334_b.jpg"
URL_UMBRELLA_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Umbrella_Corporation_logo.svg/1024px-Umbrella_Corporation_logo.svg.png"

def get_api_key():

    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]


    raise ValueError("ERRO: Chave da API não encontrada!")


api_key = get_api_key()


@st.cache_resource
def load_ai_model():
    return SentenceTransformer("all-MiniLM-L6-v2", device='cpu')


model = load_ai_model()


try:
    from features import verify_context_question, send_question
except ImportError:
    st.error("ERRO CRÍTICO: Arquivo 'features.py' não encontrado. Protocolo de segurança falhou.")
    st.stop()


st.markdown(
    f"""
    <style>
    /* Importando fonte estilo 'Terminal' do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* Aplicando a fonte em todo o app */
    html, body, [class*="css"] {{
        font-family: 'Share Tech Mono', monospace !important;
    }}

    /* Variáveis de Cores */
    :root {{
        --primary-red: #ff0000;
        --dark-bg: #000000;
    }}

    /* Background Imersivo */
    [data-testid="stAppViewContainer"] {{
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Overlay escuro mais forte para leitura */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.85); /* Mais escuro para destacar o texto vermelho */
        z-index: -1;
    }}

    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {{
        background-color: rgba(10, 10, 10, 0.95) !important;
        border-right: 1px solid var(--primary-red);
    }}

    /* Títulos com efeito de brilho (Glow) */
    h1, h2, h3 {{
        color: var(--primary-red) !important;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
    }}

    /* Estilo das mensagens do Chat */
    .stChatMessage {{
        background-color: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid #333;
        border-radius: 5px;
    }}
    
    /* Destaca o Avatar da Red Queen */
    div[data-testid="chatAvatarIcon-assistant"] {{
        background-color: var(--primary-red) !important;
        box-shadow: 0 0 15px var(--primary-red);
    }}

    /* Input do usuário estilo Terminal */
    .stChatInput textarea {{
        background-color: #111 !important;
        color: #0f0 !important; /* Texto verde matrix quando digita */
        border: 1px solid #333 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; font-size: 20px;'>SYSTEM DIAGNOSTICS</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("HIVE STATUS", "ONLINE", delta="STABLE")
    col2.metric("THREAT LEVEL", "EXTREME", delta_color="inverse")
    
    st.progress(98, text="Memory Integrity")
    st.progress(12, text="Humanity Detected")
    
    st.markdown("---")
    st.error("🔒 ACCESS RESTRICTED: CLASS 4 PERSONNEL ONLY")
    st.caption("Umbrella Corp. OS v3.1.1 | Build: Raccoon")



st.markdown("""
    <h1 style='text-align: center; color: red; font-size: 60px; text-shadow: 0 0 20px red;'>
        🔴 RED QUEEN
    </h1>
    <p style='text-align: center; letter-spacing: 3px; color: #aaa;'>
        ARTIFICIAL INTELLIGENCE DEFENSE SYSTEM
    </p>
    <hr style='border-color: red;'>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    intro_msg = "SYSTEM REBOOTED. IDENTIFY IMMEDIATELY."
    st.session_state.messages.append({"role": "assistant", "content": intro_msg})


chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🔴"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":

                 st.markdown(f"<span style='color: #ff4444; font-weight: bold;'>{message['content']}</span>", unsafe_allow_html=True)
            else:
                 st.markdown(message["content"])


if prompt := st.chat_input("Type your command..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)


    with chat_container:
        with st.chat_message("assistant", avatar="🔴"):
            placeholder = st.empty() 
            with st.spinner("PROCESSING DATA..."):
                

                if verify_context_question(model, prompt):
                    response_text = send_question(api_key, prompt)
                else:
                    time.sleep(1.5) 
                    response_text = "🚫 ACCESS DENIED. Tópico irrelevante. Protocolo de segurança ativado."


                placeholder.markdown(f"<span style='color: #ff4444; font-weight: bold;'>{response_text}</span>", unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})