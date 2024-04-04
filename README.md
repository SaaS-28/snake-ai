# Snake A.I.

**Artificial intelligence** that **plays snake**. 
This is <u>not an artifical intelligence that learns how to play</u> it but, given certain data, it **finds the best way to achieve the objectives** which are only 3 for this game: Eat the apples and avoid hitting the wall or himself.

To implementi it, I used **python**, more precisely [**pygame**]("https://www.pygame.org/news") for the game and [**tensorflow**]("https://www.tensorflow.org/") for the AI. 

This AI is a type of artificial intelligence that uses a **preadded model**. Is commonly called *"model-based artificial intelligence"* or *"neural network-based artificial intelligence"*. This approach is part of **supervised learning**, where a model is trained on a **dataset labeled** and then used to **make predictions** about new data without further adaptation during use. 

For "training" the AI use both fruit and snake position and their distance so the AI can **calculate the best path to achieve the apple without hit something** (By now the record of apple eaten is of 53 apples :) ).
