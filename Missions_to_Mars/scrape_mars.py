from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
        #Initiate connection to test browser
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        
        url = 'https://redplanetscience.com/'
        browser.visit(url)
        html=browser.html
        soup=bs(html,'html.parser')
        
        #Scrape the [Mars News Site](https://redplanetscience.com/) 
        #Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference 
        News_Title = soup.find_all('div', class_='content_title')[0].text
        
        #Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference 
        News_Paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
        
        #JPL Connection
        JPL_url = 'https://spaceimages-mars.com'
        browser.visit(JPL_url)
        html=browser.html
        soup=bs(html,'html.parser')
        
        #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
        image_url = browser.find_by_tag("img[class='headerimage fade-in']")['src']
        
        ## Mars Facts
        Facts_url = 'https://galaxyfacts-mars.com'
        browser.visit(Facts_url)
        html=browser.html
        soup=bs(html,'html.parser')
        
        #Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
        table = pd.read_html(Facts_url)
        # Store Mars table as DF
        facts_df = table[1]
        
        #Use Pandas to convert the data to a HTML table string.
        table_html = facts_df.to_html()
        table_html
        
        #Mars Hemispheres
        Hemispheres_url = 'https://marshemispheres.com/'
        browser.visit(Hemispheres_url)
        html=browser.html
        soup=bs(html,'html.parser')
        
        #Loop through hemisphere titles and append to list
        Names = []
        Hemisphere_Names = soup.find_all('h3')
        Hemisphere_Names
        
        #Loop and add to list
        for name in Hemisphere_Names:
            Names.append(name.text)

        Names = Names[:-1]
        Names = Names[0:4]
        Names
        
        #Save Hemisphere URLs
        Image_URLs = []
        Image_Path = soup.find_all('img')
        
        #https://stackoverflow.com/questions/5815747/beautifulsoup-getting-href
        #use soup.find_all to find every 'a' element with 'href' attribute, append to list
        thumbnail_list=[]

        for link in soup.find_all('a', href=True):
            if(link.img):
                thumbnail_url='https://marshemispheres.com/'+link['href']
                thumbnail_list.append(thumbnail_url)
        thumbnail_list
        #slice list
        thumbnail_list=thumbnail_list[3:]
        thumbnail_list
        
        #Full Image Links
        image_title_url=[]
        for thumb in thumbnail_list:
            url = thumb
            browser.visit(url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_title=soup.find('h2', class_='title').get_text()
            url=browser.find_by_text('Sample')['href']
            dictionary={'title':image_title,'img_url':url}
            image_title_url.append(dictionary)
        
        browser.quit()
        
        #All scraped data
        Mars_data={
            'News_Title':News_Title,
            'News_Paragraph':News_Paragraph,
            'JPL_Image':image_url,
            'HTML_Table':table_html,
            'Hemispheres':image_title_url
        }
        
        #Return results
        return Mars_data
            
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        