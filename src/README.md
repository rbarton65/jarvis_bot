## Jarvis contains two main functions - the ability to run commands, and the ability to respond to chat.

#### Commands

Commands are contained in the `commands` folder. They contain two functions: `main()` and `help()`. 
`main()` runs the actual command, returning a `text, attachments` tuple. Attachment syntax can be 
found in the GroupMe API documentation.
`help()` gives a description and example of how to use the command. It is called on by the `help` command.

Commands are coded to act like separate apps. You can activate or deactivate any command at will by listing
them in the `commands.txt` file. Any command in that file is active.

#### Brain

Jarvis's chat ability is stored in the `brain/` directory. This contains `brain.json`, which acts as Jarvis's
artificial intelligence "brain".
