import React, { useState, useEffect } from 'react';

export interface PrototypeItem {
  id: string;
  issueKey: string;
  issueSummary: string;
  executorName?: string;
  executorRole?: string;
  gitBranchName?: string;
  commitHash?: string;
  status?: string;
  creatorName?: string;
  codeSnippet?: string;
  description?: string;
}

interface PrototypeViewerProps {
  decisions: any[];
  jiraIssues: any[];
  commits: Record<string, any>;
}

export const PrototypeViewer: React.FC<PrototypeViewerProps> = ({ decisions, jiraIssues, commits }) => {
  const [items, setItems] = useState<PrototypeItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'done' | 'in_progress' | 'gemma'>('all');
  const [viewportMode, setViewportMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [activeTab, setActiveTab] = useState<'preview' | 'code' | 'spec'>('preview');
  const [realCode, setRealCode] = useState<string>('');

  useEffect(() => {
    const selectedItem = items.find(i => i.id === selectedId) || items[0];
    if (!selectedItem) return;
    setRealCode('Carregando código fonte...');
    const ext = selectedItem.issueSummary.toLowerCase().match(/tela|layout|login|visual|ui|ux|componente|botao|modal|tabela|card|jogo|velha/) ? 'tsx' : 'js';
    const filePath = `src/simulations/${selectedItem.issueKey}-code.${ext}`;
    fetch(`http://localhost:5001/api/code?file=${encodeURIComponent(filePath)}`)
      .then(res => res.json())
      .then(data => {
        if (data.content) {
          setRealCode(data.content);
        } else {
          const fallbackPath = `docs/simulations/${selectedItem.issueKey}-code.md`;
          return fetch(`http://localhost:5001/api/code?file=${encodeURIComponent(fallbackPath)}`)
            .then(res => res.json())
            .then(data2 => {
              setRealCode(data2.content || 'Código fonte não disponível.');
            });
        }
      })
      .catch(err => {
        setRealCode('Falha ao carregar código fonte: ' + err.message);
      });
  }, [selectedId, items]);

  // Combine Chamber decisions and Jira issues into unified Prototypes list
  useEffect(() => {
    const list: PrototypeItem[] = [];

    // Add Chamber decisions
    decisions.forEach(d => {
      list.push({
        id: d.id || d.issueKey,
        issueKey: d.issueKey || 'KAN-CHAMBER',
        issueSummary: d.issueSummary || d.decision || 'Entrega Autônoma',
        executorName: d.executorName || 'Equipe Flose',
        executorRole: d.executorRole || 'Developer Sênior',
        gitBranchName: d.gitBranchName || 'feature/autonoma',
        commitHash: d.commitHash || commits[d.issueKey]?.shortSha || 'HEAD',
        status: d.status || 'Done',
        description: d.decision
      });
    });

    // Add Jira issues (especially Gemma 4 generated cards)
    jiraIssues.forEach(j => {
      const exists = list.some(i => i.issueKey === j.key);
      if (!exists) {
        const descText = j.fields?.description?.content?.[0]?.content?.[0]?.text || '';
        list.push({
          id: j.key,
          issueKey: j.key,
          issueSummary: j.fields?.summary || j.key,
          executorName: j.executorName || 'Agente Dev',
          executorRole: 'Engenheiro Flose',
          gitBranchName: `feature/${j.key.toLowerCase()}`,
          commitHash: commits[j.key]?.shortSha || 'head',
          status: j.fields?.status?.name || 'In Progress',
          creatorName: j.creatorName,
          description: descText
        });
      }
    });

    setItems(list);
    if (list.length > 0 && !selectedId) {
      setSelectedId(list[0].id);
    }
  }, [decisions, jiraIssues, commits]);

  const filteredItems = items.filter(item => {
    const text = `${item.issueKey} ${item.issueSummary} ${item.executorName} ${item.creatorName}`.toLowerCase();
    const matchesSearch = text.includes(search.toLowerCase());

    if (!matchesSearch) return false;
    if (filter === 'done') return item.status?.toLowerCase().includes('done') || item.status?.toLowerCase().includes('concluid');
    if (filter === 'in_progress') return item.status?.toLowerCase().includes('progress') || item.status?.toLowerCase().includes('andamento');
    if (filter === 'gemma') return item.issueSummary.includes('[Gemma4]') || item.issueSummary.includes('Gemma');
    return true;
  });

  const selectedItem = items.find(i => i.id === selectedId) || filteredItems[0] || items[0];



  const githubCommit = selectedItem ? commits[selectedItem.issueKey] : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', width: '100%', textWrap: 'wrap' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
        <div style={{ textAlign: 'left' }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
            Protótipos & <span className="text-gradient">Telas Autônomas</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: '4px 0 0 0' }}>
            Visualizador interativo em tempo real das entregas e interfaces geradas pelo Motor Gemma 4.
          </p>
        </div>

        {/* Viewport Resizer Controls */}
        <div className="glass" style={{ padding: '6px 12px', display: 'flex', gap: '8px', alignItems: 'center', borderRadius: '10px' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, marginRight: '4px' }}>Modo de Exibição:</span>
          <button
            onClick={() => setViewportMode('desktop')}
            style={{
              padding: '6px 12px', borderRadius: '6px', border: 'none',
              background: viewportMode === 'desktop' ? 'var(--color-primary)' : 'transparent',
              color: '#fff', fontSize: '0.78rem', fontWeight: 600, cursor: 'pointer'
            }}
          >
            💻 Desktop (100%)
          </button>
          <button
            onClick={() => setViewportMode('tablet')}
            style={{
              padding: '6px 12px', borderRadius: '6px', border: 'none',
              background: viewportMode === 'tablet' ? 'var(--color-primary)' : 'transparent',
              color: '#fff', fontSize: '0.78rem', fontWeight: 600, cursor: 'pointer'
            }}
          >
            🖥️ Tablet (900px)
          </button>
          <button
            onClick={() => setViewportMode('mobile')}
            style={{
              padding: '6px 12px', borderRadius: '6px', border: 'none',
              background: viewportMode === 'mobile' ? 'var(--color-primary)' : 'transparent',
              color: '#fff', fontSize: '0.78rem', fontWeight: 600, cursor: 'pointer'
            }}
          >
            📱 Mobile (390px)
          </button>
        </div>
      </div>

      {/* Layout Principal (Sidebar 300px + Canvas Flexível 1fr) */}
      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px', alignItems: 'start', width: '100%' }}>
        
        {/* Sidebar Seletora de Entregas */}
        <div className="glass" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700, margin: 0, color: 'var(--text-secondary)' }}>
              📄 Entregas & Telas ({filteredItems.length})
            </h3>
          </div>

          {/* Search & Filters */}
          <input
            type="text"
            placeholder="🔍 Buscar entregas..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              padding: '8px 12px', borderRadius: '6px', background: 'var(--bg-secondary)',
              border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.8rem', outline: 'none'
            }}
          />

          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            <button onClick={() => setFilter('all')} style={{ padding: '3px 8px', borderRadius: '4px', border: 'none', background: filter === 'all' ? 'var(--color-primary)' : 'var(--bg-tertiary)', color: '#fff', fontSize: '0.7rem', cursor: 'pointer' }}>Todos</button>
            <button onClick={() => setFilter('gemma')} style={{ padding: '3px 8px', borderRadius: '4px', border: 'none', background: filter === 'gemma' ? '#8b5cf6' : 'var(--bg-tertiary)', color: '#fff', fontSize: '0.7rem', cursor: 'pointer' }}>🤖 Gemma 4</button>
            <button onClick={() => setFilter('done')} style={{ padding: '3px 8px', borderRadius: '4px', border: 'none', background: filter === 'done' ? '#10b981' : 'var(--bg-tertiary)', color: '#fff', fontSize: '0.7rem', cursor: 'pointer' }}>🏆 Concluídos</button>
          </div>

          {/* List of Prototype Deliverables */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '640px', overflowY: 'auto' }}>
            {filteredItems.length === 0 ? (
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>Nenhuma entrega encontrada.</span>
            ) : (
              filteredItems.map((item) => {
                const isSelected = selectedItem?.id === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setSelectedId(item.id);
                    }}
                    style={{
                      padding: '12px',
                      borderRadius: '8px',
                      border: isSelected ? '1px solid var(--color-primary)' : '1px solid var(--border-color)',
                      background: isSelected ? 'rgba(139, 92, 246, 0.12)' : 'var(--bg-secondary)',
                      color: isSelected ? '#fff' : 'var(--text-primary)',
                      cursor: 'pointer',
                      textAlign: 'left',
                      width: '100%',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.75rem', color: isSelected ? 'var(--color-primary)' : '#9ca3af' }}>{item.issueKey}</span>
                      <span style={{ fontSize: '0.65rem', padding: '1px 6px', borderRadius: '4px', background: item.status?.includes('Done') ? 'rgba(16,185,129,0.2)' : 'rgba(245,158,11,0.2)', color: item.status?.includes('Done') ? '#34d399' : '#fbbf24', fontWeight: 600 }}>{item.status || 'Done'}</span>
                    </div>
                    <div style={{ fontSize: '0.8rem', fontWeight: isSelected ? 700 : 500, margin: '4px 0', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {item.issueSummary}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between' }}>
                      <span>👤 {item.executorName?.split(' ')[0]}</span>
                      {commits[item.issueKey] && <span style={{ color: '#60a5fa' }}>🐙 {commits[item.issueKey].shortSha}</span>}
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </div>

        {/* Display Canvas Main Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', width: '100%' }}>
          
          {selectedItem ? (
            <>
              {/* Header Details Card */}
              <div className="glass" style={{ padding: '16px 20px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '12px', textAlign: 'left' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '0.75rem', background: 'var(--color-primary)', padding: '2px 8px', borderRadius: '4px', color: '#fff', fontWeight: 700 }}>{selectedItem.issueKey}</span>
                    <span style={{ fontSize: '0.75rem', background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', padding: '2px 8px', borderRadius: '4px', fontWeight: 600 }}>🤖 Gemma 4 Powered</span>
                  </div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: '6px 0 2px 0' }}>{selectedItem.issueSummary}</h2>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Desenvolvido por <strong>{selectedItem.executorName}</strong> {selectedItem.creatorName && `(Solicitado por ${selectedItem.creatorName})`}
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  {githubCommit ? (
                    <a
                      href={githubCommit.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ padding: '6px 12px', borderRadius: '6px', background: 'rgba(96, 165, 250, 0.15)', border: '1px solid #3b82f6', color: '#60a5fa', fontSize: '0.8rem', fontWeight: 600, textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '6px' }}
                    >
                      🐙 Commit GitHub: <code>{githubCommit.shortSha}</code>
                    </a>
                  ) : (
                    <span style={{ fontSize: '0.75rem', color: '#fbbf24' }}>⏳ Commit pendente</span>
                  )}
                </div>
              </div>

              {/* Visualizer Tab Switcher */}
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={() => setActiveTab('preview')}
                  style={{
                    padding: '8px 16px', borderRadius: '6px', border: 'none',
                    background: activeTab === 'preview' ? 'var(--color-primary)' : 'var(--bg-tertiary)',
                    color: '#fff', fontWeight: 600, fontSize: '0.82rem', cursor: 'pointer'
                  }}
                >
                  🖥️ Protótipo Interativo
                </button>
                <button
                  onClick={() => setActiveTab('code')}
                  style={{
                    padding: '8px 16px', borderRadius: '6px', border: 'none',
                    background: activeTab === 'code' ? 'var(--color-primary)' : 'var(--bg-tertiary)',
                    color: '#fff', fontWeight: 600, fontSize: '0.82rem', cursor: 'pointer'
                  }}
                >
                  📜 Diffs & Código Fonte (Gemma 4)
                </button>
                <button
                  onClick={() => setActiveTab('spec')}
                  style={{
                    padding: '8px 16px', borderRadius: '6px', border: 'none',
                    background: activeTab === 'spec' ? 'var(--color-primary)' : 'var(--bg-tertiary)',
                    color: '#fff', fontWeight: 600, fontSize: '0.82rem', cursor: 'pointer'
                  }}
                >
                  📋 Requisitos & DoD
                </button>
              </div>

              {/* Viewport Canvas Container */}
              {activeTab === 'preview' && (
                <div style={{
                  display: 'flex',
                  justifyContent: 'center',
                  width: '100%',
                  background: '#040711',
                  padding: viewportMode === 'mobile' ? '30px 0' : '0',
                  borderRadius: '12px',
                  border: '1px solid var(--border-color)',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: viewportMode === 'mobile' ? '390px' : viewportMode === 'tablet' ? '900px' : '100%',
                    minHeight: '620px',
                    background: '#090d16',
                    borderRadius: viewportMode === 'mobile' ? '24px' : '12px',
                    border: viewportMode === 'mobile' ? '8px solid #1f2937' : 'none',
                    boxShadow: '0 16px 40px rgba(0, 0, 0, 0.7)',
                    display: 'flex',
                    flexDirection: 'column',
                    transition: 'all 0.3s ease'
                  }}>
                    
                    {/* Browser Address Bar */}
                    <div style={{
                      background: '#131b2e',
                      padding: '10px 16px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      borderBottom: '1px solid #1e293b'
                    }}>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }}></span>
                        <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b', display: 'inline-block' }}></span>
                        <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
                      </div>
                      <div style={{
                        flex: 1, background: '#090d16', borderRadius: '6px', padding: '4px 12px',
                        color: '#94a3b8', fontSize: '0.75rem', textAlign: 'left', fontFamily: 'monospace',
                        display: 'flex', justifyContent: 'space-between'
                      }}>
                        <span>https://staging.flosestartup.ai/{selectedItem.issueKey.toLowerCase()}</span>
                        <span style={{ color: '#34d399', fontWeight: 600 }}>🔒 SSL 256-bit</span>
                      </div>
                    </div>

                    {/* Live Render Area */}
                    <div style={{ flex: 1, display: 'flex', background: '#0b0b0c', minHeight: '620px' }}>
                      <iframe
                        src={`http://localhost:5001/api/prototype/${selectedItem.issueKey}`}
                        sandbox="allow-scripts allow-same-origin"
                        style={{
                          width: '100%',
                          height: '100%',
                          minHeight: '620px',
                          border: 'none',
                          background: '#0b0b0c',
                          borderRadius: '0 0 12px 12px'
                        }}
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Code Tab: Gemma 4 Code Snippets & GitHub Commit Details */}
              {activeTab === 'code' && (
                <div className="glass" style={{ padding: '24px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem', color: '#fff' }}>📜 Código & Diff de Engenharia (Gemma 4)</h3>
                    {githubCommit && (
                      <a href={githubCommit.url} target="_blank" rel="noopener noreferrer" style={{ color: '#60a5fa', textDecoration: 'none', fontWeight: 600, fontSize: '0.8rem' }}>
                        🔗 Ver no GitHub →
                      </a>
                    )}
                  </div>

                  <div style={{ background: '#020617', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)', fontFamily: 'monospace', fontSize: '0.82rem', color: '#e2e8f0', whiteSpace: 'pre-wrap', overflowX: 'auto', maxHeight: '500px' }}>
                    {realCode}
                  </div>
                </div>
              )}

              {/* Spec Tab: Requirements & DoD */}
              {activeTab === 'spec' && (
                <div className="glass" style={{ padding: '24px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                  <h3 style={{ margin: 0, fontSize: '1.1rem', color: '#fff' }}>📋 Especificação & Critérios de Aceite (DoD)</h3>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div>✔️ Card registrado no Jira e vinculado ao Épico.</div>
                    <div>✔️ Código inspecionado e refatorado pelo motor **Gemma 4**.</div>
                    <div>✔️ Commit de evidência gravado no repositório GitHub.</div>
                    <div>✔️ Testes de regressão e homologação de QA concluídos.</div>
                  </div>
                </div>
              )}

            </>
          ) : (
            <div className="glass" style={{ padding: '60px', color: 'var(--text-muted)', fontStyle: 'italic' }}>
              Nenhum protótipo disponível. Selecione uma entrega ao lado.
            </div>
          )}

        </div>
      </div>

    </div>
  );
};
