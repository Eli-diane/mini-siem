# Mini-SIEM & Segurança de Auditoria de Logs

Sistema leve de gerenciamento de eventos de segurança e auditoria de logs, desenvolvido em Python e Django para monitoramento e rastreabilidade de aplicações em tempo real.

## Sobre o Projeto
Desenvolvido como parte de estudos práticos em **DevSecOps e Cibersegurança**, com foco em estruturar trilhas de auditoria (*audit logs*), sanitização de dados e resposta a incidentes para aplicações web sensíveis.

##  Tecnologias Utilizadas
* **Linguagem/Framework:** Python, Django
* **Frontend:** HTML5, CSS3 Customizado (Design SOC / Cyberpunk), JavaScript assíncrono
* **Segurança:** Gestão de Variáveis de Ambiente (*python-dotenv*), sanitização e trilhas de auditoria imutáveis
* **Controle de Versão:** Git & GitHub

##  Funcionalidades
* **Monitoramento em Tempo Real:** Verificação de status de portas e conexões de rede ativas.
* **Simulação de Incidentes e Alertas:** Gatilhos visuais em tempo real para detecção de anomalias de CPU e tráfego.
* **Painel de Mitigação Integrado:** Suporte à integração com motores de IA para diagnóstico e remediação rápida.
* **Trilha de Auditoria:** Registro detalhado de eventos críticos salvos diretamente no banco de dados.

##  Configuração de Segurança (Variáveis de Ambiente)

Para rodar este projeto com segurança, as chaves sensíveis nunca são expostas no código-fonte. Siga os passos abaixo:

1. Na raiz do projeto, duplique o arquivo `.env.example` e renomeie-o para `.env`.
2. Insira suas credenciais reais dentro do arquivo `.env`:
   ```env
   SECRET_KEY=sua_secret_key_do_django_aqui
   API_KEY=sua_chave_de_api_aqui´´´

#  Como Executar o Projeto Localmente

Clone o repositório:

```bash
git clone https://github.com/Eli-diane/mini-siem.git.git

Acesse a pasta - projeto:

cd mini-siem
Instale as dependências necessárias:


pip install -r requirements.txt
pip install python-dotenv
Aplique as migrações no banco de dados e inicie o servidor:


python manage.py migrate
python manage.py runserver
Acesse no navegador: http://127.0.0.1:8000/ 
```


## 👩‍💻 Autoria

Desenvolvido por **Elidiane Santos**  
[LinkedIn](https://linkedin.com/in/elidiane-santos) | [GitHub](https://github.com/Eli-diane)

---

## Licença e Direitos Autorais

Copyright © 2026 Elidiane Santos. Todos os direitos reservados.  
Este projeto é disponibilizado apenas para fins de visualização e portfólio. É estritamente proibida a reprodução, distribuição ou uso comercial sem autorização prévia.


