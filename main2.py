import requests
import argparse
import re
import os

RED = "\033[1;31m"
GREEN = "\033[1;32;0m"
OKBLUE = "\033[94m"
WHITE = "\033[0;37m"

parser = argparse.ArgumentParser(description="Subdomain Takeover Scanner")
parser.add_argument(
	'-l',
	'--list',
	default='',
	help='python3 ItsOver.py [-l, --list] file contain list of domains'
)

args = parser.parse_args()
domainList = args.list

print("Takeover testing started fro detailed analysis please find dig.txt")

if len(str(domainList)) > 0:
	if os.path.isfile(domainList):
		readWords = open(domainList, 'r')

	else:
		exit("{}File Not Found Unable To Load Targets".format(RED))	
	
	print("{}[+] Loading Targets.... [+]\033[94m\n".format(WHITE))			
	subList = []
	vuln = []
	valid= []	
	validUrls = open('validUrls.txt', 'a')
	Takeover = open('Takeover.txt', 'a')

	for words in readWords:
		if not words.isspace():
			words = words.rstrip()
			words = words.replace("https://", "")
			words = words.replace("http://", "")
			words = words.replace("https://www.", "")
			words = words.replace("http://www.", "")
			words = words.replace("/", "")
			words = "http://{}".format(words)
			subList.append(words)
			validUrls.write("{}\n".format(words))
	
	validUrls.close()
	readWords.close()

	if len(subList) > 0:
		print("\n[!] Total {} Targets Loaded [!]\033[94m".format(len(subList)))
		print("{}[!] Checking For Subdomain Takeover..... [!]\n\033[94m".format(WHITE))
		
		VulnContents = ["<strong>Trying to access your account", 
		"Use a personal domain name", 
		"The request could not be satisfied", 
		"Sorry, We Couldn't Find That Page", 
		"Fastly error: unknown domain", 
		"The feed has not been found", 
		"You can claim it now at", 
		"Publishing platform",                        
		"There isn't a GitHub Pages site here",
		"There isn't a GitHub Pages site",
		"There's nothing here",                       
		"No settings were found for this company",
		"Heroku | No such app", 
		"<title>No such app</title>",                        
		"You've Discovered A Missing Link. Our Apologies!", 
		"Sorry, couldn&rsquo;t find the status page",                        
		"NoSuchBucket", 
		"Sorry, this shop is currently unavailable", 
		"<title>Hosted Status Pages for Your Company</title>", 
		"data-html-name=\"Header Logo Link\"",                        
		"<title>Oops - We didn't find your site.</title>",
		"class=\"MarketplaceHeader__tictailLogo\"",                        
		"Whatever you were looking for doesn't currently exist at this address", 
		"The requested URL was not found on this server", 
		"The page you have requested does not exist", 
		"This UserVoice subdomain is currently available!", 
		"but is not configured for an account on our platform", 
		"<title>Help Center Closed | Zendesk</title>",
		"Thereisn'taGitHubPagessitehere.",
        "ForrootURLs(likehttp://example.com/)youmustprovideanindex.htmlfile", 
        "There'snothinghere,yet.",
        "herokucdn.com/error-pages/no-such-app.html",
        "<title>Nosuchapp</title>", 
        "TherequestedURL/wasnotfoundonthisserver.",
        "TherequestedURLwasnotfoundonthisserver", 
        "There'snothinghere.",
        "Whateveryouwerelookingfordoesn'tcurrentlyexistatthisaddress.", 
        "Sorry,thisshopiscurrentlyunavailable.",
        "Onlyonestepleft!", 
        "You'veDiscoveredAMissingLink.OurApologies!", 
        "PleasetryagainortryDesk.comfreefor14days.",
        "Sorry,WeCouldn'tFindThatPage", 
        "Buildingabrandofyourown?",
        "totargetURL:<ahref=\"https://tictail.com",
        "StartsellingonTictail.", 
        "DoublechecktheURL",
        "<strong>Tryingtoaccessyouraccount?</strong>", 
        "404NotFound", 
        "BetterStatusCommunication",
        "Youarebeing<ahref=\"https://www.statuspage.io\">redirected", 
        "NoSuchBucket",
        "Thespecifiedbucketdoesnotexist", 
        "Therequestcouldnotbesatisfied",
        "ERROR:Therequestcouldnotbesatisfied", 
        "Thepageyouhaverequesteddoesnotexist", 
        "Domainisnotconfigured", 
        "IfyouareanAcquiaCloudcustomerandexpecttoseeyoursiteatthisaddress", 
        "Pleasecheckthatthisdomainhasbeenaddedtoaservice",
        "Fastlyerror:unknowndomain", 
        "Thegodsarewise",
        "Thegodsarewise,butdonotknowofthesitewhichyouseek.", 
        "<title>HelpCenterClosed|Zendesk</title>",
        "HelpCenterClosed", 
        "ThisUserVoicesubdomainiscurrentlyavailable!", 
        "Thethingyouwerelookingforisnolongerhere",
        "Thethingyouwerelookingforisnolongerhere,orneverwas", 
        "pingdom", 
        "Domainhasbeenassigned", 
        "Doyouwanttoregister", 
        "Oops-Wedidn'tfindyoursite.", 
        "Wecouldnotfindwhatyou'relookingfor.", 
        "Nosettingswerefoundforthiscompany:", 
        "Ifyou'removingyourdomainawayfromCargoyoumustmakethisconfigurationthroughyourregistrar'sDNScontrolpanel.", 
        "Thefeedhasnotbeenfound.", 
        "projectnotfound", 
        "data-html-name", 
        "Unrecognizeddomain<strong>", 
        "Thispageisreservedforartisticdogs.",
        "<pclass=\"description\">Thepageyouarelookingfordoesn'texistorhasbeenmoved.</p>", 
        "<h1>Thepageyouwerelookingfordoesn'texist.</h1>", 
        "Youmayhavemistypedtheaddressorthepagemayhavemoved.", 
        "<h1>Error404:PageNotFound</h1>", 
        "https://www.wishpond.com/404?campaign=true", 
        "Oops.</h2><pclass=\"text-mutedtext-tight\">Thepageyou'relookingfordoesn'texist.", 
        "Thereisnoportalhere...sendingyoubacktoAha!", 
        "ErrorCode:404", 
        "<h1>Oops!Wecouldn&#8217;tfindthatpage.</h1>", 
        "alt=\"LIGHTTPD-flylight.\"", 
        "DoublechecktheURLor<ahref=\"mailto:help@createsend.com", 
        "Thesiteyouarelookingforcouldnotbefound.", 
        "Ifyouneedimmediateassistance,pleasecontact<ahref=\"mailto:support@proposify.biz", 
        "Wecan'tfindthis<ahref=\"https://simplebooklet.com", 
        "name : getresponse",
        "WithGetResponseLandingPages,leadgenerationhasneverbeeneasier", 
        "Lookslikeyou'vetraveledtoofarintocyberspace.", 
        "isnotaregisteredInCloudYouTrack.", 
        "404WebSitenotfound"
		"Sorry, We Couldn't Find That Page Please try again"]

		for domain in subList:
			print("{}[-] Checking {} [-]\033[94m".format(WHITE, domain))		
			try:
				subDoamin = requests.get("{}".format(domain.rstrip()), timeout=5).text
				for VulnContent in VulnContents:
					if VulnContent in subDoamin:
						print("{}    >>-----> Vulnerable {}\033[94m \n".format(GREEN, domain))
						vuln.append(domain)
						valid.append(domain)
						Takeover.write("{}\n".format(domain))

				if not domain in vuln:
					print("{}  -- Not Vulnerable {}\033[94m \n".format(OKBLUE, domain))
					valid.append(domain)
					
			except:
					print("!! Timeout => {}\033[94m \n".format(domain.rstrip()))			
		

		print("\n".join(valid))
		Takeover.close()				
else:
    print("\nSubdomain Takeover tools\nAuthor: Joseph Paulose\n") 
