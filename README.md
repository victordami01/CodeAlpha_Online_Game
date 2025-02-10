# Rock, Paper, Scissors Multiplayer Game

Welcome to the **Rock, Paper, Scissors Multiplayer Game**! This interactive game allows two players to compete against each other in real-time using WebSocket technology. The game features a user-friendly interface and smooth gameplay mechanics.

[![istockphoto-839977330-612x612.jpg](https://i.postimg.cc/Ssz85Qcy/istockphoto-839977330-612x612.jpg)](https://postimg.cc/G8dHTCMN)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Gameplay Instructions](#gameplay-instructions)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Live Demo](#live-demo)

## Features

- **Real-time Multiplayer:** Play against another player over the internet.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.
- **Instant Feedback:** Players receive immediate updates on moves and results.
- **Game State Management:** Automatic reset for continuous play without needing to refresh.

## Technologies Used

- **Frontend:**
  - HTML
  - CSS
  - JavaScript

- **Backend:**
  - Python
  - WebSocket (using `websockets` library)

## Usage

1. **Open the game in a web browser:**
   Navigate to `index.html` in your preferred web browser.

2. **Simulate gameplay:**
   Open the game in two different browser tabs or windows to simulate two players.

## Gameplay Instructions

1. **Choose Your Move:**
   Each player selects Rock, Paper, or Scissors by clicking the corresponding button.

2. **Determine the Winner:**
   The game uses the following rules:
   - Rock crushes Scissors (Rock wins)
   - Scissors cut Paper (Scissors win)
   - Paper covers Rock (Paper wins)
   - If both players choose the same move, it results in a tie.

3. **View Results:**
   After both players have made their moves, the winner is displayed, and the game automatically resets for the next round.

## Future Improvements

- **User Authentication:** Allow players to create accounts and track their scores.
- **Leaderboard:** Implement a leaderboard to display top players.
- **Chat Feature:** Enable players to chat during the game.
- **Enhanced UI/UX:** Improve design and animations for a better user experience.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Live Demo

Try out the game at https://sciropa.netlify.app/
