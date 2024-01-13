from flask import Flask,render_template,request
from bs4 import BeautifulSoup
import requests
import os
import logging
logging.basicConfig(filename='scraper.log',level=logging.INFO)

app = Flask(__name__)

#home page
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

#review page
@app.route('/review',methods=['GET','POST'])
def review():
    if request.method == 'POST':
        try:
            #getting the query from html page and removing the space
            query = request.form['content'].replace(" ","")
            
            #directory for images
            save_dir = "images/"
            
            #creating a directory if not exists
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            #headers to not getting blocked by google    
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            
            #keyword to search
            query = "elonmusk"
            
            #generating a response
            response = requests.get(f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwjGzIzw9NmDAxWnlWMGHTkhCZ0Q2-cCegQIABAA&oq=elonmusk&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyCggAEIAEEIoFEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOg0IABCABBCKBRBDELEDOggIABCABBCxA1D2Alj2AmDABWgAcAB4AIABaYgBzwGSAQMwLjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=TkWiZcbtBqerjuMPucKk6Ak&bih=742&biw=1536")
            
            #creating a beautifulsoup object
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #listing all the image tags from the response
            image_tags = soup.find_all('img')
            
            #deleting the first item as it not a valid data
            del image_tags[0]
            
            #saving the image in the directory
            image_data = []
            for i in image_tags:
                image_url = i['src']
                image_data = requests.get(image_url).content
                with open(os.path.join(save_dir,f'{query}_{image_tags.index(i)}.jpg'),'wb') as f:
                    f.write(image_data)
                    
            
            return "Image Loaded"
        
        
        except Exception as e:
            logging.info(e)
            return "Something is wrong"
        
    else:
        render_template("index.html")
        
    
                    
if __name__ == "__main__":
    app.run(debug=True)