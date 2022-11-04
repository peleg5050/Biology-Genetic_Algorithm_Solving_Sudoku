# Biology- Genetic Algorithm (Solving Sudoku)

#### Created by:
- Raviv Haham
- Peleg Haham

Project Description
-
In this project, we worked on several features:
We created a desktop application that runs a genetic algorithm that solves a Futoshiki puzzle board (according to the instructions provided to us in the exercise).
The application has an accessible and user-friendly interface so even a person who doesn't know how to program can easily run the program and enjoy it.
In order to select a game board you need to access the config file and there you need to change the value of the gridller variable which contains the path of the board file. By default, we run an arbitrary game board (of course, you can run a game board of any size you want depending on the code we wrote).


#### The different screens:
The main screen has a graphic display that sequentially runs all types of genetic algorithms we built. In the center of the screen there is a game board of N X N size, and the board is filled with numbers from 1 to N .In the given cells there are the same fixed digits throughout all the attempts to solve the board (since this is a hard constraint).
The screen shows the best solution among the 300 solutions that the algorithm runs, and an information bar in the left part of the screen, which contains the number of the current iteration, the score of the best solution, the score received by the worst solution and the average score obtained. When the run ends, 2 graphs are displayed that show the best solution score and the average score obtained throughout the iterations for all three different algorithms.
This is what the board looks like when running the normal genetic algorithm:
-
![UML](https://imgur.com/aNS9oJA.png)


### Running
To run, double-click the covidModel.exe file that appears in the zip folder we uploaded.
To run, enter to the folder that contains the main.exe executable file and the text file (which describes the state of the board), then open cmd for this path, and in the opened terminal write: main.exe filename.txt

קובץ ההרצה (main.exe) נמצא בתוך התיקייה dist, על מנת להריץ את התוכנית שבנינו ישנן שתי דרכים עיקריות: 
דרך ראשונה (הקלה) : יש ליצור ולהיכנס לתיקייה בה מופיע קובץ ההרצה main.exe וקובץ הטקסט (שמתאר את מצב הלוח), יש לפתוח את ה cmd עבור נתיב זה (ע"י כתיבה "cmd"
בשורת הנתיב) ובטרמינל שנפתח יש לכתוב: main.exe filename.txt  
דרך שנייה : ע"י ביצוע ההרצה מהטרמינל של סביבת הפיתוח pycharm ע"י הרצת הפקודה : py main.py filename.txt  או לחילופין python main.py filename.txt


## Future improvements:

As we continue to work on this app, we encourage anyone that wants to help out to do so!
Just open the project in Visual Studio Code and add your own touches!
Other than that, we would appreciate if you would try to stick to our design language and patterns.
Have fun with this project and don't forget to create a pull request once you're done so this project could have a little bit of YOU in it!

