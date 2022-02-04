Albert runs on the DAIDE server and Mapper available from the main site.
http://www.daide.org.uk/index.xml

***************************************
ALBERT SPECIFIC COMMANDLINE PARAMETERS
***************************************
-t Tournament Mode
This parameter disables any delay timers in the code.  These timers have been included to give Albert the appearance
of thinking like a human about retreat/adjustment phases.  For example without these delay timers Albert would submit re
treat
orders in 1/10th a second which is easily identifiable as a bot in an RT game.

-n Never Ally Mode
This parameter makes Albert treat all powers as an enemy at all times.

-g gunboat game without press, no matter what level the server has set the game to.

-d[0-100] Depth_of_Thought
This parameter sets how deeply Albert will think.  It changes both the number of iterations per turn
as well as the number of ordersets generated for each power.  Using -d0 results in a bot that is only
slightly better than KMB.  The default Albert runs with a -d50.  Using a -d100 will cause Albert to
iterate almost twice as much and generate approximately 50% more order sets per turn.  I believe there
is a point of diminishing returns.

Due to the length of time it takes to run tournaments I have not tested Albert at each level.
I have mainly worked at level -d50 which I feel is decent comprimise.

	-d20 or -d30 should already begin to yield better results, and still be relatively quick.

*****************************************************
STANDARD COMMANDLINE PARAMETERS FOR THE AI FRAMEWORK
*****************************************************

-s[Server Name] Optionally sets the connection to a server name: such as with a URL address.
-i[IP Address] Optionally sets the connection to a server's IP address.
-p[Port Number] Optionally sets the port number that the game is played on.
-r[POW:passcode] Optionally sets the reconnection attribute ex:// -rGER:4218



********************
ALBERT RELEASE NOTES
********************
Albert v6.0.1
	- Fixed bug


Albert v6.0
	- Requires AISever  version 0.38 or later
	- Requires AIMapper version 0.41 or later

	- Major Release with addition of Press for Orders during movement phases
	- Capable of press levels 10, 20 and 30
	- Capable of PCE, ALY, DMZ, XDO, NAR, NOT, DRW, SLO, AND, ORR