## API Project About Books, Quizzes and Children
This project is the backend of a website where children can read, listen and solve the quiz of the relevant book after reading / listening is finished. At the same time, it is designed with the aim that the parent or instructor can follow the quiz results and reading history of the relevant child.

### Installation
#### First Step
You have to install Python Environment to working on this project. You can find a guide about this in [here](http://https://towardsdatascience.com/virtual-environments-104c62d48c54 "here"). I don't know who wrote this article, but it can be useful for you.

#### Second Step
After installed the Python Environment, activate it. Then copy the link below and paste it into your terminal.
`https://github.com/talhakoylu/SummerInternshipBackend.git`

#### Third Step
Open the **config/** folder in the package. There is a file named **example-settings.py**. Let's rename the file with this **"settings.py"**. 
There is a line in this file starts with **SECRET_KEY**. If you want to use and develop this project for yourself, you need a key of your own. Paste this key in the corresponding file and save it. You should not share the key with anyone.

#### Fourth Step
After all these steps, you need to install required libraries. To make this, let's move your current location to **bookorbooks** or if you changed the name, write that name in your terminal. 
Example:
`(env) $: cd bookorbooks`
Then run this line of code in the terminal page.
`pip install requirements.txt`

#### Fifth Step
After the fourth step, run the line of code below in your terminal.
`python manage.py migrate`
In this way, your database will be created by Django. After that, you can create a super user account. To make this, write the code below into your terminal.
`python manage.py createsuperuser`

#### Please Note
This project has multilingual support. If you want to use this, run the line of code below in your terminal. Then you can use this feature.
`python manage.py compilemessages -l en --ignore=env`
