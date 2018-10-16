 rem usage:   profile.cmd   <python.exe> <python_script> <suffixe>
 rem
 rem   generate file profile_<suffixe>.txt
 rem
%1 -m cProfile -s cumtime %2 > profile_%3.txt