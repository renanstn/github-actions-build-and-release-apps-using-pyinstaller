# github-actions-build-and-release-apps-using-pyinstaller

Repositório de estudo de uso do github actions, para buildar e criar releases linux e windows de um app python automaticamente.

## Como funciona

Logo nas primeiras linhas do `yml`, definimos que uma nova build deve ser gerada caso haja algum push na branch `main`, **e** caso arquivo python seja alterado.

```yml
on:
  push:
    branches: [ main ]
    paths:
      - '**.py'
```

Logo abaixo, temos as definições dos jobs que buildam o app para linux e windows. Cada job tem basicamente os mesmos passos:

1 - Faz o checkout do código com a action `actions/checkout@v2`
2 - Instala as dependências com um `pip install -r requirements-dev.txt`
3 - Utiliza o [pyinstaller](https://www.pyinstaller.org/#) para transformar nosso app `.py` em um `exe`
4 - Faz o upload do artefato, que no caso é o build gerado, com a action `actions/upload-artifact@v2`

Por último, temos o job `create-release`.

A linha:

```yml
needs: [build-on-windows, build-on-linux]
```

Deixa explícito que o github deve esperar os 2 jobs de build estarem concluídos para que este rode.

- Este job baixa os 2 artefatos gerados pelos respectivos jobs de build em linux e em windows, com a action `actions/download-artifact@v2`
- Em seguida, ele cria uma release com a action `actions/create-release@v1`
- Com a `url` da release "em mãos", ele faz o upload dos 2 artefatos, linux e windows, nessa release, usando a action `actions/upload-release-asset@v1`
