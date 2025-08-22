from IPython.display import HTML

#
# Display a SVG in Jupyter notebook with pan & zoom  
#
def display_svg(file_path, width="100%", height="500px"):
  with open(file_path, 'r') as file_svg:
    svg = file_svg.read()

  html_code = f"""
    <script src="//bumbu.me/svg-pan-zoom/dist/svg-pan-zoom.js"></script>
    <div id="svg-container">
    {svg}
    </div>
    <script>
    var svgElement = document.getElementById("svg-container").children[0];
    svgElement.style.width = "{width}";
    svgElement.style.height = "{height}";
    svgPanZoom(svgElement, {{
        zoomEnabled: true,
        controlIconsEnabled: true
    }});
    </script>
  """

  HTML(html_code)