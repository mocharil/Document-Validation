# project/utils.py
import io
import requests
import re
from mimetypes import guess_type
from fastapi import HTTPException
from vertexai.generative_models import Image
from pdf_processor import PDFProcessor
from config import multimodal_model, safety_config, generation_config

def fetch_content(input_source):
    if isinstance(input_source, bytes):
        return input_source
    elif input_source.startswith(('http://', 'https://')):
        response = requests.get(input_source)
        if response.status_code == 200:
            return response.content
        else:
            raise HTTPException(status_code=400, detail="Invalid URL or unable to fetch content")
    else:
        with open(input_source, 'rb') as f:
            return f.read()
        
def analyze_content(input_source):
    contents = []
    with open('images/materai.jpg', 'rb') as f:
        sample_materai = f.read()
    contents.append(Image.from_bytes(sample_materai))
    contents.append("""[{
            "signature_count": "0",
            "signature_creator": [],
            "meterai_count": "1",           
            "company_stamp_count": "0",
            "page_image": "1"
        }]""")

    with open('images/stamp.png', 'rb') as f:
        sample_stamp = f.read()
    contents.append(Image.from_bytes(sample_stamp))
    contents.append("""[{
            "signature_count": "0",
            "signature_creator": [],
            "meterai_count": "0",          
            "company_stamp_count": "1",
            "page_image": "2"
        }]""")

    content_file = fetch_content(input_source)
    mime_type, _ = guess_type(input_source) if isinstance(input_source, str) else ('application/pdf', None)
    print(mime_type)

    pdf_processor = PDFProcessor(content_file)
    if mime_type == 'application/pdf':
        class_type = pdf_processor.classify_pdf()
        list_bytes = pdf_processor.split_pdf_to_images()
    else:
        class_type = [{'page_number': 1, 'file_type': 'ImageBased'}]
        list_bytes = [content_file]

    for byte in list_bytes:
        contents.append(Image.from_bytes(byte))

    prompt = """Analyze the images below only to identify any signatures, stamps, and duty stamps (meterai) in each image. 
    The output should be in JSON format with the following fields for each image:
        [{
            "signature_count": "<Total number of signatures present>",
            "signature_creator": ["<List of signature creators>"],
            "meterai_count": "<Total number of duty stamps (meterai) present>",
            "company_stamp_count": "<Total number of stamps present>",
            "page_number": "<Order of the image excluding example images, starting from 1>"
        }]
        
         """

    contents.append(prompt)
    responses = multimodal_model.generate_content(contents,
                                                  safety_settings=safety_config, 
                                                  generation_config=generation_config, 
                                                  stream=True)

    full_result = ''
    for response in responses:
        full_result += response.text

    usage = {}   
    for line in str(response.usage_metadata).split('\n'):
        if line.strip():
            key, value = line.split(':')
            usage.update({key.strip(): int(value.strip())})

    null = '-'
    true = True
    false = False
    try:
        result = eval(re.findall(r'\[.*\]', full_result, flags=re.I|re.S)[0])
    except:
        result = []
        for i in re.findall(r'\[(\{.*?\})\]',full_result, flags=re.I|re.S):
            result.append(eval(i))
    
    result = result[-len(class_type):]
    
    for r, t in zip(result, class_type):
        file_type = t['file_type']
        if file_type == 'TextBasedPDF':
            sign = 'electronic'
        elif file_type == 'ScannedPDF':
            sign = 'handwritten'
        else:
            sign = r['signature_type']
        r.update({'file_type': file_type, 'signature_type': sign, 'page_number':t['page_number']})
        


    return {'result': result, 'usage': usage}
