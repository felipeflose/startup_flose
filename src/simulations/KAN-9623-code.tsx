import React, { useState, useCallback, useMemo } from 'react';

interface CardData {
  id: string;
  title: string;
  content: string;
  type: 'standard' | 'featured';
  color?: string;
}

interface CardCreatorProps {
  initialCardData?: CardData;
  onCardCreated: (card: CardData) => void;
  onCancel: () => void;
}

const CardCreator: React.FC<CardCreatorProps> = ({
  initialCardData,
  onCardCreated,
  onCancel,
}) => {
  const [title, setTitle] = useState(initialCardData?.title || '');
  const [content, setContent] = useState(initialCardData?.content || '');
  const [type, setType] = useState<CardData['type']>('standard');
  const [color, setColor] = useState<string>('#ffffff');

  const isEditing = !!initialCardData;

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    if (name === 'title') setTitle(value);
    if (name === 'content') setContent(value);
  }, []);

  const handleTypeChange = useCallback((newType: CardData['type']) => {
    setType(newType);
  }, []);

  const handleColorChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setColor(e.target.value);
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !content) return;

    const newCard: CardData = {
      id: Date.now().toString(), // Simple unique ID generation
      title,
      content,
      type,
      color: color,
    };

    onCardCreated(newCard);
  }, [title, content, type, color, onCardCreated]);

  // Optimization: Memoize the card data to prevent unnecessary re-renders if possible, though here we focus on the creation flow.
  const cardDetails = useMemo(() => ({
    title,
    content,
    type,
    color,
  }), [title, content, type, color]);

  return (
    <div className="card-creator-container p-6 bg-gray-50 rounded-lg shadow-md max-w-xl mx-auto border border-gray-200">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Criar Novo Card</h2>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">Título</label>
          <input
            type="text"
            id="title"
            name="title"
            value={title}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">Conteúdo</label>
          <textarea
            id="content"
            name="content"
            value={content}
            onChange={handleInputChange}
            rows={6}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 resize-y"
            required
          />
        </div>

        <div className="flex space-x-4">
          <div className="flex-1">
            <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-1">Tipo de Card</label>
            <select
              id="type"
              name="type"
              value={type}
              onChange={(e) => handleTypeChange(e.target.value as CardData['type'])}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="standard">Padrão</option>
              <option value="featured">Destaque (Featured)</option>
            </select>
          </div>
          <div>
            <label htmlFor="color" className="block text-sm font-medium text-gray-700 mb-1">Cor de Fundo</label>
            <input
              type="color"
              id="color"
              name="color"
              value={color}
              onChange={handleColorChange}
              className="w-full h-10 p-1 border border-gray-300 rounded-md"
            />
          </div>
        </div>

        <div className="flex space-x-4 pt-4">
          <button
            type="submit"
            className="w-full px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition duration-150 shadow-lg"
          >
            Criar Card
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="w-full px-4 py-3 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300 transition duration-150"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default CardCreator;