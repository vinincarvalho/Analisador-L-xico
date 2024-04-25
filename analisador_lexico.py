import re
import tabulate
from collections import Counter

tokens = [] # Lista para armazenar os tokens reconhecidos
errors = [] # Lista para armazenar os erros encontrados

# Dicionário com os estados de aceitação e seus respectivos tokens
# Esses estados de aceitação são aqueles que não possuem transição direta para eles
final_states_indirect = {
    59: "TK_INT", 60: "TK_INT", 61: "TK_INT", 62: "TK_FLOAT", 64: "TK_COMENT_LINHA", 66: "TK_MENOR_OU_IGUAL", 65: "TK_MENOR",
    63: "TK_ID", 67: "TK_MAIOR", 58: "TK_ROTINA", 100: "TK_FIM_ROTINA", 101: "TK_SE", 102: "TK_SENAO", 103: "TK_IMPRIMA",
    104: "TK_LEIA", 105: "TK_PARA", 106: "TK_ENQUANTO", 68: "TK_END"
}

# Dicionário com os estados de aceitação e seus respectivos tokens
# Esses estados de aceitação são aqueles que possuem transição direta para eles
final_states_direct = {
    2: "TK_SOMA", 10: "TK_SUB", 11: "TK_MULTI", 12: "TK_RESTO", 25: "TK_AND", 54: "TK_OR", 52: "TK_NEGACAO", 29: "TK_DELIMITADOR_ABERTURA",
    53: "TK_DELIMITADOR_FECHAMENTO", 55: "TK_DELIMITADOR", 20: "TK_DATA", 46: "TK_COMENT_BLOCO", 47: "TK_ATRIBUICAO",
    33: "TK_DIFERENTES", 49: "TK_COMPARACAO", 51: "TK_MAIOR_OU_IGUAL", 32: "TK_CADEIA", 49: "TK_COMPARACAO"
}

# Dicionário com as palavras reservados e estados para identificálos
reserved_wors = {
    'rotina': 58, 'fim_rotina': 100, 'se': 101, 'senao': 102, 'imprima': 103, 'leia': 104, 'para': 105, 'enquanto': 106
    }

# Regex para saber se um caractere é um número
def regex_number(character):
    pattern = r'\d'
    return re.match(pattern, character) is not None

# Regex para saber se um caractere é uma letra maiúscula
def regex_uppercase_letter(character):
    pattern = r'[A-Z]'
    return re.match(pattern, character) is not None

# Regex para saber se um caractere é uma letra minúscula
def regex_lowercase_letter(character):
    pattern = r'[a-z]'
    return re.match(pattern, character) is not None

# Regex para saber se um caractere é um hexadecimal
def regex_address(character):
    pattern = r'[A-F]'
    return re.match(pattern, character) is not None

# Regex para saber se um caractere é qualquer caractere exceto o \n
def regex_any_character(character):
    pattern = r'[^"\n]'
    return re.match(pattern, character) is not None

# Função para salvar um token válido na lista de tokens
def save_tokens(token, lexeme, line, column):
    global tokens
    tokens.append({"TOKEN": token, "LEXEMA": lexeme.strip(), "LINHA": line, "COLUNA": column})

# Função para salvar um erro encontrado na lista de erros
def save_errors(line, column, error_msg):
    global errors
    errors.append({"LINHA": line, "COLUNA": column, "ERRO": error_msg})

# Função para criar um tabela com os tokens aceitos
def save_table(tokens):
    table = [[token["LINHA"], token["COLUNA"], token["TOKEN"], token["LEXEMA"]] for token in tokens]
    return tabulate.tabulate(table, headers=["LIN", "COL", "TOKEN", "LEXEMA"], tablefmt="grid")

# Função para criar tabela com os erros encontrados
def errors_table(errors):
    table = [[error["LINHA"], error["COLUNA"], error["ERRO"]] for error in errors]
    return tabulate.tabulate(table, headers=["LIN", "COL", "ERRO"], tablefmt="grid")

# Função para criar tabela com a quantidade de uso de cada token
def token_usage_table(tokens):
    token_counts = Counter(token['TOKEN'] for token in tokens)
    table = [[token, count] for token, count in token_counts.items()]
    return tabulate.tabulate(table, headers=["TOKEN", "Quantidade"], tablefmt="grid")

# Função principal de análise léxica
# Percorre o arquivo caractere por caractere, atualizando os estados do autômato
def get_token(file):
    lexeme = ''
    column = 1
    line = 1
    state = 0
    position = 0

    while position < len(file):
        character = file[position]

        if state == 0:
            if regex_number(character):
                state = 3
            elif regex_address(character):
                state = 26
            elif character == '"':
                state = 30
            elif character == '+':
                state = 2
            elif character == '-':
                state = 10
            elif character == '*':
                state = 11
            elif character == '%':
                state = 12
            elif character == '&':
                state = 25
            elif character == '|':
                state = 54
            elif character == '~':
                state = 52
            elif character == '(':
                state = 29
            elif character == ')':
                state = 53
            elif character == ':':
                state = 55
            elif character == '~':
                state = 52
            elif regex_lowercase_letter(character):
                state = 56
            elif character == '>':
                state = 50
            elif character == '=':
                state = 48
            elif character == '<':
                state = 40
            elif character == '#':
                state = 38
            elif character == '.':
                state = 6
        elif state == 3:
            if regex_number(character):
                state = 4
            elif character == 'x':
                state = 27
            elif character == '.':
                state = 7
            elif regex_number(character) == False and character != 'x' and character != '.':
                state = 59
        elif state == 4:
            if regex_number(character) == False and character != '/' and character != '_' and character != '.':
                state = 60
            elif character == '/':
                state = 13
            elif character == '_':
                state = 21
            elif regex_number(character):
                state = 5
            elif character == '.':
                 state = 7
        elif state == 13:
            if regex_number(character):
                state = 14
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 14:
            if regex_number(character):
                state = 15
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 15:
            if character == '/':
                state = 16
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 16:
            if regex_number(character):
                state = 17
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 17:
            if regex_number(character):
                state = 18
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 18:
            if regex_number(character):
                state = 19
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 19:
            if regex_number(character):
                state = 20
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 21:
            if regex_number(character):
                state = 22
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 22:
            if regex_number(character):
                state = 23
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 23:
            if character == '_':
                state = 24
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 24:
            if regex_number(character):
                state = 17
            else:
                save_errors(line, column, "Data mal formatada")
                state = 0
                lexeme = ''
        elif state == 5:
            if regex_number(character) == False and character != '.':
                state = 61
            elif regex_number(character):
                state = 1
            elif character == '.':
                state = 7
        elif state == 1:
            if regex_number(character):
                state = 1
            elif regex_number(character) == False:
                state = 61
        elif state == 7:
            if regex_number(character):
                state = 7
            elif character == 'e':
                state = 8
            elif character != 'e':
                state = 62
            else:
                save_errors(line, column-1, "Erro de float")
                state = 0
                lexeme = ''
        elif state == 8:
            if regex_number(character):
                state = 8
            elif character == '-':
                state = 9
            elif regex_number(character) == False and character != '-':
                state = 62
        elif state == 9:
            if regex_number(character):
                state = 9
            elif regex_number(character) == False:
                state = 62
            else:
                save_errors(line, column-1, "Erro de float")
                state = 0
                lexeme = ''
        elif state == 6:
            if regex_number(character):
                state = 7
            else:
                save_errors(line, column-1, "Erro de float")
                state = 0
                lexeme = ''
        elif state == 26:
            if character == 'x':
                state = 27
            else:
                save_errors(line, column-1, "Formato de endereço inválido")
        elif state == 27:
            if regex_address(character) or regex_number(character):
                state = 28
            else:
                save_errors(line, column-1, "Formato de endereço inválido")
        elif state == 28:
            if regex_address(character) or regex_number(character):
                state = 28
            elif regex_address(character) == False and regex_number(character) == False:
                state = 68
        elif state == 30:
            if character == '"':
                state = 32
            elif regex_any_character(character):
                state = 31
            else:
                save_errors(line, column-1, "Cadeia incorreta")
                state = 0
                lexeme = ''
        elif state == 31:
            if character == '"':
                state = 32
            elif regex_any_character(character):
                state = 31
            else:
                save_errors(line, column-1, "Cadeia não fechada")
                state = 0
                lexeme = ''
        elif state == 56:
            if regex_lowercase_letter(character):
                state = 57
            elif regex_uppercase_letter(character):
                state = 35
            else:
                save_errors(line, column-1, "Identificador ou palavra reservada")
                state = 0
                lexeme = ''
        elif state == 57:
            if regex_lowercase_letter(character):
                state = 57
            elif character == '_':
                state = 69
            elif regex_lowercase_letter(character) == False:
                state = 58
            else:
                save_errors(line, column-1, "Palavra reservada")
                state = 0
                lexeme = ''
        elif state == 69:
            if regex_lowercase_letter(character):
                state = 69
            elif regex_lowercase_letter(character) == False:
                state = 58
            else:
                save_errors(line, column-1, "Palavra reservada")
                state = 0
                lexeme = ''
        elif state == 35:
            if regex_lowercase_letter(character):
                state = 36
            else:
                state = 63
        elif state == 36:
            if regex_uppercase_letter(character):
                state = 35
            else:
                state = 63
        elif state == 50:
            if character != '=':
                state = 67
            elif character == '=':
                state = 51
        elif state == 48:
            if character == '=':
                state = 49
            else:
                save_errors(line, column, "Erro ==")
        elif state == 40:
            if character != '>' and character != '<' and character != '=':
                state = 65
            elif character == '>':
                state = 33
            elif character == '=':
                state = 37
            elif character == '<':
                state = 41
            else:
                save_errors(line, column, "Erro ao abrir comentário")
        elif state == 37:
            if character != '=':
                state = 66
            elif character == '=':
                state = 47
        elif state == 41:
            if character == '<':
                state = 42
            else:
                save_errors(line, column, "Erro ao fechar comentário")
        elif state == 42:
            if regex_lowercase_letter(character) or regex_number(character) or regex_uppercase_letter(character):
                state = 42
            elif character == '>':
                state = 43
            elif position == len(file) - 1:
                save_errors(line, column, "Erro ao fechar comentário")
                state = 0
                lexeme = ''
        elif state == 43:
            if regex_lowercase_letter(character) or regex_number(character) or regex_uppercase_letter(character):
                state = 43
            elif character == '>':
                state = 44
            else:
                state = 42
        elif state == 44:
            if character == '>':
                state = 46
        elif state == 38:
            if (regex_lowercase_letter(character) or regex_number(character) or regex_uppercase_letter(character)) and character != '\n':
                state = 39
            elif character == '\n':
                state = 64
        elif state == 39:
            if (regex_lowercase_letter(character) or regex_number(character) or regex_uppercase_letter(character)) and character != '\n':
                state = 39
            elif character == '\n':
                state = 64

        if state == 58:
            if lexeme.rstrip('\n') in reserved_wors:
                state = reserved_wors.get(lexeme.rstrip('\n'))
            else:
                save_errors(line, column-1, "Palavra reservada não encontrada")
                state = 0
                lexeme = ''
        if state in final_states_indirect:
            save_tokens(final_states_indirect.get(state), lexeme, line, column-1)
            state = 0
            lexeme = ''
        elif state in final_states_direct:
            lexeme += character
            save_tokens(final_states_direct.get(state), lexeme, line, column)
            state = 0
            lexeme = ''
            position += 1
            column += 1
        elif character == '\n':
            position += 1
            column = 1
            line += 1
        elif character == ',' or character == ' ':
            position += 1
            column += 1
        elif state == 0:
            if regex_number(character) == False and character != '"':
                position += 1
        else:
            lexeme += character
            position += 1
            column += 1

# Função para retornar os erros existentes em uma certa linha
def verificar_erro(lista_erros, num_linha):
    return [erro for erro in lista_erros if erro['LINHA'] == num_linha]

# Função pra printar as linhas do arquivo mostrando o local dos erros
def print_errors(archive_name, errors):
    try:
        with open(archive_name, 'r') as arquivo:
            linhas = arquivo.readlines()

            for num_linha, linha in enumerate(linhas, start=1):
                print(f"[{num_linha}] {linha.rstrip()}")

                lista_erros = verificar_erro(errors, num_linha)
                if lista_erros:
                    for erro in lista_erros:
                        coluna = erro["COLUNA"]
                        print('-' * (coluna + 3) + '^')
                    for erro in lista_erros:
                        coluna = erro["COLUNA"]
                        linha = erro["LINHA"]
                        mensagem = erro["ERRO"]
                        print(f'Erro linha {linha} coluna {coluna}: {mensagem}')

    except FileNotFoundError:
        print(f"O arquivo '{archive_name}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função main que coordena a execução do analisador léxico
def main():
    global tokens, errors
    archive_name = 'Ex-02-incorreto.cic'

    file = open(archive_name, 'r')
    get_token(file.read() + '\n')

    token_table = save_table(tokens)
    usage_table = token_usage_table(tokens)
    error_table = errors_table(errors)

    print("Tabela de Tokens:\n", token_table)
    print("\nTabela de Uso de Tokens:\n", usage_table)
    print("\nTabela de erros:\n", error_table)
    if errors:
        print("\nCódigo com erros:\n")
        print_errors(archive_name, errors)
    
main()
