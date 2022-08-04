REM Timestamp stdout&stderr logfile
echo >> logs\triggerOutputs.log
echo -------------------------------------------------------------------------------- >> logs\triggerOutputs.log
date /t >> logs\triggerOutputs.log
time /t >> logs\triggerOutputs.log
echo -------------------------------------------------------------------------------- >> logs\triggerOutputs.log

REM Dump stdout&stderr in logs\triggerOutput.log
.venv\Scripts\activate.bat && python main.py -j ambitofinanciero -j clarin -j infobae -j la100 -j lanacion -j pagina12 -j radiomitre -j tn 1>> logs\triggerOutputs.log 2>&1 && echo Successful run >> logs\triggerOutput.log && exit
echo SOMETHING WENT WRONG AND THE SCRAPPER EXITED ABNORMALLY!!! >> logs\triggerOutput.log 
exit
