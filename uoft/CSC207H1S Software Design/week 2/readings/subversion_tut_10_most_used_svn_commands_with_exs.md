#subversion tut: 10 most used svn commands with exs
January 11, 2015

**SVN checkout - create working copy**
- checkout command is used to download sources from SVN repo to working copy
- can checkout a file, directory, trunk or whole project
	`Syntax:
	`
	`$ svn checkout/co URL PATH

**SVN commit - save  changes to the repo**
	`Syntax:`
	`
	`$ svn commit -m'log messages'`
- comment with -m option
- 

**SVN list - lists directory entries**
- view the content of the SVN repo, without downloading a working copy
	`Syntax:
	`
	`$ svn list`
- when executed with -verbose option, the following is displayed:
	- revision number of the last commit
	- author of the last commit
	- size (in bytes)
	- date and time of the last commit

**SVN add - add a new file to SVN repo**
- create a file in local working copy
- add the file into SVN repo
- commit the added file (until you commit, the added file will not be available in the repo)

**SVN delete - removing a file from repo**
- need to `commit` after deleting
	`Syntax:`
	`$ svn delete URL`
- then can do svn list and check whehter the file was deleted from the repo

**SVN diff - display the difference**
	`Syntax:`
	`$ svn differ filename`
	`
	`$ svn -r R1: R2 diff filename`
	
**SVN status - status of the working copy**
- it displays whether the working copy is modified, been added/deleted, or fileis not  under revision control, etc.
	`Syntax:`
	`$ svn status PATH`
- ‘M’: been modified
- ‘svn help status’ will explain various SVN status commands

**SVN log - display log message**
	`Syntax:`
	`
	`$ svn log PATH`

**SVN move - rename file or directory**
	- the file will be moved on your local sandbox immediately (as well as on the repo after committing)
		`Syntax:`
		`$ svn move src dest`

SVN update - update the working copy
	`Syntax:`
	`
	`$ svn update PATH`