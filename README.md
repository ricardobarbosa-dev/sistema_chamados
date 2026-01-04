# 🎫 Sistema de Chamados (Ticket System)

Sistema completo de **gerenciamento de chamados** desenvolvido com **Django**, focado em regras de negócio reais, controle de leitura, notificações inteligentes e experiência de usuário moderna.

Este projeto foi pensado para **uso profissional**, **portfólio**, **faculdade** e **base sólida para evolução**.

---

## 🚀 Funcionalidades Principais

### 👤 Autenticação
- Login e logout
- Recuperação e alteração de senha
- Proteção de rotas com permissões

### 🎟️ Chamados
- Criar, editar e excluir chamados
- Listagem de chamados por usuário
- Admin visualiza todos os chamados
- Controle de status: **Aberto / Em andamento / Fechado**

### 🔔 Notificações
- Sistema de notificações com sino 🔔
- Badge com contador de não lidas
- Marcação automática como lida ao acessar o chamado
- Notificações para:
  - Mudança de status
  - Nova resposta

### 📌 Histórico & Timeline
- Timeline unificada por chamado
- Registro de:
  - Alterações de status
  - Respostas de usuários/admin
- Destaque visual para itens **não lidos**
- Marcação automática de leitura

### 🧠 Regras de Negócio
- Usuário comum **não responde chamado fechado**
- Admin pode responder e alterar status sempre
- Usuário só acessa seus próprios chamados
- Admin acessa todos
- Chamado fechado não pode ser editado por usuário comum

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Django 6.0**
- **SQLite** (pode ser alterado)
- **TailwindCSS (CDN)**
- HTML5 + CSS3 + JavaScript

---

## 📂 Estrutura do Projeto

```
sistema_chamados/
├── chamados/
│   ├── migrations/
│   ├── templates/
│   │   └── chamados/
│   ├── models.py
│   ├── views.py
│   ├── context_processors.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   └── base.html
├── static/
├── manage.py
└── requirements.txt
```

---

## ▶️ Como Rodar o Projeto

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar
venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Migrar banco
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

---

## 👥 Perfis de Usuário

### 👤 Usuário Comum
- Criar chamados
- Responder chamados abertos
- Acompanhar status
- Receber notificações

### 🛡️ Administrador
- Visualiza todos os chamados
- Altera status
- Responde qualquer chamado
- Exclui chamados

---

## 📌 Status do Projeto

✅ **Concluído (MVP sólido)**  
🔧 Pronto para produção com pequenos ajustes

---

## 🔮 Possíveis Evoluções Futuras

- WebSocket (Django Channels) para notificações em tempo real
- API REST com Django REST Framework
- Upload de anexos
- SLA por chamado
- Dashboard administrativo
- Testes automatizados
- Deploy (Railway / Render / VPS)

---

## 🧑‍💻 Autor

Projeto desenvolvido por **Ricardo Barbosa**  
Foco em aprendizado profundo, regras de negócio e arquitetura limpa.

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!
