# Playlist → NotebookLM — Brave

Aplicativo local que extrai os links individuais de vídeos de uma playlist do YouTube e tenta adicioná-los ao NotebookLM usando o navegador Brave.

> **Importante:** este projeto **não baixa vídeos**.

## ✨ Recursos

- Extrai os links dos vídeos de uma playlist.
- Copia todos os links para a área de transferência.
- Salva os links em `.txt`.
- Abre uma página do NotebookLM no Brave.
- Usa o perfil local do Brave para aproveitar a sessão Google já autenticada.
- Conecta ao Brave por CDP (Chrome DevTools Protocol).
- Não precisa armazenar senha do Google no aplicativo.

## 🖥️ Requisitos

- Linux Mint ou outra distribuição Linux compatível.
- Python 3.
- Brave Browser.
- Uma conta Google com acesso ao NotebookLM.
- Internet.

## 🚀 Instalação

Clone o projeto:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

Crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## ▶️ Executar

```bash
source .venv/bin/activate
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

Você pode abrir o aplicativo no Firefox, Chrome ou outro navegador. O Brave será usado separadamente para a automação do NotebookLM.

## 🦁 Como funciona com o Brave

O Brave normalmente precisa ser iniciado com uma porta de depuração remota para que o Playwright consiga se conectar.

Na primeira automação:

1. Salve qualquer trabalho aberto no Brave.
2. Feche todas as janelas do Brave.
3. No aplicativo, informe o link do NotebookLM.
4. Clique em **Adicionar automaticamente pelo Brave**.
5. O programa inicia o Brave usando o perfil local:
   `~/.config/BraveSoftware/Brave-Browser`
6. O programa se conecta ao Brave pela porta local `9222`.
7. O NotebookLM é aberto usando a sessão desse perfil.

### Por que fechar o Brave?

Uma instância do Brave iniciada normalmente não pode, em geral, receber a porta CDP depois que já foi iniciada. Por isso o aplicativo precisa iniciar o navegador com a opção de depuração desde o começo.

## 🔐 Privacidade e segurança

O aplicativo não deve receber sua senha do Google.

Não publique no GitHub:

- cookies;
- tokens;
- senhas;
- perfis do Brave;
- arquivos `.env` com segredos;
- arquivos de sessão;
- `notebooklm_links.txt` se ele contiver links que você não quer compartilhar.

A porta CDP usada pelo aplicativo é:

```text
127.0.0.1:9222
```

Ela deve permanecer acessível apenas localmente. **Não exponha essa porta à internet.**

## 📁 Estrutura

```text
PlaylistNotebookLM-BRAVE/
├── app.py
├── notebooklm_automacao.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── templates/
    └── index.html
```

## ⚠️ NotebookLM

A interface do NotebookLM pode mudar. A automação usa vários textos/seletores para tentar localizar os controles, mas uma mudança na interface pode exigir atualização do código.

Quando isso acontecer, a página do NotebookLM continuará no Brave para permitir uma operação manual.

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte `LICENSE`.

## 🤝 Contribuições

Pull requests e sugestões são bem-vindos.

Antes de enviar uma contribuição, confirme que nenhum cookie, senha, token ou dado privado foi incluído no commit.
