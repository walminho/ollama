import streamlit as st
import ollama
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Llama OCR")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """
                                Analise o texto na imagem fornecida. O documento pode ser um RG (Registro Geral), CNH (Carteira Nacional de Habilitação) ou outro documento similar. Extraia as seguintes informações, caso estejam presentes, e organize-as de forma estruturada. Os documentos podem ser RG, CNH, certidão de nascimento, casamento, de óbito ou outro. Os dados estão sob as chaves:

                                Nome (se identificar)
                                Data de nascimento (se identificar)
                                Data de emissão (se identificar)
                                Filiação: nome completo do pai (se aplicável) e em seguida nome completo da mãe (se aplicável)
                                Naturalidade (Cidade de nascimento)
                                RG (Registro Geral) (se identificar)
                                DOC - Descrição do coumento que origina o documento analisado
                                CPF (se identificar)
                                Número do PIS/PASEP (se aplicável)
                                Número da CNH (se aplicável)
                                Número do título de eleitor (se aplicável)

                                Após identificar e listar os dados, organize os resultados de maneira clara e concisa, como em um JSON.
                                """,
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
    print(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model2 | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")