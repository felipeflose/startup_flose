const fs = require('fs');
const path = require('path');

const BANK_FILE = path.join(__dirname, 'profiles_bank.json');

const FIRST_NAMES = [
  "Gabriel", "Lucas", "Mateus", "Pedro", "João", "Felipe", "Guilherme", "Gustavo", "Thiago", "Bruno",
  "Rodrigo", "Daniel", "Rafael", "André", "Leonardo", "Marcelo", "Arthur", "Vinícius", "Eduardo", "Diego",
  "Luiz", "Carlos", "Antônio", "José", "Francisco", "Marcos", "Paulo", "Fernando", "Alexandre", "Roberto",
  "Julia", "Sofia", "Maria", "Ana", "Laura", "Alice", "Beatriz", "Mariana", "Amanda", "Larissa",
  "Camila", "Carolina", "Letícia", "Luana", "Gabriela", "Isabela", "Helena", "Manuela", "Giovanna", "Juliana",
  "Clara", "Cecília", "Valentina", "Lorena", "Lívia", "Melissa", "Yasmin", "Nicole", "Bianca", "Rafaela",
  "Enzo", "Miguel", "Davi", "Heitor", "Lorenzo", "Samuel", "Benjamin", "Isaac", "Joaquim", "Murilo",
  "Alice", "Sophia", "Valentina", "Helena", "Isabella", "Manuela", "Laura", "Luiza", "Cecília", "Lorena",
  "Roberto", "Julio", "Fabio", "Vitor", "Renan", "Igor", "Caio", "Douglas", "Maurício", "César",
  "Tatiana", "Patrícia", "Aline", "Bruna", "Fernanda", "Vanessa", "Jéssica", "Michele", "Priscila", "Renata"
];

const LAST_NAMES = [
  "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes",
  "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
  "Rocha", "Dias", "Nascimento", "Moreira", "Andrade", "Mendes", "Nunes", "Cardoso", "Teixeira", "Melo",
  "Azevedo", "Freitas", "Pinto", "Cavalcanti", "Castro", "Campos", "Barros", "Cunha", "Macedo", "Guedes",
  "Borges", "Pinheiro", "Machado", "Santana", "Assis", "Dantas", "Coelho", "Miranda", "Farias", "Fonseca",
  "Guimarães", "Viana", "Nogueira", "Muniz", "Moraes", "Paiva", "Peixoto", "Ramos", "Figueiredo", "Sales",
  "Tavares", "Lins", "Coutinho", "Aragão", "Neto", "Brandão", "Queiroz", "Rezende", "Santiago", "Amaral",
  "Motta", "Garrido", "Valente", "Brito", "Maldonado", "Ortega", "Castelo", "Pellegrini", "Sampaio", "Moura",
  "Cardozo", "Montenegro", "Vargas", "Vasconcelos", "Goulart", "Bueno", "Diniz", "Gallo", "Maffei", "Negrão",
  "Cordeiro", "Arruda", "Furtado", "Porto", "Aguiar", "Meireles", "Pires", "Bicalho", "Sarmento", "Pacheco"
];

const MIDDLE_NAMES = [
  "Augusto", "Henrique", "Alexandre", "Junior", "Luis", "Felipe", "Eduardo", "César", "Roberto", "Maria",
  "Regina", "Beatriz", "Aparecida", "Fernanda", "Cristina", "Helena", "Gabriela", "Isabel", "Caroline", "Letícia"
];

const PROFESSIONS = [
  // Technology
  { role: "Desenvolvedor Frontend React Sênior", level: "Analista SR", avatar: "⚛️", category: "Technology",
    adv: "Domina otimização de renderização React, Redux Toolkit e arquiteturas SPA complexas.",
    dis: "Tende a negligenciar layouts responsivos em telas menores por focar em lógica complexa.",
    dil: "Criar Componentes Altamente Customizados vs. Reutilizar Bibliotecas de Componentes Prontos.",
    per: "Inovador, entusiasta de novas tecnologias e focado em experiência de usuário." },
  { role: "Desenvolvedor Backend Node.js Sênior", level: "Analista SR", avatar: "🟢", category: "Technology",
    adv: "Alta capacidade de construir APIs REST/GraphQL assíncronas e gerenciar concorrência pesada.",
    dis: "Dificuldade de documentar endpoints de forma clara e padronizada.",
    dil: "Desenvolver Rotas Altamente Genéricas vs. Criar APIs Específicas e Simples.",
    per: "Lógico, analítico, focado em performance de servidor e focado em eficiência." },
  { role: "Engenheiro de DevOps Cloud Sênior", level: "Analista SR", avatar: "🐳", category: "Technology",
    adv: "Especialista em automação de infraestrutura em nuvem (AWS/GCP), Kubernetes e Docker.",
    dis: "Recusa-se terminantemente a realizar correções manuais emergenciais fora de pipelines de CI/CD.",
    dil: "Automatizar Tudo via GitOps vs. Agilizar Hotfixes Manuais em Produção.",
    per: "Sistemático, focado em segurança operacional e avesso a processos manuais." },
  { role: "Administrador de Banco de Dados Sênior", level: "Analista SR", avatar: "💾", category: "Technology",
    adv: "Especialista em otimização de índices SQL, replicação e auditorias de concorrência.",
    dis: "Muito rígido ao liberar alterações no schema para o time de desenvolvimento.",
    dil: "Segurança de Acesso Rígida vs. Facilidade de Integração de Queries.",
    per: "Cuidadoso, focado na segurança dos dados e metódico com backups." },
  { role: "Engenheiro de IA & Machine Learning Sênior", level: "Analista SR", avatar: "🧠", category: "Technology",
    adv: "Grande experiência com RAG, fine-tuning de modelos LLM e NLP.",
    dis: "Pode demorar muito validando modelos sem focar nas integrações de produto.",
    dil: "Acurácia Absoluta do Modelo vs. Velocidade de Entrega Comercial.",
    per: "Inquisitivo, inovador, focado em dados e entusiasmado com IA." },
  { role: "Analista de Garantia de Qualidade Sênior (QA)", level: "Analista SR", avatar: "🔍", category: "Technology",
    adv: "Cobertura de testes automatizados E2E robustos utilizando Cypress e Playwright.",
    dis: "Exige 100% de cobertura de código para autorizar qualquer deploy.",
    dil: "Rigor nos Casos de Testes Automatizados vs. Agilidade na Release Comercial.",
    per: "Crítico, detalhista, atento a falhas ocultas e realista." },
    
  // Healthcare
  { role: "Psicólogo Organizacional Sênior", level: "Analista SR", avatar: "🧠", category: "Healthcare",
    adv: "Exímio avaliador de saúde mental, mediação de conflitos e cultura corporativa.",
    dis: "Tende a focar em conversações longas, atrasando decisões rápidas de gestão.",
    dil: "Resolução Lenta e Humanizada vs. Decisão Administrativa Direta.",
    per: "Empático, ouvinte atento, mediador e pacificador." },
  { role: "Médico do Trabalho Sênior", level: "Analista SR", avatar: "🩺", category: "Healthcare",
    adv: "Garante conformidade com normas regulamentadoras e exames admissionais/demissionais perfeitos.",
    dis: "Rigidez burocrática elevada com laudos e prazos legais.",
    dil: "Rigor nas Exigências Médicas vs. Agilidade na Contratação do Candidato.",
    per: "Formal, responsável, focado na integridade física e cuidadoso." },

  // Finance & HR
  { role: "Recrutador de Talentos Sênior (Tech Recruiter)", level: "Analista SR", avatar: "🙋‍♂️", category: "HR",
    adv: "Identifica hard/soft skills em minutos e possui excelente network no ecossistema.",
    dis: "Pode priorizar carisma do candidato sobre a real proficiência técnica de engenharia.",
    dil: "Contratar Perfil Técnico Excelente vs. Contratar Alinhamento Cultural Perfeito.",
    per: "Extrovertido, comunicativo, analítico de perfis comportamentais e articulado." },
  { role: "Gerente de Recursos Humanos Sênior", level: "Gerente", avatar: "👥", category: "HR",
    adv: "Elabora planos de cargos e salários atraentes e gerencia engajamento interno.",
    dis: "Dificuldade de aceitar flexibilizações salariais fora das faixas oficiais da empresa.",
    dil: "Retenção com Contratação Fora do Budget vs. Perda de Talento Chave.",
    per: "Estratégico, protetor da cultura corporativa, empático e organizado." },
  { role: "Analista Financeiro Controller Sênior", level: "Analista SR", avatar: "📊", category: "Finance",
    adv: "Modelagem financeira detalhada, controle de custos rígido e auditoria de caixa.",
    dis: "Excessivamente conservador ao aprovar verbas para inovação ou P&D.",
    dil: "Corte de Custos Operacionais vs. Investimento em Novas Ferramentas.",
    per: "Focado em números, pragmático, cauteloso e direto." },

  // Business & Design
  { role: "Designer de Produto Sênior (UI/UX)", level: "Analista SR", avatar: "✨", category: "Design",
    adv: "Cria protótipos de altíssima fidelidade embasados em testes A/B com usuários.",
    dis: "Tende a criar componentes customizados difíceis de implementar no prazo curto.",
    dil: "Interface Inovadora Personalizada vs. Reutilização de Design System Padrão.",
    per: "Criativo, focado na experiência do usuário, observador e inovador." },
  { role: "Product Owner Sênior", level: "Analista SR", avatar: "🎯", category: "Business",
    adv: "Especialista em desdobrar necessidades de clientes em histórias claras e ROI alto.",
    dis: "Às vezes pressiona o time de desenvolvimento por datas irreais.",
    dil: "Features urgentes exigidas pelo comercial vs. Estabilidade da arquitetura de TI.",
    per: "Líder, focado em valor de negócio, negociador e pragmático." }
];

function generateUniqueName(index) {
  const firstName = FIRST_NAMES[index % FIRST_NAMES.length];
  const middleName = MIDDLE_NAMES[Math.floor(index / FIRST_NAMES.length) % MIDDLE_NAMES.length];
  const lastName = LAST_NAMES[Math.floor(index / (FIRST_NAMES.length * MIDDLE_NAMES.length)) % LAST_NAMES.length];
  const uniqueSuffix = Math.floor(index / (FIRST_NAMES.length * MIDDLE_NAMES.length * LAST_NAMES.length));
  
  const suffix = uniqueSuffix > 0 ? ` ${uniqueSuffix + 1}` : "";
  return `${firstName} ${middleName} ${lastName}${suffix}`;
}

function generate45kProfiles() {
  console.log("Generating 45,000 unique profiles procedurally...");
  const profiles = [];
  const totalProfiles = 45000;

  for (let i = 0; i < totalProfiles; i++) {
    const profTemplate = PROFESSIONS[i % PROFESSIONS.length];
    const name = generateUniqueName(i);
    const id = `cand_${i}`;

    // Add unique variants to avoid identical metrics
    const advantage = `${profTemplate.adv} Experiência de ${5 + (i % 12)} anos no mercado.`;
    const disadvantage = `${profTemplate.dis} Sob forte pressão, tende a ser ${i % 2 === 0 ? "reservado" : "centralizador"}.`;
    
    profiles.push({
      id,
      name,
      role: profTemplate.role,
      level: profTemplate.level,
      category: profTemplate.category,
      avatar: profTemplate.avatar,
      advantage: advantage,
      disadvantage: disadvantage,
      dilemma: profTemplate.dil,
      personality: profTemplate.per,
      expectedSalary: 6000 + (i % 15) * 500,
      skills: [profTemplate.category, "Analista SR", "Gemma AI Verified"]
    });

    if (i > 0 && i % 10000 === 0) {
      console.log(`Generated ${i} profiles...`);
    }
  }

  console.log(`Saving ${profiles.length} profiles to database file...`);
  fs.writeFileSync(BANK_FILE, JSON.stringify(profiles, null, 2), 'utf8');
  console.log("Database file saved successfully!");
}

generate45kProfiles();
