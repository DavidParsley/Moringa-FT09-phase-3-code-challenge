from database.connection import get_db_connection # Import Database


class Author:
    def __init__(self, id, name):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("id must be an integer")
        
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("name must be a string")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError('name cannot be changed')
        
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("name must be a string")

    # Method that will return all articles associated with an author   
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id 
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
            """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]
    
    # Method that will return all magazines associated with an author
    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        SELECT magazines.id, magazines.name, magazines.category
        FROM magazines
        JOIN articles ON magazines.id = articles.magazine_id
        WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]

    def __repr__(self):
        return f'<Author {self.name}>'