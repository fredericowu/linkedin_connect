# LinkedIn Connect

Fala galera, fiz esse projeto pra facilitar a entrar em contato com vcs.

# Settings
É importante setar a variável de ambiente LINKEDIN_LOGIN e LINKEDIN_PASSWORD para ele logar com sua conta.
 
LINKEDIN_LOGIN = os.getenv("LINKEDIN_LOGIN", "NO LOGIN FOUND")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "NO PASSWORD FOUND")

```
export LINKEDIN_LOGIN='seu@email.com
export LINKEDIN_PASSWORD='senha_linkedin'
```


# Install
Primeiro instale o Docker, enquanto não dockerizo totalmente o projeto vc precisa ter o python instalado.
```
cd project
python -m venv venv

# no mac ou linux
source venv/bin/activate

# no windows
venv\Scripts\activate.bat

pip install -r requirements.txt 

```
# Run
No diretório `linkedin_connect` digite:
```
docker-compose up
```
Esse comando iniciará o selenium dentro de um container. Depois instale as dependencias:

Rode o projeto com o seguinte comando dentro do diretório `project`:
```
behave
```
