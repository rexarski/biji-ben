#Chapter 1 intro to version control
January 11, 2015

[link](http://svnbook.red-bean.com/en/1.6/svn.basic.version-control-basics.html)

##version control basics
A **version control system** is a system that tracks incremental versions (or revisions) of files and, in some cases, directorires over time.

###the repository
The **repository** _is_ a kind of file server, but what makes it special is that it remembers each version of those files.

###the working copy
A **working copy** is a local copy of a particular version of a user’s VCS-managed data upon which that user is free to work.

###versioning models
different systems use different strategies to version control.

####the problem of file sharing
what if a modified version A’’ overwrites a modifed version A’ (from two different people)?

####the lock-modify-unlock solution
- while one is editing, others cannot write.
- a bit restrictive:
	- locking may cause administrative problems. (forget to unlock, delay, waste time)
	- locking may cause unnecessary serialization. (changes have no overlap, could be done at the same time, but due to locking, this can only be done sequentially)
	- locking may create a false sense of security. (two modified files are semantically incompatible, after unlocking, they cannot work together)

####the copy-modify-merge solution
- subversion, CVS, and many other version control systems use a copy-modify-merge model instead of locking.
- working separately, merge together to a final version
- say two people get two working copies of A, they work concurrently and make changes to A. A’’ is saved first, then when one tries to save A’, the repository informs him that his file A is _out of date_. File A in the repository has somehow changed since he last copied it. So he needs his client to _merge_ any new changes from the repository into his working copy of A. Chances are that A’’ don’t overlap with A’; once he has both sets of changes integrated, he saves his working copy back to the repository.
- what if A’’ do overlap with A’? A _conflict_ happens.
	- when asking to merge, his copy of A is somehow flagged as being in a state of conflict: he will see both sets of conflicting changes and manually choose between them.
	- the software cannot automatically resolve conflicts; only human can do this.

##version control the subversion way
###subversion repositories
###revisions
A subversion client commits any number of files and directories as a single **atomic** transaction. (either all of the changes are accepted into the repository or none of them is)

each time the repo accepts a commit, it creates a new state of the filesystem tree, called a _revision_. Each revision is assigned as a unique natural number, one greater than the number assigned to the previous revision.

The initial revision of a repo is numbered 0- and consists of nothing but an empty root directory.

###addressing the repository
###subversion working copies
####how the working copy works
for each file in a working directory, subversion records:
	- what revision your working file is based on
	- a timestamp recording when the local copy was last updated by the repo

given info, by talking to repo, subversion can tell which of the following 4 states of a working file is in:
	- unchanged, and current (`svn commit` and `svn update` will do nothing)
	- locally changed, and current (`svn commit` will publish the changes, but `svn update` will do nothing)
	- unchanged, out of date (`svn commit` will do nothing, `svn update` will fold the latest changes into your working copy)
	- locally changed, and out of date (`svn commit` will fail with an ‘out-of-date’ error, should be update first; `svn update` will attempt to merge the public changes with local changes, if merge not completed automatically, need the user to resolve the conflict manually)

####fundamental working copy interactions
####mixed-revision working copies
#####updates and commits are separate
#####mixed revisions are normal
#####mixed revisions are useful
#####mixed revisions have limitations