from newsapp.models import *
from .parser import *


def results(articles_json,keyword,user):
    
    num = min(20, articles_json.get("totalResults", 0))
    
    if articles_json["totalResults"] > 20:
        num = 20
    else:
        num = int(articles_json["totalResults"])
    
    results = []

    for i in range(num):
        print(f'починаю статтю {i}')
        article = articles_json["articles"][i]
        pubdate = article.get("publishedAt", "")
        name = article.get("source", {}).get("name", "")
        title = article.get("title", "")
        description = article.get("description", "")
        link = article.get("url", "")
        print('отримав данні')

        try:
            content = parsed(url=link)
        except:
            content = 'не доросли ви до такого....'
        
        print('отримав контекст')

        db_create(user=user,keyword=keyword,pubdate=pubdate,name=name,
                    title=title,description=description,
                    link=link,content=content)

        results.append({'title': title, 'description': description, 'link': link})
        print(f'стаття {i}')
    return results

def db_create(user,keyword,pubdate,name,title,description,link,content):
    if Article.objects.filter(link=link).exists():
        pass
    else:
        article = Article(user=user,
        keyword=keyword, pubdate=pubdate, name=name, title=title,
        description=description, link=link, content=content
        )
        article.save()

        cat_name, _ = Category.objects.get_or_create(name=name)
        cat_num = CategoryNum.objects.filter(name=cat_name).first()

        if cat_num:
            cat_num.num += 1
            cat_num.save()
        else:
            CategoryNum(name=cat_name, num=1).save()