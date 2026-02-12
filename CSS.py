import streamlit as st


def local_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(300deg, #00f2ff 0%, #7000ff 50%, #ff00d4 100%) !important;
        background-attachment: fixed;
    }
    .stApp h2, .stApp h3 {
        color: white !important;
    }

    [data-testid="stMain"] h1 {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5); /* Màu gradient bạn muốn */
        -webkit-background-clip: text; /* Cắt gradient theo hình dạng chữ */
        -webkit-text-fill-color: transparent; /* Làm chữ trong suốt để lộ gradient */
        font-size: 3rem !important; /* Tăng kích thước chữ cho nổi bật */
        font-weight: 800 !important; /* Làm chữ đậm hơn */
        line-height: 1.2; 
        text-shadow: 0px 0px 10px rgba(0, 210, 255, 0.5); /* Hiệu ứng phát sáng nhẹ */
    }
    .stApp label, .stApp [data-testid="stWidgetLabel"] p {
        color: white !important;
        font-weight: 500;
    }
    
    .stTextArea textarea {
        font-family: 'Monospace', Monospace !important; 
        font-size: 16px !important;
        line-height: 1.5 !important;
        font-weight: bold;
        
    }

    
    header[data-testid="stHeader"]{
        background-color: rgba(0,0,0,0) !important;
    }
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: rgba();
        background-shadow: 10px 10px;
        color: hsl(240, 3%, 40%);
    }
    
    .block-container {
        margin-left: 0px !important;
        margin-right: auto !important;
        padding-top: 20px !important;
        padding-left: 20px !important;
        padding-right: 0px !important;
        max-width: 100% !important;
    }
    /* Phần tải ảnh */
    [data-testid="stFileUploader"] {
        width: 100%;
    }
    /* đẩy cột 2 trong Lifestyle Shot xuống */
    .layout2 {
        margin-top: 60px;
    }
    
    /* Nút tin nhắn */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 999999 !important;
        width: auto !important;
        border: none !important;
    }
    div[data-testid="stPopover"] button {
        position: relative;
        background: linear-gradient(140deg, #00f2ff, #9d50bb);
        color: white !important;
        z-index: 2 !important;
        border: none !important;
        
    }
    @property --angle {
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
    }
    div[data-testid="stPopover"]::after, div[data-testid="stPopover"]::before {
        --angle: 0deg;
        content: '';
        position: absolute;
        height: 110%;
        width: 104%;
        background-image: conic-gradient(
            from var(--angle), 
            transparent, 
            #CCFF00 0%,  
            #00FF88 20%, 
            #00A36C 40%,  
            #004D40 60%, 
            #2ECC71 85%,   
            #CCFF00 100%   
            );
        top: -5%;
        left: -2%;
        border-radius: 8px;
        animation: spin 0.8s linear infinite;
    }
    div[data-testid="stPopover"]::before {
        filter: blur(1.5rem);
        opacity: 0.5;
    }
    @keyframes spin {
       
        to {
            --angle: 360deg;
        }
    }
    
    div[data-testid="stPopover"] button:hover {
    filter: brightness(1.15);
    transform: translateY(-1px);
    transition: 0.2s ease;
    }
    
    
    
   

    </style>
    """, unsafe_allow_html=True)
