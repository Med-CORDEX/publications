import os
import requests
from collections import defaultdict

# Constants for Zotero API
GROUP_ID = "5816477"
COLLECTION_KEYS = ["CVB532F5", "DKDV3KN4"]
API_URL_TEMPLATE = f"https://api.zotero.org/groups/{GROUP_ID}/collections/{{}}/items"
HEADERS = {"Accept": "application/json"}

OUTPUT_FILE = "docs/publications.html"

def fetch_all_items():
    items = []

    for collection_key in COLLECTION_KEYS:
        start = 0
        limit = 100
        while True:
            response = requests.get(
                API_URL_TEMPLATE.format(collection_key),
                headers=HEADERS,
                params={"format": "json", "limit": limit, "start": start}
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch Zotero items for collection {collection_key}: {response.status_code}")

            page_items = response.json()
            if not page_items:
                break

            items.extend(page_items)
            start += len(page_items)

    return items

def format_authors(creators):
    authors = [f"{c['lastName']}, {c['firstName'][0]}." for c in creators if c.get("creatorType") == "author" and c.get("lastName")]
    return ", ".join(authors)

def extract_metadata(item):
    data = item.get("data", {})
    creators = data.get("creators", [])
    authors = format_authors(creators)
    title = data.get("title", "Untitled")
    publication = data.get("publicationTitle", data.get("journalAbbreviation", ""))
    year = data.get("date", "")[:4] if data.get("date") else "Unknown"
    doi = data.get("DOI", None)
    url = f"https://doi.org/{doi}" if doi else data.get("url", "")
    return year, f'''
    <li>
      {authors}
      <a href="{url}">
        {title}
      </a>
      {publication}, {year}
    </li>
    '''

def generate_html(grouped_by_year):
    lines = []
    for year in sorted(grouped_by_year.keys(), reverse=True):
        n_pub = len(grouped_by_year[year])
        lines.append(f'''
<p id="btn-cap{year}" class="capitolo">
  <span id="char-cap{year}" class="aprichiudi">
    <img alt="apri" src="https://www.medcordex.eu/charapri.jpg">
  </span>
  {year}: {n_pub} publication{'s' if n_pub != 1 else ''}
</p>

<div id="id-cap{year}" class="testocap">
  <ul class="biblio">
        ''')
        for entry in sorted(grouped_by_year[year]):
            lines.append(entry)
        lines.append('''
  </ul>
</div>
        ''')
    return "\n".join(lines)

header = '''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
   <script type="text/javascript" async="" src="https://www.medcordex.eu/js"></script>
   <script async="" src="https://www.google-analytics.com/analytics.js"></script>
   <script src="https://www.medcordex.eu/js/jquery-1.7.1.min.js"></script>
   <script src="https://www.medcordex.eu/js/js.js"></script>

   <link href="https://www.medcordex.eu/css/style_css.css" rel="stylesheet" >
   <link href="https://www.medcordex.eu/css/responsive.css" rel="stylesheet" >
   <link href="https://www.medcordex.eu/css/flexslider.css" rel="stylesheet"  > 
   <link href="https://www.medcordex.eu/css/css_default.css" rel="stylesheet"  > 
   <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,400italic,700' rel='stylesheet' type='text/css'>
   <link href='https://fonts.googleapis.com/css?family=Oswald:400,300' rel='stylesheet' type='text/css'>
   <link href="https://www.medcordex.eu/css_printer.css"   type="text/css" rel="stylesheet" media="print">
    <title>Med-CORDEX</title>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-33912801-1', 'auto');
  ga('send', 'pageview');
</script>

</head>
<body>
<div id="wrapper">

  <div id="header">
  <header>
<div class="zzz">
<div id="logo" class="sssssfloatleft">
<a href="https://www.medcordex.eu/"><img class="centro" src="https://www.medcordex.eu/logo_medcordex_200.png" alt="medcordex logo" title="medcordex logo"></a> 

</div>
</div>

    <div id="btn-menu" class="btn-responsive-menu">
       <span class="icon-bar"></span>
       <span class="icon-bar"></span>
       <span class="icon-bar"></span>
    </div>
  </header>
  </div>


  <div id="mainmenu" data-role="navbar">
     <ul>	  <li>
	   <a href="https://www.medcordex.eu/index.php/">	    <span>home</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/simulations-phase1.php">	    <span>simulations phase 1</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/simulations-phase2.php">	    <span>simulations phase 2</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/simulations-phase3.php">	    <span>simulations phase 3</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/medcordex.php">	    <span>database</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/search/index.php">	    <span>search/download</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/cdo/">	    <span>use data</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/medcordex_help.php">	    <span>help</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/sitemap/">	    <span>sitemap</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/news/">	    <span>news (Mar 04, 2024)</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/medcordex_workshops.php">	    <span>workshops</span></a>
	    	  </li><li class="lev1sel">
	   <a href="https://med-cordex.github.io/publications/publications.html">	    <span>publications</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/references.php">	    <span>references</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/contatti.php">	    <span>contacts</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/stats/medcordex_user_flags.php/">	    <span>users by nation</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/login/">	    <span>login</span></a>
	    	  </li><li>
	   <a href="https://www.medcordex.eu/cookies/">	    <span>privacy</span></a>
	    </li></ul>  </div>

<h1 id="site-title2">publications</h1><br><div id="ddmain">
<div id="content">

<p>If you plan to submit publications using Med-CORDEX simulations, please refer it with a simple sentence in the Acknowledgment: <em>"This work is part of the Med-CORDEX initiative (www.medcordex.eu) supported by the HyMeX programme (www.hymex.org)" </em>
 or  <em>"The simulations used in this work were downloaded from the Med-CORDEX database (www.medcordex.eu)"</em>.
<br>We strongly encourage people downloading data from the Med-CORDEX 
database to contact the model data producers in order to give feedbacks 
on the model simulations, interact on the scientific studies and/or 
propose co-authorships.
</p>
<h1>Publications based on Med-CORDEX simulations</h1>
'''

footer = '''
 <!-- content --></div>
 <!-- ddmain --></div>
 </div>  <!-- wrapper -->
 <div class="nofloat">
<hr>
    <p class="centro">
Your browser has cookies enabled and Google Analytics is enabled. 
Please <a class="bold" href="https://www.medcordex.eu/cookies/">see our privacy policy</a>
<br> For any problem concerning the usability of this web site, please mail emanuele.lombardi@enea.it
</p>
    </div> <!-- bottom2 -->
</body></html>
'''

def main():
    items = fetch_all_items()
    publications_by_year = defaultdict(list)

    for item in items:
        try:
            year, entry = extract_metadata(item)
            publications_by_year[year].append(entry)
        except Exception as e:
            print(f"Skipping item due to error: {e}")

    html = header + generate_html(publications_by_year) + footer

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE} with {sum(len(v) for v in publications_by_year.values())} publications.")

main()

