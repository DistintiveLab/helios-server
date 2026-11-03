- [Sistema de votação Helios como serviço de TIC](#sistema-de-votação-helios-como-serviço-de-tic)
  - [Personalizações feitas pelo IFSC no Helios](#personalizações-feitas-pelo-ifsc-no-helios)
- [Guia de instalação e configuração do Helios](#guia-de-instalação-e-configuração-do-helios)
  - [Instalação dos pacotes necessários (Ubuntu 22.04/24.04)](#instalação-dos-pacotes-necessários-ubuntu-22042404)
    - [Softwares necessários](#softwares-necessários)
  - [Preparação do ambiente para instalação do Helios](#preparação-do-ambiente-para-instalação-do-helios)
    - [Configuração do banco de dados PostgreSQL](#configuração-do-banco-de-dados-postgresql)
    - [Compilando arquivos com as traduções para português](#compilando-arquivos-com-as-traduções-para-português)
    - [Configuração dos módulos de autenticação](#configuração-dos-módulos-de-autenticação)
      - [Autenticação em uma base LDAP](#autenticação-em-uma-base-ldap)
      - [Autenticação via Discourse Connect](#autenticação-via-discourse-connect)
    - [Testando a instalação em ambiente de desenvolvimento](#testando-a-instalação-em-ambiente-de-desenvolvimento)
    - [Habilitando usuário com permissão de gestor de eleições](#habilitando-usuário-com-permissão-de-gestor-de-eleições)
  - [Preparando ambiente de produção](#preparando-ambiente-de-produção)
    - [Configuração do nginx (proxy reverso)](#configuração-do-nginx-proxy-reverso)
    - [Celery](#celery)
  - [Configurações Gerais:](#configurações-gerais)
  - [Outras personalizações feitas no Helios](#outras-personalizações-feitas-no-helios)
    - [Habilitar Interface de Administração do Django](#habilitar-interface-de-administração-do-django)
    - [Listar eleições na página inicial do Helios](#listar-eleições-na-página-inicial-do-helios)
    - [Autenticação federada via shibboleth](#autenticação-federada-via-shibboleth)
      - [Configuração da autenticação com o módulo apache shibboleth2](#configuração-da-autenticação-com-o-módulo-apache-shibboleth2)
      - [Habilitando instituições da federação para usarem o serviço Helios](#habilitando-instituições-da-federação-para-usarem-o-serviço-helios)
  - [Usando docker para desenvolvimento](#usando-docker-para-desenvolvimento)
  - [Alguns lembretes finais cruciais para o ambiente de produção](#alguns-lembretes-finais-cruciais-para-o-ambiente-de-produção)
# Sistema de votação Helios como serviço de TIC

O objetivo deste projeto era inicialmente atender a [necessidade N.47 do Plano Diretor de TI (PDTI) de 2013 do Instituto Federal de Santa Catarina (IFSC)](http://dtic.ifsc.edu.br/files/pdti2013-revisao02.pdf). No entanto, logo percebeu-se que outras instituições, especialmente as de ensino, poderiam se beneficiar das melhorias realizadas por nós no projeto original do [Ben Adida](https://github.com/benadida/helios-server). 

Sendo assim, com intuito de contribuir com o público brasileiro, optamos por manter nesse repositório todas as melhorias feitas para que outras instituições possam se beneficiar do trabalho realizado pelo IFSC em cima do projeto original. Ou seja, aquilo que é praxe na comunidade de software livre (compartilhar) e na comunidade acadêmica (referenciar trabalhos de terceiros). Da mesma forma, esperamos receber contribuições dessas instituições para melhorar o código aqui disponibilizado. :punch: 

> **Nota:** Pode-se constatar que de fato esse projeto está beneficiando o público brasileiro. Em 2013, antes desse projeto, o Helios só era usado por 2 instituições de ensino no Brasil e ambas parecem ter usado a versão original e não compartilharam o código. Em 2020 sabemos que a versão modificada pelo IFSC está sendo usada por pelo menos 20 instituições de ensino (Institutos Federais, Universidades Estaduais e Universidades Federais), por órgãos do poder executivo, por organizações e associações de classes. Muitas nos citaram :blush:, mas nem todas :worried:. E recebemos contribuições de uma dessas instituições :clap:.

## Personalizações feitas pelo IFSC no Helios

Esse repositório contém as personalizações feitas pelo IFSC no Helios. Ainda assim, buscará o sincronismo periódico com (sempre que possível e dentro do tempo possível) o projeto original do [Ben Adida](https://github.com/benadida/helios-server).

> **Nota:** este *fork* é mantido atualmente pela [DistintiveLab](https://github.com/DistintiveLab) (serviço [Coletivo](https://vote.coletivo.net.br)), que o executa em produção, conduziu a atualização para Python 3.13 / Django 5.2 (com o gerenciador de pacotes [uv](https://docs.astral.sh/uv/)) e adicionou o login via Discourse Connect.

Personalizações e contribuições que fizemos que estão aqui e que não foram para o *upstream*:
- Tradução da interface para português
- Melhorias em algumas páginas e adequação para serem responsivas
- Criação de manuais para eleitores e para gestores de eleição
- Módulo de autenticação LDAP
- Módulo de autenticação Shibboleth
- Módulo de autenticação via Discourse Connect (um fórum Discourse como provedor de login)
- Ajustes na página inicial e interface de administração para operação do Helios em ambiente Federado (Ex: Federação CAFe)
- Esse próprio arquivo com instruções para instalação do Helios :smile:

Publicamos dois artigos sobre essas personalizações (os PDFs estão disponíveis abaixo):

- CHAVES, S. A., MELLO, E. R. [Adoção de modelo controle acesso baseado em atributos em sistema de votação online para ofertá-lo como um serviço de TIC federado](artigos-publicados/chaves-sbseg15.pdf). In: WGID - Workshop de Gestão de Identidade, 2015, Florianópolis. XV Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais. 
- CHAVES, S. A., MELLO, E. R. [O uso de um sistema de votação on-line para escolha do conselho universitário](artigos-publicados/chaves-sbseg14.pdf) In: WTE - Workshop de Tecnologia Eleitoral, 2014, Belo Horizonte. XIV Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais 

Para saber um pouco mais, acesse http://dtic.ifsc.edu.br/sistemas/sistema-de-votacao-on-line-helios/

# Guia de instalação e configuração do Helios

Neste tutorial são descritos os principais passos para disponibilização do Helios em um servidor com a distribuição Linux Ubuntu (testado nas versões LTS 14.04, 16.04, 18.04, 22.04 e 24.04), embora já tenha sido feita instalação com sucesso no CentOS. 

Para seguir esse tutorial é necessário tenha alguma experiência com administração de sistemas Linux (instalação de pacotes, configuração de serviços, etc.).


## Instalação dos pacotes necessários (Ubuntu 22.04/24.04)

### Softwares necessários

* python 3.13 (e o pacote python3-dev da distribuição)
* nginx
  * atua como *proxy reverso* em produção: TLS, arquivos estáticos e repasse ao gunicorn (ver seção [Configuração do nginx (proxy reverso)](#configuração-do-nginx-proxy-reverso))
* certbot
  * emissão e renovação dos certificados Let's Encrypt usados pelo nginx
* postgresql (12 ou superior) e postgresql-contrib
  * [Aqui tem um bom tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-22-04) de como instalar no Ubuntu 22.04
* redis-server
  * atua como *message broker* do celery (ver seção [Celery](#celery))
* build-essential
* git
* gettext
  * para uso das funcionalidades de compilação de mensagens traduzidas
* [uv](https://docs.astral.sh/uv/) — gerenciador de pacotes Python, instalado por exemplo com:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* libsasl2-dev e libldap2-dev
  * cabeçalhos necessários para compilar o pacote python-ldap (usado pelo módulo de autenticação LDAP)

> Obs.: 
> 1) Para instalação dos pacotes apresentados acima foi necessário editar o arquivo  `/etc/apt/sources.list` e adicionar na seguinte linha a opção `universe`:
>```bash
>deb http://archive.ubuntu.com/ubuntu bionic main universe
>```
> Depois é só fazer um `sudo apt update` e instalar os pacotes apresentados acima com o `sudo apt install`

> 2) Esta versão do Helios utiliza [Python 3.13](https://docs.python.org/3.13/) e [Django 5.2](https://docs.djangoproject.com/en/5.2/), com as dependências gerenciadas pelo [uv](https://docs.astral.sh/uv/) no arquivo `pyproject.toml` (não existe mais `requirements.txt`). O driver PostgreSQL (`psycopg2-binary`) e o `python-ldap` são instalados automaticamente pelo `uv sync`.

## Preparação do ambiente para instalação do Helios

Recomendo que crie um usuário no sistema específico para o helios, por exemplo, usuário `helios`. 

### Configuração do banco de dados PostgreSQL

Editar o arquivo `pg_hba.conf` e inserir a linha:

Logo acima da linha:
```bash
local   all             all         peer
```

inserir a seguinte linha:
```bash
local   all              helios                         md5
```

A configuração acima corrige o seguinte erro:

```bash
Exception Type: 	OperationalError
Exception Value: 	
FATAL:  Peer authentication failed for user "helios"
```


>**Observação:** Com a configuração padrão do postgresql só é possível se conectar nele a partir da máquina em que ele está instalado. Caso você queira se conectar na base com um cliente como o pgAdmin, sem abrir a configuração para conexão a partir de outra máquina, basta utilizar um túnel ssh. Editar `~/.ssh/config` e inserir a entrada abaixo, substituindo os valores em letra maiúscula pelas configurações da sua instalação (e não esquecer que precisa haver uma conexão ssh aberta com o servidor do banco para que a configuração abaixo seja efetiva!):
>
>```bash
>Host NOMEDOHOST
>User NOMEDOUSER
>Hostname ENDERECODOHOST
>Port PORTASSH
>LocalForward PORTALOCAL 127.0.0.1:PORTAREMOTA
>```

Todas as instruções abaixo devem ser executadas com o usuário `helios` e não com o superusuário (root).

Baixe o código fonte desse repositório:
```bash
git clone https://github.com/DistintiveLab/helios-server.git
```

As dependências do projeto são gerenciadas pelo [uv](https://docs.astral.sh/uv/), que cria e mantém automaticamente um ambiente virtual (`.venv`) no diretório do projeto, separando as dependências sem interferir em outros sistemas na mesma máquina.

Dentro do diretório onde o Helios foi baixado, execute o comando:

```bash
uv sync
```

Isso criará o ambiente virtual e instalará os pacotes listados no arquivo `pyproject.toml`, incluindo o `django-auth-ldap` e outros necessários para as personalizações feitas neste *fork* do Helios. Para executar comandos dentro do ambiente use `uv run <comando>`, por exemplo `uv run python manage.py ...` — não é preciso ativar o ambiente manualmente.

> **ATENÇÃO:** apesar de se pretender manter este repositório atualizado com o do [Ben Adida](https://github.com/benadida/helios-server), não necessariamente vai ser simultâneo, então se você utilizar o dele, pode haver versões diferentes de pacotes.

> **Observação:** o pacote `python-ldap` é compilado a partir do código fonte no momento do `uv sync`; se a compilação falhar por falta de cabeçalhos, instale `libsasl2-dev`, `libldap2-dev` e `build-essential` e execute `uv sync` novamente.

A conexão com o banco de dados é configurada por variáveis de ambiente, lidas no `settings.py`. Os valores padrão são os do docker-compose (host `db`, usuário/banco/senha `helios`), portanto numa instalação direta no servidor defina no ambiente (por exemplo no arquivo `.env`; veja o `.env.sample`):

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DB_NAME=helios
DB_USER=helios
DB_PWD=SENHADOHELIOS
```

Alternativamente, a variável `DATABASE_URL` (ex.: `postgres://usuario:senha@localhost:5432/helios`) substitui toda a configuração acima e força o uso de SSL na conexão.

Por fim, você precisará inicializar o esquema no banco de dados (criar as tabelas, etc.). Em ambiente de desenvolvimento isso pode ser feito com o script `reset.sh` (não faça como root), que além das migrações cria um usuário inicial de exemplo:
```bash
./reset.sh
```

> **ATENÇÃO:** o `reset.sh` é destrutivo: ele **apaga e recria** o banco de dados (`dropdb helios` + `createdb helios`) antes de rodar as migrações. Use-o apenas em ambiente de desenvolvimento; numa implantação nova em servidor basta `uv run python manage.py migrate`. Note também que o `dropdb`/`createdb` conectam pelo socket local com o seu usuário de shell, enquanto os comandos Django usam as variáveis de ambiente (`POSTGRES_HOST`, `DB_USER`, etc.).

> **Observação:** Se tiver algum problema ao executar o script acima, provavelmente vai ser relacionado à configuração do PostgreSQL e, nesse caso, o *Google é seu amigo.* Porém, o erro mais comum é que você tenha executado o script como root e o `postgres` acuse que não há um usuário root. Recomendo criar um usuário que não seja root (por exemplo, helios) e usar o mesmo nome para usuário do banco. Ou executar os comandos contidos no script com o usuário adequado do banco.

### Compilando arquivos com as traduções para português

A interface do Helios foi traduzida para o português e assim é necessário que compile os arquivos de tradução, caso queira usar a tradução que fizemos. Execute o seguinte comando a partir do diretório do Helios:
```bash
uv run python manage.py compilemessages -l pt_BR
```

Após a compilação, arquivos `.mo` devem ter sido gerados em `locale/pt_BR/LC_MESSAGES`

> **Observação:** Para alterar alguma tradução é possível utilizar o aplicativo [POEDIT](https://poedit.net), os mesmo editar diretamente os arquivos `django.po` e `djangojs.po` no editor de texto de sua preferência.

Se você adicionou alguma mensagem nova para ser traduzida e gostaria que fossem adicionadas aos arquivos de tradução, execute os comandos abaixo.

1. Para adicionar strings de arquivos python:

```bash
uv run python manage.py makemessages -l pt_BR
```
2. Para adicionar strings de arquivos .js (os que passam pelo engine do Django):

```bash
uv run python manage.py makemessages -d djangojs -l pt_BR --ignore=.venv
```
> **Observação:** Para a coleta de mensagens de arquivos .js, se você tiver criado o diretório do ambiente virtual relativo ao diretório do helios (o `uv` cria o `.venv`), você pode passar o parâmetro `--ignore=.venv` conforme acima, para ignorar esse diretório.

### Configuração dos módulos de autenticação

Você precisará habilitar em `settings.py` os módulos de autenticação que deseja. Por exemplo, poderia usar os módulos de autenticação do projeto original e permitir a autenticação de usuários por meio de contas Google, Facebook ou Twitter. 

Na seção abaixo apresentamos as configurações necessárias para permitir a autenticação de usuários de uma base LDAP. Se não tiver um servidor LDAP e só queira testar o Helios, então talvez possa ser interessante tentar com os outros módulos de autenticação citados acima.

#### Autenticação em uma base LDAP

Habilite o módulo LDAP em `settings.py`:

```bash
AUTH_ENABLED_AUTH_SYSTEMS = get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'ldap').split(",")
```

A documentação da biblioteca utilizada pode ser encontrada em http://pythonhosted.org/django-auth-ldap/example.html. Ela não é muito completa, mas as configurações principais estão no `settings.py` e são: `AUTH_LDAP_SERVER_URI`, `AUTH_LDAP_BIND_PASSWORD`, e `AUTH_LDAP_USER_SEARCH`. 

As opções `AUTH_LDAP_BIND_DN` e `AUTH_LDAP_BIND_PASSWORD` deverão ter um valor configurado se o servidor LDAP exigir autenticação de usuário mesmo que seja para fazer consultas.

> Observação: Você pode testar a conexão usando o próprio teste unitário do app de autenticação. Para tal, edite o arquivo [helios_auth/tests.py](helios_auth/tests.py), altere o usuário (euclid) e senha (password) que estão no teste usando o [servidor de testes LDAP da ForumSys](https://www.forumsys.com/tutorials/integration-how-to/ldap/online-ldap-test-server/) para um usuário e senha válidos no LDAP que você configurou no arquivo [settings.py](settings.py) e execute `uv run python manage.py test helios_auth`

#### Autenticação via Discourse Connect

Este *fork* dispõe de um módulo de autenticação via [Discourse Connect](https://meta.discourse.org/t/discourseconnect-official-single-sign-on-for-discourse-sso/13045) (o antigo SSO do Discourse), que permite usar um fórum Discourse como provedor de login — adicionado para que usuários do fórum da SEPLA (`foro.sepla21.org`) possam se autenticar no Helios.

O protocolo é o padrão do Discourse Connect com assinatura HMAC-SHA256: o Helios gera um *nonce* e redireciona o usuário para `<DISCOURSE_URL>/session/sso_provider`; no retorno, valida a assinatura e o *nonce* da sessão antes de criar o login (implementação em [helios_auth/auth_systems/discourse.py](helios_auth/auth_systems/discourse.py)).

Para habilitá-lo:

1. Inclua `discourse` na lista de sistemas de autenticação habilitados (já consta no padrão do `settings.py`):

```bash
AUTH_ENABLED_AUTH_SYSTEMS = get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'ldap,password,google,facebook,discourse').split(",")
```

2. Configure o provedor pelas variáveis de ambiente (lidas no `settings.py` via `get_from_env`; defina por exemplo no arquivo `.env`, veja o `.env.sample`):

```bash
DISCOURSE_URL=https://seu-forum.exemplo.org
DISCOURSE_SECRET=chave-secreta-compartilhada
```

3. No painel administrativo do Discourse (`/admin/settings`), habilite o provedor **Discourse Connect** (*enable discourse connect provider*) e cadastre em *discourse connect provider secrets* a mesma chave secreta, no formato `endereco-do-seu-helios:chave-secreta` (apenas a chave, sem host, aceita qualquer origem).

> **Observações:**
> - O identificador do usuário no Helios é o `username` do Discourse; o e-mail usado é o cadastrado no fórum.
> - A chave secreta é compartilhada entre o Helios e o Discourse e deve ser mantida sigilosa, pois é ela que assina e valida as mensagens trocadas entre os dois sistemas.
> - As variáveis `DISCOURSE_URL` e `DISCOURSE_SECRET` são lidas do ambiente pelo `settings.py` (via `get_from_env`); o mesmo vale para as demais configurações (banco, email, broker) — prefira usar o arquivo `.env` em vez de editar o `settings.py`.

### Testando a instalação em ambiente de desenvolvimento

Ao executar o script `reset.sh`, você teve que criar um usuário de administração do django. Isso se deve ao fato de aplicação `admin` estar habilitada no arquivo `settings.py` (django.contrib.admin), pois iremos utilizá-la em algumas personalizações feitas para este *fork* do Helios.

>*Observação*: você sempre pode criar um novo usuário para o django admin site executando o comando `uv run python manage.py createsuperuser`

Se tudo estiver correto até aqui, agora você poderá executar o servidor web para desenvolvimento que é provido pelo próprio django. Use esse servidor somente para verificar se a instalação foi feita com sucesso, porém não use-o caso queira colocar o Helios no ambiente de produção.

Execute o seguinte comando:

```bash
uv run python manage.py runserver 0.0.0.0:8000
```

Além disso, você precisa ter o celery rodando, pois algumas tarefas como processamento de arquivo de eleitores e envio de emails dependem dele.

Abra um outro terminal para deixar o [celery](https://docs.celeryq.dev/) em execução (com o `uv` não é necessário ativar ambiente algum; o Redis precisa estar acessível, pois é o *broker* padrão `redis://127.0.0.1:6379`):


```bash
uv run celery --app helios worker -l info
```

> Refrisando, essa parte é importante, pois é o celery responsável pelas tarefas de gravação dos votos, envio de emails, processamento do arquivo de eleitores, etc.


Feito isso, você pode acessar a URL http://endereco-do-seu-servidor-helios e se autenticar com algum usuário presente em sua base LDAP (ou um usuário de algum outro sistema de autenticação que tenha habilitado para o Helios).

Esse usuário não conseguirá criar eleições ainda, mas esse passo é necessário para que seja criada uma entrada para esse usuário na base. No próximo passo, [Habilitando usuário com permissão de criar eleições](#habilitando-usuário-com-permissão-de-criar-eleições),usaremos a aplicação `admin` do django para dar privilégio de gestor de eleição para esse usuário. 

### Habilitando usuário com permissão de gestor de eleições

Acesse a URL http://endereco-do-seu-servidor-helios/admin e se autentique com o usuário e senha de administração (você fez isso quando executou o script `reset.sh`). 

>*Observação*: Se você não lembra qual senha você criou, mas lembra o usuário, então é possível mudar a senha executando o comando `uv run python manage.py changepassword <usuario>`

Na página de administração são apresentados os *apps* habilitados. Localize a opção `Helios_Auth` e clique em *Users*. Na página seguinte, escolha o usuário que você deseja editar (basta clicar somente o login do mesmo). Na página de edição, marque a opção *Admin_p* e salve.

Pronto! O usuário em questão recebeu o papel de **gestor de eleição** e será capaz de criar e gerenciar eleições com o Helios.

> **Atenção**: só será possível dar o privilégio `admin_p` para usuários que se autenticaram previamente na aplicação Helios. Isso se deve à lógica de criação desse login, que é feita durante o login do usuário, caso ainda não exista. 


## Preparando ambiente de produção

Na seção anterior foi usado o servidor web de desenvolvimento provido pelo próprio Django (`uv run python manage.py runserver 0.0.0.0:8000`). No entanto, ele é apenas para desenvolvimento e **não deve** ser usado em um ambiente de produção.

Em produção, recomenda-se o [nginx](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/) atuando como *proxy reverso*: ele termina o TLS, serve os arquivos estáticos diretamente do disco (muito mais rápido do que a aplicação) e repassa o restante das requisições à aplicação Django, que roda sob o [gunicorn](https://docs.gunicorn.org/) escutando apenas em `127.0.0.1:8013`. O gunicorn já é instalado pelo `uv sync`.

### Configuração do nginx (proxy reverso)

Este repositório traz um exemplo funcional e comentado, baseado na configuração em produção de `vote.coletivo.net.br`: o arquivo [nginx.conf.example](nginx.conf.example). Após ajustar nele o domínio, o caminho da instalação e a porta do gunicorn, ative-o com:

```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/helios
sudo ln -s /etc/nginx/sites-available/helios /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

E inicie a aplicação com o gunicorn (mantenha-o sob systemd ou [supervisor](http://supervisord.org/introduction.html); exemplos do supervisor em [docker/supervisor](docker/supervisor/)):

```bash
uv run gunicorn wsgi --workers 3 --bind 127.0.0.1:8013
```

#### Como o nginx serve o Helios

| Prefixo de URL | Servido a partir de | Conteúdo |
| -------------- | ------------------- | -------- |
| `/static/` | `staticfiles/` (gerado por `collectstatic`) | admin do Django e demais assets referenciados por `{% static %}` |
| `/booth/` | `heliosbooth/` | cabine de votação (aplicação JavaScript) |
| `/verifier/` | `heliosverifier/` | verificador de cédulas (aplicação JavaScript) |
| `/media/` | `media/` | assets estáticos do fork (bootstrap, css, js) e uploads |
| `/ajuda/` | `ajuda/` | páginas de ajuda |
| demais URLs | gunicorn em `127.0.0.1:8013` | a aplicação Django |

Como `heliosbooth` e `heliosverifier` são servidos direto do código-fonte pelo nginx, apenas os demais arquivos estáticos (CSS, JavaScript, imagens, incluindo os do módulo `admin` do Django) precisam ser reunidos no diretório `staticfiles` (definido em `STATIC_ROOT`) após cada atualização do código:

```bash
uv run python manage.py collectstatic
```

#### TLS/HTTPS e outros detalhes importantes

- Os certificados do exemplo são os padrão do [Certbot / Let's Encrypt](https://certbot.eff.org/); a renovação automática funciona porque o bloco HTTP responde ao prefixo `/.well-known/acme-challenge/` antes de redirecionar tudo para HTTPS.
- `client_max_body_size 25m` é necessário para o upload do arquivo de eleitores.
- O cabeçalho `X-Forwarded-Proto` informado no bloco `proxy` é o que permite ao Django saber que a conexão original era HTTPS: com `SSL=1` no `.env`, o `SECURE_PROXY_SSL_HEADER` (ver [`settings.py`](settings.py)) o utiliza para forçar HTTPS e marcar os cookies como seguros.

> **Nota (legado):** a configuração histórica com Apache + mod_wsgi continua disponível como referência em [helios.conf.exemplo](helios.conf.exemplo) e [docker/apache/helios-ssl.conf](docker/apache/helios-ssl.conf), mas o nginx é a configuração recomendada e documentada para produção.

### Celery

Lembrando mais uma vez que o [celery](https://docs.celeryq.dev/) precisa estar em execução, pois ele é o enfileirador de tarefas, como a tarefa de envio de emails e a tarefa de registro de votos.

Esta versão utiliza o celery 5, que suporta o Django [*out of the box*](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html), com o [Redis](https://redis.io/) como *message broker* (padrão `redis://127.0.0.1:6379`, configurável pela variável `CELERY_BROKER_URL`). O resultado das tarefas é guardado no próprio banco do Django através do app `django_celery_results` (junto com o `django_celery_beat`, ambos em `INSTALLED_APPS`).

Em produção é interessante rodar o celery com múltiplos processos, para acelerar por exemplo envio de emails. Na prática, 5 processos em paralelo se mostrou suficiente:

```bash
uv run celery -A helios worker -l info --concurrency=5
```


Para que o resultado da execução das tarefas seja guardado no backend, adicionou-se o app `django_celery_results` e o `django_celery_beat` em INSTALLED_APPS.

O celery beat, agendador de tarefas periódicas, como limpar a tabela de resultados de execução de tarefas de tempos em tempos (o que pode crescer bastante), pode ser executado pelo comando celery, mas passando o parâmetro *beat* ao invés de *worker*:

`uv run celery -A helios beat -l info`

No arquivo [`settings.py`](settings.py) , colocou-se 60 dias como o prazo para apagar essas tarefas:

```bash
CELERY_RESULT_EXPIRES = 5184000 # 60 days
```

Se não desejar limpar da tabela de resultados das tarefas (`django_celery_results_taskresult`) dessa forma, basta não iniciar o celery beat.
Conforme documentação, a tarefa de limpeza dessa tabela, considerando o prazo de expiração configurado, executa todo dia às 4 horas da manhã (GMT-3, então 1:00 da madrugada horário de Brasília). É possível ver esses resultados direto no banco na tabela `django_celery_results_taskresult` ou então via interface administrativa do django, na seção Celery Results -> Task results. A aplicação responsável por guardar esses resultados no backend do Django é a [django-celery-results](https://django-celery-results.readthedocs.io/).


>**Observação:**
>Todos esses processos podem ser gerenciados com o [supervisor](http://supervisord.org/introduction.html). Você encontra exemplos de uso em [docker/supervisor](docker/supervisor/)

## Configurações Gerais:

- Para o ambiente de produção, em `settings.py`, configurar `ALLOWED_HOSTS` para o seu domínio. Exemplo:
  ```bash
  # set a value for production environment, alongside with debug set to false
  ALLOWED_HOSTS = get_from_env('ALLOWED_HOSTS', 'endereco-do-seu-servidor-helios').split(",")
  ```
- Para que qualquer usuário que se logar no sistema possa receber automaticamente o papel de **gestor de eleição**, e por consequência, receber o privilégio para criar e gerir eleições, edite o arquivo `settings.py` e deixe como `False` a opção `HELIOS_ADMIN_ONLY`


## Outras personalizações feitas no Helios

Além do que já foi relatado na seção [Personalizações feitas no Helios](#personalizações-feitas-no-helios), detalhamos aqui algumas das personalizações realizadas. 

### Habilitar Interface de Administração do Django

O projeto original do Helios não vem com essa aplicação habilitada. [A interface de administração automática](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/) facilita algumas atividades de gerenciamento dentro da organização, como por exemplo dar permissão de criação de eleição para um usuário. Você encontra diversas referências a essa interface ao longo deste tutorial.

### Listar eleições na página inicial do Helios

Nessa personalização, as eleições que são listadas na página inicial são as que são explicitamente marcadas dessa forma via interface de administração do django (o módulo /admin que foi adicionado neste *fork*).

Se você quiser que uma eleição seja listada na página inicial do Helios, faça:
- Na página de administração do Django, localize a opção `Helios` e clique em *Elections*. 
- Na página seguinte, clique no nome da eleição que você gostaria que fosse listada na página pública e na tela de edição, marque a opção *Featured p* e salve.

### Autenticação federada via shibboleth

Para a utilização federada do Helios, diversas personalizações foram efetuadas tanto na página pública, quando na parte de gerenciamento de eleições. Essas personalizações estão hoje no ramo `helios_shibboleth` e somente no repositório https://github.com/shirlei/helios-server. 

> Obs.: como esse branch não foi integrado ao branch principal, e desde a última versão estável várias atualizações, incluindo versões de software foram realizadas no branch principal(master), o branch `helios_shibboleth` precisará de trabalho de merge e resolução de possíveis conflitos.


#### Configuração da autenticação com o módulo apache shibboleth2

Além do módulo de autenticação LDAP, também foi desenvolvido um módulo de autenticação considerando o módulo shibboleth2 para o Apache. Nesse caso, o Helios funciona como um Provedor de Serviço (Service Provider - SP).

> Se o SP estiver na federação, então qualquer usuário autenticado em um IdP da federação será capaz de acessar o Helios. Agora se o SP não ficar na federação, então é possível estabelecer confiança mútua entre o SP e o IdP de sua instituição. Dessa forma, somente os usuários oriundos do IdP de sua instituição poderão acessar o SP Helios

Para utilizar essa funcionalidade, deve-se instalar o módulo apache shibb (funcionalidade testada com libapache2-mod-shib2) do servidor que vai servir o SP Helios e efetuar as configurações necessárias do shibboleth. Essas configurações incluem por exemplo o estabelecimento de confiança com o IdP, obtenção de metadados do IdP, envio de metadados do SP para o IdP, etc. Um bom ponto de partida, caso a instituição não costume configurar SPs shibboleth, é pesquisar por tutoriais que auxiliem na configuração de um SP.

Além disso, o módulo de autenticação shibboleth deve ser habilitado no arquivo `settings.py` e torná-lo padrão, para que a interface multi-instituição seja utilizada:

```bash
AUTH_ENABLED_AUTH_SYSTEMS = get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'shibboleth').split(",")

AUTH_DEFAULT_AUTH_SYSTEM = get_from_env('AUTH_DEFAULT_AUTH_SYSTEM', 'shibboleth')
```

Deve-se também configurar os demais atributos em `settings.py`, na seção `#Shibboleth auth settings`.

> **Observação:** As configurações aqui indicadas supõe que o provedor de serviço (apache, módulo shibboleth e demais configurações) está configurado e funcional.


#### Habilitando instituições da federação para usarem o serviço Helios

Toda instituição a utilizar o Helios federado deve ser previamente cadastrada. Esse cadastro é feito na parte administrativa do Django. Acesse http://endereco-do-seu-servidor-helios/admin, procure por *HeliosInstitution* e clique em *Institutions* e então em *Adicionar Institution*. Forneça os dados necessários e clique em salvar.

Toda instituição deve ter pelo menos um usuário com o papel de **administrador da instituição**. Para adicionar esse papel a um usuário acesse o aplicativo *admin* do Django e:

1. Em *HeliosInstitution*, clique em *Institution user profiles* e depois em *Adicionar institution user profiles*
2. Se o usuário a ser cadastrado já se conectou alguma vez via federação, deve aparecer no campo *Helios user*. Se não, deixe em branco. 
3. No campo *django user*, é necessário adicionar um novo usuário. Clique no ícone + e informe no campo usuário o email do administrador e em permissões selecione *Institution Admin*. Clique em salvar. 
4. No campo *institution*, selecione a instituição previamente criada.
5. Em e-mail, informe o e-mail do administrador. Se desejar, informe a data de expiração desse usuário. Deixe o campo *active* desmarcado (será marcado quando o usuário se conectar no serviço pela primeira vez).

## Usando docker para desenvolvimento

O objetivo desta seção é repassar as informações necessárias para subir containeres docker para ambiente de desenvolvimento. Alguma familiaridade com o uso do docker é necessária, para ajustes eventuais de acordo com a sua realidade.

Os arquivos relacionados ao docker são os seguintes:

- [docker-compose.yml](docker-compose.yml)

Execute `docker-compose up -d`, por exemplo, para iniciar os containeres. Imagens inexistentes serão baixadas (python e redis) e os builds necessários serão realizados, assim como a inicialização dos containers.
Se você já executou essa operação e quer forçcar fazer build novamente, pode por exemplo rodar o mesmo comando, adicionando também o parâmetro *--build*
Como a intenção deste tutorial não é ensinar a usar o docker, por favor verifique a [documentação](https://docs.docker.com/compose/reference/overview/) para outras informações e detalhes.

Ao término, você terá os seguintes serviços em containeres:

- `helios`: a aplicação Django servida por gunicorn (script `/start`; na inicialização o container executa `migrate` e `collectstatic` automaticamente); o servidor de desenvolvimento fica disponível em `127.0.0.1:8000`;
- `celeryworker` e `celerybeat`: os processos de tarefas assíncronas e agendadas do celery;
- `redis`: o *message broker* do celery;
- `nginx`: serve os arquivos estáticos de `staticfiles/` na porta 1337.

O serviço de banco PostgreSQL (`db`) está comentado no `docker-compose.yml`: usa-se um PostgreSQL externo, ajustando `POSTGRES_HOST` (e usualmente `DB_USER`/`DB_PWD`) no `.env`.

Você pode logar no container e verificar as configurações e também pode, supondo que nenhuma modificação foi feita nos arquivos de build, acessar localhost:8000 no navegador para o ambiente de dev, e localhost:1337 para os arquivos estáticos servidos pelo nginx.

>Obs.: alterações que você faça localmente no código fonte (veja que o código fonte foi montado como um volume), se refletirão 'automaticamente' apenas para localhost:8000 (ou outra porta que você tenha configurado), que é onde está rodando o servidor de desenvolvimento. Para refletir para os demais serviços você precisa reiniciar o container correspondente.

- [docker folder](docker)
    - [Dockerfile](docker/app/Dockerfile)
    Arquivo de build da imagem a ser usada pelos containeres do serviço helios.
    - [Arquivos supervisor](docker/supervisor)
    Arquivos de exemplo de configuração de processos (apache, celery, redis) pelo gerenciador [*supervisor*](http://supervisord.org/)
    - [Arquivos Apache2](docker/apache)
    Arquivo de configuração para o helios ser servido pelo Apache. Os arquivos de certificados não são válidos, você deve gerar um autoassinado para testes em desenvolvimento, como uma ferramenta como o *openssl* ou usar algum que você já possua para esse propósito. Basta substituir os arquivos.
    - [docker-entrypoint.sh](docker/app/docker-entrypoint.sh)
    Script que aguarda a disponibilidade do PostgreSQL antes de iniciar a aplicação.
    - [Arquivos postgres](docker/db/init.sql)
    Script de inicialização da base de dados a ser usada pelo helios.


Antes de executar o docker-compose, você pode criar um arquivo .env na raiz deste projeto, contendo as seguintes variáveis de ambiente listadas abaixo. Essa configuração é boa prática, mas não é obrigatória, você pode deixar os valores informados no próprio arquivo [settings.py](settings.py).

>**Atenção**: se o celery estiver rodando supervisionado pelo supervisor, por questões de funcionamento de subprocessos e variáveis de ambiente, essas variáveis podem não ficar disponíveis no contexto de execução das tarefas pelo celery e então elas devem estar configuradas, especialmente as de email, no próprio settings.py. Ver mais detalhes em [Subprocess Environment](http://supervisord.org/subprocess.html#subprocess-environment) ou então configuradas como estão na indicação do manual do supervisor, como parâmetro, no arquivo de configuração do supervisor. Se você tiver uma ideia melhor, por favor compartilhe!

        DEBUG=1
        ALLOWED_HOSTS='localhost,192.168.15.7'
        SECRET_KEY='^m-&-5eq6bu))ovhgzuus4g)#v-&m&0d8qaf)f2*z9av!t!7+('
        POSTGRES_PASSWORD=postgres
        DB_NAME=helios
        DB_PWD=helios
        DB_USER=helios
        POSTGRES_HOST=db
        POSTGRES_PORT=5432
        EMAIL_USE_TLS=1
        EMAIL_HOST=<your smtp server>
        EMAIL_PORT=587
        EMAIL_HOST_USER=<email a ser usado como remetente>
        EMAIL_HOST_PASSWORD=<a senha do email fornecido em EMAIL_HOST_USER>
        URL_HOST=http://localhost
        SECURE_URL_HOST=https://localhost
        DJANGO_SUPERUSER_USERNAME=admin
        DJANGO_SUPERUSER_EMAIL=<adicione um email valido>
        DJANGO_SUPERUSER_PASSWORD=admin
        GROUP_ID=1000
        USER_ID=1000
        CELERY_BROKER_URL=redis://127.0.0.1:6379


DEBUG=1 indica que o django está em modo DEBUG, exibindo por exemplos mensagens de erro da aplicação com detalhamento no navegador. Use apenas em desenvolvimento!

Em ALLOWED_HOSTS indique o(s) nomes de hosts/domínios nos quais o Django pode servir o Helios. Obrigatório configurar se DEBUG configurada pra false (DEBUG=0).

Para a SECRET_KEY, troque os valores conforme orientação em [Alguns lembretes finais cruciais para o ambiente de produção](#alguns-lembretes-finais-cruciais-para-o-ambiente-de-produção)

DB_NAME, DB_PWD e DB_USER devem conferir com nome do banco, usuário e senha fornecidos no arquivo [init.sql](docker/db/init.sql) para o container do postgres.

POSTGRES_HOST e POSTGRES_PORT devem conferir com o nome do serviço e porta definidos no [docker-compose.yml](docker-compose.yml) para o postgres.

As variáveis EMAIL_* devem ser preenchidas com o serviço de email a ser usado para as atividades de envio de email pelo Helios.

URL_HOST indica endereço sem considerar HTTPS e SECURE_URL_HOST indica o endereço a ser usado quando HTTPS configurado. 

>**Observação**: Para o caso de desenvolvimento, é importante indicar a porta na qual o servidor de desenvolvimento foi iniciado (no caso do nosso docker-compose.yml, a porta 8000), para que a navegação se direcione para essa porta e possa ser utilizada a funcionalidade de *reload* automático para mudanças de código.

DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL e  DJANGO_SUPERUSER_PASSWORD são as informações para criar um usuário admin (você pode configurar outro username no arquivo .env, assim como outra senha!), aquele que você normalmente criaria executando no shell o comando `uv run python manage.py createsuperuser`. Esse usuário é o usuário do app django admin site, que foi habilitado para essa personalização do helios. Com ele você acessa, por exemplo, http://localhost:8000/admin e consegue executar algumas operações administrativas, como habilitar um usuário que já logou previamente no helios para ser gestor de eleições ou então visualizar lista de usuários do helios. Não confundir com usuário gestor de eleição do helios! Esse usuário não é usuário que consegue logar na aplicação Helios. A aplicação Helios depende de módulo de autenticação próprio habilitado, dentre os disponíveis (Google ou Ldap, por exemplo).

O GROUP_ID e USER_ID você pode usar o do usuário local, no host em que você vai rodar o docker-compose, para evitar problemas de permissão de diretórios. Por exemplo, o teu usuário local tem o uid 1000 e você montou o diretório local onde baixou o helios para um volume do docker, no qual o usuário criado tem outro uid. Importante: se você não quiser fornecer esse valor, remova o parâmetro -g e -u do comando `RUN groupadd -r -g 1000 helios && useradd -r -g helios -u 1000 helios` no [Dockerfile da imagem](docker/app/Dockerfile).

CELERY_BROKER_URL indica o endereço e credenciais de acesso ao serviço de message broker, no caso, o Redis.

Importante destacar que para variáveis que não sejam informadas, será utilizado o valor padrão definido em [settings.py](settings.py). Você também pode configurar assim outras variáveis do settings.py que achar necessário, seguindo o mesmo padrão.

>**Observação**: Todos os valores de configuração e escolhas de organização de serviços e containeres foram feitas pensando em ambiente de desenvolvimento local, para facilitar configurar o ambiente especialmente considerando questões de versões de software (como a versão do Python, por exemplo). Questões de segurança e até melhores práticas de separação de serviços por containers e etc não estão aqui consideradas!

## Alguns lembretes finais cruciais para o ambiente de produção

- Em `settings.py` alterar de `True` para `False` o valor da constante `DEBUG`
- Alterar obrigatoriamente o valor do [SECRET_KEY](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY). Há ferramentas na web pra isso, como a disponível em [http://www.miniwebtool.com/django-secret-key-generator/](http://www.miniwebtool.com/django-secret-key-generator/)
- Conforme indicado no `settings.py`, não se deve alterar o valor da opção `SECURE_URL_HOST` após você já ter o sistema em produção, com eleições criadas (em andamento ou finalizadas), pois caso contrário a URL para depósito da cédula se tornará inválida.
