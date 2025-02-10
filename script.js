 const statusElement = document.getElementById('status');
    const yourMoveElement = document.getElementById('your-move');
    const opponentMoveElement = document.getElementById('opponent-move');
    const resultsElement = document.getElementById('results');
    const buttons = document.querySelectorAll('#moves button');

    // ✅ Change WebSocket URL when deploying online
    // const socket = new WebSocket('ws://localhost:10000');
    const socket = new WebSocket('wss://codealpha-online-game.onrender.com');

    let player;

    socket.onopen = () => {
        console.log("Connected to WebSocket server");
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Received:", data);  // ✅ Debugging

        if (data.type === 'init') {
            player = data.player;
            statusElement.textContent = `You are Player ${player + 1}`;
        } else if (data.type === 'update') {
            updateGameState(data.game);
        } else if (data.type === 'result') {
            showResult(data.winner);
        }
    };

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const move = button.id;
            socket.send(JSON.stringify({ type: 'move', move }));
            yourMoveElement.textContent = move;
        });
    });

    function updateGameState(game) {
        if (!game.ready) {
            statusElement.textContent = 'Waiting for Player...';
            yourMoveElement.textContent = 'Waiting';
            opponentMoveElement.textContent = 'Waiting';
        } else {
            statusElement.textContent = 'Your Move';

            // ✅ Fix: Use `p1Went` and `p2Went` instead of `bothWent()`
            if (game.p1Went && game.p2Went) {
                yourMoveElement.textContent = player === 0 ? game.p1Move : game.p2Move;
                opponentMoveElement.textContent = player === 0 ? game.p2Move : game.p1Move;
            } else {
                // ✅ Show waiting/locked-in status for each player
                if (player === 0) {
                    yourMoveElement.textContent = game.p1Went ? game.p1Move : 'Waiting';
                    opponentMoveElement.textContent = game.p2Went ? 'Locked In' : 'Waiting';
                } else {
                    yourMoveElement.textContent = game.p2Went ? game.p2Move : 'Waiting';
                    opponentMoveElement.textContent = game.p1Went ? 'Locked In' : 'Waiting';
                }
            }
        }
    }

    function showResult(winner) {
        if (winner === player) {
            resultsElement.textContent = '🎉 You Won!';
        } else if (winner === -1) {
            resultsElement.textContent = '⚖️ Tie Game!';
        } else {
            resultsElement.textContent = '😢 You Lost!';
        }
        setTimeout(() => {
            resultsElement.textContent = '';
            yourMoveElement.textContent = 'Waiting';
            opponentMoveElement.textContent = 'Waiting';
        }, 2000);
    }

