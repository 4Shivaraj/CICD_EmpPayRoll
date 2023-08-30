# CICD_EmpPayRoll

I Got an error as "Error saving credentials: error storing credentials - err: exit status 1, out: `error listing credentials - err: exit status 0xc0000142, out: ```"

Resolution: 

Solution

In the file ~/.docker/config.json, change credsStore to credStore (note the missing s).

Explanation

The error seems to be introduced when moving from 'docker' to 'Docker Desktop', and vice-versa. In fact, Docker Desktop uses an entry credsStore, while docker installed from apt uses credStore.