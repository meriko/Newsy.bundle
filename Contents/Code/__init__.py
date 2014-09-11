TITLE  = 'Newsy News'
PREFIX = '/video/newsy'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
BASE_URL = 'http://www.newsy.com'

###################################################################################################
def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art    = R(ART)
    DirectoryObject.thumb  = R(ICON)
    
    HTTP.CacheTime             = CACHE_1HOUR
    HTTP.Headers['User-agent'] = USER_AGENT
    
###################################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
    oc = ObjectContainer()
    
    title = 'Most Popular'
    oc.add(
        DirectoryObject(
            key =
                Callback(
                    MostPopular,
                    title = title,
                    url = BASE_URL + '/'
                ),
            title = title
        )
    )
    
    title = 'Recent'
    oc.add(
        DirectoryObject(
            key =
                Callback(
                    Videos,
                    title = title,
                    url = BASE_URL + '/'
                ),
            title = title
        )
    )

    pageElement = HTML.ElementFromURL(BASE_URL)
    
    for item in pageElement.xpath("//*[@id='topnav']//li"):
        url = item.xpath(".//a/@href")[0]
        
        if not url.startswith("http"):
            url = BASE_URL + url
        
        title = item.xpath(".//a/text()")[0].title()
        
        oc.add(
            DirectoryObject(
                key =
                    Callback(
                        Videos,
                        title = title,
                        url = url
                    ),
                title = title
            )         
        )
    
    
    return oc

####################################################################################################
@route(PREFIX + '/MostPopular')
def MostPopular(title, url):
    oc = ObjectContainer(title2 = title)
    
    pageElement = HTML.ElementFromURL(url)
    
    for item in pageElement.xpath("//*[@class='mph_video']"):
        videoURL = item.xpath(".//a/@href")[0]

        if not videoURL.startswith('http'):
            videoURL = BASE_URL + videoURL
            
        videoTitle = item.xpath(".//a/text()")[0]
        videoThumb = item.xpath(".//img/@src")[0]
        
        oc.add(
            VideoClipObject(
                url = videoURL,
                title = videoTitle,
                thumb = videoThumb
            )
        )
        
    return oc
    

####################################################################################################
@route(PREFIX + '/Videos', page = int)
def Videos(title, url, page = 1):
    oc = ObjectContainer(title2 = title)
    
    pageElement = HTML.ElementFromURL(url + "?page=" + str(page))
    
    for item in pageElement.xpath("//*[@class='rvs']//*[@class='rv']"):        
        videoURL = item.xpath(".//a/@href")[0]
        
        if not videoURL.startswith('http'):
            videoURL = BASE_URL + videoURL
            
        videoTitle = item.xpath(".//a/text()")[0]
        videoThumb = item.xpath(".//img/@src")[0]
        
        oc.add(
            VideoClipObject(
                url = videoURL,
                title = videoTitle,
                thumb = videoThumb
            )
        )
        
    if len(oc) < 1:
        oc.header  = "Sorry"
        oc.message = "Couldn't find any more videos"
    else:
        oc.add(
            NextPageObject(
                key =
                    Callback(
                        Videos,
                        title = title,
                        url = url,
                        page = page + 1
                    ),
                title = 'More ...'
            )
        )
      
    return oc
