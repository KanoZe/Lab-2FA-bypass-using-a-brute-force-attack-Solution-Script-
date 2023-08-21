# Lab-2FA-bypass-using-a-brute-force-attack-Solution-Script-
The base_script needs to be given updated links to login and login2 pages since they keep chaning the links. 
The base script is a multithreaded script that runs a series of 2 (could be increased, just add new requests to the tasks)
async requests against the target url, it works by macroing the initial login process and then submitting the MFA code once from each async request. 
When there's a returned 302 response status, the response headers and session will be displayed which then can be used to 
navigate to the /my-account page and login in using the session.

The script itself spawns 10 of the above script to make use of multithreading, each with a range of 1000 calls, which cuts down the time to brute force 
by x10. The number of scripts can also be further customized. Just add new scripts to the tasks list and decreace the range for each to increase the number 
of scripts, and decrease it for doing the opposite. 
