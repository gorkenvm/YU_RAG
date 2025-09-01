# YU_RAG

University of Yasar GDG on Campus RAG GENERATIVE AI

## Proje Hakkında

YU_RAG, Yaşar Üniversitesi öğrencileri için duyuruları ve diğer akademik bilgileri sunan bir chatbot uygulamasıdır. Bu proje, Generative AI ve Retrieval-Augmented Generation (RAG) tekniklerini kullanarak öğrencilere en güncel ve doğru bilgileri sağlamayı amaçlamaktadır.

## Özellikler

- **Duyuru Çekme ve İşleme:** Üniversite web sitesinden duyuruları otomatik olarak çeker ve işler.
- **Chatbot:** Öğrencilerin sorularını yanıtlayan ve onlara yardımcı olan bir chatbot.
- **Embeddings ve Benzerlik Arama:** Sorgulara en uygun yanıtları bulmak için metin embeddings ve benzerlik arama kullanır.
- **Streamlit Arayüzü:** Kullanıcı dostu bir web arayüzü ile etkileşim sağlar.

## Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın:**
    ```sh
    git clone https://github.com/kullanici_adi/YU_RAG.git
    cd YU_RAG
    ```

2. **Gerekli Paketleri Yükleyin:**
    ```sh
    pip install -r requirements.txt
    ```

3. **API Anahtarlarını Ayarlayın:**
    `.env` dosyasını oluşturun ve gerekli API anahtarlarını ekleyin:
    ```env
    GEMINI_API_KEY="your_gemini_api_key"
    OPENAI_API_KEY="your_openai_api_key"
    ```

NOTE : GEMINI_API_KEY'i yazmak yeterli olacaktır.

4. **Uygulamayı Başlatın:**
    `YU_app.py` dosyasını çalıştırarak Streamlit uygulamasını başlatın:
    ```sh
    streamlit run YU_app.py
    ```

## Kullanım

- **Ana Sayfa:** Chatbot ile etkileşime geçebilir ve sorularınızı sorabilirsiniz.
- **Duyurular:** Üniversite duyurularını görüntüleyebilir ve detaylarına ulaşabilirsiniz.
- **RAG Mimarisi:** RAG mimarisi hakkında bilgi alabilir ve örnek uygulamaları inceleyebilirsiniz.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın. Her türlü katkı ve geri bildirim memnuniyetle karşılanır.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.



## 📊 RAG Pipeline

The architecture of the project is illustrated below:

```mermaid
flowchart TD
    A[University Website] -->|Scraping| B[Scrape Duyurular]
    B -->|Processed Data| C[Create Vectors]
    C -->|Embeddings| D[(Vector Database)]
    D -->|Semantic Search| E[Chatbot Functions]
    E -->|Response| F[Streamlit App]

