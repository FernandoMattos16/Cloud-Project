# Projeto Kubernetes com EKS e FastAPI

Este projeto demonstra o uso do **Amazon EKS (Elastic Kubernetes Service)** para implantar uma aplicação FastAPI integrada a um banco de dados PostgreSQL. O objetivo é criar uma API RESTful funcional, gerenciada em um cluster Kubernetes.

---

## 🎯 Funcionalidades

- API RESTful desenvolvida com **FastAPI**.
- Banco de dados **PostgreSQL** integrado.
- Deploy gerenciado no **Amazon EKS**.
- **Endpoints**:
  - **Registrar**: Cadastra usuários no banco de dados.
  - **Login**: Autentica usuários e retorna um token JWT.
  - **Consultar**: Retorna as cotações das ações da NVIDIA dos últimos 5 dias.

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework para desenvolvimento da API.
- **PostgreSQL**: Banco de dados relacional.
- **Docker**: Containerização dos serviços.
- **Kubernetes**: Orquestração de contêineres.
- **Amazon EKS**: Serviço gerenciado para clusters Kubernetes.

---

## 🚀 Configuração e Implantação

### Pré-requisitos

- Conta na AWS com permissões para criar recursos no **EKS**.
- **kubectl** configurado para acessar o cluster.
- AWS CloudShell (ou CLI local configurada).

### Passos para Configuração

1. **Criar o Cluster no EKS**
   - Primeiro Crie um cluster EKS na AWS isso foi feito seguindo o tutorial no video: [Como criar um cluster Kubernetes na AWS com EKS](https://www.youtube.com/watch?v=JrT5YV1KMeY&t=3585s)
   - Configure o acesso com:
     ```bash
     aws eks --region <sua-regiao> update-kubeconfig --name <nome-do-cluster>
     ```

2. **Aplicar os Arquivos YAML**
   - Faça upload dos arquivos YAML para o ambiente CloudShell:
     - `env-secret.yaml`: Credenciais do PostgreSQL.
     - `postgres-deployment.yaml`: Deployment e Service do PostgreSQL.
     - `api-deployment.yaml`: Deployment e Service da API FastAPI.
   - Aplique os arquivos ao cluster:
     ```bash
     kubectl apply -f env-secret.yaml
     kubectl apply -f postgres-deployment.yaml
     kubectl apply -f api-deployment.yaml
     ```

3. **Verificar os Recursos no Cluster**
   - Liste os pods:
     ```bash
     kubectl get pods -n app
     ```
   - Liste os serviços:
     ```bash
     kubectl get svc -n app
     ```

4. **Testar os Endpoints**
   - Use o IP externo do serviço da API para acessar os endpoints. Exemplo:
     ```bash
     curl -X POST http://<EXTERNAL-IP>/registrar -d '{"nome":"user", "email":"user@example.com", "senha":"123456"}' -H "Content-Type: application/json"
     ```

---

## 🎥 Demonstração

[Vídeo de demonstração](https://youtu.be/8QZQBffF7eU)

---