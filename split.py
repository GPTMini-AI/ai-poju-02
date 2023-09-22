import openai
import psycopg2
import requests
from bs4 import BeautifulSoup

EMBEDDING_MODEL = "text-embedding-ada-002"

# 连接RDS PostgreSQL数据库
conn = psycopg2.connect(database="<数据库名>",
                        host="<RDS实例连接地址>",
                        user="<用户名>",
                        password="<密码>",
                        port="<数据库端口>")
conn.autocommit = True

# OpenAI的API Key
openai.api_key = '<Secret API Key>'

# 自定义拆分方法（仅为示例）
def get_text_chunks(content, max_chunk_size):
    chunks_ = []

    length = len(content)
    start = 0
    while start < length:
        end = start + max_chunk_size
        if end >= length:
            end = length

        chunk_ = content[start:end]
        chunks_.append(chunk_)

        start = end

    return chunks_


# 指定需要拆分的网页
url = 'https://mp.weixin.qq.com/s/51ZcgCgWVsEUeBBJnw1-Ew'

response = requests.get(url)
if response.status_code == 200:
    # 解析网页内容
    web_html_data = response.text
    soup = BeautifulSoup(web_html_data, 'html.parser')
    # 获取标题（H1标签）
    title = soup.find('h1').text.strip()
    # 发布信息（div标签）
    description = soup.find('div', class_='rich_media_meta_list').text.strip()
    # 文章详情（div标签）
    content = soup.find('div', class_='rich_media_content').text.strip()

    # 拆分并存储
    chunks = get_text_chunks(content, 500)
    for chunk in chunks:
        doc_item = {
            'title': title,
            'url': url,
            'description': description,
            'doc_chunk': chunk
        }

        query_embedding_response = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=chunk,
        )

        doc_item['embedding'] = query_embedding_response['data'][0]['embedding']

        cur = conn.cursor()
        insert_query = '''
        INSERT INTO documents 
            (title, url, description, doc_chunk, embedding) VALUES (%s, %s, %s, %s, %s);
        '''

        cur.execute(insert_query, (
            doc_item['title'], doc_item['url'], doc_item['description'], doc_item['doc_chunk'],
            doc_item['embedding']))

        conn.commit()

else:
    print('网页加载失败')