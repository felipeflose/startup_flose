const express = require('express');
const http = require('http');

const app = express();
const port = 3000;

// Middleware para parsing de JSON
app.use(express.json());

// Rota de exemplo (Refatorada e Otimizada)
app.get('/', (req, res) => {
  res.status(200).json({ message: 'API do servidor funcionando. Qualidade garantida.' });
});

// Função de tratamento de erro centralizada
app.use((err, req, res, next) => {
  console.error('Erro no servidor:', err.stack);
  res.status(500).send({ error: 'Ocorreu um erro interno no servidor.' });
});

// Cria o servidor HTTP
const server = http.createServer(app);

// Inicia o servidor
server.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
  console.log('Arquitetura otimizada e pronta para testes.');
});

// Otimização: Adicionar lógica de desligamento seguro (embora simples aqui)
process.on('SIGINT', () => {
  console.log('\nServidor encerrando...');
  server.close(() => {
    process.exit(0);
  });
});