HTML
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jogo de Paciência</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f4f4f9;
            margin: 0;
        }
        .game-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 90%;
            max-width: 400px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        #status {
            font-size: 1.5em;
            margin: 20px 0;
            color: #007bff;
            min-height: 30px; /* Reserve space for status messages */
        }
        button {
            padding: 12px 20px;
            font-size: 1em;
            cursor: pointer;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>

    <div class="game-container">
        <h1>Jogo de Paciência</h1>
        <p id="status">Aguardando o início...</p>
        <button id="startButton">Começar Jogo</button>
        <button id="resetButton" style="display: none;">Reiniciar</button>
    </div>

    <script>
        const statusElement = document.getElementById('status');
        const startButton = document.getElementById('startButton');
        const resetButton = document.getElementById('resetButton');

        let currentCount = 0;
        let gameInterval = null;
        let isPlaying = false;
        const targetNumber = 100; // O alvo que o jogador deve esperar/alcançar

        function updateStatus(message) {
            statusElement.textContent = message;
        }

        function startGame() {
            if (isPlaying) return;

            currentCount = 0;
            isPlaying = true;
            startButton.style.display = 'none';
            resetButton.style.display = 'none';
            updateStatus("Contagem em andamento. Espere o número atingir " + targetNumber);

            // Simulação de espera/progressão (Paciência)
            gameInterval = setInterval(() => {
                if (currentCount < targetNumber) {
                    // Incrementa lentamente para simular a passagem do tempo ou evento
                    currentCount += Math.floor(Math.random() * 5) + 1; // Aumenta de 1 a 5 por tick
                    updateStatus(`Tempo decorrido: ${currentCount}/${targetNumber}`);

                    if (currentCount >= targetNumber) {
                        clearInterval(gameInterval);
                        isPlaying = false;
                        updateStatus(`PARABÉNS! Você alcançou o alvo: ${targetNumber}!`);
                        resetButton.style.display = 'inline-block';
                    }
                } else {
                    // Se já atingiu, para o loop mas mantém a mensagem final
                    clearInterval(gameInterval);
                }
            }, 500); // Atualiza a cada 500ms
        }

        function resetGame() {
            if (gameInterval) {
                clearInterval(gameInterval);
            }
            isPlaying = false;
            currentCount = 0;
            updateStatus("Jogo reiniciado. Clique em Começar Jogo para recomeçar.");
            startButton.style.display = 'inline-block';
            resetButton.style.display = 'none';
        }

        startButton.addEventListener('click', startGame);
        resetButton.addEventListener('click', resetGame);

        // Inicialização
        updateStatus("Clique em Começar Jogo para iniciar o jogo de paciência.");

    </script>

</body>
</html>