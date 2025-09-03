import streamlit as st
import json
from YU_functions import execute_query
import os

# Dosya yollarını programatik olarak ayarlayın
base_path = os.getcwd()
data_path = os.path.join(base_path, 'data', 'vectorDatasetDuyurular.json')
logo_path = os.path.join(base_path, 'images','GDG on Campus University of YASAR.png')
rag_image_path = os.path.join(base_path, 'images','rag.png')
bot_image_path = os.path.join(base_path, 'images','bot.png')



# Asıl veri setinin yolunu güncelleyin
with open(data_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


# Sohbet geçmişini saklamak için Streamlit session_state içinde bir liste oluşturun
if 'history_list' not in st.session_state:
    st.session_state['history_list'] = []



# Web uygulaması başlık ve ikon
st.set_page_config(page_title="YaŞarCaNBot", page_icon="🚣")

# Sidebar'a logo ekleme
st.sidebar.image(logo_path, width=275)

# Sidebar (Navbar) oluşturma
with st.sidebar:
    st.header("Yaşar Üniversitesi")
    page = st.radio("Seçenekler", ("YaşarCaN😎", "RAGarchitecture🛠️", "Codes 📂", "Free GenAI Courses 🎓"))

    if page == "YaşarCaN😎" :
        # Bu kısımada gösterilecek bilgileri ekle
        st.write("💬 Yaşar Üniversitesi'nin chatbotu **YaşarCaN** ile sohbet edebilirsiniz.")
        st.write("📢 **YaşarCaN** size Duyurular hakkında bilgi verebilir, ders programınızı (Halüsülasyon) oluşturabilir ve daha fazlasını yapabilir.")
        st.write("✍️ Sorularınızı yazın ve **YaşarCaN** size yardımcı olsun.")
        
        
    # RAGarchitecture seçildiğinde resim gösterme
    if page == "RAGarchitecture🛠️":
        st.image(rag_image_path, width=1000)

    # Codes seçildiğinde kod gösterme
    if page == "Codes 📂":

        # Sidebar başlığı
        st.sidebar.title("WEB Scrapping")


        # Yeni bir bölüm Connec2MsSQL
        st.sidebar.header("www.yasar.edu.tr Duyurular") 
        st.sidebar.code("""

        def fetch_announcements(url):
            Bir URL'den duyuruları çeker ve JSON formatında döndürür.
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
        
        
        
        def fetch_content(announcements):
        Her bir duyurunun linkine giderek içerik bilgisini çeker ve yapıya ekler
            
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
    
        """)


    if page == "Free GenAI Courses 🎓":
                st.markdown("""
        <h2>NVIDIA</h2>
        <ul>
            <li>📕 <a href="https://lnkd.in/dBAWT8fZ" target="_blank">Generative AI Explained</a></li>
            <li>📕 <a href="https://lnkd.in/dNN8gmdb" target="_blank">Introduction to Physics-informed Machine Learning with Modulus</a></li>
            <li>📕 <a href="https://lnkd.in/d6zEbNGp" target="_blank">Building A Brain in 10 Minutes</a></li>
            <li>📕 <a href="https://lnkd.in/dPmcZE_z" target="_blank">Accelerate Data Science Workflows with Zero Code Changes</a></li>
            <li>📕 <a href="https://lnkd.in/dxRHzBKN" target="_blank">Building RAG Agents with LLMs</a></li>
            <li>📕 <a href="https://lnkd.in/d7eUBKfw" target="_blank">Augment your LLM Using Retrieval Augmented Generation</a></li>
        </ul>
        <h2>STANFORD UNIVERSITY</h2>
        <ul>
            <li>🎈 <a href="https://lnkd.in/dei3h4XP" target="_blank">Databases: Advanced Topics in SQL</a></li>
            <li>🎈 <a href="https://lnkd.in/d3uYRUFY" target="_blank">Databases: Relational Databases and SQL</a></li>
            <li>🎈 <a href="https://lnkd.in/dfAmMY3v" target="_blank">Databases: Semistructured Data</a></li>
            <li>🎈 <a href="https://lnkd.in/d-A6Kr5F" target="_blank">Mining Massive Data Sets</a></li>
            <li>🎈 <a href="https://lnkd.in/dgCG-n84" target="_blank">Statistical Learning with Python</a></li>
            <li>🎈 <a href="https://lnkd.in/dk6-mtu5" target="_blank">Statistical Learning with R</a></li>
            <li>🎈 <a href="https://lnkd.in/d_avmgYm" target="_blank">R Programming Fundamentals</a></li>
            <li>🎈 <a href="https://lnkd.in/dNr3GCHC" target="_blank">Machine Learning Specialization</a></li>
        </ul>
        <h2>DEEPLEARNING.AI</h2>
        <h3>𝐁𝐞𝐠𝐢𝐧𝐧𝐞𝐫</h3>
        <ul>
            <li>⏩ <a href="https://lnkd.in/diy9VGm2" target="_blank">AI Python for Beginners</a></li>
            <li>⏩ <a href="https://lnkd.in/d4RFYVD3" target="_blank">ChatGPT Prompt Engineering for Developers</a></li>
            <li>⏩ <a href="https://lnkd.in/dHti9pXw" target="_blank">Pretraining LLMs</a></li>
            <li>⏩ <a href="https://lnkd.in/dKsjtDA2" target="_blank">Pair Programming with a Large Language Model</a></li>
            <li>⏩ <a href="https://lnkd.in/d4-YpzXu" target="_blank">LLMOps</a></li>
            <li>⏩ <a href="https://lnkd.in/d8y9tX77" target="_blank">Understanding and Applying Text Embeddings</a></li>
            <li>⏩ <a href="https://lnkd.in/dKXwvD-e" target="_blank">LangChain for LLM Application Development</a></li>
            <li>⏩ <a href="https://lnkd.in/dbwT8ajS" target="_blank">Embedding Models: From Architecture to Implementation</a></li>
            <li>⏩ <a href="https://lnkd.in/d4RFYVD3" target="_blank">Multi AI Agent Systems with crewAI</a></li>
        </ul>
        <h3>𝐈𝐧𝐭𝐞𝐫𝐦𝐞𝐝𝐢𝐚𝐭𝐞</h3>
        <ul>
            <li>⏩ <a href="https://lnkd.in/dNsDhdsE" target="_blank">Improving Accuracy of LLM Applications</a></li>
            <li>⏩ <a href="https://lnkd.in/d7w_Niuf" target="_blank">AI Agents in LangGraph</a></li>
            <li>⏩ <a href="https://lnkd.in/dZyEwWEa" target="_blank">Building Multimodal Search and RAG</a></li>
            <li>⏩ <a href="https://lnkd.in/dtzADAPM" target="_blank">Functions, Tools and Agents with LangChain</a></li>
        </ul>
        """, unsafe_allow_html=True)
        



st.image(bot_image_path, width=350)  # Logonun yolunu ve genişliğini ayarlayın
# Streamlit uygulaması
st.title("YaşarCaN ile Duyurular")
st.markdown("""
Selam ben YaşarCaN Duyurular benden Sorulur 😎 
""")


# Kullanıcıdan input almak için kutu
query = st.text_input("Mesajınızı yazın:")

# Mesaj gönder butonuna bastığında
if st.button("Gönder"):
    if query:
        # Query işleniyor ve yeni tarihi kaydediyor.
        result, history = execute_query(query, data, [])  # Burada tek bir geçmişi ([]) göndermek önemli
        st.session_state['history_list'].extend(history)
        # Metin kutusunu temizle
        query = ''

# Sohbet geçmişini göster (ters sıralı)
for message in reversed(st.session_state['history_list']):  # reversed() ile döngüyü tersine çeviriyoruz
    user_message = message['question_user']
    bot_message = message['answer_bot']
    
    # Kullanıcı mesajı sağa hizala ve emoji ekle
    st.chat_message("human").markdown(
    f"""
    <div style='text-align: right;'>
        <div style='background-color:#333333; color:#FFFFFF; padding:5px; border-radius:5px; display:inline-block;'>
            <strong>🙋 </strong> {user_message}
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

    # Bot cevabı sola hizala (varsayılan) ve emoji ekle
    #st.chat_message("ai").markdown(f"**🤖 YaşarBot**: \n\n{bot_message}")
    st.chat_message("ai").markdown(
        f"""
        <div style='text-align: left;'>
            <div style='background-color:#444444; color:#FFFFFF; padding:10px; border-radius:10px; display:inline-block;'>
                <strong>🤖 YaşarBot:</strong><br>
                {bot_message}</div></div>
        """, 
        unsafe_allow_html=True
    )