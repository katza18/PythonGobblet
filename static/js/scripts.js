
// document.addEventListener('click', function(){
//     var selectedPieces = document.getElementsByClassName('selected');
//     while (selectedPieces.length > 0) {
//         selectedPieces[0].classList.remove('selected');
//     }
// })

window.onload = function() {
    fetch('/reset', {
        method: 'POST',
    })
    .then(response => response.json())
}


function deselectAll() {
    var selectedPieces = document.getElementsByClassName('selected');
    while (selectedPieces.length > 0) {
        selectedPieces[0].classList.remove('selected');
    }
}


function selectPiece(event, pieceId) {
    // Ensure the event doesn't bubble up to the board space
    event.stopPropagation();

    // Get all selected pieces
    var selectedPieces = document.getElementsByClassName('selected');
    var piece = document.getElementById(pieceId);

    // Check if another piece is selected and then check if that piece is smaller so it can be gobbled
    if (selectedPieces.length > 0 && selectedPieces[0].id != pieceId) {
        // Get the spaceId of the piece to gobble
        spaceId = document.getElementById(pieceId).parentElement.id;

        // If the spaceId is a home space, then clear the selected pieces
        console.log(spaceId);
        if (spaceId[0] ==  "h") {
            // Clear the selected pieces and select the new piece
            deselectAll();

            // Select the new piece
            piece.classList.add('selected');

            return;
        }

        // Move the piece to the space.
        movePiece(spaceId);
        return;
    }
    else {
        // If there are no selected pieces, select the piece (this will highlight the piece)
        piece.classList.add('selected');

        // Consider having a selected piece in the backend (although, this may not be necessary)
    }
}


function movePiece(spaceId) {
    // We are checking the document for the selected piece. This will be inefficient, so it may be better to keep track of the selected piece in a variable.
    var piece = document.getElementsByClassName('selected')[0];
    piece.classList.remove('selected');
    var pieceId = piece.id;
    if (!piece) {
        return;
    }
    var targetSpace = document.getElementById(spaceId);

    // Request backend to move piece
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            // Piece id format == 'xyz' where x = player (0 = player, 1 = ai), y = home stack idx, z = piece size (4-1)
            pieceId: pieceId,
            // Space id format == 'xy' where x = row idx, y = col idx
            spaceId: spaceId,
            // Depth == difficulty of the AI
            depth: 1,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Set message div text
        var messageDiv = document.getElementById('message');
        messageDiv.innerText = data.message;

        console.log(data);

        if (data.valid) {
            // Move the piece
            piece.classList.remove('selected');
            targetSpace.appendChild(piece);
        }

        if (data.winner) {
            // Lock the board. Show a winner animation.
        }

        // Otherwise, move the ai piece since there was no winner
        const aiPieceElement = document.getElementById(data.aiPiece);
        const aiSpaceElement = document.getElementById(data.aiTargetLocation);
        aiSpaceElement.appendChild(aiPieceElement);
    });
}
