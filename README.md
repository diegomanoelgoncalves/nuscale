# Projeto de Simulação para Reator NuScale

Este projeto contém uma série de scripts e arquivos de material necessários para a geração e simulação de um reator NuScale utilizando o software de simulação Serpent. O arquivo principal, scrip_nuscale.py, é responsável por gerar o cartão de leitura (input card) para o Serpent, que é utilizado para realizar simulações nucleares.
Estrutura do Projeto
Scripts Principais

    detector.py: Este script é responsável por configurar e gerenciar os detectores utilizados nas simulações para capturar dados de interesse, como fluxo de nêutrons e taxa de captura.

    scrip_nuscale.py: O script principal do projeto, que gera o cartão de leitura para o Serpent. Este cartão de leitura contém todas as definições geométricas, de materiais e de fontes de radiação necessárias para a simulação do reator NuScale.

    isotope_abundances.py: Este script calcula e fornece as abundâncias isotópicas dos materiais que serão utilizados na simulação.

## Arquivos de Material

Estes arquivos são geradores de materiaisi e contêm as definições dos materiais que serão utilizados nas simulações, com suas respectivas composições e propriedades nucleares:

    mat_water.py: Definição da água como material moderador no reator.
    mat_h3bo3.py: Definição do ácido bórico (H3BO3) como veneno nuclear.
    mat_uo2gd.py: Definição do combustível UO2 com adição de Gd2O3 (óxido de gadolínio) para controle de reatividade.
    mat_uo2gd_vary.py: Variante do material UO2 com Gd2O3, com propriedades ajustáveis.
    mat_utho2gd_vary.py: Variante do combustível UThO2 com Gd2O3, com propriedades ajustáveis.
    mat_utho2gd.py: Definição do combustível UThO2 com adição de Gd2O3.
    mat_h3bo3_vary.py: Variante do ácido bórico com propriedades ajustáveis.
    mat_water_vary.py: Variante da água com propriedades ajustáveis.

## Arquivos de Material (Inc)

Estes arquivos são incluídos diretamente no cartão de leitura do Serpent para definir as propriedades dos materiais estruturais e de blindagem do reator:

    mat_inconel625.inc: Definição do material Inconel 625.
    mat_B4C.inc: Definição do material B4C (Carbeto de Boro).
    mat_AIC.inc: Definição do material AIC (Controle de Absorção de Íons).
    mat_zircaloy4.inc: Definição do material Zircaloy-4, usado principalmente para o revestimento do combustível.
    mat_air.inc: Definição do ar utilizado em áreas não submersas do reator.
    mat_inconel718.inc: Definição do material Inconel 718.
    mat_ss304.inc: Definição do aço inoxidável 304 (SS304).
    mat_m5.inc: Definição do material M5, utilizado em componentes do reator.
    mat_helium.inc: Definição do hélio, utilizado como gás inerte no reator.
    mat_ss508.inc: Definição do aço inoxidável 508 (SS508).
    mat_ss304l.inc: Definição do aço inoxidável 304L (SS304L).

## Uso

Para gerar o cartão de leitura do Serpent, execute o script scrip_nuscale.py. Certifique-se de que todos os arquivos de material e scripts auxiliares estejam na mesma pasta do projeto ou que os caminhos para eles estejam corretamente configurados no script.
Exemplo de Execução

bash

python3 scrip_nuscale.py

Este comando irá gerar um arquivo de entrada que pode ser utilizado diretamente no Serpent para iniciar uma simulação.
Requisitos

    Python 3.x
    Serpent (versão compatível para simulação nuclear)

### Contribuição

Contribuições são bem-vindas! Se você tiver melhorias ou sugestões, sinta-se à vontade para abrir um "pull request" ou "issue" no repositório.

Aqui está um exemplo de um arquivo README em português para o projeto que inclui os arquivos mencionados:

---

# Projeto de Simulação para Reator NuScale

Este projeto contém uma série de scripts e arquivos de material necessários para a geração e simulação de um reator NuScale utilizando o software de simulação Serpent. O arquivo principal, `scrip_nuscale.py`, é responsável por gerar o cartão de leitura (`input card`) para o Serpent, que é utilizado para realizar simulações nucleares.

## Estrutura do Projeto

### Scripts Principais

- **`detector.py`**: Este script é responsável por configurar e gerenciar os detectores utilizados nas simulações para capturar dados de interesse, como fluxo de nêutrons e taxa de captura.

- **`scrip_nuscale.py`**: O script principal do projeto, que gera o cartão de leitura para o Serpent. Este cartão de leitura contém todas as definições geométricas, de materiais e de fontes de radiação necessárias para a simulação do reator NuScale.

- **`isotope_abundances.py`**: Este script calcula e fornece as abundâncias isotópicas dos materiais que serão utilizados na simulação.

### Arquivos de Material

Estes arquivos contêm as definições dos materiais que serão utilizados nas simulações, com suas respectivas composições e propriedades nucleares:

- **`mat_water.py`**: Definição da água como material moderador no reator.
- **`mat_h3bo3.py`**: Definição do ácido bórico (H3BO3) como veneno nuclear.
- **`mat_uo2gd.py`**: Definição do combustível UO2 com adição de Gd2O3 (óxido de gadolínio) para controle de reatividade.
- **`mat_uo2gd_vary.py`**: Variante do material UO2 com Gd2O3, com propriedades ajustáveis.
- **`mat_utho2gd_vary.py`**: Variante do combustível UThO2 com Gd2O3, com propriedades ajustáveis.
- **`mat_utho2gd.py`**: Definição do combustível UThO2 com adição de Gd2O3.
- **`mat_h3bo3_vary.py`**: Variante do ácido bórico com propriedades ajustáveis.
- **`mat_water_vary.py`**: Variante da água com propriedades ajustáveis.

### Arquivos de Material (Inc)

Estes arquivos são incluídos diretamente no cartão de leitura do Serpent para definir as propriedades dos materiais estruturais e de blindagem do reator:

- **`mat_inconel625.inc`**: Definição do material Inconel 625.
- **`mat_B4C.inc`**: Definição do material B4C (Carbeto de Boro).
- **`mat_AIC.inc`**: Definição do material AIC (Controle de Absorção de Íons).
- **`mat_zircaloy4.inc`**: Definição do material Zircaloy-4, usado principalmente para o revestimento do combustível.
- **`mat_air.inc`**: Definição do ar utilizado em áreas não submersas do reator.
- **`mat_inconel718.inc`**: Definição do material Inconel 718.
- **`mat_ss304.inc`**: Definição do aço inoxidável 304 (SS304).
- **`mat_m5.inc`**: Definição do material M5, utilizado em componentes do reator.
- **`mat_helium.inc`**: Definição do hélio, utilizado como gás inerte no reator.
- **`mat_ss508.inc`**: Definição do aço inoxidável 508 (SS508).
- **`mat_ss304l.inc`**: Definição do aço inoxidável 304L (SS304L).

## Uso

Para gerar o cartão de leitura do Serpent, execute o script `scrip_nuscale.py`. Certifique-se de que todos os arquivos de material e scripts auxiliares estejam na mesma pasta do projeto ou que os caminhos para eles estejam corretamente configurados no script.

### Exemplo de Execução

```bash
python3 scrip_nuscale.py
```

Este comando irá gerar um arquivo de entrada que pode ser utilizado diretamente no Serpent para iniciar uma simulação.

## Requisitos

- Python 3.x
- Serpent (versão compatível para simulação nuclear)

### Contribuição

Contribuições são bem-vindas! Se você tiver melhorias ou sugestões, sinta-se à vontade para abrir um "pull request" ou "issue" no repositório.

### Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).

---

Este README fornece uma visão geral do projeto, explicando o propósito de cada arquivo e como utilizá-los para gerar simulações com o Serpent.
