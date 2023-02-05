# Real Estate Analysis

## Arquitetura (Modelagem lógica):

IMAGEM

### 1. Coleta

Nessa etapa iremos capturar dados sobre apartamentos para alugar na cidade de Sobral de diversas origens.

Método:
- [x] Um crawler para cada origem.
- [ ] API com um endpoint de extração para cada origem. Esse método será implementado como uma forma de "evolução" de todo o pipeline.

### 2. Extração e Transformação

Nessa etapa iremos implementar um data lake com camadas raw, cleansed e trusted. Na camada trusted iremos utilizar um banco de dados Postgres para criar a tabela no formato star schema e disponibilizar para a visualização.

### 3. Visualização

Nessa camado irei criar um dashboard com o Metabase