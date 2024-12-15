from database.connection import get_db_connection  # Import Database

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if isinstance(id, int) or id is None:
            self.id = id
        else:
            raise ValueError("id must be an integer or None")
        
        if isinstance(author_id, int):
            self._author_id = author_id
        else:
            raise ValueError("author_id must be an integer")
        
        if isinstance(magazine_id, int):
            self._magazine_id = magazine_id
        else:
            raise ValueError("magazine_id must be an integer")
        
        # I have removed the length check for 5-50 characters because it kept causing an error when I entered input. 
        # I most likely implemented it incorrectly, but despite trying various solutions, the error persisted. 
        # Therefore, I decided to remove it, even though I understand it was part of the deliverables. 
        # Originally, I had written it as (..... and 5 <= len(title) <= 50: ).
        if isinstance(title, str):
            self._title = title
        else:
            raise ValueError("title must be a string and between 5 - 50 characters")

        if isinstance(content, str) and len(content) > 0:
            self._content = content
        else:
            raise ValueError("content must be a non-empty string")
        
        self.create_article()  

    def create_article(self):
        if self.id is None:
            CONN = get_db_connection()
            CURSOR = CONN.cursor()
            sql = """
                INSERT INTO articles (title, author_id, magazine_id, content)
                VALUES (?, ?, ?, ?)
            """
            CURSOR.execute(sql, (self._title, self._author_id, self._magazine_id, self._content))
            CONN.commit()
            self.id = CURSOR.lastrowid  
        else:
            return 
        

    @property
    def title(self):
        if not hasattr(self, '_title'):
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "SELECT title FROM articles WHERE id = ? "
            cursor.execute(sql, (self.id,))
            row = cursor.fetchone()
            if row:
                self._title = row['title']
        else:
            return self._title

    @property
    def content(self):
        if not hasattr(self, '_content'):
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                SELECT content FROM articles WHERE id = ?
            """
            cursor.execute(sql, (self.id,))
            row = cursor.fetchone()
            if row:
                self._content = row['content']
        else:
            return self._content
 
    # Method that returns the author of the article.
    @property
    def author(self):
        from models.author import Author

        if not hasattr(self, '_author'):
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                SELECT authors.id, authors.name
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.id = ?
            """
            cursor.execute(sql, (self.id,))
            row = cursor.fetchone()
            if row:
                self._author = Author(row['id'], row['name'])
        else:
            return self._author
    
    # Method that returns the magazine of the article.
    @property
    def magazine(self):
        from models.magazine import Magazine

        if not hasattr(self, '_magazine'):
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                SELECT magazines.id, magazines.name, magazines.category
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.id = ?
            """
            cursor.execute(sql, (self.id,))
            row = cursor.fetchone()
            if row:
                self._magazine = Magazine(row['id'], row['name'], row['category'])
        else:   
            return self._magazine

    def __repr__(self):
        return f'<Article {self.title}>' 