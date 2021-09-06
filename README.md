# github-actions-build-and-release-apps-using-pyinstaller

[![Python](https://img.shields.io/badge/python-%2314354C.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
![GitHub Actions](https://img.shields.io/badge/githubactions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)


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

1. Faz o checkout do código com a action `actions/checkout@v2`
2. Instala as dependências com um `pip install -r requirements-dev.txt`
3. Utiliza o [pyinstaller](https://www.pyinstaller.org/#) para transformar nosso app `.py` em um `exe`
4. Faz o upload do artefato, que no caso é o build gerado, com a action `actions/upload-artifact@v2`

```yml

jobs:
  build-on-windows:
    runs-on: windows-latest

    strategy:
      matrix:
        python-version: [3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt

    - name: Build with pyinstaller
      run: |
        pyinstaller --onefile --noconsole src\\app.py

    - uses: actions/upload-artifact@v2
      with:
        name: app_windows
        path: .\dist\app.exe
```

Por último, temos o job `create-release`.

A linha:

```yml
needs: [build-on-windows, build-on-linux]
```

Deixa explícito que o github deve esperar os 2 jobs de build estarem concluídos para que este rode.

- Este job baixa os 2 artefatos gerados pelos respectivos jobs de build em linux e em windows, com a action `actions/download-artifact@v2`
- Em seguida, ele cria uma release com a action `actions/create-release@v1`
- Com a `url` da release "em mãos", ele faz o upload dos 2 artefatos, linux e windows, nessa release, usando a action `actions/upload-release-asset@v1`

```yml
jobs:
  create-release:
    runs-on: ubuntu-latest
    needs: [build-on-windows, build-on-linux]

    steps:
    - uses: actions/download-artifact@v2
      with:
        path: ./

    - name: Create github release
      id: create_release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.RELEASE_TOKEN }}
      with:
        tag_name: v${{ github.run_number }}
        release_name: Release Version ${{ github.run_number }}
        draft: false
        prerelease: false

    - name: Upload windows artifact to github release
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.RELEASE_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: ./app_windows/app.exe
        asset_name: app_windows.exe
        asset_content_type: application

    - name: Upload linux artifact to github release
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.RELEASE_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: ./app_linux/app
        asset_name: app_linux
        asset_content_type: application

```
