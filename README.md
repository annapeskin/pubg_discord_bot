# pubg_discord_bot
A discord bot that provides information about the game PlayerUnknown's Battlegrounds (PUBG), a multiplayer online battle royale video game - where players drop on an island and fight for survival.

# Getting started
## Using `virtualenv`
* Install `virtualenv`  
`pip install virtualenv`
* Create the environment  
`virtualenv <envname>`
* Run the environment  
Windows: `.\<envname>\Scripts\activate`
* Install dependencies  
`pip install -r requirements.txt`

## Configuration
* Create a file called `private_constants.py` in the root directory  
* Add two variables:  
`API_KEY`, which is the [Pubg tracker](https://pubgtracker.com/site-api) Api key  
`BOT_TOKEN`, which is the [Discord bot](https://discordapp.com/developers) token

## Guidelines
* Please keep all new additions related to PUBG
* Pease follow the [Pep8 style guide](https://www.python.org/dev/peps/pep-0008/) (with the exception of line length, which can be increased from 79 to 150

### TODO:  
Add better handling for invalid requests  
Add better handling for if the sites used to pull the stats from are down  
Add gun comparison  
Add a fun command the user can use if they get a win  
Add a command the user can use to find out how long until loot box prices are reset (Sunday 6PM PST)
