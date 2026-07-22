const axios = require('axios');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

if (!JIRA_HOST || !JIRA_USER || !JIRA_TOKEN) {
  console.error("Missing JIRA credentials in .env file.");
  process.exit(1);
}

const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
const base64Credentials = Buffer.from(credentials).toString('base64');
const headers = {
  'Authorization': `Basic ${base64Credentials}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
};

const IMPROVEMENTS = [
  {
    summary: "Refatorar server.cjs para ES Modules",
    description: "Converter require() em import/export no server.cjs para alinhar com o type:module do package.json do ecossistema Node da startup."
  },
  {
    summary: "Implementar Rate Limiting nos endpoints da API local",
    description: "Adicionar express-rate-limit no backend para proteger os proxies de chamadas ao Jira e ao motor de IA contra abusos de requisições."
  },
  {
    summary: "Adicionar Error Boundary global no React Frontend",
    description: "Implementar componente de captura de erros globais no React (App.tsx) para evitar tela branca em caso de falha de renderização de cards."
  },
  {
    summary: "Implementar testes unitários com Vitest para componentes UI",
    description: "Escrever testes automatizados para verificar a integridade visual e interativa dos componentes OrgChart, AgentCard e GemmaConsole."
  },
  {
    summary: "Configurar Pipeline CI/CD com GitHub Actions",
    description: "Criar workflow do GitHub Actions (.github/workflows) para rodar npm run lint e npm run build automaticamente em cada Pull Request."
  },
  {
    summary: "Conectar motor Gemma 4 a API real de LLM (Vertex AI / Gemini)",
    description: "Substituir as respostas estáticas da sala de debate por chamadas de API reais com base no prompt de dilema de cada agente."
  },
  {
    summary: "Adicionar cache em memória para busca de 45k candidatos",
    description: "Implementar cache em memória ou Redis no backend para acelerar a paginação e busca no banco de 45.000 perfis."
  },
  {
    summary: "Criar gráfico de Burn Rate Financeiro no RH",
    description: "Exibir a soma de salários pretendidos/pagos de todos os agentes ativos contratados comparado com o orçamento inicial da startup."
  },
  {
    summary: "Otimizar paginação de candidatos no backend",
    description: "Modificar o endpoint /api/candidates para fatiar o arquivo JSON de 45k em streams de leitura em vez de carregar tudo em memória a cada GET."
  },
  {
    summary: "Adicionar Sanitização contra XSS nos inputs de novos tickets",
    description: "Utilizar biblioteca DOMPurify ou similar no input de novos tickets para evitar injeção de scripts maliciosos nos debates de agentes."
  }
];

async function createImprovementCards() {
  console.log(`Starting creation of ${IMPROVEMENTS.length} improvement cards on Jira...`);
  
  for (const card of IMPROVEMENTS) {
    try {
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: `MELHORIA INTERNA: ${card.summary}`,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: card.description,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          issuetype: { name: 'Task' }
        }
      };

      const response = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, { headers });
      console.log(`Created card ${response.data.key} successfully: ${card.summary}`);
    } catch (err) {
      console.error(`Failed to create card: ${card.summary}. Error: ${err.message}`);
    }
  }
  
  console.log("All improvement cards created successfully!");
}

createImprovementCards();
