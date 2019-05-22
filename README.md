# linker
Web app that allows to shorten links.

You can find this app at https://evo-linker.herokuapp.com/

Just enter some link (redirection link) and receive shortlink that is synonym for the first one.

### Internal principle of app hosting: 
This web app is running by Flask on www.heroku.com

### Internal principle of data storage: 
Redirection links (rlinks) and shortlinks (slinks) are stored in SQL database.  
This database is representation of traditional python dictionary where keys are rlinks and values are lists of slinks.  
Slinks are totaly unique: entering a rlink that has already been added gives a new slink.

### Internal principle of shortlink generation: 
Output slink looks like https://evo-linker.herokuapp.com/HASH, where HASH is special code that idicates the page to be redirected.  
HASH can contain the following characters: 01..89AB..YZab..yz (62 in total).  
HASH for a new rlink is generated by "incrementing" previous generated rlink's HASH (stores in txt file).   
For the first 62 requests after deploying this app HASH will consist of only one character.  
HASH for the first request is "0", the second is "1",.., 11th is "A",.., 36th is "Z", 37th is "a",.., 62th is "z".  
The only thing that determines view of HASH for some rlink - number of HASHes generated in all the time.  
When there will be no way to "increment" the new character will be added (HASH for the 63th request is "00", 64th is "01",...).   
For example: HASH starts containing 10 characters when it recieves 13537086546263553th request.  
In general: HASH starts containing N characters when it recieves (62^(N-1)+1)th request.
