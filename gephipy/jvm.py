import jpype

from pathlib import Path
import urllib.request

started = None
""" whether the JVM has been started """

GTK_URL="https://repo1.maven.org/maven2/org/gephi/gephi-toolkit/0.10.1/gephi-toolkit-0.10.1-all.jar"

def lol():
  jpype.startJVM(classpath=["./gephi-toolkit-all.jar"])
    
#
# Initialize the context
#
def start(gephi_jar_path="./gephi-toolkit-all.jar"):
  global started
  print(started)
  if started is None:
    gtk_jar = Path(gephi_jar_path)
    if not gtk_jar.is_file():
      print("Download the Gephi toolkit jar")
      urllib.request.urlretrieve(GTK_URL, gephi_jar_path)
    
    # Starts the JVM with the GTK in the classpath
    try:
      print("start JVM")
      jpype.startJVM(classpath=[gephi_jar_path])
    except OSError as e: 
      print(f"Warning: {e}")
    
    started = True
    
def stop():
  """
  Kills the JVM.
  """
  global started
  if started is not None:
    started = None
    jpype.shutdownJVM()