# ia-base-expert


---

### Neste meu projeto, eu quero criar um ambiente pyenv....  crie os passos a passos, de modo que seja simples de acompanhar e evitar erros.... numere os passos:

-------------------------

Para este projeto, o caminho mais seguro é usar pyenv + pyenv virtualenv com Python 3.11.11. No seu ambiente, isso já está instalado, e essa versão tende a ser mais compatível com notebooks e bibliotecas do que 3.14.3.

-------------------------

1 - Entre na pasta do projeto.

cd /home/wolf/Documentos/desenvolvimento/dsa/treinamentos/fundamentos-linguagem-python-basico-aplicacoes-ia

-------------------------

2 - Confira se o pyenv está funcionando e veja as versões disponíveis.

pyenv --version
pyenv versions

obs: Você já tem 3.11.11 instalada, então não precisa baixar outra agora.

-------------------------

3 - Crie um ambiente virtual do projeto.

pyenv virtualenv 3.11.11 fundamentos-python-ia


atencao:

Se aparecer erro dizendo que o ambiente já existe:

pyenv virtualenv-delete fundamentos-python-ia
pyenv virtualenv 3.11.11 fundamentos-python-ia


-------------------------

4 - Vincule esse ambiente à pasta do projeto.

pyenv local fundamentos-python-ia


observacao:

Isso cria o arquivo .python-version na raiz do projeto.

-------------------------

5 - Ative o ambiente e valide.

pyenv activate fundamentos-python-ia
python --version
which python


observacao:

O python --version deve mostrar 3.11.11

-------------------------

6 - Atualize as ferramentas básicas do pip.

python -m pip install --upgrade pip setuptools wheel

-------------------------

7 - Instale os pacotes mais prováveis para os seus notebooks.

python -m pip install jupyterlab ipykernel pandas numpy matplotlib seaborn scikit-learn


atencao: 
Se for usar também o notebook de petrofísica, adicione:

python -m pip install lasio

python -m pip install welly

-------------------------

8 - Registre o ambiente como kernel do Jupyter.

python -m ipykernel install --user --name fundamentos-python-ia --display-name "Python (fundamentos-python-ia)"

-------------------------

9 - Faça um teste rápido para evitar erro de import depois.

python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('ambiente OK')"


observacao:
Se for usar petrofísica:

python -c "import lasio; print('lasio OK')"

python -c "import lasio; print('welly OK')"

-------------------------

10 - Abra o Jupyter e selecione o kernel certo.

jupyter lab


observacao:
OPCIONAL

Dentro do notebook, escolha o kernel Python (fundamentos-python-ia).

-------------------------

11 - Quando terminar, saia do ambiente.

pyenv deactivate

-------------------------

12 - Para uso diário, basta entrar na pasta do projeto.

cd /home/wolf/Documentos/desenvolvimento/dsa/treinamentos/fundamentos-linguagem-python-basico-aplicacoes-ia
pyenv activate fundamentos-python-ia

-------------------------

OBSERVACAO:

Observação importante: este projeto não tem requirements.txt 
nem pyproject.toml, então hoje os pacotes precisam ser instalados 
manualmente. Se quiser, no próximo passo eu posso criar para você 
um requirements.txt básico e deixar esse projeto mais organizado.

-------------------------

Vou preparar o projeto para isso de forma simples: criar um requirements.txt inicial e, junto, te deixar os comandos corretos para gerar e atualizar esse arquivo com pip freeze

Vou gerar o requirements.txt a partir do ambiente fundamentos-python-ia que já está vinculado ao projeto. Depois eu confirmo o conteúdo e te passo o comando correto, porque a sintaxe certa usa > para redirecionar a saída.

-------------------------

Criei o arquivo requirements.txt com base no ambiente fundamentos-python-ia.

-------------------------

O comando correto é este, com redirecionamento:

pip freeze > requirements.txt

-------------------------

Passo a passo simples para usar daqui em diante:

-------------------------

1 - Entre na pasta do projeto.

cd /home/wolf/Documentos/desenvolvimento/dsa/treinamentos/fundamentos-linguagem-python-basico-aplicacoes-ia

-------------------------

2 - Ative o ambiente do projeto.

pyenv activate fundamentos-python-ia

-------------------------

3 - Instale novos pacotes normalmente quando precisar.

pip install nome-do-pacote

-------------------------

4 - Atualize o arquivo de dependências.

pip freeze > requirements.txt

-------------------------

5 - Confira se o arquivo foi atualizado.

cat requirements.txt

-------------------------

6 - Em outra máquina ou em um ambiente novo, recrie tudo assim:

pyenv virtualenv 3.11.11 fundamentos-python-ia
pyenv local fundamentos-python-ia
pyenv activate fundamentos-python-ia
pip install -r requirements.txt

-------------------------

7 - Quando terminar, desative o ambiente.

pyenv deactivate

-------------------------

---
