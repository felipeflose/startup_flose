const candidateData = [
    { name: "Alice", experienceYears: 10, domainExpertiseScore: 85, leadershipRating: 90 },
    { name: "Bob", experienceYears: 5, domainExpertiseScore: 70, leadershipRating: 75 },
    { name: "Charlie", experienceYears: 12, domainExpertiseScore: 92, leadershipRating: 88 }
];

function evaluateCandidates(candidates) {
    let bestCandidate = null;
    let maxScore = -1;

    for (const candidate of candidates) {
        // Simplified scoring mechanism reflecting the CEO's immediate need for speed
        const combinedScore = (candidate.domainExpertiseScore * 0.5) + (candidate.leadershipRating * 0.5);

        if (combinedScore > maxScore) {
            maxScore = combinedScore;
            bestCandidate = candidate;
        }
    }

    return {
        recommendation: bestCandidate,
        score: maxScore,
        details: candidates
    };
}

function hireAIExecutive() {
    const results = evaluateCandidates(candidateData);

    console.log("--- AI Executive Hiring Simplificada (Sprint Atual) ---");
    if (results.recommendation) {
        console.log(`Recomendação Rápida (CEO): Contratar ${results.recommendation.name}`);
        console.log(`Pontuação Combinada: ${results.score.toFixed(2)}`);
    } else {
        console.log("Nenhum candidato encontrado para recomendação.");
    }

    // Débito Técnico Registrado (CTO): A complexidade real da avaliação e refinamento dos pesos de score será tratada na próxima sprint.
    console.log("\n--- Débito Técnico Registrado ---");
    console.log("A lógica de pontuação foi simplificada. Refatoração para incluir fatores de custo, alinhamento cultural e análise preditiva avançada será implementada na próxima Sprint (CTO).");
}

hireAIExecutive();