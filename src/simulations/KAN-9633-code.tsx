import React, { useState, useCallback } from 'react';

interface CardData {
  title: string;
  description: string;
  category: string;
  imageUrl?: string;
  createdAt: Date;
}

interface CardCreatorProps {
  onCardCreated: (card: CardData) => void;
}

const CardCreator: React.FC<CardCreatorProps> = ({ onCardCreated }) => {
  const [title, setTitle] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [category, setCategory] = useState<string>('General');
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTitle(name === 'title' ? value : title);
    setDescription(name === 'description' ? value : description);
    setCategory(name === 'category' ? value : category);
    setImageUrl(name === 'imageUrl' ? value : imageUrl);
  };

  const handleCardCreation = useCallback(async () => {
    if (!title || !description) {
      alert('Título e Descrição são obrigatórios.');
      return;
    }

    setIsLoading(true);
    
    try {
      const newCard: CardData = {
        title: title.trim(),
        description: description.trim(),
        category: category,
        imageUrl: imageUrl || null,
        createdAt: new Date(),
      };
      
      // Simula a chamada à API ou lógica de persistência
      await new Promise(resolve => setTimeout(resolve, 500)); 
      
      onCardCreated(newCard);
      
      // Resetar o formulário após sucesso
      setTitle('');
      setDescription('');
      setImageUrl('');
      setCategory('General');

    } catch (error) {
      console.error('Erro ao criar o card:', error);
      alert('Ocorreu um erro ao criar o card.');
    } finally {
      setIsLoading(false);
    }
  }, [title, description, category, imageUrl, onCardCreated]);

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', maxWidth: '600px', margin: 'auto' }}>
      <h2>Criar Novo Card</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <label>Título:</label><br/>
        <input
          type="text"
          name="title"
          value={title}
          onChange={handleInputChange}
          style={{ width: '100%', padding: '8px', margin: '5px 0', display: 'block' }}
          placeholder="Título do Card"
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Descrição:</label><br/>
        <textarea
          name="description"
          value={description}
          onChange={handleInputChange}
          rows={4}
          style={{ width: '100%', padding: '8px', margin: '5px 0', display: 'block' }}
          placeholder="Detalhes do Card"
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Categoria:</label><br/>
        <select
          name="category"
          value={category}
          onChange={handleInputChange}
          style={{ width: '100%', padding: '8px', margin: '5px 0', display: 'block' }}
        >
          <option value="General">Geral</option>
          <option value="Tech">Tecnologia</option>
          <option value="Art">Arte</option>
          <option value="Travel">Viagem</option>
        </select>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Imagem (URL):</label><br/>
        <input
          type="text"
          name="imageUrl"
          value={imageUrl}
          onChange={handleInputChange}
          style={{ width: '100%', padding: '8px', margin: '5px 0', display: 'block' }}
          placeholder="URL da Imagem (Opcional)"
        />
      </div>

      <button
        onClick={handleCardCreation}
        disabled={isLoading}
        style={{ 
          padding: '10px 15px', 
          backgroundColor: isLoading ? '#ccc' : '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '5px', 
          cursor: isLoading ? 'not-allowed' : 'pointer' 
        }}
      >
        {isLoading ? 'Criando...' : 'Criar Card'}
      </button>
    </div>
  );
};

export default CardCreator;