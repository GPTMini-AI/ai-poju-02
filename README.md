# ai-poju-02
AI编程 | AI破局 | 航海02期

## 安装PostgreSQL

```shell
git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git
cd pgvector
docker build --build-arg PG_MAJOR=15 -t ai/pgvector .
docker run -d -p 5432:5432 -e POSTGRES_USER=ai -e POSTGRES_PASSWORD=poju ai/pgvector
```

## 创建表结构

```sql
CREATE DATABASE ai_emb;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE documents (
  id bigserial PRIMARY KEY, 
  title text,        
  url text,                         
  description text,                  
  doc_chunk text,                  
  embedding vector(1536)); 
```

## 安装python依赖

```shell
pip install openai psycopg2 requests beautifulsoup4 numpy
```

## 执行步骤

注意替换关键信息为自己的

先切分文档存库，计算向量

相似度搜索