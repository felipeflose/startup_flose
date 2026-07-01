import React, { useState, useCallback } from 'react';

// --- MOCKS & TYPES ---
type Module = 'MM' | 'SD' | 'Dashboard';

interface SystemState {
    currentModule: Module;
    inventory: Record<string, number>;
    salesOrders: string[];
}

// Mock service simulating Cortex integration with GCP (e.g., BigQuery or Cloud Functions)
const callGcpIntegration = async (action: string, payload: any): Promise<string> => {
    console.log(`[GCP/Cortex] Initiating ${action} check...`);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network latency

    if (action === 'STOCK_CHECK') {
        const sku = payload.sku;
        const stock = Math.floor(Math.random() * 50) + 10;
        return `[SUCCESS] SKU ${sku}: Stock level verified. Available units: ${stock}.`;
    }
    if (action === 'INVOICE_GEN') {
        return `[SUCCESS] Invoice generated successfully via GCP service. Document ID: ${Date.now().toString().slice(-6)}`;
    }
    return `[INFO] Operation ${action} completed successfully.`;
};

// --- COMPONENTS ---

// 1. Module Card Component
const ModuleCard: React.FC<{ module: Module; title: string; description: string; onClick: (m: Module) => void }> = ({ module, title, description, onClick }) => (
    <div 
        onClick={() => onClick(module)} 
        className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition duration-150 cursor-pointer flex flex-col justify-center items-center text-center"
    >
        <h3 className="text-xl font-semibold text-indigo-600">{title}</h3>
        <p className="text-sm text-gray-500 mt-1">{description}</p>
        <p className="text-xs mt-2 text-indigo-500/70">Clique para acessar</p>
    </div>
);

// 2. MM Module (Materials Management)
const MMModule: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [sku, setSku] = useState('');
    const [message, setMessage] = useState('');

    const handleStockCheck = useCallback(async () => {
        if (!sku) {
            setMessage('Por favor, insira um SKU.');
            return;
        }
        setMessage('Verificando estoque via GCP...');
        const result = await callGcpIntegration('STOCK_CHECK', { sku });
        setMessage(result);
    }, [sku]);

    return (
        <div className="p-6 bg-gray-50 rounded-lg shadow-inner">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">📦 MM - Materials Management</h2>
            <p className="mb-6 text-sm text-gray-600">Gestão de Inventário e Compras.</p>

            <div className="bg-white p-6 rounded-lg shadow-lg border border-yellow-200">
                <h3 className="text-xl font-semibold mb-4 text-yellow-700">Verificação de Estoque (GCP Integration)</h3>
                <div className="flex gap-4 mb-4">
                    <input
                        type="text"
                        value={sku}
                        onChange={(e) => setSku(e.target.value)}
                        placeholder="Ex: ABC-123"
                        className="flex-grow p-2 border border-gray-300 rounded focus:ring-yellow-500 focus:border-yellow-500"
                    />
                    <button
                        onClick={handleStockCheck}
                        className="px-6 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition duration-150"
                    >
                        Checar Estoque
                    </button>
                </div>
                {message && (
                    <div className={`mt-4 p-3 rounded ${message.includes('[SUCCESS]') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                        {message}
                    </div>
                )}
            </div>
            
            <button onClick={onBack} className="mt-8 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
                &larr; Voltar ao Dashboard
            </button>
        </div>
    );
};

// 3. SD Module (Sales & Distribution)
const SDModule: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [customerId, setCustomerId] = useState('');
    const [message, setMessage] = useState('');

    const handleInvoiceGeneration = useCallback(async () => {
        if (!customerId) {
            setMessage('Por favor, insira um ID de Cliente.');
            return;
        }
        setMessage('Gerando fatura via GCP...');
        const result = await callGcpIntegration('INVOICE_GEN', { customerId });
        setMessage(result);
    }, []);

    return (
        <div className="p-6 bg-gray-50 rounded-lg shadow-inner">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">🛒 SD - Sales & Distribution</h2>
            <p className="mb-6 text-sm text-gray-600">Gestão de Pedidos de Venda e Faturamento.</p>

            <div className="bg-white p-6 rounded-lg shadow-lg border border-green-200">
                <h3 className="text-xl font-semibold mb-4 text-green-700">Faturamento de Pedido (GCP Integration)</h3>
                <div className="flex gap-4 mb-4">
                    <input
                        type="text"
                        value={customerId}
                        onChange={(e) => setCustomerId(e.target.value)}
                        placeholder="ID Cliente (Ex: CUST-001)"
                        className="flex-grow p-2 border border-gray-300 rounded focus:ring-green-500 focus:border-green-500"
                    />
                    <button
                        onClick={handleInvoiceGeneration}
                        className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition duration-150"
                    >
                        Gerar Fatura
                    </button>
                </div>
                {message && (
                    <div className={`mt-4 p-3 rounded ${message.includes('[SUCCESS]') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                        {message}
                    </div>
                )}
            </div>
            
            <button onClick={onBack} className="mt-8 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
                &larr; Voltar ao Dashboard
            </button>
        </div>
    );
};


// 4. Main Dashboard Component
const SystemDashboard: React.FC = () => {
    const [state, setState] = useState<SystemState>({
        currentModule: 'Dashboard',
        inventory: { 'ABC-123': 150, 'XYZ-999': 45 },
        salesOrders: ['SO-1001', 'SO-1002']
    });

    const setModule = useCallback((module: Module) => {
        setState(prevState => ({ ...prevState, currentModule: module }));
    }, []);

    const renderContent = () => {
        switch (state.currentModule) {
            case 'MM':
                return <MMModule onBack={() => setModule('Dashboard')} />;
            case 'SD':
                return <SDModule onBack={() => setModule('Dashboard')} />;
            case 'Dashboard':
            default:
                return (
                    <div className="p-6">
                        <h2 className="text-3xl font-extrabold mb-2 text-indigo-700">
                            Flose ERP Core System (v0.1)
                        </h2>
                        <p className="text-gray-500 mb-8">
                            Sistema de Gestão Modular (SAP Style) - KAN-1941
                        </p>

                        {/* --- Technical Debt Notice (For CTO) --- */}
                        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8" role="alert">
                            <p className="font-bold">⚠️ TECHNICAL DEBT WARNING (CTO Review)</p>
                            <p className="text-sm">
                                A gestão de estado é feita via `useState` e prop-drilling. Para escala, deve ser refatorado para um Context API ou Redux/Zustand para evitar problemas de performance e complexidade de manutenção.
                            </p>
                        </div>
                        {/* --------------------------------------- */}

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <ModuleCard 
                                module="MM" 
                                title="Materials Mgmt (MM)" 
                                description="Controle de estoque, recebimento e requisição de materiais." 
                                onClick={setModule} 
                            />
                            <ModuleCard 
                                module="SD" 
                                title="Sales & Distribution (SD)" 
                                description="Gestão de pedidos, faturamento e logística de vendas." 
                                onClick={setModule} 
                            />
                            <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg shadow-sm flex flex-col justify-center items-center text-center cursor-default">
                                <h3 className="text-xl font-semibold text-indigo-700">Dashboard</h3>
                                <p className="text-sm text-gray-500 mt-1">Visão geral e relatórios rápidos.</p>
                            </div>
                        </div>

                        <div className="mt-12 p-6 bg-gray-100 rounded-lg shadow-inner">
                            <h3 className="text-xl font-bold mb-3 text-gray-700">Status do Sistema</h3>
                            <p className="text-sm text-gray-600">
                                Integração de Backend: Cortex/GCP (Simulado).
                            </p>
                            <p className="text-sm text-gray-600 mt-1">
                                Últimos Pedidos (SD): {state.salesOrders.join(', ')}
                            </p>
                            <p className="text-sm text-gray-600 mt-1">
                                Inventário Crítico (MM): {Object.keys(state.inventory).length} SKUs monitorados.
                            </p>
                        </div>
                    </div>
                );
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            {renderContent()}
        </div>
    );
};

export default SystemDashboard;