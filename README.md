# Dataset template

Este repositório serve para testar validação online de dados com o pacote Frictionless, para o caso de uso de promoção e progressão em escala dos servidores de carreiras de diferentes órgãos

## Passos para montagem

1. Geração de arquivo no BO com todas as siglas de 
  - carreiras
  - níveis
  - graus
  - símbolos vencimento

2. Atualização do datapackage.yaml, que é o esquema de metadados que contém os valores possíveis listados no item 1 acima. Um script útil de conversão de listagem para o formato `yaml` encontra-se [neste google colab](https://colab.research.google.com/drive/1E9GaVpOFCNzhngA70jXTVVDpbjq6st9h?authuser=0#scrollTo=57fLnvkpcmxu)

- [ ] falta entender por que a formatação da coluna `simbolo` não foi aceita no actions do github, sendo que um linter online validou o arquivo `yaml`

3. Adição de comando de junção de arquivos no script de conversão de excel para csv, removendo cabeçalhos e linhas duplicadas (para o caso de duplicadas, o script preservará as mais recentes)

4. Adicionar comando de remoção de arquivos que já estiverem processados (processo externo com trigger no Power Automate, a cada mês, para Mantis da PRODEMGE)

## Passos para testagem

- [ ] carregar arquivo de algum dos órgãos

- [ ] verificar funcionamento do relatório de validação

- [ ] rodar ETL com remoção de arquivo já copiado para Mantis pelo fluxo do Power Automate
