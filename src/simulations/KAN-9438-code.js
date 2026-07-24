const express = require('express');
const app = express();
const PORT = 3000;

// Middleware para parsear JSON
app.use(express.json());

/**
 * Função de tratamento de erro centralizada.
 * Esta função garante que todos os erros sejam respondidos de forma consistente.
 * @param {Error} err O erro a ser tratado.
 * @param {object} req Objeto de requisição (necessário para contexto).
 * @param {object} res Objeto de resposta (necessário para enviar a resposta).
 */
const errorHandler = (err, req, res, next) => {
    console.error('ERRO FATAL NO SERVIDOR:', err.stack);

    // Determinar o status code e a mensagem de erro
    let statusCode = err.status || 500;
    let message = err.message || 'Erro interno do servidor.';

    // Se for um erro de validação customizado, pode usar um código diferente
    if (err.isValidationError) {
        statusCode = 400;
        message = err.message;
    }

    // Enviar a resposta ao cliente
    res.status(statusCode).json({
        success: false,
        error: {
            status: statusCode,
            message: message,
        }
    });
};

// Middleware para tratar erros de rota (catch errors thrown by route handlers)
app.use((err, req, res, next) => {
    // Se o erro já foi processado pelo errorHandler, não o reprocessamos
    if (res.headersSent) {
        return;
    }
    // Passa o erro para o handler central
    errorHandler(err, req, res, next);
});


// --- Rotas de Exemplo com Tratamento de Erros Refatorado ---

// Rota que simula um erro de validação
app.post('/api/data', (req, res, next) => {
    const { value } = req.body;
    if (value === undefined || isNaN(Number(value))) {
        // Lança um erro customizado que será capturado pelo middleware
        const error = new Error('Valor inválido fornecido.');
        error.isValidationError = true; // Flag para o handler
        return next(error);
    }
    res.status(201).json({ success: true, data: `Valor processado: ${value}` });
});

// Rota que simula um erro interno (erro de banco de dados, etc.)
app.get('/api/fail', (req, res, next) => {
    // Simula uma falha crítica
    throw new Error('Falha de conexão com o serviço externo.');
});


// Rota de sucesso
app.get('/', (req, res) => {
    res.send('Servidor rodando com sucesso.');
});

// Aplica o middleware de tratamento de erros no final
app.use(errorHandler);


// Iniciar o servidor
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});