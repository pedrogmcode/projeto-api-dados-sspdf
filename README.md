# API de Dados SSP-DF 🐍

Esta API de dados SSP-DF possibilita o acesso e objetanção de dados e métricas da base de dados de formato .csv obtida no site da Secretaria de Estado de Segurança Pública - SSP/DF: https://www.agenciabrasilia.df.gov.br/web/ssp/dados-por-regiao-administrativa#DF 

Esas api, por meio de seus enpoints:
* Fornece os códigos e nomes das Regiões Administrativas do DF
* Fornece os códigos e as Naturezas das Ocorrências Policiais do DF entre 2020 e 2024
* Fornece informações de ocorrências policiais (2020 e 2024) por Natureza da Ocorrência, Mẽs e Região Administrativa do Distrito Federal.
* Fornece a Média Histórica (2020 a 2024) das quantidades de ocorrências policiais para cada Mês, Região Administrativa e Natureza da Ocorrência.

  

## Como Executar

  

```bash

pip  install  -r  requirements.txt

uvicorn  src.api.main:app  --reload

```

  

Acesse: http://localhost:8000/docs

  

## Endpoints

  

### GET / Natureza da Ocorrência

  

http://localhost:8000/natureza/4

  

```json

/natureza/4'

```

  

**Resposta:**

```json

{

"cod_natureza": 4,

"natureza": "ROUBO EM COLETIVO"

}

```

### Regra de Negócio

Selecionando um código de Natureza de ocorrência, é retornado o nome do crime, isto é, a natureza.

  

### GET / Ocorrências Natureza

  

http://localhost:8000/ocorrencias_nomes?id_ra=1&ano=2024&mes=12'

  

```json

/ocorrencias_nomes?id_ra=1&ano=2024&mes=12'

```

  

**Resposta:**

```json

{

"ANO": 2024,

"COD_NATUREZA": 7,

"ID_RA": 14,

"MES": 6,

"Natureza": "HOMICÍDIO",

"QUANTIDADE": 15,

"RegiaoAdministrativa": "PLANO PILOTO"

}

```

  

### GET / Ocorrências Média

  

http://localhost:8000/ocorrencias_media?id_ra=14&ano=2024&mes=6&cod_natureza=7'

  

```json

/ocorrencias_media?id_ra=14&ano=2024&mes=6&cod_natureza=7'

```

  

**Resposta:**

```json

{

"MES": 6,

"ANO": 2024,

"Natureza": "HOMICÍDIO",

"RegiaoAdministrativa": "PLANO PILOTO",

"Quantidade_Atual": 15,

"Media_Historica_Mes": 12.55,

"ID_RA": 14,

"COD_NATUREZA": 7

}

```

  

### Cálculo:

Se a base de dados tem 5 anos (de $2020$ a $2024$) com registros para a ocorrência "Roubo a Transeunte" em "Gama" no mês de Janeiro:$$\bar{Q}_{\text{Janeiro, Gama, Roubo}} = \frac{Q_{1, \text{Gama}, \text{Roubo}, 2020} + Q_{1, \text{Gama}, \text{Roubo}, 2021} + Q_{1, \text{Gama}, \text{Roubo}, 2022} + Q_{1, \text{Gama}, \text{Roubo}, 2023} + Q_{1, \text{Gama}, \text{Roubo}, 2024}}{5}$$

  

### Regra de Negócio

  

#### RESUMO:

MÉDIA HISTÓRICA = Média da QUANTIDADE DE OCORRÊNCIAS para cada NATUREZA DE OCORRÊNCIA, MÊS e REGIÃO ADMINISTRATIVA, todos fixos, considerando todos os ANOS disponíveis.

  

#### EXPLICAÇÃO:

Considerando $Q_{m, a}$ a Quantidade de ocorrências para um Mês ($m$) e Ano ($a$) específicos.

  

O Mês de Análise ($M$), a Região Administrativa ($R$), e o Código de Natureza ($N$) são fixos.

  

A Média Histórica ($\bar{Q}_{M, R, N}$) é a média da Quantidade para todas as ocorrências que compartilham o Mês ($M$), a Região Administrativa ($R$), e o Código de Natureza ($N$), independentemente do ano ($a \in  \text{Anos Disponíveis}$).

  

$$\bar{Q}_{M, R, N} = \frac{1}{\sum_{a} I} \sum_{a} Q_{M, R, N, a}$$

  

Onde: $Q_{M, R, N, a}$:

Quantidade de ocorrências para o Mês $M$, Região $R$, Natureza $N$ no Ano $a$.

  

$\sum_{a}$: Somatória sobre todos os anos ($a$) disponíveis nos dados que satisfazem a condição de

$M$, $R$ e $N$.

$\sum_{a} I$: Contagem do número de meses/anos ($I$) que satisfazem a condição (ou seja, o número total de anos na base de dados que possuem registro para o $M$, $R$ e $N$ especificados).

  

## Testes


```bash

## Autores

* Micael Macedo Pereira da Trindade
* Pedro Henrique de Magalhães Casimiro
* Daniel Barrozo Lima
* Pedro Guilherme Feitoza Melo

pytest src/api/tests/ -v

```
