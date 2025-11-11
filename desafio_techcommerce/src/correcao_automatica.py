"""
🔧 Sistema de Correção Automática - TechCommerce
Implementa correções automáticas para problemas de qualidade de dados
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional
import logging
from difflib import SequenceMatcher

class DataCorrectionEngine:
    """Engine para correção automática de problemas de qualidade"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.correction_log = []
        
        # Padrões de correção
        self.email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        self.phone_pattern = re.compile(r'^[1-9][1-9][0-9]{9}$')
        
        # Listas de referência para correção
        self.valid_states = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        
        self.valid_categories = [
            "Eletrônicos", "Informática", "Casa", "Moda", "Esportes",
            "Livros", "Beleza", "Automotivo", "Jardim", "Brinquedos"
        ]
        
        self.valid_status_venda = ["Concluída", "Pendente", "Cancelada", "Processando"]
        self.valid_status_entrega = ["Entregue", "Em Trânsito", "Cancelada", "Aguardando"]
        
    def _setup_logging(self) -> logging.Logger:
        """Configura logging para correções"""
        logger = logging.getLogger('DataCorrection')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _log_correction(self, dataset: str, row_id: any, column: str, 
                       old_value: any, new_value: any, correction_type: str):
        """Registra correção no log"""
        correction_entry = {
            "timestamp": datetime.now().isoformat(),
            "dataset": dataset,
            "row_id": row_id,
            "column": column,
            "old_value": str(old_value),
            "new_value": str(new_value),
            "correction_type": correction_type
        }
        self.correction_log.append(correction_entry)
        
    def correct_clientes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica correções específicas para dataset de clientes"""
        df_corrected = df.copy()
        
        self.logger.info("🔧 Iniciando correções para dataset CLIENTES")
        
        # 1. REMOVER DUPLICATAS
        df_corrected = self._remove_duplicates(df_corrected, "clientes", "id_cliente")
        
        # 2. CORRIGIR EMAILS
        df_corrected = self._correct_emails(df_corrected, "clientes")
        
        # 3. CORRIGIR TELEFONES
        df_corrected = self._correct_phones(df_corrected, "clientes")
        
        # 4. PADRONIZAR ESTADOS
        df_corrected = self._standardize_states(df_corrected, "clientes")
        
        # 5. PREENCHER CAMPOS VAZIOS
        df_corrected = self._fill_missing_cliente_data(df_corrected)
        
        # 6. PADRONIZAR DATAS
        df_corrected = self._standardize_dates(df_corrected, "clientes", 
                                             ["data_nascimento", "data_cadastro"])
        
        self.logger.info(f"✅ Correções aplicadas em CLIENTES: {len(self.correction_log)} alterações")
        return df_corrected
    
    def correct_produtos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica correções específicas para dataset de produtos"""
        df_corrected = df.copy()
        
        self.logger.info("🔧 Iniciando correções para dataset PRODUTOS")
        
        # 1. REMOVER DUPLICATAS
        df_corrected = self._remove_duplicates(df_corrected, "produtos", "id_produto")
        
        # 2. CORRIGIR PREÇOS NEGATIVOS
        df_corrected = self._correct_negative_prices(df_corrected)
        
        # 3. CATEGORIZAR PRODUTOS SEM CATEGORIA
        df_corrected = self._auto_categorize_products(df_corrected)
        
        # 4. PADRONIZAR CATEGORIAS
        df_corrected = self._standardize_categories(df_corrected)
        
        # 5. CORRIGIR ESTOQUE NEGATIVO
        df_corrected = self._correct_negative_stock(df_corrected)
        
        # 6. PADRONIZAR CAMPO ATIVO
        df_corrected = self._standardize_boolean_field(df_corrected, "produtos", "ativo")
        
        self.logger.info(f"✅ Correções aplicadas em PRODUTOS: {len(self.correction_log)} alterações")
        return df_corrected
    
    def correct_vendas(self, df: pd.DataFrame, df_clientes: pd.DataFrame, 
                      df_produtos: pd.DataFrame) -> pd.DataFrame:
        """Aplica correções específicas para dataset de vendas"""
        df_corrected = df.copy()
        
        self.logger.info("🔧 Iniciando correções para dataset VENDAS")
        
        # 1. CORRIGIR QUANTIDADES NEGATIVAS/ZERO
        df_corrected = self._correct_invalid_quantities(df_corrected)
        
        # 2. CORRIGIR VALORES NEGATIVOS
        df_corrected = self._correct_negative_values(df_corrected)
        
        # 3. CORRIGIR CÁLCULO VALOR_TOTAL
        df_corrected = self._correct_total_calculation(df_corrected)
        
        # 4. CORRIGIR REFERÊNCIAS ÓRFÃS
        df_corrected = self._correct_orphan_references(df_corrected, df_clientes, df_produtos)
        
        # 5. CORRIGIR DATAS FUTURAS
        df_corrected = self._correct_future_dates(df_corrected, "vendas", "data_venda")
        
        # 6. PADRONIZAR STATUS
        df_corrected = self._standardize_status(df_corrected, "vendas", "status", self.valid_status_venda)
        
        self.logger.info(f"✅ Correções aplicadas em VENDAS: {len(self.correction_log)} alterações")
        return df_corrected
    
    def correct_logistica(self, df: pd.DataFrame, df_vendas: pd.DataFrame) -> pd.DataFrame:
        """Aplica correções específicas para dataset de logística"""
        df_corrected = df.copy()
        
        self.logger.info("🔧 Iniciando correções para dataset LOGÍSTICA")
        
        # 1. PREENCHER TRANSPORTADORAS VAZIAS
        df_corrected = self._fill_missing_transportadora(df_corrected)
        
        # 2. CORRIGIR REFERÊNCIAS ÓRFÃS PARA VENDAS
        df_corrected = self._correct_logistica_orphan_references(df_corrected, df_vendas)
        
        # 3. CORRIGIR INCONSISTÊNCIAS DE DATAS
        df_corrected = self._correct_date_inconsistencies(df_corrected)
        
        # 4. PADRONIZAR STATUS DE ENTREGA
        df_corrected = self._standardize_status(df_corrected, "logistica", "status_entrega", 
                                              self.valid_status_entrega)
        
        # 5. PREENCHER DATAS DE ENVIO AUSENTES
        df_corrected = self._fill_missing_shipping_dates(df_corrected, df_vendas)
        
        self.logger.info(f"✅ Correções aplicadas em LOGÍSTICA: {len(self.correction_log)} alterações")
        return df_corrected
    
    def _remove_duplicates(self, df: pd.DataFrame, dataset: str, id_column: str) -> pd.DataFrame:
        """Remove duplicatas mantendo o primeiro registro"""
        initial_count = len(df)
        
        # Identificar duplicatas
        duplicates = df.duplicated(subset=[id_column], keep='first')
        duplicate_ids = df[duplicates][id_column].tolist()
        
        # Remover duplicatas
        df_clean = df.drop_duplicates(subset=[id_column], keep='first')
        
        # Log das correções
        for dup_id in duplicate_ids:
            self._log_correction(dataset, dup_id, id_column, "duplicated", "removed", "DEDUPLICATION")
        
        removed_count = initial_count - len(df_clean)
        if removed_count > 0:
            self.logger.info(f"Removidas {removed_count} duplicatas em {dataset}")
        
        return df_clean
    
    def _correct_emails(self, df: pd.DataFrame, dataset: str) -> pd.DataFrame:
        """Corrige emails inválidos"""
        if 'email' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            email = str(row['email'])
            
            if pd.isna(row['email']) or email == 'nan':
                continue
                
            # Tentar corrigir emails comuns
            corrected_email = self._fix_common_email_errors(email)
            
            if corrected_email != email:
                df_corrected.at[idx, 'email'] = corrected_email
                self._log_correction(dataset, row.get('id_cliente', idx), 'email', 
                                   email, corrected_email, "EMAIL_CORRECTION")
        
        return df_corrected
    
    def _fix_common_email_errors(self, email: str) -> str:
        """Corrige erros comuns em emails"""
        if not isinstance(email, str):
            return email
        
        # Remover espaços
        email = email.strip()
        
        # Corrigir domínios comuns
        common_fixes = {
            '@gmail': '@gmail.com',
            '@hotmail': '@hotmail.com',
            '@yahoo': '@yahoo.com',
            '@outlook': '@outlook.com',
            '.co': '.com'
        }
        
        for wrong, correct in common_fixes.items():
            if wrong in email and correct not in email:
                email = email.replace(wrong, correct)
        
        # Verificar se ficou válido
        if self.email_pattern.match(email):
            return email
        
        return email  # Retorna original se não conseguiu corrigir
    
    def _correct_phones(self, df: pd.DataFrame, dataset: str) -> pd.DataFrame:
        """Corrige telefones inválidos"""
        if 'telefone' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            phone = str(row['telefone'])
            
            if pd.isna(row['telefone']) or phone == 'nan':
                continue
            
            # Limpar telefone (remover caracteres especiais)
            clean_phone = re.sub(r'[^\d]', '', phone)
            
            # Tentar corrigir formato
            corrected_phone = self._fix_phone_format(clean_phone)
            
            if corrected_phone != phone:
                df_corrected.at[idx, 'telefone'] = corrected_phone
                self._log_correction(dataset, row.get('id_cliente', idx), 'telefone', 
                                   phone, corrected_phone, "PHONE_CORRECTION")
        
        return df_corrected
    
    def _fix_phone_format(self, phone: str) -> str:
        """Corrige formato de telefone"""
        if not phone.isdigit():
            return phone
        
        # Se tem menos de 11 dígitos, tentar adicionar 9 no início do número
        if len(phone) == 10 and phone[2] not in ['9']:
            phone = phone[:2] + '9' + phone[2:]
        
        # Se tem 11 dígitos e formato válido
        if len(phone) == 11 and self.phone_pattern.match(phone):
            return phone
        
        return phone  # Retorna original se não conseguiu corrigir
    
    def _standardize_states(self, df: pd.DataFrame, dataset: str) -> pd.DataFrame:
        """Padroniza códigos de estado"""
        if 'estado' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            state = str(row['estado']).upper().strip()
            
            if state in self.valid_states:
                continue
            
            # Tentar encontrar estado similar
            best_match = self._find_best_match(state, self.valid_states)
            
            if best_match and best_match != state:
                df_corrected.at[idx, 'estado'] = best_match
                self._log_correction(dataset, row.get('id_cliente', idx), 'estado', 
                                   state, best_match, "STATE_STANDARDIZATION")
        
        return df_corrected
    
    def _fill_missing_cliente_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preenche dados ausentes de clientes usando regras de negócio"""
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            # Preencher nome vazio com base no email
            if pd.isna(row['nome']) or str(row['nome']).strip() == '':
                if pd.notna(row['email']):
                    name_from_email = str(row['email']).split('@')[0].replace('.', ' ').title()
                    df_corrected.at[idx, 'nome'] = name_from_email
                    self._log_correction("clientes", row.get('id_cliente', idx), 'nome', 
                                       'NULL', name_from_email, "NAME_INFERENCE")
        
        return df_corrected
    
    def _correct_negative_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige preços negativos"""
        if 'preco' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if row['preco'] < 0:
                # Converter para positivo
                corrected_price = abs(row['preco'])
                df_corrected.at[idx, 'preco'] = corrected_price
                self._log_correction("produtos", row.get('id_produto', idx), 'preco', 
                                   row['preco'], corrected_price, "NEGATIVE_TO_POSITIVE")
        
        return df_corrected
    
    def _auto_categorize_products(self, df: pd.DataFrame) -> pd.DataFrame:
        """Categoriza automaticamente produtos sem categoria"""
        if 'categoria' not in df.columns or 'nome_produto' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        # Palavras-chave para categorização
        category_keywords = {
            "Eletrônicos": ["smartphone", "celular", "tablet", "tv", "televisão", "som", "fone"],
            "Informática": ["notebook", "computador", "mouse", "teclado", "monitor", "impressora"],
            "Casa": ["mesa", "cadeira", "sofá", "cama", "armário", "decoração"],
            "Moda": ["camisa", "calça", "vestido", "sapato", "tênis", "bolsa"],
            "Esportes": ["bola", "raquete", "bicicleta", "academia", "fitness"],
            "Livros": ["livro", "revista", "manual", "guia"],
            "Beleza": ["perfume", "maquiagem", "creme", "shampoo"],
            "Automotivo": ["pneu", "óleo", "bateria", "peça"],
            "Jardim": ["planta", "vaso", "terra", "adubo"],
            "Brinquedos": ["boneca", "carrinho", "jogo", "puzzle"]
        }
        
        for idx, row in df_corrected.iterrows():
            if pd.isna(row['categoria']) or str(row['categoria']).strip() == '':
                product_name = str(row['nome_produto']).lower()
                
                # Buscar categoria baseada em palavras-chave
                for category, keywords in category_keywords.items():
                    if any(keyword in product_name for keyword in keywords):
                        df_corrected.at[idx, 'categoria'] = category
                        self._log_correction("produtos", row.get('id_produto', idx), 'categoria', 
                                           'NULL', category, "AUTO_CATEGORIZATION")
                        break
                else:
                    # Se não encontrou, usar categoria padrão
                    df_corrected.at[idx, 'categoria'] = "Outros"
                    self._log_correction("produtos", row.get('id_produto', idx), 'categoria', 
                                       'NULL', "Outros", "DEFAULT_CATEGORIZATION")
        
        return df_corrected
    
    def _correct_invalid_quantities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige quantidades inválidas (negativas ou zero)"""
        if 'quantidade' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if row['quantidade'] <= 0:
                # Definir quantidade padrão como 1
                df_corrected.at[idx, 'quantidade'] = 1
                self._log_correction("vendas", row.get('id_venda', idx), 'quantidade', 
                                   row['quantidade'], 1, "INVALID_QUANTITY_CORRECTION")
        
        return df_corrected
    
    def _correct_total_calculation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige cálculo do valor total"""
        if not all(col in df.columns for col in ['quantidade', 'valor_unitario', 'valor_total']):
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            expected_total = row['quantidade'] * row['valor_unitario']
            
            if abs(row['valor_total'] - expected_total) > 0.01:  # Tolerância de 1 centavo
                df_corrected.at[idx, 'valor_total'] = expected_total
                self._log_correction("vendas", row.get('id_venda', idx), 'valor_total', 
                                   row['valor_total'], expected_total, "CALCULATION_CORRECTION")
        
        return df_corrected
    
    def _correct_orphan_references(self, df_vendas: pd.DataFrame, 
                                 df_clientes: pd.DataFrame, df_produtos: pd.DataFrame) -> pd.DataFrame:
        """Corrige referências órfãs removendo registros inválidos"""
        df_corrected = df_vendas.copy()
        
        valid_clientes = set(df_clientes['id_cliente'].unique())
        valid_produtos = set(df_produtos['id_produto'].unique())
        
        # Marcar registros para remoção
        to_remove = []
        
        for idx, row in df_corrected.iterrows():
            if row['id_cliente'] not in valid_clientes:
                to_remove.append(idx)
                self._log_correction("vendas", row.get('id_venda', idx), 'id_cliente', 
                                   row['id_cliente'], 'REMOVED', "ORPHAN_REFERENCE_REMOVAL")
            
            if row['id_produto'] not in valid_produtos:
                to_remove.append(idx)
                self._log_correction("vendas", row.get('id_venda', idx), 'id_produto', 
                                   row['id_produto'], 'REMOVED', "ORPHAN_REFERENCE_REMOVAL")
        
        # Remover registros com referências órfãs
        df_corrected = df_corrected.drop(to_remove)
        
        if to_remove:
            self.logger.info(f"Removidos {len(to_remove)} registros com referências órfãs")
        
        return df_corrected
    
    def _standardize_dates(self, df: pd.DataFrame, dataset: str, date_columns: List[str]) -> pd.DataFrame:
        """Padroniza formato de datas"""
        df_corrected = df.copy()
        
        for col in date_columns:
            if col not in df.columns:
                continue
            
            for idx, row in df_corrected.iterrows():
                if pd.notna(row[col]):
                    try:
                        # Tentar converter para datetime e depois para string padronizada
                        date_obj = pd.to_datetime(row[col])
                        standardized_date = date_obj.strftime('%Y-%m-%d')
                        
                        if str(row[col]) != standardized_date:
                            df_corrected.at[idx, col] = standardized_date
                            self._log_correction(dataset, row.get(f'id_{dataset.rstrip("s")}', idx), 
                                               col, row[col], standardized_date, "DATE_STANDARDIZATION")
                    except:
                        # Se não conseguir converter, manter original
                        pass
        
        return df_corrected
    
    def _find_best_match(self, target: str, options: List[str], threshold: float = 0.6) -> Optional[str]:
        """Encontra a melhor correspondência em uma lista de opções"""
        if not target or not options:
            return None
        
        best_match = None
        best_ratio = 0
        
        for option in options:
            ratio = SequenceMatcher(None, target.upper(), option.upper()).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = option
        
        return best_match
    
    def _standardize_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza categorias usando correspondência fuzzy"""
        if 'categoria' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if pd.notna(row['categoria']):
                category = str(row['categoria']).strip()
                
                if category not in self.valid_categories:
                    best_match = self._find_best_match(category, self.valid_categories)
                    
                    if best_match:
                        df_corrected.at[idx, 'categoria'] = best_match
                        self._log_correction("produtos", row.get('id_produto', idx), 'categoria', 
                                           category, best_match, "CATEGORY_STANDARDIZATION")
        
        return df_corrected
    
    def _correct_negative_stock(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige estoque negativo"""
        if 'estoque' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if row['estoque'] < 0:
                # Definir estoque como 0
                df_corrected.at[idx, 'estoque'] = 0
                self._log_correction("produtos", row.get('id_produto', idx), 'estoque', 
                                   row['estoque'], 0, "NEGATIVE_STOCK_CORRECTION")
        
        return df_corrected
    
    def _standardize_boolean_field(self, df: pd.DataFrame, dataset: str, column: str) -> pd.DataFrame:
        """Padroniza campos booleanos"""
        if column not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            value = str(row[column]).lower().strip()
            
            if value in ['true', '1', 'sim', 'yes', 'ativo']:
                standardized = True
            elif value in ['false', '0', 'não', 'no', 'inativo']:
                standardized = False
            else:
                continue  # Manter valor original se não conseguir interpretar
            
            if row[column] != standardized:
                df_corrected.at[idx, column] = standardized
                self._log_correction(dataset, row.get(f'id_{dataset.rstrip("s")}', idx), 
                                   column, row[column], standardized, "BOOLEAN_STANDARDIZATION")
        
        return df_corrected
    
    def _correct_negative_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige valores negativos em vendas"""
        if 'valor_total' not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if row['valor_total'] < 0:
                # Converter para positivo
                corrected_value = abs(row['valor_total'])
                df_corrected.at[idx, 'valor_total'] = corrected_value
                self._log_correction("vendas", row.get('id_venda', idx), 'valor_total', 
                                   row['valor_total'], corrected_value, "NEGATIVE_VALUE_CORRECTION")
        
        return df_corrected
    
    def _correct_future_dates(self, df: pd.DataFrame, dataset: str, date_column: str) -> pd.DataFrame:
        """Corrige datas futuras"""
        if date_column not in df.columns:
            return df
        
        df_corrected = df.copy()
        today = date.today()
        
        for idx, row in df_corrected.iterrows():
            if pd.notna(row[date_column]):
                try:
                    date_value = pd.to_datetime(row[date_column]).date()
                    
                    if date_value > today:
                        # Definir como hoje
                        corrected_date = today.strftime('%Y-%m-%d')
                        df_corrected.at[idx, date_column] = corrected_date
                        self._log_correction(dataset, row.get(f'id_{dataset.rstrip("s")}', idx), 
                                           date_column, row[date_column], corrected_date, 
                                           "FUTURE_DATE_CORRECTION")
                except:
                    pass
        
        return df_corrected
    
    def _standardize_status(self, df: pd.DataFrame, dataset: str, 
                          status_column: str, valid_statuses: List[str]) -> pd.DataFrame:
        """Padroniza valores de status"""
        if status_column not in df.columns:
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if pd.notna(row[status_column]):
                status = str(row[status_column]).strip()
                
                if status not in valid_statuses:
                    best_match = self._find_best_match(status, valid_statuses)
                    
                    if best_match:
                        df_corrected.at[idx, status_column] = best_match
                        self._log_correction(dataset, row.get(f'id_{dataset.rstrip("s")}', idx), 
                                           status_column, status, best_match, "STATUS_STANDARDIZATION")
        
        return df_corrected
    
    def _fill_missing_transportadora(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preenche transportadoras ausentes"""
        if 'transportadora' not in df.columns:
            return df
        
        df_corrected = df.copy()
        default_transportadora = "Correios"  # Transportadora padrão
        
        for idx, row in df_corrected.iterrows():
            if pd.isna(row['transportadora']) or str(row['transportadora']).strip() == '':
                df_corrected.at[idx, 'transportadora'] = default_transportadora
                self._log_correction("logistica", row.get('id_entrega', idx), 'transportadora', 
                                   'NULL', default_transportadora, "DEFAULT_TRANSPORTADORA")
        
        return df_corrected
    
    def _correct_logistica_orphan_references(self, df_logistica: pd.DataFrame, 
                                           df_vendas: pd.DataFrame) -> pd.DataFrame:
        """Corrige referências órfãs na logística"""
        df_corrected = df_logistica.copy()
        valid_vendas = set(df_vendas['id_venda'].unique())
        
        to_remove = []
        
        for idx, row in df_corrected.iterrows():
            if row['id_venda'] not in valid_vendas:
                to_remove.append(idx)
                self._log_correction("logistica", row.get('id_entrega', idx), 'id_venda', 
                                   row['id_venda'], 'REMOVED', "ORPHAN_REFERENCE_REMOVAL")
        
        df_corrected = df_corrected.drop(to_remove)
        
        if to_remove:
            self.logger.info(f"Removidos {len(to_remove)} registros de logística com referências órfãs")
        
        return df_corrected
    
    def _correct_date_inconsistencies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige inconsistências entre datas de envio e entrega"""
        if not all(col in df.columns for col in ['data_envio', 'data_entrega_real']):
            return df
        
        df_corrected = df.copy()
        
        for idx, row in df_corrected.iterrows():
            if pd.notna(row['data_envio']) and pd.notna(row['data_entrega_real']):
                try:
                    data_envio = pd.to_datetime(row['data_envio'])
                    data_entrega = pd.to_datetime(row['data_entrega_real'])
                    
                    if data_entrega < data_envio:
                        # Corrigir data de entrega para ser igual à data de envio
                        corrected_date = data_envio.strftime('%Y-%m-%d')
                        df_corrected.at[idx, 'data_entrega_real'] = corrected_date
                        self._log_correction("logistica", row.get('id_entrega', idx), 
                                           'data_entrega_real', row['data_entrega_real'], 
                                           corrected_date, "DATE_CONSISTENCY_CORRECTION")
                except:
                    pass
        
        return df_corrected
    
    def _fill_missing_shipping_dates(self, df_logistica: pd.DataFrame, 
                                   df_vendas: pd.DataFrame) -> pd.DataFrame:
        """Preenche datas de envio ausentes baseadas na data da venda"""
        if 'data_envio' not in df_logistica.columns:
            return df_logistica
        
        df_corrected = df_logistica.copy()
        
        # Criar mapeamento de venda para data
        venda_to_date = dict(zip(df_vendas['id_venda'], df_vendas['data_venda']))
        
        for idx, row in df_corrected.iterrows():
            if pd.isna(row['data_envio']) or str(row['data_envio']).strip() == '':
                if row['id_venda'] in venda_to_date:
                    try:
                        # Usar data da venda + 1 dia como data de envio
                        venda_date = pd.to_datetime(venda_to_date[row['id_venda']])
                        envio_date = (venda_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                        
                        df_corrected.at[idx, 'data_envio'] = envio_date
                        self._log_correction("logistica", row.get('id_entrega', idx), 
                                           'data_envio', 'NULL', envio_date, 
                                           "SHIPPING_DATE_INFERENCE")
                    except:
                        pass
        
        return df_corrected
    
    def get_correction_summary(self) -> Dict:
        """Retorna resumo das correções aplicadas"""
        if not self.correction_log:
            return {"total_corrections": 0, "by_type": {}, "by_dataset": {}}
        
        df_log = pd.DataFrame(self.correction_log)
        
        summary = {
            "total_corrections": len(self.correction_log),
            "by_type": df_log['correction_type'].value_counts().to_dict(),
            "by_dataset": df_log['dataset'].value_counts().to_dict(),
            "by_column": df_log.groupby(['dataset', 'column']).size().to_dict()
        }
        
        return summary
    
    def save_correction_log(self, output_path: str):
        """Salva log de correções em arquivo"""
        if self.correction_log:
            df_log = pd.DataFrame(self.correction_log)
            df_log.to_csv(output_path, index=False)
            self.logger.info(f"Log de correções salvo em: {output_path}")

if __name__ == "__main__":
    # Exemplo de uso
    corrector = DataCorrectionEngine()
    
    # Carregar dados (exemplo)
    # df_clientes = pd.read_csv("data/raw/clientes.csv")
    # df_corrected = corrector.correct_clientes(df_clientes)
    
    print("🔧 Sistema de Correção Automática TechCommerce inicializado!")