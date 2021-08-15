# CI Grader
Corretor automático para laboratório de ensino baseado em CI.

Esse repositório deve ser clonado pelo aluno. O repositório do professor não precisa de _template_.

## Variável

Essa variável deve ser definida como `secret` do repositório do estudante:

- **PROF_GITHUB**: Repositório do professor (https://github.com/usuario/repositorio), onde serão fornecidos os executáveis corretores

## Instruções ao estudante

1. Importe esse repositório como um repositório privado
2. Dê permissão de administrador para o professor
3. Para cada lista, faça uma pasta com o nome da lista, como especificado pelo professor
4. Dentro da pasta de uma determinada lista, ponha os exercícios conforme especificado pelo professor
5. A cada modificação que fizer, sua nota aparece na pasta `comments`, na raiz do projeto

## Instruções ao professor

1. Crie um repositório público em branco
2. Para cada lista, faça uma pasta com o nome da lista e forneça esse nome para o aluno criar uma pasta de mesmo nome
3. Dentro da pasta de uma determinada lista, ponha no máximo dois arquivos:
  
    - OPCIONAL: arquivo `due_to.txt` com um `datetime` no formato `YYYY-mm-ddTHH:MM:SS` com a data limite de entrega do trabalho
    - OBRIGATÓRIO: o executável do corretor (será executado no linux como ./<nome do arquivo>). Caso precise compilar o corretor, uma sugestão para `python`:
  
```bash
pyinstaller --onefile arquivo.py
```
    
5. O corretor tem que escrever na saída padrão. A última linha da saída do corretor deve conter um JSON em que as chaves são os nomes dos exercícios e os valores são as notas.
6. O CI vai exceutar todos os corretores referentes aos arquivos editados pelo estudante e a última linha do log do passor `Grader` do CI será um JSON formado por uma lista de tarefas conforme o exemplo abaixo:

```json
[{"scores": {"ex1": 1.0, "ex2": 0, "ex3": 0, "ex4": 0, "ex5": 0, "ex6": 0, "ex7": 0, "ex8": 0, "ex9": 0, "ex10": 0}, "task": "lista01"}]
```

Fornecemos uma sugestão de script usando Google Sheets para planilha de notas em https://github.com/ufscar/CIgrader-utils para baixar os logs, interpretar e atulizar a planilha de notas, tendo o endereço do github dos estudantes.
 
