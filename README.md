- [Sistema de votação Helios como serviço de TIC](#sistema-de-votação-helios-como-serviço-de-tic)
  - [Personalizações feitas pelo IFSC no Helios](#personalizações-feitas-pelo-ifsc-no-helios)
- [Guia de instalação e configuração do Helios](#guia-de-instalação-e-configuração-do-helios)
  - [Preparação do ambiente para execução do Helios](#preparação-do-ambiente-para-execução-do-helios)
    - [Configuração do banco de dados PostgreSQL](#configuração-do-banco-de-dados-postgresql)
    - [Compilando arquivos com as traduções para português](#compilando-arquivos-com-as-traduções-para-português)
    - [Configuração dos módulos de autenticação](#configuração-dos-módulos-de-autenticação)
      - [Autenticação em uma base LDAP](#autenticação-em-uma-base-ldap)
    - [Testando a instalação em ambiente de desenvolvimento](#testando-a-instalação-em-ambiente-de-desenvolvimento)
    - [Habilitando usuário com permissão de gestor de eleições](#habilitando-usuário-com-permissão-de-gestor-de-eleições)
  - [Preparando ambiente de produção](#preparando-ambiente-de-produção)
    - [Celery](#celery)
  - [Configurações Gerais:](#configurações-gerais)
  - [Outras personalizações feitas no Helios](#outras-personalizações-feitas-no-helios)
    - [Habilitar Interface de Administração do Django](#habilitar-interface-de-administração-do-django)
    - [Listar eleições na página inicial do Helios](#listar-eleições-na-página-inicial-do-helios)
  - [Alguns lembretes finais cruciais para o ambiente de produção](#alguns-lembretes-finais-cruciais-para-o-ambiente-de-produção)
    - [Autenticação federada via shibboleth](#autenticação-federada-via-shibboleth)
      - [Configuração da autenticação com o módulo apache shibboleth2](#configuração-da-autenticação-com-o-módulo-apache-shibboleth2)
      - [Habilitando instituições da federação para usarem o serviço Helios](#habilitando-instituições-da-federação-para-usarem-o-serviço-helios)
# Sistema de votação Helios como serviço de TIC

O objetivo deste projeto era inicialmente atender a [necessidade N.47 do Plano Diretor de TI (PDTI) de 2013 do Instituto Federal de Santa Catarina (IFSC)](http://dtic.ifsc.edu.br/files/pdti2013-revisao02.pdf). No entanto, logo percebeu-se que outras instituições, especialmente as de ensino, poderiam se beneficiar das melhorias realizadas por nós no projeto original do [Ben Adida](https://github.com/benadida/helios-server). 

Sendo assim, com intuito de contribuir com o público brasileiro, optamos por manter nesse repositório todas as melhorias feitas para que outras instituições possam se beneficiar do trabalho realizado pelo IFSC em cima do projeto original. Ou seja, aquilo que é praxe na comunidade de software livre (compartilhar) e na comunidade acadêmica (referenciar trabalhos de terceiros). Da mesma forma, esperamos receber contribuições dessas instituições para melhorar o código aqui disponibilizado. :punch: 

> **Nota:** Pode-se constatar que de fato esse projeto está beneficiando o público brasileiro. Em 2013, antes desse projeto, o Helios só era usado por 2 instituições de ensino no Brasil e ambas parecem ter usado a versão original e não compartilharam o código. Em 2020 sabemos que a versão modificada pelo IFSC está sendo usada por pelo menos 20 instituições de ensino (Institutos Federais, Universidades Estaduais e Universidades Federais), por órgãos do poder executivo, por organizações e associações de classes. Muitas nos citaram :blush:, mas nem todas :worried:. E recebemos contribuições de uma dessas instituições :clap:.

## Personalizações feitas pelo IFSC no Helios

Esse repositório contém as personalizações feitas pelo IFSC no Helios. Ainda assim, buscará o sincronismo periódico com (sempre que possível e dentro do tempo possível) o projeto original do [Ben Adida](https://github.com/benadida/helios-server).

Personalizações e contribuições que fizemos que estão aqui e que não foram para o *upstream*:
- Tradução da interface para português
- Melhorias em algumas páginas e adequação para serem responsivas
- Criação de manuais para eleitores e para gestores de eleição
- Módulo de autenticação LDAP
- Módulo de autenticação Shibboleth
- Ajustes na página inicial e interface de administração para operação do Helios em ambiente Federado (Ex: Federação CAFe)
- Esse próprio arquivo com instruções para instalação do Helios :smile:

Publicamos dois artigos sobre essas personalizações (os PDFs estão disponíveis abaixo):

- CHAVES, S. A., MELLO, E. R. [Adoção de modelo controle acesso baseado em atributos em sistema de votação online para ofertá-lo como um serviço de TIC federado](artigos-publicados/chaves-sbseg15.pdf). In: WGID - Workshop de Gestão de Identidade, 2015, Florianópolis. XV Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais. 
- CHAVES, S. A., MELLO, E. R. [O uso de um sistema de votação on-line para escolha do conselho universitário](artigos-publicados/chaves-sbseg14.pdf) In: WTE - Workshop de Tecnologia Eleitoral, 2014, Belo Horizonte. XIV Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais 

# Guia de instalação e configuração do Helios

As instruções de configuração e disponibilização descritas neste README vão considerar especificamente o uso em ambiente containerizado, considerando como base a imagem [python:3.6.15-buster](https://hub.docker.com/layers/library/python/3.6.15-buster/images/sha256-08e91f391139ff24d82df572307b30ee850b78884ec633cf10f5a6e990dd9920?context=explore), considerando a última atualização do projeto do [Helios](https://github.com/benadida/helios-server) pelo mantenedor para a versão [3.6 do python](https://github.com/benadida/helios-server/commit/64f603375298d45f5a74d172fcd9a3763af5e587) 


> Obs.: A maioria dos passos aqui descritos foram historicamente executados para disponibilização do Helios em um servidor com a distribuição Linux Ubuntu (testado nas versões LTS 14.04, 16.04 e 18.04), embora já tenha sido feita instalação com sucesso no CentOS, e devem continuar na maior parte válidos para distribuições mais recentes do Ubuntu, por exemplo, com suporte à Python 3.6. Para a última versão considerando Python 2 e o README para instalação direto num host linux, acesse a tag [python2](https://github.com/ifsc/helios-server/releases/tag/python2)

Para seguir esse tutorial é necessário alguma experiência com administração de sistemas Linux (instalação de pacotes, configuração de serviços, etc.) e também uso do docker.


## Preparação do ambiente para execução do Helios

*Você vai precisar de um host em que possa executar o docker e o docker-compose.*

> Para o Compose V2, usar `docker compose` (sem p "-"). Veja mais aqui: https://docs.docker.com/compose/reference/

Recomendo que crie um usuário no sistema específico para o helios, por exemplo, usuário `helios`.

No [docker-compose.yml](docker-compose.yml) exemplo que acompanha este repositório, há entrada (comentada) para uso do postgres conteinerizado. Em ambiente de produção isso pode não ser desejado por diversas razões. Se for realizar uma instalação do postgres localmente para utilização, na seção [Configuração do banco de dados PostgreSQL](#configuração-do-banco-de-dados-postgresql) abaixo são listadas algumas informações/configurações importantes a serem realizadas após a instalação do Postgres. Se você já tem uma instalação disponível ou pretende utilizar como container, pode pular para a seção [Obtenção de código fonte e preparo da aplicação](#obtenção-de-código-fonte-e-preparo-da-aplicação)

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
git clone https://github.com/ifsc/helios-server.git
```

Copie ou renomeie o o arquivo [.env.sample](.env.sample) para .env e edite os valores de acordo.

Se você já tem uma instalação do Postgres na qual foi criada uma base de dados para uso pelo helios e para a qual lhe forneceram os dados de acesso (host, db, user, password), basta informar estes dados no arquivo .env (conferir nome das variáveis em [settings.py](settings.py), na seção DATABASES). Alternativamente, você pode informar esses valores diretamente no arquivo settings.py

Edite o arquivo `settings.py` e localize a seção databases. Adicione as informações para conexão no banco de dados, conforme o exemplo. `get_from_env` vai tentar obter o valor da variável a partir das variáveis de ambiente configuradas no arquivo .env e se ausentes, o valor atribuído manualmente. Por exemplo, se DB_NAME ausente, utilizará o valor `helios` na config abaixo.

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_from_env('DB_NAME', 'helios'),
        'USER': get_from_env('DB_USER', 'helios'),
        'PASSWORD': get_from_env('DB_PWD', 'helios'),
        'HOST': get_from_env('POSTGRES_HOST', 'db'),
        'PORT': get_from_env('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 600,
    }
}
```

Com os valores das variáveis configuradas em .env, execute o seguinte comando:

`docker-compose up -d --build`

O comando acima irá realizar os builds necessários e iniciar os containers dos serviços listados na seção `service` do arquivo [docker-compose.yml](docker-compose.yml)


### Compilando arquivos com as traduções para português

A interface do Helios foi traduzida para o português e assim é necessário que compile os arquivos de tradução, caso queira usar a tradução que fizemos. Execute o seguinte comando a partir do diretório do Helios:
```bash
python manage.py compilemessages -l pt_BR
```

docker:

`docker exec -it helios-server-helios-1 python manage.py compilemessages -l pt_BR`

Após a compilação, arquivos `.mo` devem ter sido gerados em `locale/pt_BR/LC_MESSAGES`

> **Observação:** Para alterar alguma tradução é possível utilizar o aplicativo [POEDIT](https://poedit.net), os mesmo editar diretamente os arquivos `django.po` e `djangojs.po` no editor de texto de sua preferência.

Se você adicionou alguma mensagem nova para ser traduzida e gostaria que fossem adicionadas aos arquivos de tradução, execute os comandos abaixo.

1. Para adicionar strings de arquivos python:

```bash
python manage.py makemessages -l pt_BR
```

docker:

```bash
docker exec -it helios-server-helios-1 python manage.py makemessages -l pt_BR --ignore=venv
```

2. Para adicionar strings de arquivos .js (os que passam pelo engine do Django):

```bash
python manage.py makemessages -d djangojs -l pt_BR --ignore=venv
```
> **Observação:** Para a coleta de mensagens de arquivos .js, se você tiver criado o diretório de virtualenv relativo ao diretório do helios e chamado de por exemplo `venv`, você pode passar o parâmetro `--ignore=venv` conforme acima, para ignorar esse diretório.

### Configuração dos módulos de autenticação

Você precisará habilitar em `settings.py` os módulos de autenticação que deseja. Por exemplo, poderia usar os módulos de autenticação do projeto original e permitir a autenticação de usuários por meio de contas Google, Facebook ou Twitter. 

Na seção abaixo apresentamos as configurações necessárias para permitir a autenticação de usuários de uma base LDAP. Se não tiver um servidor LDAP e só queira testar o Helios, então talvez possa ser interessante tentar com os outros módulos de autenticação citados acima.

#### Autenticação em uma base LDAP

Habilite o módulo LDAP em `settings.py`:

```bash
AUTH_ENABLED_SYSTEMS = get_from_env('AUTH_ENABLED_SYSTEMS',
                                    get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'ldap')
                                    ).split(",")
```

A documentação da biblioteca utilizada pode ser encontrada em https://django-auth-ldap.readthedocs.io/en/4.0.0/example.html. As configurações principais estão no `settings.py` e são: `AUTH_LDAP_SERVER_URI`, `AUTH_LDAP_BIND_PASSWORD`, e `AUTH_LDAP_USER_SEARCH`. 

As opções `AUTH_LDAP_BIND_DN` e `AUTH_LDAP_BIND_PASSWORD` deverão ter um valor configurado se o servidor LDAP exigir autenticação de usuário mesmo que seja para fazer consultas.

> Observação: Você pode testar a conexão usando o próprio teste unitário do app de autenticação. Para tal, edite o arquivo [helios_auth/tests.py](helios_auth/tests.py), altere o usuário (euclid) e senha (password) que estão no teste usando o [servidor de testes LDAP da ForumSys](https://www.forumsys.com/tutorials/integration-how-to/ldap/online-ldap-test-server/) para um usuário e senha válidos no LDAP que você configurou no arquivo [settings.py](settings.py) e execute `python manage.py test helios_auth`

### Testando a instalação em ambiente de desenvolvimento

Ao rodar a aplicação, você deve criar um usuário de administração do django. Isso se deve ao fato de aplicação `admin` estar habilitada no arquivo `settings.py` (django.contrib.admin), pois iremos utilizá-la em algumas personalizações feitas para este *fork* do Helios.

Você pode criar um novo usuário para o django admin site executando o comando no host em que o helios está instalado `python manage.py createsuperuser` ou via `docker exec`:

```
docker exec -it helios-server-helios-1 python manage.py createsuperuser
````

Preencha os dados solicitados de usuário e senha e guarde a senha, pois ela será necessária para acesso à interface administrativa posteriormente.

Quando o comando `docker-compose up -d --build` foi executado, diversos containeres foram inicializados, a saber (nomes considerando o nome do serviço no [docker-compose.yml](docker-compose.yml)):

1. helios-server-nginx-1: servidor web
2. helios-server-helios-1: aplicação, na qual roda o servidor de aplicação gunicorn
3. helios-server-celeryworker-1: celery worker, responsável pela execução de tarefas como o envio de emails e processamento do arquivo de eleitores.
4. helios-server-celerybeat-1: executa tarefas em intervalos agendados, como a limpeza a cada 60 dias do resultado das tarefas executadas
5. helios-server-redis-1: message broker (à exemplo do RabbitMQ)

Se você rodou o postgres containerizado, também o container helios-server-db-1, o qual executa o postgres.

Nas configurações disponibilizadas no referido docker-compose.yml, o nginx atende na porta 1337.

Feito isso, você pode acessar a URL http://endereco-do-seu-servidor-helios:1337 e se autenticar com algum usuário presente em sua base LDAP (ou um usuário de algum outro sistema de autenticação que tenha habilitado para o Helios).

Esse usuário não conseguirá criar eleições ainda, mas esse passo é necessário para que seja criada uma entrada para esse usuário na base. No próximo passo, [Habilitando usuário com permissão de criar eleições](#habilitando-usuário-com-permissão-de-criar-eleições),usaremos a aplicação `admin` do django para dar privilégio de gestor de eleição para esse usuário. 

### Habilitando usuário com permissão de gestor de eleições

Acesse a URL http://endereco-do-seu-servidor-helios:1337/admin e se autentique com o usuário e senha de administração (você fez isso quando executou o script `reset.sh`). 

>*Observação*: Se você não lembra qual senha você criou, mas lembra o usuário, então é possível mudar a senha executando o comando `python manage.py changepassword <usuario>`

Na página de administração são apresentados os *apps* habilitados. Localize a opção `Helios_Auth` e clique em *Users*. Na página seguinte, escolha o usuário que você deseja editar (basta clicar somente o login do mesmo). Na página de edição, marque a opção *Admin_p* e salve.

Pronto! O usuário em questão recebeu o papel de **gestor de eleição** e será capaz de criar e gerenciar eleições com o Helios.

> **Atenção**: só será possível dar o privilégio `admin_p` para usuários que se autenticaram previamente na aplicação Helios. Isso se deve à lógica de criação desse login, que é feita durante o login do usuário, caso ainda não exista. 


Para rodar o servidor de desenvolvimento do django, para facilitar verificar as mudanças de código, você pode colocar o servidor de dev para rodar executando `python manage.py runserver 0.0.0.0:8000` no container.

```bash
docker exec -it helios-server-helios-1 python manage.py runserver 0.0.0.0:8000
```

Dessa forma, você pode acessar o helios http://endereco-do-seu-servidor-helios:8000 e aproveitar o recurso de auto reload do servidor de dev, para ver as alterações efetuadas (pela porta 1337 via nginx você tem que reiniciar o container).

## Preparando ambiente de produção

Na seção anterior foi usado o servidor web de desenvolvimento provido pelo próprio Django (`python manage.py runserver 0.0.0.0:8000`). No entanto, ele é apenas para desenvolvimento e **não deve** ser usado em um ambiente de produção.

É possível trabalhar com diversos servidores web, porém no caso em questão optou-se na atualização do helios para o python 3 (conforme o projeto original do [Ben Adida](https://github.com/benadida/helios-server)) em se utilizar o Nginx ao invés do Apache previamente utilizado (ver a tag [python2](https://github.com/ifsc/helios-server/releases/tag/python2)).


### Celery

Lembrando mais uma vez que o [celery](http://www.celeryproject.org/) precisa estar em execução, pois ele é o enfileirador de tarefas, como a tarefa de envio de emails e a tarefa de registro de votos.

Em produção é interessante rodar o celery com múltiplos processos, para acelerar por exemplo envio de emails.  Na prática, 4 à 5 processos em paralelo se mostrou suficiente. 

O comando executado para iniciar o celery worker no container *helios-server-celeryworker-1* é o presente no arquiv [docker/app/start-celeryworker](docker/app/start-celeryworker). Esse arquivo é passado como *entrypoint* para o container. Note que o valor de CELERY_WORKER_CONCURRENCY precisa ser configurado no arquivo .env antes de fazer o build. Por padrão, no arquivo .env.sample que você irá usar de apoio, esse valor está configurado para 4.

Para que o resultado da execução das tarefas seja guardado no backend, adicionou-se o app `django_celery_results` (tabela django_celery_results_taskresult) e o `django_celery_beat` em INSTALLED_APPS.

O celery beat, agendador de tarefas periódicas, como limpar a tabela de resultados de execução de tarefas de tempos em tempos (o que pode crescer bastante), pode ser executado pelo comando celery, mas passando o parâmetro *beat* ao invér de *worker*:

O comando executado para iniciar o celery beat no container *helios-server-celerybeat-1* é o presente no arquiv [docker/app/start-celerybeat](docker/app/start-celerybeat). Esse arquivo é passado como *entrypoint* para o container.

No arquivo [`settings.py`](settings.py) , colocou-se 60 dias como o prazo para apagar essas tarefas:

```bash
CELERY_RESULT_EXPIRES = 5184000 # 60 days
```

Se não desejar limpar da tabela de resultados das tarefas (`django_celery_results_taskresult`) dessa forma, basta não iniciar o celery beat.
Conforme documentação, a tarefa de limpeza dessa tabela, considerando o prazo de expiração configurado, executa todo dia às 4 horas da manhã (GMT-3, então 1:00 da madrugada horário de Brasília). É possível ver esses resultados direto no banco na tabela `django_celery_results_taskresult` ou então via interface administrativa do django, na seção Celery Results -> Task results. A aplicação responsável por guardar esses resultados no backend do Django é a [django-celery-results)[https://docs.celeryproject.org/en/v4.2.1/django/first-steps-with-django.html#extensions].


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

O projeto original do Helios não vem com essa aplicação habilitada. [A interface de administração automática](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/) facilita algumas atividades de gerenciamento dentro da organização, como por exemplo dar permissão de criação de eleição para um usuário. Você encontra diversas referências a essa interface ao longo deste tutorial.

### Listar eleições na página inicial do Helios

Nessa personalização, as eleições que são listadas na página inicial são as que são explicitamente marcadas dessa forma via interface de administração do django (o módulo /admin que foi adicionado neste *fork*).

Se você quiser que uma eleição seja listada na página inicial do Helios, faça:
- Na página de administração do Django, localize a opção `Helios` e clique em *Elections*. 
- Na página seguinte, clique no nome da eleição que você gostaria que fosse listada na página pública e na tela de edição, marque a opção *Featured p* e salve.

## Alguns lembretes finais cruciais para o ambiente de produção

- Alterar o valor de DEBUG para que seja falso. Na avaliação sendo feita em [settings.py](settings.py), o valor de DEBUG=1 no arquivo .env indica que o django está em modo DEBUG, exibindo por exemplos mensagens de erro da aplicação com detalhamento no navegador. Use apenas em desenvolvimento! Para produção, utilize DEBUG=0 em .env (e se fizer alterações, lembre-se de reiniciar os containeres envolvidos).

- Alterar obrigatoriamente o valor do [SECRET_KEY](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY). Há ferramentas na web pra isso, como a disponível em [http://www.miniwebtool.com/django-secret-key-generator/](http://www.miniwebtool.com/django-secret-key-generator/).
  
- Conforme indicado no `settings.py`, não se deve alterar o valor da opção `SECURE_URL_HOST` após você já ter o sistema em produção, com eleições criadas (em andamento ou finalizadas), pois caso contrário a URL para depósito da cédula se tornará inválida.

- Em ALLOWED_HOSTS indique o(s) nomes de hosts/domínios nos quais o Django pode servir o Helios. Obrigatório configurar se DEBUG configurada pra false (DEBUG=0).

- As variáveis EMAIL_* devem ser preenchidas com o serviço de email a ser usado para as atividades de envio de email pelo Helios.

- URL_HOST indica endereço sem considerar HTTPS e SECURE_URL_HOST indica o endereço a ser usado quando HTTPS configurado. 

- O GID e UID você pode usar o do usuário local, no host em que você vai rodar o docker-compose, para evitar problemas de permissão de diretórios. Por exemplo, o teu usuário local tem o uid 1000 e você montou o diretório local onde baixou o helios para um volume do docker, no qual o usuário criado tem outro uid.

- CELERY_BROKER_URL indica o endereço e credenciais de acesso ao serviço de message broker, no caso, o Redis.

- Importante destacar que para variáveis que não sejam informadas, será utilizado o valor padrão definido em [settings.py](settings.py). Você também pode configurar assim outras variáveis do settings.py que achar necessário, seguindo o mesmo padrão.


### Autenticação federada via shibboleth

Para a utilização federada do Helios, diversas personalizações foram efetuadas tanto na página pública, quando na parte de gerenciamento de eleições. Essas personalizações estão hoje no ramo `helios_shibboleth` e somente no repositório https://github.com/shirlei/helios-server. 

> Obs.: como esse branch não foi integrado ao branch principal, e desde a última versão estável várias atualizações, incluindo versões de software foram realizadas no branch principal (master), o branch `helios_shibboleth` precisará de trabalho de merge e resolução de possíveis conflitos, incluindo muito possivelmente a atualização para python3. Esta seção está sendo mantida aqui para fins apenas informativos.

#### Configuração da autenticação com o módulo apache shibboleth2

Além do módulo de autenticação LDAP, também foi desenvolvido um módulo de autenticação considerando o módulo shibboleth2 para o Apache. Nesse caso, o Helios funciona como um Provedor de Serviço (Service Provider - SP).

> Se o SP estiver na federação, então qualquer usuário autenticado em um IdP da federação será capaz de acessar o Helios. Agora se o SP não ficar na federação, então é possível estabelecer confiança mútua entre o SP e o IdP de sua instituição. Dessa forma, somente os usuários oriundos do IdP de sua instituição poderão acessar o SP Helios

Para utilizar essa funcionalidade, deve-se instalar o módulo apache shibb (funcionalidade testada com libapache2-mod-shib2) do servidor que vai servir o SP Helios e efetuar as configurações necessárias do shibboleth. Essas configurações incluem por exemplo o estabelecimento de confiança com o IdP, obtenção de metadados do IdP, envio de metadados do SP para o IdP, etc. Um bom ponto de partida, caso a instituição não costume configurar SPs shibboleth, é pesquisar por tutoriais que auxiliem na configuração de um SP.

Além disso, o módulo de autenticação shibboleth deve ser habilitado no arquivo `settings.py` e torná-lo padrão, para que a interface multi-instituição seja utilizada:

```bash
AUTH_ENABLED_SYSTEMS = get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'shibboleth').split(",")

AUTH_ENABLED_SYSTEMS = get_from_env('AUTH_DEFAULT_AUTH_SYSTEM', 'shibboleth')
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

