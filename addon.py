import xbmcgui
import xbmcaddon
import requests

__addon__ = xbmcaddon.Addon(id='plugin.audio.headphones_manager')

hostname=__addon__.getSetting("hostname")
port=__addon__.getSetting("port")
apikey=__addon__.getSetting("api")

dialog = xbmcgui.Dialog()
search_term = dialog.input('Enter Artist to add:', type=xbmcgui.INPUT_ALPHANUM, autoclose=20000)

if search_term:

	base_url="http://"+hostname+":"+port+"/api?apikey="+apikey+"&cmd="

	try:
		headphones_response=requests.get(base_url+"findArtist&name="+search_term)

		artistlist=[]
		if headphones_response.status_code < 400:
			response_fields=headphones_response.json()
			if response_fields is False:
				xbmcgui.Dialog().ok('Headphones response:','Search did not return any usable results.')
			else:
				for artist in response_fields:
					artistlist.append(str(artist['score']).rjust(3)+"% - "+artist['uniquename'])

				chosen=xbmcgui.Dialog().select('Choose artist to add:',artistlist)
				
				if chosen is not -1:

					xbmcgui.Dialog().notification('Adding/updating artist:',response_fields[chosen]['uniquename'])

					mbid=response_fields[chosen]['id']
					requests.get(base_url+"addArtist&id="+mbid)
		
		else:
			xbmcgui.Dialog().ok('Something went wrong:','Headphones appears to be non-responding.')

	except requests.exceptions.RequestException:
		xbmcgui.Dialog().ok('Something went wrong:','Headphones appears to be non-responding.')