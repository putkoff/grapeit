from abstract_utilities import *
import os
# Example data snippet
titles = [
    "Chief Technology Officer  Executive Finance Information Technology",
    "President and Co Founder   Operations",
    "Product Manager, Engineering Operations  Management",
    "Chief Executive Officer   Save",
    "Marketing and Product Director Product",
    "Engineering  Engineering",
    "CEO   Save",
    "President",
    "Vice President - Solar Farm Development  VP Management",
    "Program and Project Management  Manager Management",
    "Co-Founder, Chairman & Chief Executive Officer   Save",
    "Chief Technology Officer  Executive Engineering Information Technology",
    "Chief Financial Officer  Executive Finance",
    "Chief Operating Officer Executive Finance Operations",
    "Senior Vice President  VP Finance Management",
    "Vice President - Investments VP Management",
    "Vice President - Development  VP Engineering Information Technology Sales Save",
    "Vice President  VP Management Operations",
    "Senior Vice President - Development  VP Engineering Management",
    "Senior Vice President  VP Management Operations",
    "Senior Vice President - Projects and Engineering  VP Engineering Management",
    "Vice President, Investments & Project Finance VP Management",
    #... add the remaining titles here ...
]

# Dictionary to hold the mappings
title_dict = {}

# Function to clean and standardize titles
def clean_title(unclean_title):
    # Common replacements and cleanup
    replacements = {
        "Chief Executive Officer": "CEO",
        "Chief Operations Officer": "COO",
        "Chief Operating Officer": "COO",
        "Chief Financial Officer": "CFO",
        "Chief Technology Officer": "CTO",
        "President and Co Founder": "President",
        "Co-Founder, Chairman & Chief Executive Officer": "CEO",
        "Senior Vice President": "SVP",
        "Vice President": "VP",
        "Director": "Director",
        "Manager": "Manager",
        "Product Manager,": "Product Manager",
        "Program and Project Management": "Project Manager",
        "Executive": "",
        "Engineering": "Engineer",
        "Finance": "Finance",
        "Information Technology": "IT",
        "Operations": "Operations",
        "Management": "",
        "Marketing and Product Director": "Director of Sales/Marketing",
        "Marketing": "Sales/Marketing",
        "Sales": "Sales/Marketing",
        " - ": " ",
        ",": "",
        "  ": " ",
        "Save": ""
    }

    clean_title = unclean_title
    for key, value in replacements.items():
        clean_title = clean_title.replace(key, value).strip()
    
    # Simplify titles with multiple designations
    if "VP" in clean_title and "SVP" not in clean_title:
        clean_title = "VP"
    if "Engineer" in clean_title and clean_title.count(" ") > 1:
        clean_title = "Engineer"
    if "Manager" in clean_title and clean_title.count(" ") > 1:
        clean_title = "Manager"
    
    return clean_title.split("Showing")[0]
def get_title_js():
    if not os.path.isfile('title_js.json'):
        data={}
        safe_dump_to_file(data=data,file_path='title_js.json')
    return safe_read_from_json(file_path='title_js.json')
def save_title_js(key,value):
    data = get_title_js()
    data[key]=value
    safe_dump_to_file(data=data,file_path='title_js.json')
def change_titles():
    title_js = get_title_js()
    datas_clean=[]
    for data in DATAS.split('\n'):
        if data:
            spl_data = data.split("\t")
            title = spl_data[-1]
            if title not in title_js:
                title_js[title]=spl_data[-1]
                title_js[title] =     input(f'enter for original title:\n{spl_data[-1]}, \n\npress c for clean title:\n{clean_title(spl_data[-1])} \n\nmake a new one:') or title_js[title]
                if title_js[title] == 'c':
                   title_js[title]= clean_title(title)
                save_title_js(spl_data[-1],title_js[title])
                datas_clean.append({"name":spl_data[0],"emails":spl_data[1],"title":title_js[title]})
                while '' in spl_data:
                    spl_data.remove('')
    return get_title_js()
def get_company_name(name):
    return {"pvcomplete":"PV Complete","condoit":"Condoit","soltage":"Soltage","solar-states":"Solar States","38degreesn":"38 Degrees North","maltainc":"Malta inc.","southwestsunsolar":"Southwest Sun Solar"}.get(name,name)
DATAS = """
Brian Hogan	brian@pvcomplete.com	Chief Technology Officer  Executive Finance Information Technology
Claudia Eyzaguirre	claudia@pvcomplete.com	Operations Save
Daniel Sherwood	daniel@pvcomplete.com	President and Co Founder   Operations
Scott Mathewson	scott@pvcomplete.com	Product Manager, Engineering Operations  Management Showing 4 of 4
Ian Hoppe	ian@condoit.io	Chief Executive Officer   Save
Spencer Wyatt	spencer@condoit.io	Marketing and Product Director Product
Chauncey Philpot	chauncey@condoit.io	Engineering  Engineering
Tilden Hagan	tilden@greenstatepower.com	CEO   Save
Will Stewart	will@greenstatepower.com	President
Carrie Stewart	carrie@greenstatepower.com	Vice President - Solar Farm Development  VP Management
Joe Hodges	joe@greenstatepower.com	Program and Project Management  Manager Management Showing 4 of 4
Jesse Grossman	jgrossman@soltage.com	Co-Founder, Chairman & Chief Executive Officer   Save
Robin Gray	rgray@soltage.com	Chief Technology Officer  Executive Engineering Information Technology
Sripradha Ilango	silango@soltage.com	Chief Financial Officer  Executive Finance
Stephen Goodbody	sgoodbody@soltage.com	Chief Operating Officer Executive Finance Operations
Chaim Grushko	cgrushko@soltage.com	Senior Vice President  VP Finance Management
Dylan Hammer	dhammer@soltage.com	Vice President - Investments VP Management
Jonathan Roberts	jroberts@soltage.com	Vice President - Development  VP Engineering Information Technology Sales Save
Lori Bilella (they/them)	l(they/them)@soltage.com	Vice President  VP Management Operations
Marc Miller	mmiller@soltage.com	Senior Vice President - Development  VP Engineering Management
Mihir Mehta	mmehta@soltage.com	Senior Vice President  VP Management Operations
Paul Zensky	pzensky@soltage.com	Senior Vice President - Projects and Engineering  VP Engineering Management
Vidyu Kishor	vkishor@soltage.com	Vice President, Investments & Project Finance VP Management
Alex Schild	aschild@soltage.com	Director of Development Director Marketing Medical & Science
Brandon Ball	bball@soltage.com	Operations Director Operations
Evangelos Karambelas	ekarambelas@soltage.com	Director, Mergers and Acquisitions Director Finance Medical & Science
Fred Farella	ffarella@soltage.com	Director of Storage Development Director
Jason Miller	jmiller@soltage.com	Engineering Director Engineering Management
Joy Crossman	jcrossman@soltage.com	Sales and Support Director
Stephanie Sienkowski	ssienkowski@soltage.com	Business Management Director Medical & Science
Yolainne Mary Moran	ymoran@soltage.com	Director, Asset Management Director Medical & Science
Zac Meyer	zmeyer@soltage.com	Business Management Manager Director Management
Acacia Hernandez	ahernandez@soltage.com	Manager of Development Manager Sales
Dominic Lopez	dlopez@soltage.com	Program and Project Management Manager
Edgar Puesán	epuesán@soltage.com	Program and Project Management  Manager Operations Product
Jeannette Carambot	jcarambot@soltage.com	Finance and Administration Manager
Justin Chon	jchon@soltage.com	Finance and Administration  Manager Finance
Kate HollyWolf	khollywolf@soltage.com	Business Management Manager
Shemar Davis	sdavis@soltage.com	Finance and Administration  Manager Finance Operations
Sid Shah	sshah@soltage.com	Manager - Development Manager Management
Steve Rutherford	srutherford@soltage.com	Program and Project Management  Manager Management Operations
Vanessa Colon	vcolon@soltage.com	Operations Manager Manager Operations
Vanessa P. Colon	vcolon@soltage.com	Operations Manager Manager Operations
Asher Talerman	atalerman@soltage.com	Senior Finance Analyst
Audrey Aberg	aaberg@soltage.com	Finance and Administration
Catherine Griffin	cgriffin@soltage.com	Banking and Wealth Management
Connor Kreb	ckreb@soltage.com	Engineering  Engineering
Devang Shah	dshah@soltage.com	Business Management
Dirk Ouwerkerk	douwerkerk@soltage.com	Engineering  Engineering
Dominic Lopez	dlopez@soltage.com	Project Manager  Management
Hediamarie Rodriguez	hrodriguez@soltage.com	Staff Accountant  Management
Ilan Gmach	igmach@soltage.com	Senior Asset Manager  Finance
Iradeep Sachar	isachar@soltage.com	Finance and Administration
Jamak Ali	jali@soltage.com	Finance and Administration
Jon Marco Sanchez	jsanchez@soltage.com	Engineering  Engineering
Junhao Gao	jgao@soltage.com	Finance and Administration
Justin Castro	jcastro@soltage.com	Project Engineer  Engineering
Lucas Maass	lmaass@soltage.com	Finance and Administration
Mohammed Alam	malam@soltage.com	Business Management
Noah Conforti	nconforti@soltage.com	Finance and Administration
Samuel Maddox	smaddox@soltage.com	Asset Manager  Finance
Sylar Holmes	sholmes@soltage.com	Finance and Administration
Thomas Stewart	tstewart@soltage.com	Finance and Administration
Yolainne Moran	ymoran@soltage.com	Finance and Administration
Nick Snow	nsnow@soltage.com	Director of Operations Medical & Science Showing 54 of 54
Micah Gold-Markel	micah@solar-states.com	Founder
Skyler Willman-Cole	skyler@solar-states.com	Chief Operations Officer   Operations Save
Jael Sims	jael@solar-states.com	Director of Human Resources and Business Operations  Director Sales
Agustina Cusimano	agustina@solar-states.com	Program and Project Management Manager
Ava Shore	ava@solar-states.com	Logistics Manager Manager Operations
Jack Steketee	jack@solar-states.com	Operations Manager Operations
Jacob Gross	jacob@solar-states.com	Sales and Support  Manager Operations
Jared Pashko	jared@solar-states.com	Real Estate  Manager Pro Services
Marc Shackelford-Rowell	marc@solar-states.com	Installer / Permitting and Interconnection Manager / Project Manager Manager Management
Marilyn Candeloro	marilyn@solar-states.com	Business Management Manager
Oliver Ingram	oliver@solar-states.com	Program and Project Management Manager
Sebastian Zawierucha	sebastian@solar-states.com	Operations Manager Operations
Andrew Kleeman	andrew@solar-states.com	Sales and Support
Bill McBride	bill@solar-states.com	Community
Eric Papa	eric@solar-states.com	Sales and Support
Greg Smith	greg@solar-states.com	Consulting
Gregory Mollusky	gregory@solar-states.com	Project Manager  Operations
Isaiah Smith	isaiah@solar-states.com	Engineering  Engineering
Leif Barron	leif@solar-states.com	Solar & Battery Designer  Management
Mariia Ktitorova	mariia@solar-states.com	Operations  Operations
Maurice Peaker	maurice@solar-states.com	Operations  Operations
Michael Mannix	michael@solar-states.com	Chief Education Officer  Finance
Moises Morales	moises@solar-states.com	Education Department Lead
Todd Baylson	todd@solar-states.com	Partnerships, Policy and Solar Projects  Sales
Zach Dean	zach@solar-states.com	Solar Energy Consultant  Sales Showing 25 of 25
Albert Morales	albert.morales@maltainc.com	Chief Financial Officer  Executive Finance
Ramya Swaminathan	ramya.swaminathan@maltainc.com	CEO  Save
Alvaro Mozo	alvaro.mozo@maltainc.com	Vice President, Supply Chain VP Management
Ben Bollinger	ben.bollinger@maltainc.com	VP Strategic Initiatives  VP Engineering Management
Erhan Karaca	erhan.karaca@maltainc.com	VP of Engineering VP Management
Kevin Stone	kevin.stone@maltainc.com	Vice President, Engineering  VP Engineering Information Technology Management
Melissa DeValles	melissa.devalles@maltainc.com	Vice President, North America VP Pro Services
Ahmed Kherati	ahmed.kherati@maltainc.com	Finance and Administration Manager Director Finance
Alessio Cacitti	alessio.cacitti@maltainc.com	Director, Control Systems Engineering Director Medical & Science
Gunnar Marquardt	gunnar.marquardt@maltainc.com	Finance and Administration Director Finance
Jin Noh	jin.noh@maltainc.com	Sales and Support Director
Mert Geveci	mert.geveci@maltainc.com	Director, Digital Technologies Director Information Technology
Samar Shah	samar.shah@maltainc.com	Marketing and Product Director Operations
Tom LeRoy	tom.leroy@maltainc.com	Principal Plant Systems Integration Leader Director Management
Carla Niederhofer	carla.niederhofer@maltainc.com	Program and Project Management Manager Operations
Michael Geyer	michael.geyer@maltainc.com	Engineering Manager Engineering
Mike Boisclair	mike.boisclair@maltainc.com	Engineering Manager Engineering
Tian J. Ong	tian.ong@maltainc.com	Marketing and Product  Manager Engineering
Alex J Dunne	alex.dunne@maltainc.com	Legal  Legal
Alex Vicente Hernandez	alex.hernandez@maltainc.com	Legal  Legal
Alexandra "Alie"" Pruner"	alexandra.pruner"@maltainc.com	Business Management
Bao Truong	bao.truong@maltainc.com	Technical Lead, Strategic Initiatives  Information Technology
Danielle Colson	danielle.colson@maltainc.com	Commercialization Associate  Operations
David Martin	david.martin@maltainc.com	Marketing and Product
Elyse Doyle	elyse.doyle@maltainc.com	Project Manager  Pro Services
Erin O'Kelly	erin.o'kelly@maltainc.com	Finance and Administration
Geoff Cusano	geoff.cusano@maltainc.com	Engineering  Engineering
Grant Wirth	grant.wirth@maltainc.com	Finance and Administration
Jaime Gonzalez	jaime.gonzalez@maltainc.com	Engineering  Engineering
Janina Hippler-Nettlau	janina.hippler-nettlau@maltainc.com	Project Engineer  Engineering
Kurt Waldner	kurt.waldner@maltainc.com	Senior Product Manager  Product
Luke Rose	luke.rose@maltainc.com	Head of Sustainability
Maeve Rushe	maeve.rushe@maltainc.com	Communications Associate  Management
Philippe Delleville	philippe.delleville@maltainc.com	Business Management
Ramya Swaminathan	ramya.swaminathan@maltainc.com	Business Management
Todd Bates	todd.bates@maltainc.com	Finance Associate  Management
Venkatesh Chinnakonda	venkatesh.chinnakonda@maltainc.com	Commercialization Associate  Engineering Showing 37 of 37
Mimi Ngo	mimi@southwestsunsolar.com	President   Save
Hugh Nguyen	hugh@southwestsunsolar.com	Director Director Medical & Science
Betty Valdez	betty@southwestsunsolar.com	Sales and Support Manager
Jesus Soto	jesus@southwestsunsolar.com	Sales and Support Manager Operations
Kay Heap	kay@southwestsunsolar.com	Sales and Support Manager Operations
Mon Caleon	mon@southwestsunsolar.com	Sales and Support Manager Management Operations
Serafin Pereyra	serafin@southwestsunsolar.com	Regional Manager Manager Management
Trang Pham	trang@southwestsunsolar.com	Sales and Support Manager Operations
Christopher Cao	christopher@southwestsunsolar.com	Senior Engineer  Engineering
Hieu Nguyen	hieu@southwestsunsolar.com	Business Management  Operations Show More Showing 10 of 14
Timothy Luthin	timothy@38degreesn.com, tim@38degreesn.com	Vice President  VP Management Save
Lara Younes	lara@38degreesn.com, unknown@38degreesn.com	Banking and Wealth Management Manager
Bob Schutz	bob@38degreesn.com, unknown@38degreesn.com	Business Management
Chris Bailey	chris@38degreesn.com, unknown@38degreesn.com	Partner  Management
Eric Restic, CPA	unknown@38degreesn.com, eric@38degreesn.com	Finance and Administration
Jack Williams	jack@38degreesn.com, unknown@38degreesn.com	Banking and Wealth Management
Jake Carney	unknown@38degreesn.com, jake@38degreesn.com	Business Management
Manaswini Challa	unknown@38degreesn.com, manaswini@38degreesn.com	Banking and Wealth Management
Ryan Bennett	ryan@38degreesn.com, unknown@38degreesn.com	Business Management
Ryan Macdonald	ryan@38degreesn.com, unknown@38degreesn.com	Investment Associate  Showing 10 of 10
Ali Kchia	ali.kchia@bcg.com	Finance and Administration  Save
Matthew Hayes	matthew.hayes@bcg.com	Head of Development and Origination  Showing 2 of 2
"""

def get_message(Name,jobTitle,companyName):
    return f"""{Name},

 

I know you’re the {jobTitle} at {companyName} so I wanted to reach out- my name is Matt Matsuda, EVP of Westlake Origination Center. We are a Live-Transfer Fulfillment company that provides exclusive, region specific solar transfers. 

 

I’m reaching out because I want to give you 20 live transfers, absolutely for free with no strings attached.

We provide the highest quality live transfers in the industry, which provides you with an unmatched ROI on your money and your top agents time-and I’m willing to put my money where my mouth is to prove it to you, again at no cost.

 

Let me know when would be good for us to speak or feel free to call me at 916.750.9165. I look forward to speaking with you!

 

20 leads even at 25k per system = $500,000 in business for free…. Why not?"""
for data in DATAS.split('\n'):
    if data:
        spl_data = data.split("\t")
        input(get_message(spl_data[0],get_title_js()[spl_data[-1]],get_company_name(spl_data[1].split('@')[1].split('.')[0])))
    
        

