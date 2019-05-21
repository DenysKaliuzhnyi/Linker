# evo-linker
Web app that allows to shorten links.

This app you can find at https://evo-linker.herokuapp.com/

Just enter some link (redirecion link) and receive shortlink that is synonym for the first one.

### Internal principle of data storage: 
This web app is running by Flask on www.heroku.com

### Internal principle of data storage: 
Redirecion links and shortlinks are stored in SQL database. This database is representation of traditional python dictionary
where keys are redirection links and values are lists of shortlinks (for repeating link you receive new shortlink).

### Internal principle of shortlink generation: 
Output shortlink looks like https://evo-linker.herokuapp.com/HASH, where HASH is special code that idicates the page to be redirected. 
Lets speek more about HASH. HASH for new link is generated by "incrementing" previous generated link's HASH (stores in txt file). 
Note that view of input link doesn't influence on view of HASH. 
Possible values of characters containing in HASH are [0,1,..,8,9,A,B,..,Y,Z,a,b,..,y,z] (62 in total). 
From the begining (for first requests after deploy), the HASH will consists only of one character. 
When there will be no way to "increment" the new character will be added. 
(for the 63th request second character will be appended and third character only for 62^2+1=3845th request. 
In general: HASH starts containing N characters when it recieves (62^(N-1)+1)th request).
