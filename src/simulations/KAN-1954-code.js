import React, { useState, useCallback, useMemo } from 'react';

// Interfaces for type safety
interface Asset {
  id: string;
  name: string;
  resonanceSignature: number; // Non-traditional metric
  temporalDriftFactor: number; // How far off schedule it is
}

interface ScanResult {
  assetId: string;
  resonanceScore: number;
  status: 'Optimal' | 'Caution' | 'Critical';
  recommendation: string;
}

// --- Utility Functions (Mocking Complex Backend Logic) ---

/**
 * Calculates the 'Resonance Score' based on non-linear asset metrics.
 * This is the core, non-traditional logic.
 * @param asset - The asset object.
 * @returns A complex, derived score.
 */
const calculateResonanceScore = (asset: Asset): number => {
  // Mocking a complex, non-linear calculation that shouldn't be client-side.
  // CTO Debt Marker: This calculation needs to be moved to a dedicated microservice (e.g., /api/v2/resonance)
  // and handled with proper type checking for floating point arithmetic.
  const baseScore = asset.resonanceSignature * Math.pow(1.1, asset.temporalDriftFactor);
  let finalScore = baseScore / Math.sqrt(asset.id.length + 1);

  // Introduce a simple, arbitrary decay factor for demonstration
  if (asset.temporalDriftFactor > 0.8) {
    finalScore *= 0.8;
  }
  return parseFloat(finalScore.toFixed(2));
};

/**
 * Determines the asset status based on the calculated score.
 */
const determineStatus = (score: number): { status: ScanResult['status']; recommendation: string } => {
  if (score > 150) {
    return { status: 'Optimal', recommendation: 'Flux stable. Monitor passively.' };
  } else if (score >= 80) {
    return { status: 'Caution', recommendation: 'Drift detected. Recommend recalibrating the temporal anchor.' };
  } else {
    return { status: 'Critical', recommendation: 'Resonance collapse imminent. Isolate the asset immediately.' };
  }
};

// --- Components ---

/**
 * Component simulating the main scanning interface.
 * This is the "quick delivery" part (CEO).
 */
const ResonanceScanner: React.FC<{ assets: Asset[]; setAssets: React.Dispatch<React.SetStateAction<Asset[]>> }> = ({ assets, setAssets }) => {
  const [scanResults, setScanResults] = useState<ScanResult[]>([]);
  const [loading, setLoading] = useState(false);

  const runScan = useCallback(() => {
    if (assets.length === 0) {
      alert("Nenhum ativo registrado para o escaneamento.");
      return;
    }

    setLoading(true);
    setScanResults([]);

    // Simulate API latency
    setTimeout(() => {
      const results: ScanResult[] = assets.map(asset => {
        const score = calculateResonanceScore(asset);
        const { status, recommendation } = determineStatus(score);
        return { assetId: asset.id, resonanceScore: score, status, recommendation };
      });

      setScanResults(results);
      setLoading(false);
    }, 800);
  }, [assets]);

  return (
    <div className="scanner-panel">
      <h2><span role="img" aria-label="📡">📡</span> Resonance Scanner v0.1 (KAN-1954)</h2>
      <p className="debt-note">
        ⚠️ **[CTO Debt Marker]:** A lógica de escaneamento está hardcoded neste componente. 
        Deve ser refatorada para um Hook customizado (`useResonanceScan`) e consumir um endpoint assíncrono real.
      </p>
      
      <button 
        onClick={runScan} 
        disabled={loading} 
        className="scan-button"
      >
        {loading ? 'Escaneando Fluxo...' : 'Executar Escaneamento de Ativos'}
      </button>

      {scanResults.length > 0 && (
        <div className="results-grid">
          <h3>Resultados de Fluxo:</h3>
          {scanResults.map((result, index) => (
            <div key={index} className={`result-card status-${result.status.toLowerCase()}`}>
              <p><strong>Ativo ID:</strong> {result.assetId}</p>
              <p><strong>Resonance Score:</strong> {result.resonanceScore}</p>
              <p><strong>Status:</strong> {result.status}</p>
              <p className="recommendation-text">Recomendação: {result.recommendation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

/**
 * Component for adding assets (simplified, mock input).
 * This is the 'quick delivery' input mechanism.
 */
const AssetInputForm: React.FC<{ setAssets: React.Dispatch<React.SetStateAction<Asset[]>> }> = ({ setAssets }) => {
  const [name, setName] = useState('');
  const [signature, setSignature] = useState('');
  const [drift, setDrift] = useState('');

  const handleAddAsset = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Basic validation and type conversion
    const newAsset: Asset = {
      id: `A-${Date.now()}`,
      name: name || `Ativo ${Math.floor(Math.random() * 100)}`,
      resonanceSignature: parseFloat(signature) || 0,
      temporalDriftFactor: parseFloat(drift) || 0,
    };

    setAssets(prevAssets => [...prevAssets, newAsset]);
    
    // Reset form
    setName('');
    setSignature('');
    setDrift('');
  };

  return (
    <div className="input-form">
      <h3>Registrar Novo Ativo (Input Simplificado)</h3>
      <form onSubmit={handleAddAsset}>
        <input
          type="text"
          placeholder="Nome do Ativo (Ex: Gerador Temporal)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Sinalização de Ressonância (0-1000)"
          value={signature}
          onChange={(e) => setSignature(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Fator de Deriva Temporal (0-1)"
          value={drift}
          onChange={(e) => setDrift(e.target.value)}
          required
        />
        <button type="submit" className="add-button">Adicionar e Registrar</button>
      </form>
    </div>
  );
};

/**
 * Main Application Component.
 */
const AssetControlSystem: React.FC = () => {
  // State to hold the list of assets
  const [assets, setAssets] = useState<Asset[]>([
    { id: 'A-1001', name: 'Núcleo de Energia Prime', resonanceSignature: 950, temporalDriftFactor: 0.2 },
    { id: 'A-1002', name: 'Transmissor de Dados Quânticos', resonanceSignature: 450, temporalDriftFactor: 0.9 },
    { id: 'A-1003', name: 'Unidade de Estabilização', resonanceSignature: 70, temporalDriftFactor: 0.1 },
  ]);

  // Memoize the list of assets for display
  const assetListDisplay = useMemo(() => (
    <div className="asset-list">
      <h3>Ativos Registrados ({assets.length})</h3>
      {assets.map((asset) => (
        <div key={asset.id} className="asset-card">
          <h4>{asset.name}</h4>
          <p>ID: {asset.id}</p>
          <p>Resonance Signature: {asset.resonanceSignature}</p>
          <p>Temporal Drift: {Math.round(asset.temporalDriftFactor * 100)}%</p>
        </div>
      ))}
    </div>
  ), [assets]);

  return (
    <div className="asset-control-system">
      <h1>Sistema de Controle de Ativos (KAN-1954)</h1>
      <p className="system-meta">
        <strong>Status:</strong> Implementação Rápida (CEO). 
        <strong>Próxima Ação:</strong> Refatoração Estrutural (CTO Debt).
      </p>
      
      <div className="main-layout">
        <div className="input-area">
          {assetListDisplay}
          <AssetInputForm setAssets={setAssets} />
        </div>
        <div className="scanner-area">
          <ResonanceScanner assets={assets} setAssets={setAssets} />
        </div>
      </div>
    </div>
  );
};

export default AssetControlSystem;

// Note: This code assumes a basic CSS setup for demonstration purposes, 
// but only the functional component structure is provided as required.
/* 
// Example CSS structure required for proper rendering:
.asset-control-system { font-family: sans-serif; padding: 20px; }
.system-meta { background: #ffe0b2; padding: 10px; border-left: 4px solid orange; margin-bottom: 20px; }
.main-layout { display: flex; gap: 40px; }
.input-area, .scanner-area { flex: 1; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
.asset-card, .result-card { border: 1px solid #eee; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
.status-optimal { background-color: #e8f5e9; border-left: 4px solid green; }
.status-caution { background-color: #fff9c4; border-left: 4px solid orange; }
.status-critical { background-color: #ffcdd2; border-left: 4px solid red; }
.scan-button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; margin-top: 15px; }
.debt-note { background-color: #f5f5f5; padding: 10px; border-radius: 4px; color: #d32f2f; }
*/