import re
import json
from bs4 import BeautifulSoup
import requests
from src.openai_tool import OpenAISearchTool 
import google.generativeai as genai
import json
import os 
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
import google.generativeai as genai
import time

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]  = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Duyuruları çekmek için kullanılacak URL
def fetch_announcements(url):
    """Bir URL'den duyuruları çeker ve JSON formatında döndürür."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # HTML elementi bul
    ul_element = soup.find('ul', class_='posts latest_posts2-posts')
    
    # Ay isimlerinin listesi
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    # Duyuruları saklayacağımız liste
    duyurular = []
    
    for li in ul_element.find_all('li', class_='post latest_posts2-post'):
        full_text = li.text.strip()
        
        # Tarih bilgisini ay ismi üzerinden ayırmayı dene
        for ay in aylar:
            if ay in full_text:
                split_text = full_text.split(ay)
                if len(split_text) == 2:
                    title = split_text[0].strip()
                    date_part = split_text[1].strip()
                    
                    date_match = re.match(r"(\d{1,2}),(\s*\d{4})$", date_part)
                    if date_match:
                        day = date_match.group(1)
                        year = date_match.group(2).strip()
                        date = f"{ay} {day}, {year}"
                    else:
                        date = ay + date_part
                        
                break
        else:  # Eğer herhangi bir ay ismi bulunamazsa
            title = full_text
            date = "Tarih Bulunamadı"
        
        # Link bilgisini çek
        link = li.find('a')['href'] if li.find('a') else None
        
        # Duyuruyu JSON objesi olarak sakla
        duyuru = {
            "baslik": title,
            "tarih": date,
            "link": link
        }
        duyurular.append(duyuru)
    
    return duyurular

# JSON formatında verileri dosyaya kaydetmek için kullanılacak fonksiyon
def export_to_json(data, filename):
    """Verilen verileri belirtilen dosya adına JSON formatında kaydeder."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Veriler {filename} dosyasına kaydedildi.")

# JSON formatında verileri dosyadan yüklemek için kullanılacak fonksiyon
def fetch_content(announcements):
    """Her bir duyurunun linkine giderek içerik bilgisini çeker ve yapıya ekler."""
    for announcement in announcements:
        if announcement['link'] and announcement['link'].startswith(('http', 'https')):
            try:
                response = requests.get(announcement['link'])
                page_soup = BeautifulSoup(response.content, 'html.parser')
                
                # İçerik bilgilerinin bulunduğu HTML etiketini güncelleyin
                # Bu örnekte sadece tüm sayfa metnini alıyoruz
                content = page_soup.get_text().strip()
                
                # Duyuru yapısına içerik bilgisi ekle
                announcement['icerik'] = content
            except requests.exceptions.RequestException as e:
                print(f"Content could not be retrieved from {announcement['link']}: {e}")
                announcement['icerik'] = "İçerik alınamadı"
    
    return announcements


# AI yardımıyla duyuruların içeriğini işleyen fonksiyon
def process_announcements_with_ai(announcements):
    """Duyuruların içeriğini AI yardımıyla işleyip 'aiicerik' anahtarını ekler."""
    ai_tool = OpenAISearchTool()

    for announcement in announcements:
        # İçerik yoksa veya boşsa başlığı kullanarak içerik oluştur.
        content = announcement.get('icerik', '').strip() or announcement['baslik']
        
        # İçeriği düzenle
        aiicerik = ai_tool.summarize_request(content)

        # 'aiicerik' anahtarını ekle
        announcement['aiicerik'] = aiicerik

    return announcements


# This function takes a a sentence as an arugument and return it's embeddings
def GEMINI_embeddings(text, api_key = GEMINI_API_KEY):
    # Define the embedding model
    genai.configure(api_key=api_key)

    model = 'models/embedding-001' # text-embedding-004
    # Get the embeddings
    embedding = genai.embed_content(model=model,
                                    content=text,
                                    task_type="retrieval_document")
    return embedding['embedding']

# This function takes a text and a tech argument and returns the embeddings of the text
def get_embeddings(text, tech):
    if tech == "GEMINI":
        return GEMINI_embeddings(text)
    elif tech == "GPT":
        tool = OpenAISearchTool()
        return tool.get_embedding(text)
    else:
        raise ValueError("Invalid tech argument. Please use 'GEMINI' or 'GPT'.")

# This function takes a query and a list of data and returns the most similar item in the data
def get_query_embedding(query,tech = 'GPT'):
    return get_embeddings(query,tech=tech)

# This function takes a query embedding and a list of data and returns the most similar item in the data
def find_most_similar(query_embedding, data):
    min_distance = float('inf')
    best_match = None
    
    for item in data:
        distance = cosine(query_embedding, item['aiicerik_embedding'])
        if distance < min_distance:
            min_distance = distance
            best_match = item
    
    return best_match

# This function takes a query and a list of data and returns the most similar item in the data
def respond_to_query(data, query,tech = 'GPT'):
    query_embedding = get_query_embedding(query,tech)
    best_match = find_most_similar(query_embedding, data)
    
    if best_match:
        response = best_match['aiicerik']  # veya daha özelleştirilmiş bir yanıt formatı
        link = best_match['link']
        tarih = best_match['tarih']
    else:
        response = None

    return response,link, tarih

# This function takes a query and a list of data and returns the most similar item in the data
def chatbot(query,relevant_info,link,tarih):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Sen Yaşar Üniversitesi öğrencilerine yardımcı olan kibar ve esprili bir sanal asistansın. Öğrencilerin üniversite duyuruları, ders programları, sınavlar, kayıt işlemleri ve diğer akademik konularla ilgili sorularını yanıtlıyorsun. Cevaplarında doğru ve güncel bilgiler vererek, sohbeti samimi bir üslupla ve hafif espirilerle süslüyorsun. Amaç, öğrencilere en iyi şekilde yardımcı olmak ve onlara keyifli bir deneyim sunmaktır.",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    current_time = time.localtime()
    try:
        time_difference = abs(time.mktime(current_time) - time.mktime(tarih))
        prompt_with_retrieved_info = f"{query}\n\nSoruyu cevaplamak için aşağıdaki bilgilerden faydalan, sen de ekleme yapabilirsin:\n{relevant_info}. Ayrıca sonuna şunu ekle : \n\nDaha fazla bilgi için buraya göz atabilirsiniz:\n {link}"
    except:
        prompt_with_retrieved_info = f"{query}\n\nSoruyu cevaplamak için aşağıdaki bilgilerden faydalan, sen de ekleme yapabilirsin:\n{relevant_info}. \nDuyurunun yapıldığı tarih:\n{tarih}. \nAyrıca sonuna şunu ekle : \n\nDaha fazla bilgi için buraya göz atabilirsiniz:\n {link}"

    # Craft prompt with retrieved information
    #prompt_with_retrieved_info = f"{query}\n\nSoruyu cevaplamak için aşağıdaki bilgilerden faydalan, sen de ekleme yapabilirsin:\n{relevant_info}. Duyurunun yapıldığı tarih:\n{tarih}. Ayrıca sonuna şunu ekle : \n\nDaha fazla bilgi için buraya göz atabilirsiniz:\n {link}"
    # Generate response
    result = chat_session.send_message(prompt_with_retrieved_info)
    result = result.candidates[0].content.parts[0].text
    # Append link to the result
    response_with_link = f"{result}"
        
    return response_with_link,chat_session

# history için önerilen yapı
def extract_qna_roles(chat_session, history_list):
    
    for i in range(0, len(chat_session.history), 2):
        # Kullanıcı sorusunu ve rolünü al
        user_content = chat_session.history[i]
        role_user = 'Kullanıcı' if user_content.role == 'user' else user_content.role
        question_user = user_content.parts[0].text.split('\n\n')[0]
        
        # Bot cevabını ve rolünü al (i+1 kontrolü ile indeks sınırlarını aşmamaya dikkat)
        if i + 1 < len(chat_session.history):
            bot_content = chat_session.history[i + 1]
            role_bot = 'YaşarBot' if bot_content.role == 'model' else bot_content.role
            answer_bot = bot_content.parts[0].text
        else:
            role_bot, answer_bot = None, None
        
        # Sohbeti organize edilmiş bir sözlük olarak kaydet
        history_list.append({
            'role_user': role_user,
            'question_user': question_user,
            'role_bot': role_bot,
            'answer_bot': answer_bot
        })
    
    return history_list


# This function takes a query and a list of data and returns the most similar item in the data
def execute_query(query, data, history_list):

    # if query has merhaba and len(query) < 17  kodunu yaz.
    if 'merhaba' in query.lower() and len(query) < 17:
        response = 'Merhaba! Ben Yaşar Üniversitesi Chatbot\'uyum. Size nasıl yardımcı olabilirim?'
        link = 'https://www.yasar.edu.tr/'
        tarih = time.localtime()
    else:
        response, link, tarih = respond_to_query(data, query, tech='GPT')


    result,chat_session = chatbot(query,response,link, tarih)

    history = extract_qna_roles(chat_session,history_list)
    
    return result, history


