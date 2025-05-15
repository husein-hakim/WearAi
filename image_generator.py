from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

def generate_image(user: list, cloth: str, prompt: str):
    client = genai.Client(api_key=os.getenv("gemini_api_key"))

    for file in user:
        uploaded_file = client.files.upload(file=file)

    with open(cloth, 'rb') as f:
        cloth = f.read()

    # Create the prompt with text and multiple images
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[
            prompt,
            uploaded_file,  # Use the uploaded file reference
            types.Part.from_bytes(
                data=cloth,
                mime_type='image/png'
            )
        ],
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            return image


new_image = generate_image(['user1.webp', 'user2.webp', 'user3.webp', 'user4.webp'], 'cloth.jpg')
new_image.save('generated.jpg')
