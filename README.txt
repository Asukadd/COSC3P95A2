For the ass2 of COSC3P95A2, ta may use vscode to run codes.
(We wrote some codes and put some ideals in it but it cannot run we save as ServerSide and ClientSide)
Firstly, ta should run Createfiles.py to create 20 files with varying sizes, from 5KB to 100MB.
Then, ta may use 2 terminals. One run python ServerSide.py firstly and another run python ClientSide.py after running python ServerSide.
If ta wants to finish runng, ta will go to WINDOWS TERMINAL to close the process by 
netstat -ano | findstr :9999 to check PID and  use taskkill /F /PID num you see.
For example, >netstat -ano | findstr :9999
  TCP    0.0.0.0:9999           0.0.0.0:0              LISTENING       27888
>taskkill /F /PID 27888