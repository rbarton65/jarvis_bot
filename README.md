# Jarvis GroupMe Bot
Jarvis adds multiple commands to make life in your GroupMe chat fun and easy.

## Commands
##### /info

    /info {topic}

/info searches Wikipedia and returns a 2 sentence summary on the topic searched.

##### /lmgtfy, /google

    /lmgtfy {topic}
    
    /google {topic}

/lmgtfy and /google creates a "let me google that for you" link on the topic specified.

##### /urban
    
    /urban {topic}
    
/urban searches urbandictionary.com and returns a definition with examples.

##### /map

    /map from {location A} to {location B}
    
/map uses the Google Maps API to determine how long it would take to drive from location A to location B.

##### /video, /youtube

    /video {topic}
    
/video and /youtube returns a YouTube link from the top YouTube result from the topic searched.

##### /flip

    /flip
    
/flip flips a coin, returns either heads or tails

##### /current

```/current {zip code}```
    
```/current {city}```
    
/current returns the current weather of the specified city
    
##### /forecast

    /forecast {zip code}
    
    /forecast {city}
    
/forecast returns the 5 day forecast of the specified city
    
##### /gpoem

    /gpoem {topic}

/gpoem uses google's autocomplete to create a 4 line poem
    
##### /seen

    /seen {name}

/seen shows the last time someone in the group commented

##### /anim

    /anim {topic}

/anim uses the giphy api to return a gif based on the topic specified
    
##### /tap

    /tap at {bar} in {location}

/tap returns the top 5 beers of a bar based on the untappd api
   
##### /karma

    /karma

    {topic/name}++

    {topic/name}--

Karma uses a csv file to keep track of karma points given or taken from specified topic/name. Meaningless internet points.
   
## Other features

* Specify Jarvis's name for him to respond with his chatbot capability.

## How it Works
Jarvis has multiple files, including a port listening script, the main jarvis file, and command files. The server listens to the specified port for any data sent from the GroupMe chatroom. This data comes in the format of a json file, which can be manipulated to extract the text and perform the necessary commands based on the text. The result is a text format that the bot posts as a reply to the GroupMe chatroom.

## Ideas to Implement in the Future

* Reminders
* A.I.
