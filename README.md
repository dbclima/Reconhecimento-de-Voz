# Reconhecimento-de-Voz
Repositório para o trabalho de reconhecimento de voz

## Set Up
É necessária a instalação de algumas bibliotecas, utilizando:
```
pip install -r requirements.txt
```

## Utils
Arquivos que contém funcionalidades que podem ser aproveitadas no projeto da disciplina

### `gravar.py`
Arquivo que grava audios de 3 segundos em pasta outputs com o nome equivalente ao timestamp.

### `reproduzir.py`
Arquivo que reproduz arquivos .wav no computador.

### `tempo_real.py`
Arquivo que exibe sinal recebido em tempo real

### `plot_tempo_real.py`
Arquivo que exibe plot dinâmico

## Interface
O arquivo `interface.py` contém uma interface simples que realiza gravação e reprodução de arquivos `.wav`, utilizado por diversas bibliotecas para codificação de audio em tensors utilizando PCM (caso do `TensorFlow`).

