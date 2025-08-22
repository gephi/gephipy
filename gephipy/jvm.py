import jpype

from pathlib import Path
import urllib.request

GTK_URL="https://repo1.maven.org/maven2/org/gephi/gephi-toolkit/0.10.1/gephi-toolkit-0.10.1-all.jar"

#
# Initialize the context
#
def initialize(gephi_jar_path="./gephi-toolkit-all.jar"):
    gtk_jar = Path(gephi_jar_path)
    if not gtk_jar.is_file():
      print("Download the Gephi toolkit jar")
      urllib.request.urlretrieve(GTK_URL, gephi_jar_path)
    # Starts the JVM with the GTK in the classpath
    try:
      jpype.startJVM(classpath=[gephi_jar_path])
    except OSError as e: 
      print(f"Warning: {e}")