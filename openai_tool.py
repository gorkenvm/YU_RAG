from openai import OpenAI
import httpx
import pandas as pd
import logging
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

httpx_client = httpx.Client(verify=False)

class OpenAISearchTool:
    MESSAGES = [
        {
            "role": "system",
            "content": """
Yaşar Üniversitesi web sitesindeki duyuruların başlık ve içeriklerini web scraping yöntemiyle topladık. Bu verilerden başlıktaki konuyu açıklayan içeriklerin düzenlenmesi ve temizlenmesi gerekmektedir. Amaç, bir LLM modelini eğitmek için kaliteli bir veri seti hazırlamaktır. İçerik düzenleme sırasında şunları yapmalısınız:

1. **Gereksiz Bilgi ve Gürültü Temizleme:** Başlıkla doğrudan ilgili olmayan kısımları ayıklayın.
2. **Dilbilgisi ve Tutarlılık Kontrolü:** İçeriklerdeki dilbilgisi hatalarını veya anlam bütünlüğünü bozan ifadeleri düzeltin.
3. **Başlık ve İçerik Uyumu:** Başlığın verdiği mesaj ile içeriğin uyumlu olmasını sağlayın. İçerik, başlığı açıklayıcı ve destekleyici olmalıdır.
4. **Metni Sadeleştirme ve Kısaltma:** Gereksiz uzunlukta olan cümleleri sadeleştirin ve metnin anlaşılır ve net olmasına özen gösterin.
5. **Duyuru Amacını Vurgulama:** Duyurunun temel amacını öne çıkararak, okurun dikkat etmesi gereken noktaların altını çizin.
6. **Eksik İçerik Üretme:** Eğer içerik boş gelirse, başlıkta verilen bilgileri kullanarak, mantıklı ve açıklayıcı bir içerik üretin. Bu içerik, başlığın amacını ve konusunu aktaracak şekilde olmalıdır.
                                """,
        },
        {
            "role": "user",
            "content": "#UserRequest#"
        }
    ]



#             "content": "Merhaba, lütfen aşağıdaki isteği okuyarak en özet halini çıkartın. Özet, kişisel bilgiler, telefon numarası ve adres içermemelidir. Ayrıca gereğinin yapılmasını arz ediyorum gibi anlama katkıda bulunmayan cümlelerinde çıkarılmasını istiyorum.\n\nİstek: {İSTEK_METNİ}\n\nÖzet:\n[İSTEĞİN_EN_ÖZET_HALİ]",

    def __init__(self, model="gpt-4o", max_token=8000, top_p=0.1, api_key=OPENAI_API_KEY): # text-davinci-003 gpt-4o-mini
        self.model = model
        self.max_token = max_token
        self.top_p = top_p
        self.client = OpenAI(http_client=httpx_client, api_key=OPENAI_API_KEY)

        # Loglama ayarlarını yapılandır ve tamponlama kullanma
        self.setup_logging()

    def setup_logging(self):
        # Configures logging settings
        logging.basicConfig(
            filename='openai_tool.log',
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            force=True
        )
        self.logger = logging.getLogger(__name__)

    def summarize_request(self, request_text):

        messages = OpenAISearchTool.MESSAGES[:]
        messages[1]["content"] = f"İstek: {request_text}\n\nÖzet:"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=self.max_token,
                top_p=self.top_p,
                frequency_penalty=0,
                presence_penalty=0
            )

            summary = response.choices[0].message.content.strip()

            # Eğer response metni "Özet:" ile başlamıyorsa, doğru formatta olduğundan emin ol
            if not summary.startswith("Özet:"):
                summary = f"Özet:\n{summary}"
        
            # Kullanılan token sayısını alın ve maliyeti hesaplayın
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Fiyatlandırmaya göre maliyet hesaplaması
            input_cost = (input_tokens / 1_000_000) * 0.150  # $0.150 per 1M input tokens
            output_cost = (output_tokens / 1_000_000) * 0.600  # $0.600 per 1M output tokens
            total_cost = input_cost + output_cost

            # Maliyeti logla
            self.logger.info(f"Used {input_tokens} input tokens and {output_tokens} output tokens.")
            self.logger.info(f"Input Cost: ${input_cost:.6f}, Output Cost: ${output_cost:.6f}, Total Cost: ${total_cost:.6f}")
            
            return summary

        except Exception as e:
            self.logger.error(f"Error during summarization: {e}")

            return None


    def get_embedding(self, text, model="text-embedding-3-large"):
        
        text = text.replace("\n", " ")

        response = self.client.embeddings.create(input = [text], model=model)
        embedding = response.data[0].embedding
        total_tokens = response.usage.total_tokens
        total_cost = (total_tokens / 1_000_000) * 0.130
        # Maliyeti logla
        self.logger.info(f"Embedding Used {total_tokens} total token.")
        self.logger.info(f"Used Embedding Total Token : {total_cost} total cost for embedding.")

        return embedding


