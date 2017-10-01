# pubg_discord_bot
A discord bot that provides information about the game PlayerUnknown's Battlegrounds (a multiplayer online battle royale video game - where players drop on an island and fight for survival).

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
`BOT_TOKEN`, which is the discord bot token.

### TODO:  
Add better handling for invalid requests  
Add better handling for if the sites used to pull the stats from are down  
Add gun comparison  
Add a fun command the user can use if they get a win  