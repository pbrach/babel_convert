"""
Convert CIF to SDF and remove hydrogens and also separate
to connected components
"""

import subprocess
import sys
import threading

in_name = sys.argv[1]
outname = sys.argv[2]

"""
Convert CIF to SDF and remove hydrogens and properties
"""
p1 = subprocess.Popen([
  "obabel", 
  "-icif",
  in_name, 
  "-osdf", 
  "-O", 
  outname,
  "-e",              # try to continue after errors
  "---errorlevel 0", # out put only very severe errors
  "-xm",             # wirte no properties
  "-d"])             # delete hydrogens

# Killer thread - kill after 150 seconds
kill_1 = threading.Timer(150.0, p1.kill )
kill_1.start()

# cancel the kill process if it was not necessary:
p1.wait() #we can start with p2 only if p1 ended
kill_1.cancel()


"""
Separate connected components into their individual molecule entries
"""
p2 = subprocess.Popen([
  "obabel", 
  "-isdf",
  outname, 
  "-osdf", 
  "-O", 
  outname,
  "-e",
  "---errorlevel 0",
  "--separate"])     # split into connectedComponents

# Killer thread - kill after 150 seconds

kill_2 = threading.Timer(150.0, p2.kill )
kill_2.start()

# cancel the kill process if it was not necessary:
p2.wait()
kill_2.cancel()



