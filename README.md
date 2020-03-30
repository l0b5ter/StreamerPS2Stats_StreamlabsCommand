# StreamerPS2Stats_StreamlabsCommand
Show streamer's planetside2 stats!
I saw that the chatbot can be used in discord, so this script sud work there to.

Script-version: 1.0.0.0                     
Last-modified: 30.03.2020                     
Made by: lobster/loster31345 from WiAD                           
Based on the [StreamerPS2Online_StreamlabsCommand](https://github.com/l0b5ter/StreamerPS2Online_StreamlabsCommand) script.

## Functions:
1. On command in chat will make the bot lookup which character the streamer is playing as and display its stats!
2. Shows all-time stats KPM (kill per minute), KDR (kills and deaths ratio), ADR (capture and defense ratio), Score/Minute (score per minute), Total-captures and Total-defends.
3. Works with discord
4. Supports unlimited characters
5. Simple and clean way to add and removed.


## Instructions on how to get it up
1. download .zip
2. This folder is in a zip-file, so extract it and move the folder StreamerPS2Stats
 into the streamlabs chat bot "Scripts" folder.
3. Three files for each faction, look into the "Example" folder for example.
Or just move them into your "Config" folder and replace the character names in each of them.
4. Default command is "stats" (however if you wanna change this, open the "StreamerPS2Online_StreamlabsSystem.py" in a text editor like notepad++ and change the variable Command. ```Command = "stats"```)
6. Yay you done mate, just reload the scripts and see the magic^^

## Notice:
The response is delayed due to accessing the ps2 api twice, first to find character and then to grab stats.         
Only put your characters in the files. If there is more than 1 online at the same time, will make the script pick the first character in the list.

Feel free to take a look at the script "StreamerPS2Stats_StreamlabsCommand.py", however if you make a change dont come and say its not working. Ill galdly help fix or improve it^^

