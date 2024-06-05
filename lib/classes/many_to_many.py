class Article:

    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)
        

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value: str):
        # Inserting an extra condition to handle fringe cases like the someone declaring the title as None
        if hasattr(self, '_title') and self._title is not None:
            raise AttributeError("Title can only be set once.")
        if isinstance(value, str) and 5<= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be of type str and between 5 and 50 characters.")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self,value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise ValueError("Must be of type Author")   
        
    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self,value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise ValueError("Must be of type Magazine")   
class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        # Inserting the same extra condition as in the Article for handling None
        if hasattr(self, '_name') and self._name is not None:
            raise AttributeError("Name can only be set once.")
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Title must be of type str and longer than 0 characters.")

    def articles(self):
        result = []
        for article in Article.all:
            if article.author == self:
                result.append(article)
        return result

    # Alternatively we can use list comprehension
    # def articles(self):
    #    return [article for article in Article.all if article.author == self]

    def magazines(self):
        # Since we need unique values we initialise a set that we will later convert into a list    
        result = set()  
        for article in Article.all:
            if article.author == self:
                result.add(article.magazine)
        return list(result)

    # Alternatively we can handle it this way
    # def magazines(self):
    #     result = list(set(article.magazine for article in Article.all if article.author == self))
    #     return result

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        result = set()
        for magazine in self.magazines():
            result.add(magazine.category)
        # So apparently in python you can include an if statement in the return statement which is pretty cool tbh 
        return list(result) if result else None

class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and 2<= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Magazine name must be of type str and longer than 0 characters.")
        
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be of type str and longer than 0 characters.")

    def articles(self):
        result = []
        for article in Article.all:
            if article.magazine == self:
                result.append(article)
        return result

    def contributors(self):
        # Same as before in the Author class, since we need unique values we initialise a set that we will later convert into a list    
        result = set()  
        for article in Article.all:
            if article.magazine == self:
                result.add(article.author)
        return list(result)
    
    # Alternatively
    # def contributors(self):
    #     return list(set(article.author for article in self.articles()))

    def article_titles(self):
        result = []
        for article in Article.all:
           if article.magazine == self:
               result.append(article.title)
        return result if result else None

    def contributing_authors(self):
        author_count = {}
        for article in Article.all:
            if article.magazine == self:
                if article.author in author_count:
                    author_count[article.author] += 1
                else:
                    author_count[article.author] = 1

        result = [author for author, count in author_count.items() if count > 2]
        return result if result else None
    
    # Since top_publisher needs to keep track of all the magazine objects we can handle it using the class method
    # I'll test this later
    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        
        magazine_article_count = {magazine: 0 for magazine in cls.all_magazines}

        for article in Article.all:
            if article.magazine in magazine_article_count:
                magazine_article_count[article.magazine] += 1

        top_magazine = max(magazine_article_count, key=magazine_article_count.get, default=None)

        return top_magazine if magazine_article_count[top_magazine] > 0 else None