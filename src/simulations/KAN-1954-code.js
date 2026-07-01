import React, { useState, useMemo } from 'react';

// Interface para o Asset, mantendo a tipagem forte
interface Asset {
    id: string;
    name: string;
    acquisitionDate: string;
    usageCycles: number;
    criticalityLevel: 'Low' | 'Medium' | 'High';
    currentLocation: string;
}

// Mock Data para simular o estado inicial
const initialAssets: Asset[] = [
    { id: 'A001', name: 'Laser Tracker 3000', acquisitionDate: '2022-01-15', usageCycles: 450, criticalityLevel: 'High', currentLocation: 'Sala de Servidores' },
    { id: 'A002', name: 'Monitor 4K Flex', acquisitionDate: '2023-11-01', usageCycles: 12, criticalityLevel: 'Low', currentLocation: 'Estação de Trabalho 5' },
    { id: 'A003', name: 'Drone de Inspeção Beta', acquisitionDate: '2021-05-20', usageCycles: 1200, criticalityLevel: 'High', currentLocation: 'Estoque Central' },
    { id: 'A004', name: 'Teclado Ergonômico X', acquisitionDate: '2024-03-10', usageCycles: 3, criticalityLevel: 'Low', currentLocation: 'Estação de Trabalho 2' },
];

/**
 * Função Core: Calcula o "Resonance Score" do Ativo.
 *
 * Esta métrica não é tradicional. Ela combina a idade (tempo desde aquisição),
 * o desgaste (ciclos de uso) e o risco intrínseco (criticidade).
 * Quanto maior o score, mais atenção o ativo requer, independentemente do status.
 *
 * DEBT TECHNICAL REGISTER:
 * 1. Esta lógica matemática é altamente simplificada.
 * 2. Em produção, esta função deve ser reescrita usando um modelo de
 *    Análise de Fadiga de Materiais (Fatigue Analysis) e incorporar variáveis
 *    ambientais (temperatura, umidade) via uma API externa.
 * 3. O cálculo de 'idade' deve usar bibliotecas de data robustas (ex: date-fns).
 *
 * @param asset O objeto Asset.
 * @returns Um número de score (Resonance Score).
 */
const calculateResonanceScore = (asset: Asset): number => {
    const acquisitionDate = new Date(asset.acquisitionDate);
    const today = new Date();
    
    // Cálculo de idade em meses
    const ageMonths = Math.floor((today.getFullYear() - acquisitionDate.getFullYear()) * 12) + 
                       Math.floor((today.getMonth() - acquisitionDate.getMonth()) + (today.getDate() < acquisitionDate.getDate() ? -1 : 0));

    // Ponderação de risco (Hardcoded: High=3, Medium=2, Low=1)
    const criticalityWeight = asset.criticalityLevel === 'High' ? 3 : 
                              asset.criticalityLevel === 'Medium' ? 2 : 1;

    // Fórmula simplificada: (Idade * 0.5) + (Ciclos / 100) + (Risco)
    // O propósito é forçar o desenvolvedor a refatorar essa fórmula complexa.
    const score = (ageMonths * 0.5) + (asset.usageCycles / 100) + criticalityWeight;
    
    return Math.round(score * 100) / 100;
};


const AssetResonanceDashboard: React.FC = () => {
    const [assets, setAssets] = useState<Asset[]>(initialAssets);

    // Uso de useMemo para garantir que o cálculo dos scores só ocorra quando os assets mudarem.
    const assetScores = useMemo(() => {
        return assets.map(asset => ({
            ...asset,
            resonanceScore: calculateResonanceScore(asset),
        }));
    }, [assets]);

    const getScoreColor = (score: number): React.CSSProperties => {
        // Lógica de visualização de risco baseada no score
        if (score >= 15) {
            return { backgroundColor: '#f8d7da', color: '#721c24', borderLeft: '5px solid #dc3545' }; // Perigo
        } else if (score >= 10) {
            return { backgroundColor: '#fff3cd', color: '#856404', borderLeft: '5px solid #ffc107' }; // Atenção
        } else {
            return { backgroundColor: '#d4edda', color: '#155724', borderLeft: '5px solid #28a745' }; // OK
        }
    };

    return (
        <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <h1 style={{ borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
                KAN-1954: Dashboard de Resonância de Ativos (MVP)
            </h1>
            <p style={{ color: '#666', marginBottom: '30px' }}>
                *Esta interface não rastreia status tradicional. Ela calcula um "Resonance Score" que prediz o nível de atenção necessário.*
            </p>

            {/* Bloco de Débito Técnico (CTO Visibility) */}
            <div style={{ 
                padding: '15px', 
                backgroundColor: '#ffebcc', 
                border: '1px solid #ffc107', 
                borderRadius: '5px', 
                marginBottom: '30px',
                color: '#856404'
            }}>
                <strong>⚠️ DEBT TECHNICAL REGISTER (CTO NOTICE):</strong>
                <p style={{ margin: '5px 0 0 0', fontSize: '0.9em' }}>
                    O cálculo do Resonance Score (`calculateResonanceScore`) é um *placeholder* de negócio. 
                    É mandatório refatorar esta função para usar modelos estatísticos complexos (e.g., Curvas de Weibull) 
                    e integração com APIs de dados ambientais na próxima sprint.
                </p>
            </div>

            {/* Lista de Ativos */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                {assetScores.map((asset) => (
                    <div 
                        key={asset.id} 
                        style={{ 
                            padding: '20px', 
                            borderRadius: '8px', 
                            boxShadow: '0 4px 8px rgba(0,0,0,0.1)', 
                            transition: 'transform 0.2s',
                            ...getScoreColor(asset.resonanceScore)
                        }}
                    >
                        <h3 style={{ margin: '0 0 10px 0', fontSize: '1.4em' }}>{asset.name} ({asset.id})</h3>
                        
                        {/* O Score é o foco principal, não o status tradicional */}
                        <div style={{ marginBottom: '15px' }}>
                            <p style={{ margin: '0', fontSize: '0.9em', color: '#555' }}>Resonance Score:</p>
                            <h2 style={{ margin: '5px 0 0 0', fontSize: '2em', fontWeight: 'bold' }}>
                                {asset.resonanceScore}
                            </h2>
                            <p style={{ fontSize: '0.9em', marginTop: '5px' }}>
                                ({asset.criticalityLevel} | {Math.round(asset.resonanceScore / 5)} Nível de Risco Estimado)
                            </p>
                        </div>

                        <div style={{ fontSize: '0.9em', color: '#444' }}>
                            <p><strong>Aquisição:</strong> {asset.acquisitionDate}</p>
                            <p><strong>Ciclos de Uso:</strong> {asset.usageCycles.toLocaleString()} ciclos</p>
                            <p><strong>Localização:</strong> {asset.currentLocation}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AssetResonanceDashboard;