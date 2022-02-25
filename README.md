### Pagamentos
Aplicação que tem a ideia de uma carteira on-line, cadastre os seus depósitos, débitos e anotações.

### Requisitos

* 1 - Criar uma conta no SendGrid, o cadastro é free, e possui 100 e-mails diários.

		https://app.sendgrid.com/signup?id=71713987-9f01-4dea-b3d4-8d0bcd9d53ed

		Com a conta aberta no SendGrid, encontre a função para gerar a Api Key, iremos usar para inserir no arquivo de configuração do projeto.

* 2 - Criar um arquivo chamado .init.ini na pasta '/app/conf/', com a estrutura abaixo.

		[postgresql]
		DATABASE_ENGINE: postgresql_psycopg2
		DATABASE_NAME: payments
		DATABASE_USER: payments
		DATABASE_PASSWORD: payments
		DATABASE_HOST: localhost
		DATABASE_PORT: 5432

		[sqlite3]
		DATABASE_ENGINE: sqlite3
		DATABASE_NAME: db.sqlite3

		[user_config]
		PASSWORD: pbkdf2_sha256$20000$KcOIieukIS3L		$QApWmGR98uBW54DsUZBuMxmDoPLhk7pmK8TVPSNCFj8=
		EMAIL: teste@teste.com
		CPF: 11111111111
		SENDGRID_API_KEY: SG.aoijaoiFJASF1OIASJFOAISJFA.		aposkspadk_PASKFPOSAKPFKASPFKPSAKFPSAK212331231
	Atenção com os campos *SENDGRID_API_KEY, coloque a Api Key gerada no SendGrid, *PASSWORD por default é root.


* 3	- Exportar a variável de ambiente, com o nome do arquvio de configuração, rodando o script dentro do projeto.

		source ./config_vars.sh

### Instalação

* 1 - make install
* 2 - make config

* OBSERVAÇÃO:

	Para alterar a configuração, entre os arquivos e banco de dados, use como parametro o comando:

	* make config settings='production'

	* A aplicação esta configurada para usar os banco de dados *(sqlite3 / postgresql)

	* Para inserir outro banco de dados, basta incluir uma nova seção no arquivo /.init.ini, é obrigatório que o Django suporte.

	acesse:
		 * http://localhost:8000/
		 informações do super usuário estão no arquivo de arquivo /.init.ini



### Comandos

* make start
* make migrate
* make clean
* make clean_migrations
	* Cuidado: este comando apaga os arquivos de migração

### Atenção

 * SEMPRE QUE RODAR UM COMANDO, não esqueça de colocar o parametro, indicando qual arquivo de configuração será usado.
 	* ex: make start settings='production'


;)