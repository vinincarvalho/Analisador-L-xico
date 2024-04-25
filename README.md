
---

# Analisador Léxico

Este é um analisador léxico implementado em Python para a linguagem de programação fictícia "cic". O analisador léxico identifica tokens válidos, como palavras-chave, identificadores, números, operadores, delimitadores e cadeias de caracteres, enquanto reporta erros encontrados no código fonte.

## Funcionalidades Principais

- **Identificação de Tokens**: O analisador léxico identifica e classifica os tokens presentes no código fonte, como palavras-chave (`rotina`, `fim_rotina`, `se`, etc.), identificadores, números inteiros e de ponto flutuante, operadores aritméticos e lógicos, delimitadores e cadeias de caracteres.
  
- **Tratamento de Erros**: Caso o código fonte contenha erros léxicos, como tokens inválidos ou formatação incorreta, o analisador léxico os detecta e reporta, incluindo informações sobre a linha, coluna e tipo de erro encontrado.

- **Visualização de Resultados**: Após a análise léxica, o analisador gera tabelas contendo informações sobre os tokens reconhecidos, a quantidade de vezes que cada token foi utilizado e os erros encontrados no código fonte.

## Uso

Para executar o analisador léxico, siga estes passos:

1. Certifique-se de ter o interpretador Python instalado na sua máquina.
2. Clone este repositório ou baixe o arquivo `analisador_lexico.py`.
3. Execute o arquivo Python `analisador_lexico.py` em um ambiente Python. Certifique-se de ter permissões de leitura para o arquivo de código fonte que deseja analisar.
4. Após a execução, o analisador exibirá as tabelas de tokens reconhecidos, uso de tokens e erros encontrados, juntamente com uma versão do código fonte destacando a localização dos erros.

## Exemplo de Uso

```bash
python analisador_lexico.py
```

## Autor

Este analisador léxico foi desenvolvido por Vinícius Carvalho(https://github.com/vinincarvalho).

--- 
