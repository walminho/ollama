import streamlit as st
import ollama
from PIL import Image
import io
import time  # Importa a biblioteca para medir o tempo

# Configuração da página
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição na área principal
st.title("🦙 Llama OCR")

# Botão de limpar no canto superior direito
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        if 'execution_time' in st.session_state:
            del st.session_state['execution_time']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Controles de upload na barra lateral
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Exibe a imagem carregada
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                start_time = time.time()  # Inicia a contagem do tempo
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """
                                Analise o texto na imagem fornecida. Extraia os seguintes datapoints, caso estejam presentes, e organize-as de forma estruturada. Os documentos podem ser RG, CNH, certidão de nascimento, casamento, de óbito ou outro. Os dados estão sob as chaves:

                                Nome (se identificar)
                                Data de nascimento (se identificar)
                                Data de emissão (se identificar)
                                Filiação: nome completo do pai (se aplicável) e em seguida nome completo da mãe (se aplicável)
                                Naturalidade (Cidade de nascimento)
                                RG (Registro Geral) (se identificar)
                                DOC - Descrição do documento que origina o documento analisado
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
                end_time = time.time()  # Finaliza a contagem do tempo
                st.session_state['execution_time'] = end_time - start_time

# Área principal para resultados
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
    st.success(f"Execution time: {st.session_state['execution_time']:.2f} seconds")  # Exibe o tempo de execução
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Rodapé
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model2 | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")
