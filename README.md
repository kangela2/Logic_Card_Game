# Logic_Card_Game


This is a multiplayer card game you play in teams of 2 with 4 people total. This is a game of educated guesses. 

It will most likely stay as a single player game vs bots, but maybe there can be an option for multiplayer depending on how much time we have. There will be optionality for the difficulty of the opponents, and potentially be trained by an AI model. 

For the tech stack the front end will be TypeScript, React, and Bootstrap while the backend will be JavaScript, Node.js, Express.js, and PostgreSQL. For authentication I was thinking Firebase Authenitication and TBD for AI training, potentially use Pytorch or Tensorflow. 


# Game Rules

## Setup 
There are two teams of two in this game and each person's partner's cards are directly opposite from them. 
  
The game uses 24 cards from a standard deck of cards, a black and red pair of the face values 2 to King with 2 being the lowest value card and King being the highest value card. There is no value difference between the black and red version of a card and there is no value difference if the black suit is a club or a spade, or if the red suit is a diamond or a heart. Once the cards are gathered, they are shuffled and equally distributed to each player. 
  
Each player should have six cards and only know what their cards are. Once the player sees their card, they sort the cards lowest to highes in front of them, faced down. The lowest card should be on the left side of the player and the highest card is on the player's right side. 

## Player turn
Once everyone's cards are sorted and faced down the game begins. A random player is selected and during their turn they must complete two actions. 

First, their partner will hand them a card from their deck. Everyone will see what the card position in relation to the partner's deck, but only the player who's turn it is will see the value of the card. After the player sees the card, they return it facedown to their partner. The player can have the option to request to see a certain card, ie. lowest or highest, or can leave it up to their partner's discretion to pick a card for them to show. This discussion is open and everyone on the table can hear this. 

Second, the player must pick a card from the opponent's side and guess what is the face value of the card. Whether it is a red or black version of the card is irrelevant. If the player guessed the card correctly, the opponent must turn the guessed card faced up. If the player guessed incorrectly then they must flip over one of their six faced down cards. Once the card is flipped over, the player's turn ended and the next person, who should be on the opposing team, goes. 

## Other Rules
A player is only allowed to look at one of their partner's card during their turn. Their partner can send a card that was previously sent before. 
All communication must be open ie, when talking to your partner, they and the opponents will hear what you will say. 

## Win Conditions
There are two ways to end the game. 

First, a team wins if they manage to flip all of the six faced down cards of an opponent. 

Second, a player during their turn can at any point during the game can "push the red button". This is when they attempt to guess all of cards on the table. If they guess correctly then their team wins. If they guess incorrectly then the other team wins. 

## Tips For Playing
When revealing a card, the optimal play is to show the card that reveals the least amount of information about you and your partner's cards. For example if your lowest card is a 9, do not reveal it unless there is no other option because it reveals that your cards' value skew high and potentially that your partner's cards skew low. 

When sending a card over, if you have any doubles, try sending cards that will telegraph that to your partner. For example if you have a double King, if you send your second highest card to your partner, they can deduce that your highest card is also a King. However, be careful when employing this strategy because the opponent may be able to deduce the same thing because the card's position in your sorted deck is open to the opponents while the value is only revealed to your partner. 
  

  
