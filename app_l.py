import chainlit as cl
import ollama

@cl.on_chat_start
async def start():
    # Send initial message
    await cl.Message(
        content="Welcome! Please send an image and I'll analyze it for you."
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Get image elements from the message
    image_elements = message.elements
    
    if not image_elements:
        await cl.Message(
            content="Please provide an image to analyze."
        ).send()
        return
        
    # Process each image element
    for image in image_elements:
        try:
            # Get image content
            if image.path:
                with open(image.path, 'rb') as file:
                    image_data = file.read()
            else:
                image_data = image.content
                
            # Send image to Ollama for analysis
            response = ollama.chat(
                model='llama3.2-vision',  # Update model name as needed
                messages=[
                    {
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
                        'images': [image_data],
                    },
                ],
            )
            
            # Display the image and analysis
            await cl.Message(
                content=response['message']['content'],
                elements=[
                    cl.Image(
                        name="Analyzed Image",
                        content=image_data,
                        display="inline"
                    )
                ]
            ).send()
            
        except Exception as e:
            await cl.Message(
                content=f"Error processing image: {str(e)}"
            ).send()