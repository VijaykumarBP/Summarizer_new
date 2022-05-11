import uuid
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import openai
import gtts
from .models import Prompt, PromptReview, Review
from .forms import PromptForm, ReviewForm, PromptReviewForm
from django.utils.datastructures import MultiValueDictKeyError
import string, random
import os
from django.contrib import messages
import pdfplumber
import docx
from langdetect import detect
import newspaper
from newspaper import Config
import json
from PIL import Image
import pytesseract
from .secrets import secrets
from decouple import config


FILE_TYPES = ['pdf','docx']
FILE_TYPES_IMG = ['jpg','jpeg','jfif','png','JPG','JPEG','JFIF','PNG']

# Create your views here.
def test(request):
    return render(request, 'home.html')

class Error(Exception):
    pass

class PromptRaiseError(Error):
    pass

def summary(request):
    if request.method == "POST":
        myRange = request.POST['myRange']
        url = request.POST['url']
        file_type = ""
        myFile = ""
        prompt1 = ""
        print("URL&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",url)
        try:
            if url == "":            
                if request.FILES:
                    myFile = request.FILES['myFile']
                    file_type = str(myFile).split('.')[-1]
                else:
                    prompt1 = request.POST['prompt']

                try:
                    if file_type == "pdf":
                        # pdfFileObj = open(myFile, 'rb')
                        with pdfplumber.open(myFile) as pdf:
                            first_page = pdf.pages[0]
                            print(first_page.extract_text())                              
                            prompt1 += first_page.extract_text()
                    elif file_type == "docx":
                        doc = docx.Document(myFile)
                        print(len(doc.paragraphs))
                        fullText = []
                        for para in doc.paragraphs:
                            fullText.append(para.text)
                        prompt1 = ""
                        prompt1 = '\n'.join(fullText)
                    elif file_type in FILE_TYPES_IMG:
                        pytesseract.pytesseract.tesseract_cmd = 'C:/Users/VI20279003/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
                        # pytesseract.pytesseract.tesseract_cmd = 'https://github.com/VijaykumarBP/News_Summairzer/tree/main/static/tesseract.exe'                        
                        im = Image.open(myFile)
                        prompt1 = pytesseract.image_to_string(im)
                    elif file_type not in FILE_TYPES and file_type not in FILE_TYPES_IMG and prompt1=="" and url=="":
                        if len(prompt1) < 1 and len(url) < 1:
                            messages.error(request,"Please paste URL or upload a file/image or paste an article in the text area")
                        elif file_type not in FILE_TYPES:
                            messages.error(request,"Please upload either PDF or DOCX file only")
                        elif file_type not in FILE_TYPES_IMG:
                            messages.error(request,"Please upload images in (JPG/PNG/JFIF) formats only")
                        return HttpResponseRedirect('/')
                except:
                    messages.error(request,"The file seems to be invalid, please upload a valid file!!")
                    return HttpResponseRedirect('/')            
            else:
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
                config = Config()
                config.browser_user_agent = user_agent
                config.request_timeout = 10

                article = newspaper.Article(url=url, config=config)
                print("AAARTICLEEEEEEEEEE", article)
                article.download()
                article.parse()

                article = {
                    "title": str(article.title),
                    "text": str(article.text),
                    "authors": article.authors,
                    "published_date": str(article.publish_date),
                    "top_image": str(article.top_image),
                    "videos": article.movies,
                    "keywords": article.keywords,
                    "summary": str(article.summary)
                }
                prompt1 = article["text"]
                
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect('/')
        
        language = detect(prompt1)
        print('DETECTED', language)
        engine = request.POST['engine']
        # language = request.POST['language']
        article_name = request.POST['article_name']
        prompt = prompt1 + " \nTl;dr:"
        try:
            audiocheck = request.POST['audiocheck']
        except:
            audiocheck = False
        
        while True:
            try:                
                if  len(prompt1) <= 50 :
                    raise PromptRaiseError
                else:                        
                    openai.api_key = config('SECRET_KEY')
                    response = openai.Completion.create(
                        engine = engine,
                        prompt = prompt,
                        temperature=0.5,
                        max_tokens=int(myRange),
                        top_p=1,
                        best_of=5,
                        # n=4,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )                              
                    break
            except PromptRaiseError:
                messages.error(request,"Please enter a valid article to summarize!!")
                return HttpResponseRedirect('/')
            except Exception as e:
                messages.info(request,e)
                return HttpResponseRedirect('/')
        summary = response['choices'][0]['text']
        # summary = "Summary text added for testing purpose"
        
        if audiocheck:
            obj = gtts.gTTS(text=summary, lang=language, slow=False)
            print('DETECTED2', language)
            # text_val_list = summary.split()
            ULR = string.ascii_uppercase
            LLR = string.ascii_lowercase
            NR = string.digits
            all = ULR + LLR + NR
            temp = random.sample(all, 10)
            app_temp = "".join(temp)
            text_save = article_name + "_" + language + "_" + engine + "_" + app_temp
            # for i in range(3):
            #     text_save += text_val_list[i] + "_"

            obj_save = obj.save(text_save+".mp3")

            main_file = open(text_save+".mp3", "rb").read()
            # dest_file1 = open("static/audios/"+text_save+".mp3", 'wb+')
            dest_file2 = open("media/audios/"+text_save+".mp3", 'wb+')
            # dest_file1.write(main_file)
            # dest_file1.close()
            dest_file2.write(main_file)
            dest_file2.close()
            os.remove(text_save+".mp3")
        
        else:
            text_save=""
            
        form = Prompt.objects.create(article_name=article_name, prompt=prompt, engine=engine, language=language, summary=summary, audio=text_save, myRange=myRange, myFile=myFile, url=url)
        form.save()
        review_id = form.id
        # print("FORM",form)

        context = {'engine':engine, 'language':language, 'article_name':article_name, 'prompt':prompt1, 'summary':summary, 'audio':text_save, 'form':form, 'review_id':review_id}
        return render(request, 'summary/summaries.html',context)

def reviews(request,pk):
    review_id = Prompt.objects.get(id=pk)
    comments = request.POST['comments']
    try:
        rate = request.POST['rate']
    except:
        rate = None
    rform = Review.objects.create(review=review_id,comments=comments,rate=rate)
    rform.save()
    print("RFORM_IIDDDDDDD", rform.review_id)
    context = {'rate':rate,'comments':comments, 'review_id':rform.review_id}
    return render(request, 'summary/endpage.html', context)

def review_back(request, pk):
    prompt_form = Prompt.objects.get(id=pk)
    review_form = Review.objects.filter(review=pk).latest('created')
    pform = PromptForm(instance=prompt_form)
    rform = ReviewForm(instance=review_form)
    print("RFORM", review_form.rate)
    var1 = ""
    var2 = var3 = var4 = var5 = var1

    if review_form.rate == '5':
        var1 = "checked"
    elif review_form.rate == '4':
        var2 = "checked"
    elif review_form.rate == '3':
        var3 = "checked"
    elif review_form.rate == '2':
        var4 = "checked"
    elif review_form.rate == '1':
        var5 = "checked"


    # form = PromptReview.objects.create(article_name=pform.article_name, prompt=pform.prompt, engine=pform.engine, language=pform.language, summary=pform.summary, audio=pform.text_save)

    # if request.method == "POST":
    #     pform = PromptForm(request.POST, instance=prompt_form)
    #     rform = ReviewForm(request.POST, instance=review_form)

    # form.save()
    # print(form)
    context = {'pform':pform, 'pk':pk, 'rform':rform, 'var1':var1, 'var2':var2, 'var3':var3, 'var4':var4, 'var5':var5}
    return render(request, 'summary/back.html', context)