# 🏛️ Governança de Dados - TechCommerce

## 📊 Organograma de Dados

### Data Owners (Proprietários dos Dados)
- **Clientes**: Diretor de Marketing (responsável pela estratégia de clientes)
- **Produtos**: Diretor de Produtos (responsável pelo catálogo e precificação)
- **Vendas**: Diretor Comercial (responsável pelas transações e receita)
- **Logística**: Diretor de Operações (responsável pela entrega e fulfillment)

### Data Stewards (Guardiões dos Dados)
- **Clientes**: Analista de CRM Senior
- **Produtos**: Product Manager Senior
- **Vendas**: Analista de Vendas Senior
- **Logística**: Coordenador de Logística

### Data Custodians (Custodiantes Técnicos)
- **Infraestrutura**: Engenheiro de Dados Senior
- **Qualidade**: Especialista em Qualidade de Dados
- **Segurança**: Analista de Segurança da Informação

## 📋 Políticas de Qualidade de Dados

### 1. Completude
- **Definição**: Percentual de campos obrigatórios preenchidos
- **Meta**: ≥ 98% para campos críticos, ≥ 95% para campos importantes
- **Ação Corretiva**: Bloqueio de processamento se < 90%

### 2. Unicidade
- **Definição**: Ausência de registros duplicados
- **Meta**: 0% duplicatas em chaves primárias
- **Ação Corretiva**: Deduplicação automática com log de auditoria

### 3. Validade
- **Definição**: Conformidade com formatos e regras de negócio
- **Meta**: ≥ 99% para dados críticos
- **Ação Corretiva**: Correção automática quando possível, quarentena caso contrário

### 4. Consistência
- **Definição**: Coerência entre sistemas e ao longo do tempo
- **Meta**: ≥ 98% consistência cross-sistema
- **Ação Corretiva**: Sincronização automática entre fontes

### 5. Precisão
- **Definição**: Correspondência com a realidade
- **Meta**: ≥ 97% precisão verificada
- **Ação Corretiva**: Validação com fontes externas

### 6. Atualidade
- **Definição**: Dados atualizados dentro do prazo esperado
- **Meta**: Latência < 1 hora para dados críticos
- **Ação Corretiva**: Alertas automáticos para atrasos

## 📚 Glossário de Negócios

### Entidades Principais

#### Cliente Ativo
- **Definição**: Cliente com pelo menos uma compra nos últimos 12 meses
- **Critérios**: data_ultima_compra >= hoje - 365 dias

#### Venda Válida
- **Definição**: Transação com status "Concluída" e valor > 0
- **Critérios**: status = "Concluída" AND valor_total > 0

#### Produto Ativo
- **Definição**: Produto disponível para venda
- **Critérios**: ativo = true AND estoque >= 0

### Padrões de Formato

#### Datas
- **Formato**: YYYY-MM-DD
- **Timezone**: UTC
- **Validação**: data_nascimento < hoje, data_venda <= hoje

#### Telefones
- **Formato**: 11 dígitos (DDxxxxxxxxx)
- **Validação**: regex ^[1-9][1-9][0-9]{9}$

#### Emails
- **Formato**: usuario@dominio.extensao
- **Validação**: regex ^[\w\.-]+@[\w\.-]+\.\w+$

#### Estados
- **Formato**: 2 caracteres maiúsculos
- **Valores válidos**: SP, RJ, MG, RS, PR, SC, etc.

### Regras de Relacionamento

#### Cliente → Vendas
- **Integridade**: Todo id_cliente em vendas deve existir em clientes
- **Cardinalidade**: 1:N (um cliente pode ter várias vendas)

#### Produto → Vendas
- **Integridade**: Todo id_produto em vendas deve existir em produtos
- **Cardinalidade**: 1:N (um produto pode estar em várias vendas)

#### Vendas → Logística
- **Integridade**: Todo id_venda em logística deve existir em vendas
- **Cardinalidade**: 1:1 (uma venda tem uma entrega)

## 🚨 Matriz de Criticidade

### Crítico (Bloqueante)
- Chaves primárias nulas ou duplicadas
- Valores negativos em preços/quantidades
- Datas futuras em transações passadas
- Referências órfãs (foreign keys inválidas)

### Alto (Correção Imediata)
- Emails inválidos
- Telefones mal formatados
- Estados inválidos
- Produtos sem categoria

### Médio (Correção em 24h)
- Campos opcionais vazios
- Inconsistências menores de formato
- Dados desatualizados

### Baixo (Correção em 7 dias)
- Dados de enriquecimento ausentes
- Métricas derivadas desatualizadas