Projeto de Containers e Microsserviços

O projeto consiste em 5 desafios propostos pelo Professor Jorge Soares para compor a nota da disciplina de Fundamentos de Computação Concorrida, Paralela e Distribuída.

Estrutura do Repositório

Projeto2FCCPD/
├── desafio1/
├── desafio2/
├── desafio3/
├── desafio4/
├── desafio5/
└── README.md

Desafio 1 - Containers em Rede
Descrição
Implementei dois containers Docker que se comunicam através de uma rede bridge customizada. O primeiro container executa um servidor web Flask na porta 8080, enquanto o segundo atua como cliente HTTP fazendo requisições periódicas ao servidor.

Como funciona
Servidor Web (Flask)
Três endpoints REST: / (principal), /status (health check), /info (estatísticas).
Porta 8080 exposta tanto internamente quanto mapeada para o host.
Variável de estado que incrementa a cada acesso (contador).
Retorna sempre JSON para facilitar o parse no cliente.
Cliente HTTP
Loop infinito com sleep de 5 segundos entre requisições.
Usa a biblioteca requests do Python.
Faz GET para http://servidor-web:8080 (resolução por DNS).
Tratamento de exceções para TimeoutError e ConnectionError.
Rede Docker Bridge
Nome: rede-desafio1.
Driver: bridge (padrão).
Subnet automático atribuído pelo Docker.
Embedded DNS server que resolve servidor-web para o IP interno do container.

A criação da rede rede-desafio1 foi necessária pois a rede bridge padrão do Docker não suporta resolução automática de nomes de containers (service discovery). Ao utilizar uma user-defined network, habilitei o DNS interno do Docker, permitindo que o cliente se comunicasse via hostname (http://servidor-web), o que é essencial em ambientes onde IPs são atribuídos dinamicamente.
Configurei um time.sleep(5) no loop do cliente para evitar a geração excessiva de logs e consumo desnecessário de CPU, facilitando o acompanhamento visual do funcionamento via docker logs -f.

Instruções de Execução
Entre na pasta do desafio:
cd desafio1

Execute o script de automação:
.\executar.ps1

Acompanhar logs:
.\ver-logs.ps1

Validação externa:
curl http://localhost:8080/info

Encerrar:
.\parar.ps1

Desafio 2 - Volumes e Persistência
Descrição
Criei um sistema que demonstra o conceito de persistência de dados usando Docker Volumes. A aplicação consiste em um container rodando Python + SQLite, onde o arquivo do banco de dados é armazenado em um volume Docker que sobrevive à destruição do container.

Como funciona
Menu com 3 opções: adicionar registro, listar registros, sair.
Usa SQLite3 nativo.
Banco salvo em /data/meu_banco.db (diretório montado do volume).
Auto-detecção: Verifica se o banco já existe na inicialização.
Volume Docker
Nome lógico: dados-desafio2.
Ponto de montagem: /data (dentro do container).
Persiste o arquivo meu_banco.db fisicamente no host.

Decisões Técnicas
A utilização do SQLite facilita a visualização do conceito de volumes. Por ser um banco serverless baseado em um único arquivo, torna-se evidente que o arquivo .db gravado e lido no volume é o mesmo, independentemente do ciclo de vida do container que o acessa.
Montei o volume no caminho /data dentro do container. Durante o desenvolvimento, tive problemas de permissão ("Permission denied") ao tentar montar o arquivo do banco diretamente no Windows/WSL2. Consultei IA para diagnosticar o erro e a solução adotada foi isolar o banco em um diretório dedicado dentro do volume, garantindo a compatibilidade com o sistema de arquivos do host.
Implementei uma verificação com os.path.exists(). Quando o segundo container sobe e detecta o arquivo, imprime "BANCO EXISTENTE ENCONTRADO!" - servindo como prova visual da persistência nos logs.

Instruções de Execução
Execução rápida:
cd desafio2
.\executar.ps1

Demonstração completa do ciclo (Persistência):
.\testar-persistencia.ps1

Container de leitura (Read-only):
.\ler-dados.ps1

Desafio 3 - Docker Compose com 3 Serviços
Descrição
Implementei uma arquitetura de 3 serviços orquestrados via Docker Compose (YAML):
Processador (porta 5000): Coordenador.
Armazenador (porta 5001): Persistência.
Notificador (porta 5002): Eventos.

Como funciona
Processador recebe POST.
Transforma dados
Envia requests síncronas para Armazenador e Notificador.
Retorna status.

Decisões Técnicas
O uso do Docker Compose permitiu definir a infraestrutura de forma declarativa. Utilizei a diretiva depends_on para controlar a ordem de inicialização dos containers e garantir que todos estivessem na mesma rede virtual (rede-servicos) criada automaticamente.

Identifiquei que o depends_on garante apenas o início do container, e não que a aplicação Flask está pronta para receber conexões. Isso causava falhas na primeira execução. Para corrigir, implementei uma lógica de retry com backoff (tentativas repetidas com intervalo progressivo) no código Python do Processador, garantindo tolerância a falhas na inicialização dos serviços dependentes.

Instruções de Execução
cd desafio3
.\executar.ps1

Testar o fluxo completo:
curl -X POST http://localhost:5000/processar -H "Content-Type: application/json" -d "{\"dado\":\"teste\"}"

Verificar todos os serviços:
docker-compose logs -f

Desafio 4 - Microsserviços Independentes
Descrição
Arquitetura Consumer/Provider:

Serviço de Usuários (Provider - 5000).

Serviço de Relatório (Consumer - 5001).

Decisões Técnicas
Utilizei variáveis de ambiente (USUARIOS_URL) para definir os endpoints. Isso permite reconfigurar a comunicação entre os serviços sem necessidade de alterar o código fonte ou rebuildar a imagem, facilitando a portabilidade entre ambientes.

Aplicando o aprendizado do Desafio 3, mitiguei o delay de inicialização do Flask de duas formas: adicionei um sleep estratégico no script de automação e implementei validação de status no serviço consumidor para garantir a disponibilidade do provider.

Utilizei a biblioteca dateutil.relativedelta para realizar cálculos de diferença de datas (anos/meses) de forma precisa, atendendo ao requisito de formatação do relatório.

Instruções de Execução
cd desafio4
.\executar.ps1

Testar relatório:
curl http://localhost:5001/relatorio/completo

Desafio 5 - API Gateway
Descrição
Implementei um API Gateway como ponto único de entrada.

Arquitetura:
API Gateway (8000): Público.
Serviço de Usuários (5001) e Pedidos (5002): Privados (sem porta exposta ao host).

Como funciona:
O Gateway atua como proxy reverso e agregador. No endpoint /orders/user/<id>, ele orquestra chamadas para os dois microsserviços e combina os dados em uma única resposta JSON.

Decisões Técnicas
A decisão arquitetural chave foi não expor as portas 5001 e 5002 no docker-compose.yml. Desta forma, os microsserviços são acessíveis apenas dentro da rede Docker, simulando uma zona privada (DMZ), obrigando todo o tráfego externo a passar pelo Gateway.

Para evitar o bloqueio de recursos caso um serviço fique lento, implementei timeouts explícitos (timeout=10) em todas as chamadas do Gateway. Adicionalmente, utilizei blocos try/except para capturar falhas e retornar status HTTP 504 (Gateway Timeout), aplicando um padrão simplificado de Circuit Breaker.

Orquestração No endpoint de dashboard, o Gateway realiza a agregação de dados através de chamadas sequenciais aos serviços de backend para compor a resposta final.

Instruções de Execução
cd desafio5
.\executar.ps1

Testar agregação (Dashboard):
curl http://localhost:8000/dashboard

Testar orquestração (Usuário + Pedidos):
curl http://localhost:8000/orders/user/1

Tecnologias Utilizadas
Docker & Docker Compose
Python 3 / Flask
SQLite
Requests Library

Conforme as diretrizes da disciplina, utilizei ferramentas de IA (Copilot/ChatGPT/Gemini) como apoio ao aprendizado e para solução de problemas em cenários específicos onde a documentação padrão não foi suficiente:
Entendimento de Erros: Para diagnosticar a causa raiz do erro de permissão de arquivos em volumes no Windows (no desafio 2) e problemas de race condition na inicialização de containers interdependentes (no desafio 3).
Conceitos de Arquitetura: Para esclarecer as diferenças de implementação entre Health Checks via Docker vs. tratamento de exceções na aplicação.
Sintaxe: Consulta rápida para comandos específicos do PowerShell e flags do Docker CLI.