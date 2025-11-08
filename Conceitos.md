# DataOps - Governança e Qualidade de Dados: O Motor da Confiança nos Dados

Este documento serve como a fundação teórica para entender como a disciplina **DataOps** se relaciona com os pilares da **Governança** e da **Qualidade de Dados**, transformando dados em um **Ativo Corporativo** confiável e estratégico.

## A Era do Dado como Ativo Corporativo

É fundamental internalizar a ideia de que o **dado é um ativo corporativo**. Assim como o capital financeiro, o maquinário ou os recursos humanos, os dados possuem um valor intrínseco e exigem um sistema de gestão robusto para maximizar seu potencial e mitigar riscos. Esse sistema é a **Governança de Dados**.

## A Estrutura da Governança de Dados

A Governança de Dados é o conjunto de **regras, responsabilidades, processos e políticas** que asseguram que os dados de uma organização sejam gerenciados de forma eficaz e ética, desde sua criação até seu descarte. Pense nela como a estrutura legal e organizacional que define **quem pode fazer o quê, quando, onde e por que** com os dados.

### O Propósito da Governança (Os Quatro Pilares)

O objetivo primário da governança é garantir quatro pilares nos dados:

* **Disponibilidade:** Os dados precisam estar acessíveis para quem precisa, quando precisa.
* **Usabilidade:** Os dados devem estar em um formato e estado que permita seu uso imediato em análises e processos.
* **Integridade:** Garantir a precisão e a completude dos dados.
* **Segurança:** Proteger os dados contra acesso não autorizado e perdas.

### A Conexão DataOps e Governança

> **Governança de Dados** define **O QUÊ** precisa ser feito (as regras, políticas e padrões).
>
> **DataOps** define **COMO** isso será implementado de forma automatizada, colaborativa e contínua (metodologias ágeis e CI/CD).
>
> **DataOps é o motor que executa e monitora as políticas estabelecidas pela Governança.**

---

## Os Pilares Fundamentais da Governança de Dados

A Governança se sustenta sobre três grandes pilares: **Pessoas, Processos e Tecnologia**.

### 1. Pessoas (Roles & Responsibilities - Papéis e Responsabilidades)

A clareza sobre quem é responsável pelo quê é vital para o funcionamento da governança.

| Papel | Responsabilidade Principal | Exemplo |
| :--- | :--- | :--- |
| **Data Owners** (Proprietários) | Responsabilidade máxima pela **qualidade e uso** de um conjunto de dados. **Definem as regras.** | Gerente de Marketing (para dados de clientes). |
| **Data Stewards** (Guardiões) | Responsáveis por **implementar e monitorar** as políticas. Atuam no dia a dia, corrigindo problemas. | Analistas de Dados Sênior que monitoram a qualidade. |
| **Data Custodians** (Custodiantes) | Responsáveis pela **gestão técnica, segurança e armazenamento** dos dados (infraestrutura). | Engenheiros de Dados e DBAs. |

### 2. Processos

Refere-se à definição clara de como o dado é tratado em cada etapa de seu **Ciclo de Vida** (coleta, armazenamento, processamento, retenção, arquivamento e descarte seguro).

### 3. Tecnologia

São as ferramentas e sistemas utilizados para suportar e automatizar a Governança.

* **Catálogos de Dados:** Biblioteca central de dados, incluindo glossário de negócios, dicionário de dados e metadados.
* **Ferramentas de Qualidade de Dados:** Sistemas que monitoram e executam as regras de validação.

### Políticas e Procedimentos: A Lei dos Dados

A formalização das regras é crucial:

* **Definição de Dados (Glossário de Negócios):** Criar um vocabulário comum (Ex: O que significa "Cliente Ativo"?).
* **Padrões de Dados:** Estabelecer regras de formato (Ex: datas AAAA-MM-DD, convenções de nomenclatura).
* **Auditoria e Rastreabilidade (Linhagem):** Capacidade de registrar e rastrear quem acessou, usou ou modificou um dado e quando.
* **Segurança e Conformidade:**
    * **Regulamentações:** Conformidade com leis como **LGPD, GDPR e HIPAA**.
    * **Segurança:** Políticas para controle de acesso, Criptografia (em transmissão e repouso) e Mascaramento de Dados.

---

## 💯 Qualidade de Dados - O Fator Crítico de Confiança

A **Qualidade de Dados** é a medida de quão bem o dado atende ao seu propósito pretendido. A falta de qualidade é o principal motivo de falha em projetos de análise e Machine Learning.

### As Seis Dimensões da Qualidade de Dados

| Dimensão | Pergunta Chave | Exemplo de Verificação |
| :--- | :--- | :--- |
| **Acurácia** (Accuracy) | O dado está **correto** e reflete a realidade? | O endereço do cliente é o endereço real? |
| **Completude** (Completeness) | Todos os dados esperados estão **presentes**? | O campo CPF não está vazio em mais de X% dos registros? |
| **Consistência** (Consistency) | O dado é o **mesmo** em todos os sistemas onde aparece? | O status de um pedido é "Enviado" no sistema de estoque E no sistema de vendas? |
| **Pontualidade** (Timeliness) | O dado está disponível **quando necessário** e é atual o suficiente? | O dashboard usa dados com no máximo 15 minutos de idade? |
| **Unicidade** (Uniqueness) | Não existem cópias ou **duplicatas** desnecessárias? | Cada cliente tem apenas um número de ID único. |
| **Validade** (Validity) | O dado está em um formato e domínio **aceitáveis**? | A idade é um número inteiro entre 0 e 120. |

### Por que Testar Dados é Essencial em DataOps?

Em DataOps, a Qualidade de Dados é garantida pela **automação de testes**. É mais fácil e barato corrigir um dado ruim assim que ele entra no sistema do que meses depois, quando já poluiu análises e modelos.

### Tipos de Testes de Dados (Conceitos Chave)

* **Testes de Schema (Estrutura):**
    * Verifica: Nomes e tipos de dados das colunas (Ex: Coluna `ID_CLIENTE` deve ser um inteiro).
* **Testes de Integridade (Relacionamentos e Unicidade):**
    * Integridade Referencial: Garante que um dado referenciado exista (Ex: `Item de Pedido` referencia um `Pedido` que existe).
    * Unicidade: Garante a ausência de duplicatas em colunas críticas (Ex: Campo `CPF`).
* **Testes de Validade (Regras de Conteúdo):**
    * Domínio: O valor está em um conjunto predefinido (Ex: `Status` só pode ser 'Aprovado', 'Pendente' ou 'Rejeitado').
    * Formato/Padrão: O valor segue um padrão de escrita (Ex: Formato de e-mail).
    * Intervalo: O valor está dentro de um range aceitável (Ex: Valor de compra $ > 0$).
* **Testes de Consistência (Comparação):**
    * Entre Fontes: Comparar totais entre sistemas (Ex: Total de clientes no BD Transacional = Total no Data Warehouse).
    * Ao Longo do Tempo: Verificar se uma regra se mantém e não há saltos inexplicáveis.
* **Testes de Volume/Performance:**
    * Verifica: Se o sistema processa o volume esperado dentro do tempo limite (teste de qualidade do pipeline).

---

## Integrando Testes no Pipeline DataOps

A excelência em DataOps é transformar as regras de Governança e Qualidade em **código automatizado**, integrando-o ao fluxo de trabalho (pipeline).

### Onde os Testes Acontecem no Pipeline

| Etapa | Tipo de Dado | Testes Recomendados | Objetivo |
| :--- | :--- | :--- | :--- |
| **Após Ingestão** | Dados Brutos (Raw Data) | Schema, Unicidade e Completude básica. | Garantir que o dado fonte chegou sem corrupção. |
| **Após Transformação** | Dados Limpos (Cleaned Data) | Validade, Consistência, Integridade Referencial. | Validar que as transformações de negócio foram aplicadas corretamente. |
| **Antes do Carregamento** | Destino | Testes de Aceitação. | Garantir que o dado transformado atende aos requisitos do sistema de destino. |

### Automação e a Regra da Falha

A chave é a **Automação**. Os scripts de teste (Ex: Python/Pandas, Great Expectations) devem ser parte do orquestrador (Airflow, Prefect).

> **A Regra do DataOps:** Se o teste de qualidade falha, **o pipeline deve parar**.
>
> A falha deve gerar uma notificação imediata para os Data Stewards/engenheiros, e o lote de dados problemático deve ser colocado em quarentena para correção.

### Monitoramento Contínuo

O trabalho se estende além da execução:

* **Dashboards de Qualidade de Dados:** Visualizações que mostram a saúde geral (taxas de completude, falha em testes).
* **Alertas:** Acionados automaticamente em caso de anomalia ou violação de regra.
* **Ferramentas Especializadas:** Softwares como **Great Expectations** ou **Deequ**.

---

## REFERÊNCIAS

* Dama-Dmbok (2Nd Edition): Data Management Body of Knowledge: 2nd Edition, Revised
* Lei Geral de Proteção de Dados Pessoais (LGPD)