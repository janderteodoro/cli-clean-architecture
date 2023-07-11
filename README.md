
# CLI-CLEAN-ARCHITECTURE

Este projeto consiste em uma CLI que monta uma base de um microsserviço em **Node.js** já na arquitetura hexagonal:

<img src="docs/CleanArchitecture.jpg" width="300" height="200">

## Como rodar localmente
Trata-se de um projeto em Python, portanto para que você consiga instalar e utilizar essa ferramenta, é necessário que tenha o Python 3 instalado com o virtualenv. Caso não tenha pode encontrar aqui no [site oficial](www.python.org) do Python.<br>
Após instalar siga os seguintes passos:<br>
1. Clone o repositorio -> `https://github.com/janderteodoro/cli-clean-architecture.git`
2. Crie um ambiente virtual -> `python3 -m venv venv`
3. Ative o ambiente virtual ->  `source venv/bin/activate`
4. Instale as dependências -> `pip install -r requirements.txt`
5. Execute o script main.py -> `python3 cli/main.py`

## Casos de uso

### <p style="color: blue;">Linux / MacOS</p>
- Após rodar a CLI. irá se deparar com a seguinte tela:<br><br>
<img src="docs/initial-screen.png" width="500" height="300">


- Então inserimos o nome do nosso projeto
- Após, escolhemos se nosso projeto irá ter o Mongo ou o MySql<br>
<img src="docs/databasechoice.png" width="400" height="150">
- O CLI irá abrir o exporador de arquivos para que escolha a pasta de destino<br><br>
<img src="docs/finder.png" width="300" height="200">

- Após escolher a pasta, voltamos para o terminal onde continuará todo o processo de instalação das libs e etc...<br><br>
<img src="docs/npm.png" wifth="150" height="100">

- Então navegue até o diretório que criou seu projeto e abra ele no vscode com  `code <nome-da-sua-api>`
- Insira o script `start`dentro do **package.json** -> `"start": "node src/bin/www"`, ficando da seguinte forma:<br><br>
<img src="docs/api.png" width="300" height="200">

- Ao executar terá o seguinte resultado, caso ainda não tenha colocado suas envs:<br><br>
<img src="docs/start.png" width="500" height="150">

- Após inserir irá logar apenas `node ./src/bin/www`, ficando da seguinte forma:<br>
<img src="docs/run.png" width="500" height="150">

### <p style="color: green;">Windows</p>
Será bem parecido, a única diferença é que (até o momento) não foi possível colocar a fature de selecionar a pasta, portanto, por padrão, ele cria a o projeto na Área de Trabalho. Então siga os passos acima, ignorando apenas a etapa de seleção da pasta de destino. 
