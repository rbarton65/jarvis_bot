# Jarvis GroupMe Bot
Jarvis is a GroupMe chatbot that uses static commands as well as artificial intelligence to respond to chat.

## Commands
##### /wiki

    /wiki {topic}

/wiki searches Wikipedia and returns a summary on the topic searched.


##### /urban
    
    /urban {topic}
    
/urban searches urbandictionary.com and returns a definition with examples.


##### /anim

    /anim {topic}

/anim uses the giphy api to return a gif based on the topic specified
    

##### /8ball

    /8ball {question}

/8ball responds to a question in the form of a magic 8 ball


## Other features

* Specify Jarvis's name for him to respond with his chatbot capability.

## How it Works
Jarvis has multiple files, including a port listening script, the main jarvis file, and command files. The server listens to the specified port for any data sent from the GroupMe chatroom. This data comes in the format of a json file, which can be manipulated to extract the text and perform the necessary commands based on the text. The result is a text format that the bot posts as a reply to the GroupMe chatroom.

