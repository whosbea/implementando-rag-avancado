# Laboratório 09 — Arquitetura RAG Avançada com HNSW, HyDE e Cross-Encoder

## 1. Objetivo do laboratório

Este laboratório teve como objetivo implementar, em Python, um pipeline de **Retrieval-Augmented Generation (RAG)** com componentes mais próximos de um cenário real de produção. Em vez de depender apenas de uma busca vetorial simples, a arquitetura foi construída com três camadas principais:

- **HNSW**, para indexação vetorial eficiente;
- **HyDE**, para transformar consultas coloquiais em uma ponte semântica técnica;
- **Cross-Encoder**, para reranquear os documentos recuperados e melhorar a precisão final.

A ideia central foi reduzir o problema de desalinhamento entre a forma como o usuário pergunta e a forma como o conhecimento técnico aparece nos documentos.

## 2. Domínio escolhido

O domínio escolhido foi:

**Manuais técnicos de análise forense digital**

Essa escolha foi feita porque esse domínio apresenta uma diferença muito clara entre:

- linguagem coloquial do usuário;
- terminologia técnica dos manuais.

Exemplos desse contraste:

- “apagaram uns arquivos, ainda dá pra recuperar?”
- “mexeram no computador depois do fato?”
- “como saber se alteraram uma imagem?”

Essas perguntas, em um manual técnico, aparecem com termos como:

- recuperação de arquivos excluídos;
- espaço não alocado;
- aquisição forense;
- análise de timestamps;
- metadados;
- integridade por hash;
- cadeia de custódia.

Esse cenário torna o uso de **HyDE** especialmente útil, porque ele ajuda a converter a intenção coloquial em um documento técnico hipotético mais próximo do espaço vetorial dos manuais.

## 3. Visão geral da arquitetura

A arquitetura final foi composta pelas seguintes etapas:

1. construção de um corpus técnico simulado;
2. geração de embeddings densos;
3. indexação vetorial com **HNSW**;
4. transformação da query com **HyDE**;
5. recuperação inicial dos **Top-10** documentos;
6. reranqueamento com **Cross-Encoder**;
7. seleção dos **Top-3** documentos finais.

Em termos simples, o pipeline funciona como um funil:

- primeiro, faz uma busca rápida e ampla;
- depois, faz uma análise mais precisa e profunda;
- por fim, retorna apenas os documentos mais relevantes para serem usados como contexto.

## 4. O que é RAG

**RAG (Retrieval-Augmented Generation)** é uma arquitetura em que o modelo de linguagem não responde apenas com base nos seus parâmetros internos. Antes de gerar a resposta, ele consulta uma base de documentos relevantes.

### Por que isso é importante
Sem RAG, o modelo depende apenas do que já “sabe”.  
Com RAG, ele pode consultar material específico antes de responder.

### No contexto deste laboratório
O modelo não respondeu diretamente usando só memória paramétrica.  
Primeiro ele buscou fragmentos técnicos do corpus de análise forense digital.  
Esses documentos seriam, em um sistema completo, injetados como contexto para a geração final.

## 5. Estrutura do projeto

```text
implementando-rag-avancado/
├── data/
│   ├── manual_fragments.jsonl
│   ├── hnsw_index.faiss
│   └── hnsw_metadata.pkl
├── src/
│   ├── generate_corpus.py
│   ├── build_index.py
│   └── rag_pipeline.py
├── requirements.txt
└── README.md
```

## 6. Construção do corpus técnico

O corpus foi construído no arquivo:

**`src/generate_corpus.py`**

Foram criados **25 fragmentos técnicos** de análise forense digital. O laboratório exigia pelo menos 20, então o corpus foi ampliado para aumentar a variedade semântica.

### Tipos de tópicos incluídos no corpus

Entre os assuntos presentes no corpus, foram incluídos:

- cadeia de custódia digital;
- aquisição forense bit a bit;
- verificação de integridade com hash;
- análise de timestamps;
- espaço não alocado;
- recuperação de arquivos excluídos;
- memória volátil;
- imagem forense;
- metadados;
- dispositivos USB;
- logs de autenticação;
- correlação temporal;
- evidência em rede;
- bloqueadores de escrita;
- correlação entre evidência local e evidência em nuvem.

### Justificativa da construção manual

O corpus foi elaborado de forma manual e supervisionada, com apoio do **ChatGPT 5.4 Thinking**, e revisado por **Beatriz Barreto**. Essa escolha permitiu:

- maior controle sobre o vocabulário técnico;
- maior coerência temática entre os fragmentos;
- menor risco de inconsistência terminológica;
- melhor aderência ao domínio de análise forense digital.

## 7. Formato dos dados

O corpus foi salvo em formato `.jsonl`.

### O que é JSONL
**JSONL (JSON Lines)** é um formato em que cada linha do arquivo contém um objeto JSON completo.

### Exemplo
```json
{"id": 1, "title": "Cadeia de custódia digital", "text": "A cadeia de custódia digital consiste..."}
{"id": 2, "title": "Aquisição forense bit a bit", "text": "A aquisição forense bit a bit corresponde..."}
```

### Por que usar JSONL
Esse formato é simples de ler linha por linha e funciona bem em pipelines de indexação e recuperação documental.

## 8. Embeddings

Depois da construção do corpus, cada fragmento técnico foi convertido em um vetor denso.

### Modelo de embedding utilizado

Foi utilizado o modelo:

**`sentence-transformers/all-MiniLM-L6-v2`**

### O que é embedding
Um **embedding** é uma representação numérica de um texto em um espaço vetorial.  
A ideia é que textos semanticamente parecidos fiquem próximos geometricamente.

### Por que embeddings são importantes aqui
Sem embeddings, o sistema teria que comparar textos de forma literal ou baseada só em palavras exatas.  
Com embeddings, ele pode capturar semelhança de significado.

### Justificativa da escolha do modelo
O modelo `all-MiniLM-L6-v2` foi escolhido porque:

- é leve;
- roda bem localmente;
- tem boa qualidade para recuperação semântica;
- é suficiente para um laboratório acadêmico.

## 9. Indexação vetorial com HNSW

Depois da geração dos embeddings, foi criado um índice vetorial usando **FAISS** com arquitetura **HNSW**.

### O que é FAISS
**FAISS** é uma biblioteca voltada para busca vetorial eficiente.

### O que é HNSW
**HNSW (Hierarchical Navigable Small World)** é uma estrutura de grafo usada para busca aproximada de vizinhos mais próximos.

Em vez de comparar um vetor com todos os outros de forma exata, o HNSW organiza os vetores em uma estrutura navegável que torna a busca muito mais rápida.

### Como ele foi configurado
Foram usados:

- `M = 32`
- `efConstruction = 200`

### O que significa `M`
`M` controla quantas conexões cada nó tende a manter no grafo.

#### Efeito prático
- valores maiores de `M` aumentam conectividade;
- isso pode melhorar a qualidade da busca;
- mas também aumenta o consumo de memória RAM.

### O que significa `efConstruction`
`efConstruction` controla o esforço da etapa de construção do índice.

#### Efeito prático
- valores maiores tornam a construção mais cuidadosa;
- isso tende a melhorar a qualidade da vizinhança no grafo;
- mas aumenta tempo de construção e uso de memória.

### Comparação com KNN exato
Em uma busca **KNN exata**, o sistema compara a query com todos os vetores do conjunto, o que tende a ser mais custoso em tempo e escala.

No **HNSW**, há custo adicional de memória para manter a estrutura do grafo, especialmente quando `M` e `efConstruction` aumentam. Em troca, a busca tende a ser muito mais rápida do que KNN exato, sobretudo em bases maiores.

### Resumo analítico para o README
- **KNN exato**: menor complexidade estrutural, mas custo alto de busca;
- **HNSW**: maior consumo de RAM para manter conexões no grafo, porém busca mais eficiente;
- aumentar **M** e **efConstruction** melhora a qualidade da indexação, mas também aumenta uso de memória.

Essa é a análise pedida no enunciado sobre como os hiperparâmetros do HNSW afetam RAM em comparação a uma busca KNN exata.

## 10. Query Transformation com HyDE

A próxima etapa da arquitetura foi a transformação da query com **HyDE**.

### O que é HyDE
**HyDE (Hypothetical Document Embeddings)** é uma técnica em que, antes de buscar documentos reais, o sistema pede a um LLM que gere um **documento hipotético** tecnicamente plausível sobre a pergunta do usuário.

Depois disso, em vez de vetorizar a query coloquial original, o sistema vetoriza esse documento técnico artificial.

### Por que isso ajuda
A query original do usuário pode ser curta, vaga ou coloquial.  
Isso pode deixá-la distante do espaço vetorial dos documentos técnicos.

O HyDE atua como uma ponte semântica.

### Exemplo do teste realizado
Query original:

> apagaram uns arquivos e eu quero saber se ainda dá pra recuperar

Documento hipotético gerado:

> análise forense de recuperação de artefatos digitais excluídos, espaço não alocado, sobrescrita, slack space e file carving.

Esse comportamento apareceu no console durante a execução do pipeline. 

### LLM utilizado no HyDE
Foi utilizado o **Gemini** por meio da biblioteca `google-genai`.

### Justificativa
Essa escolha permitiu usar um LLM para gerar a reformulação técnica sem depender de um modelo local pesado.

## 11. Busca rápida via Bi-Encoder

Depois do HyDE, o sistema gerou o embedding do documento hipotético e consultou o índice HNSW.

### O que significa Bi-Encoder
Em recuperação semântica, um **Bi-Encoder** é um modelo que transforma cada texto em um vetor de forma independente. Depois, a similaridade é calculada entre os vetores.

No nosso caso:

- os documentos do corpus foram embutidos em vetores;
- o documento HyDE também foi embutido;
- a busca foi feita por similaridade vetorial.

### Resultado dessa etapa
O pipeline recuperou os **Top-10 documentos mais próximos** no índice HNSW, conforme exigido pelo laboratório. 

## 12. Re-ranking com Cross-Encoder

Depois da recuperação inicial, foi aplicado um **Cross-Encoder** para reranquear os resultados.

### Modelo utilizado
Foi usado o modelo:

**`cross-encoder/ms-marco-MiniLM-L-6-v2`**

### O que é Cross-Encoder
Diferentemente do Bi-Encoder, o Cross-Encoder avalia a query e o documento **juntos**, observando interação profunda entre os tokens.

### Por que isso melhora a precisão
A busca vetorial inicial é rápida, mas pode trazer documentos semanticamente próximos sem tanta precisão contextual.

O Cross-Encoder funciona como um filtro fino:
- recebe a query original e cada documento recuperado;
- calcula um score mais preciso;
- reordena os candidatos.

### No laboratório
Foram reranqueados os **10 documentos recuperados** na etapa anterior, e os **Top-3 finais** foram impressos no console, como exigido pelo enunciado. 

## 13. Resultado do teste

A query utilizada no teste foi:

> apagaram uns arquivos e eu quero saber se ainda dá pra recuperar

### Resultado do HyDE
O sistema gerou um documento hipotético técnico coerente com recuperação de artefatos excluídos, espaço não alocado, sobrescrita e file carving. 

### Resultado da busca rápida
Os Top-10 recuperados incluíram documentos como:

- autenticidade de imagens digitais;
- memória volátil;
- metadados de arquivos;
- bloqueadores de escrita;
- imagem forense;
- aquisição forense bit a bit. 

### Resultado do reranking
Após o Cross-Encoder, os Top-3 finais foram:

1. **Aquisição forense bit a bit**
2. **Metadados de arquivos**
3. **Correlação temporal de eventos** 

### Análise honesta do resultado
O pipeline se comportou corretamente do ponto de vista arquitetural. O HyDE funcionou e o reranking refinou a busca.

Apesar disso, os resultados ainda não ficaram perfeitos semanticamente. Para a query sobre arquivos apagados, seria desejável que documentos como:

- espaço não alocado;
- recuperação de arquivos excluídos;
- imagem forense

aparecessem em posições ainda mais altas.

Mesmo assim, o experimento demonstrou claramente o funcionamento das três camadas da arquitetura:

- transformação da query;
- recuperação vetorial rápida;
- reranqueamento fino.

## 14. Explicação dos principais termos da arquitetura

### Corpus
Conjunto de documentos usados como base de conhecimento.

### Fragmento
Trecho individual do corpus. Neste projeto, cada fragmento corresponde a um mini trecho de manual técnico.

### Embedding
Vetor numérico que representa o significado de um texto.

### Similaridade de cosseno
Métrica usada para medir o quanto dois vetores apontam em direções parecidas no espaço vetorial.

### Índice vetorial
Estrutura de dados usada para armazenar vetores e permitir busca eficiente.

### HNSW
Estrutura em grafo para busca aproximada de vizinhos mais próximos.

### KNN exato
Busca exata pelos vizinhos mais próximos, geralmente mais cara em tempo quando a base cresce.

### HyDE
Técnica que cria um documento hipotético técnico para melhorar a recuperação semântica.

### Bi-Encoder
Modelo que gera embeddings independentes para query e documento.

### Cross-Encoder
Modelo que avalia query e documento juntos para gerar um score de relevância mais preciso.

### Re-ranking
Reordenação fina dos documentos recuperados inicialmente.

### Top-10
Os dez documentos inicialmente recuperados no funil largo.

### Top-3
Os três documentos finais mais relevantes após o reranking.

## 15. Como executar o projeto

### 15.1 Criar o ambiente virtual
```bash
python -m venv .venv
```

### 15.2 Ativar no fish
```fish
source .venv/bin/activate.fish
```

### 15.3 Instalar dependências
```bash
pip install -r requirements.txt
```

### 15.4 Gerar o corpus
```bash
python src/generate_corpus.py
```

### 15.5 Construir o índice vetorial
```bash
python src/build_index.py
```

### 15.6 Executar o pipeline RAG
```bash
python src/rag_pipeline.py
```

## 16. Dependências principais

As bibliotecas principais utilizadas foram:

- `sentence-transformers`
- `transformers`
- `torch`
- `faiss-cpu`
- `numpy`
- `google-genai`

## 17. Ambiente utilizado

O laboratório foi desenvolvido em ambiente local com:

- Python 3.12.8
- ambiente virtual `.venv`

## 18. Observação sobre uso de IA

**Partes deste laboratório foram geradas/complementadas com IA, revisadas e validadas por Beatriz Barreto.**

Houve apoio de IA na elaboração dos fragmentos técnicos, na organização do pipeline e na estruturação da documentação. Todo o conteúdo foi revisado, executado e validado por **Beatriz Barreto**. 

## 19. Conclusão

O laboratório permitiu implementar um pipeline RAG mais avançado do que uma busca vetorial simples. A arquitetura construída mostrou, de forma prática, como combinar:

- um índice vetorial eficiente (**HNSW**);
- uma ponte semântica com LLM (**HyDE**);
- um filtro fino de relevância (**Cross-Encoder**).

O resultado final demonstrou que essa combinação melhora a capacidade do sistema de conectar perguntas coloquiais a documentos técnicos especializados em análise forense digital.
