
# projeto-api-dados-sspdf 🐍

  

  

## SETUP DO PROJETO

  

- Python do Sistema Operacional (SO) é uma dependência crítica para o Ubuntu pois ferramentas do SO como o gerenciador de pacotes (apt) e algumas interfaces gráficas dependem do Python que vem instalado no SO (Python 3.13.7)

  

- Modificar, atualizar ou instalar bibliotecas de projeto diretamente neste Python (sudo pip install), gera o risco de quebrar o SO.

  

- Python do SO só deve ser usado para scripts que interagem diretamente com o Ubuntu. Para desenvolvimento de projetos, ele deve ser ignorado.

  

- pyenv é um gerenciador de versões que instala o python em um diretório de usuário tornandp-o completamente isolado do Python do SO.

  

- O que for instalado no pyenv não afeta o python do SO.

  

  

#### Navegar até o diretório que deseja instalar o pyenv

  

  

```cd /Documentos/PosGraduacao/EngSoft```

  

  

#### Instalar o pyenv local

  

  

```pyenv local 3.12.3```

  

  

#### Ativar a venv criada com o Python 3.12.9

  

  

```source venv/bin/activate```

  

  

#### IMPORTAÇÃO DO PROJETO

  

Projeto criado pelo desenvolvedor Pedro Guilherme em: [https://github.com/pedrogmcode/projeto-api-dados-sspdf](https://github.com/pedrogmcode/projeto-api-dados-sspdf)

  

  

#### Navegar até o diretório de nível superior onde você quer guardar o projeto

  

```cd /home/pedro/Documentos/PosGraduacao/EngSoft```

  

  

#### Clonar o repositório (Isso criará a pasta 'projeto-api-dados-sspdf')

  

```git clone https://github.com/pedrogmcode/projeto-api-dados-sspdf```

  

  

#### Entrar no novo diretório do projeto

  

```cd projeto-api-dados-sspdf```

  

  

#### Criar e ativar uma nova venv (com o seu Python 3.12.9)

  

```python3.12 -m venv venv```

  

  

```source venv/bin/activate```

  

  

- O prompt deve mudar para (venv) para indicar que está ativo.

  

  

#### Instalar as bibliotecas

  

```pip install -r requirements.txt```

  

  

#### Atualizar o branch main

  

```git pull origin main```

  

  

#### Criar e mudar para um novo branch (Usar nome descritivo)

  

```git checkout -b chore/atualizar-estrutura-projeto```

  

  

- O terminal confirmará que você está no novo branch.

  

  

## ***INICIAR ETAPAS DO PROJETO***

  

  

### ESTRUTURA DE DIRETÓRIOS

  

A estrutura segue o princípio de separação de responsabilidades, tornando o projeto mais organizado, fácil de manter, de colaborar e de testar.

  

  

```src``` - Código-fonte principal da aplicação. Core do projeto. Local do código de produção, que será usado para rodar a aplicação ou o modelo.

  

  

```src/api``` - Diretório de armazenamento do código que disponibiliza o modelo de ML para o mundo através de uma API web (FastAPI). Serve para que outros sistemas possam enviar dados e receber predições do seu modelo.

  

  

```src/data``` - Manipulação e Processamento de Dados. Diretório de scripts para coleta, limpeza, pré-processamento (engenharia de features) e divisão dos dados (treino, validação, teste). Diretório do código que interage com o dataset cru.

  

  

```src/models``` - Definição e Treinamento de Modelos. Diretório do código que define a arquitetura do seu modelo (ex: classes de redes neurais, funções de ML), o script para o treinamento em si e a avaliação do modelo.

  

  

```tests``` - Testes de Unidade e Integração. Armazena os testes de código. Testes são fundamentais para garantir que cada parte do seu código (src) funcione corretamente.

  

  

```logs``` - Armazena arquivos de logs que registram o que acontece quando o seu código é executado, seja durante o treinamento do modelo (para monitorar o progresso) ou quando a API está rodando (para debugging).

  

  

```artifacts``` - Armazena os produtos gerados pelo seu projeto que não são código-fonte ou dados brutos, mas que são resultados importantes.

  

  

```artifacts/models``` - Subpasta crítica para armazenar os modelos de Machine Learning já treinados e serializados (salvos em formatos como .pkl, .h5, ou SavedModel). Esses são os arquivos que a src/api irá carregar para fazer predições.

  

  

### Executar no Terminal Linux

  

  

```bash

  

mkdir  src

  

mkdir  src/api

  

mkdir  src/data

  

mkdir  src/models

  

mkdir  tests

  

mkdir  logs

  

mkdir  artifacts

  

mkdir  artifacts/models

  

```

  

  

## Arquivos __init__.py

  

- Arquivos ```__init__.py__``` são fundamentais no Python porque transformam um diretório comum em um pacote Python (ou package).

  

- Quando o Python encontra um diretório que contém um arquivo ```__init__.py__```, o trata não apenas como uma pasta, mas como um módulo ou pacote que pode ser importado.

  

  

### Criar arquivos `__init__.py`

  

  

```bash

  

  

# Mac/Linux

  

touch  src/__init__.py

  

touch  src/api/__init__.py

  

touch  src/data/__init__.py

  

touch  src/models/__init__.py

  

touch  tests/__init__.py

  

```

  

  

#### Fim de uma etapa de trabalho na branch

  

```chore/atualizar-estrutura-projeto```

  

  

#### Adicionar todos os novos diretórios e arquivos ao stage do Git

  

```git add .```

  

  

#### Fazer commit com uma mensagem clara sobre a natureza da mudança (chore = tarefa de manutenção)

  

```git commit -m "chore: Adiciona estrutura completa de diretórios (tests, logs, artifacts)"```

  

  

#### Enviar a branch para o repositório remoto

  

  

-  ```-u``` define o upstream e só é necessário na primeira vez)

  

  

```git push -u origin chore/atualizar-estrutura-projeto```

  

  

#### Criar o Pull Request (PR) e fazer o Merge no GitHub

  

  

- Acessar o link do seu repositório: [https://github.com/pedrogmcode/projeto-api-dados-sspdf](https://github.com/pedrogmcode/projeto-api-dados-sspdf)

  

  

- O GitHub geralmente detecta automaticamente o seu novo push e exibe um botão para comparar e criar pull request ```Compare & Pull Request```

  

  

- Clicar no botão para criar um novo PR

  

  

- Conferir se a ```Branch Base``` está definida como ```main``` e o ```Branch Comparativo``` está definido como ```chore/atualizar-estrutura-projeto```.

  

  

- Adicionar uma descrição: *"Estrutura final de diretórios para ML/EngSoft"* e crie o PR.

  

  

- A boa prática indica que um outro desenvolvedor revise e faça o merge (fusão) do PR para a main.

  

  

#### Voltar para a branch main

  

```git checkout main```

  

  

#### Puxar as mudanças para sincronizar sua main local (nova estrutura)

  

```git pull origin main```

  

  

#### Remover a branch de tarefa local, pois ela já foi mesclada (opcional)

  

```git branch -d chore/atualizar-estrutura-projeto```

  

## ***INICIAR NOVA ETAPAPA DO PROJETO***

  

#### Criar e mudar para um novo branch

  

```git checkout -b chore/config-qualidade```

  

#### Criar arquivo pyproject.toml na raiz do projeto

```touch pyproject.toml```

  

- 📄 O que é o Arquivo pyproject.toml?

- O arquivo ```pyproject.toml``` é um padrão moderno no ecossistema Python. Serve como um arquivo de configuração centralizado para diversas ferramentas de Python, substituindo ou complementando arquivos antigos como setup.cfg, flake8.ini, ou mypy.ini.

- Em resumo, ele é a "central de comando" do seu projeto, dizendo a todas as ferramentas instaladas (como Black, Ruff, e Mypy) como elas devem se comportar.

-  **Configurando o Black:** O Black garante que todo o código Python no seu projeto tenha a mesma aparência, aplicando regras de estilo de forma automática.

-  ```[tool.black]``` - Tabela de Configuração: Inicia a seção de configurações para a ferramenta Black

-  ```line-length = 88``` - Tamanho Máximo da Linha: Define que o Black deve quebrar as linhas de código que ultrapassarem 88 caracteres. (88 é o padrão do Black e é um valor considerado bom para legibilidade).

-  ```target-version = ['py312']``` - Versão do Python Alvo: Diz ao Black que o código deve ser formatado usando a sintaxe e as regras do Python 3.12 (a versão da sua venv).

  

-  **Configurando o Ruff:** O Ruff é um linter extremamente rápido. Ele verifica seu código em busca de erros de programação (bugs) e problemas de estilo (pycodestyle), e ainda organiza seus imports.

  

-  ```[tool.ruff]``` - Exclusão de Diretórios: Lista as pastas que o Ruff deve ignorar durante a verificação, pois não contêm código de produção (ex: venv e as pastas de logs e artefatos).

  

-  ```line-length = 88``` - Tamanho Máximo da Linha: O Ruff deve respeitar o mesmo limite de 88 caracteres definido para o Black, garantindo consistência.

  

-  ```select = ["F", "E", "W", "I"]``` - Regras a Habilitar: Ativa grupos específicos de regras de verificação: F (Pyflakes, para bugs), E (Estilo básico, do pycodestyle), W (Warnings, avisos) e I (Organização de Imports).

-  ```ignore = ["E501"]``` - Regras a Ignorar: Desabilita a regra específica E501, que checa o tamanho da linha. Como o Black já cuida da formatação, essa regra é redundante e pode causar conflitos.

  

-  ```exclude = [...]``` - Exclusão de Diretórios: Lista as pastas que o Ruff deve ignorar durante a verificação, pois não contêm código de produção (ex: venv e as pastas de logs e artefatos).

  

-  ```[tool.ruff.per-file-ignores]``` - Tabela para Exceções Específicas: Permite ignorar regras apenas em certos arquivos ou padrões.

  

-  ```"__init__.py" = ["F401"]``` - Exceção de Regra: Ignora a regra F401 (que avisa sobre "imports não utilizados") em todos os arquivos __init__.py. Isso é feito porque esses arquivos geralmente ficam vazios ou contêm apenas imports propositais que o linter não precisa checar.

  

#### Adicionar todos os arquivos modificados ao stage do Git

```git add .```

  

#### Fazer commit com mensagem clara

```git commit -m "chore: Adiciona configuração inicial de Black, Ruff e Mypy em pyproject.toml e adiciona conteúdo ao README.md"```

  

#### Enviar o novo branch para o repositório remoto

```git push -u origin chore/config-qualidade```

#### Executar testes
```git push -u origin chore/config-qualidade```