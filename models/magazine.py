from database.connection import get_db_connection # Import Database


class Magazine:
    def __init__(self, id, name, category=None):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("id must be an integer")

        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise ValueError("name must be a string between 2 and 16 characters")

        if category is None:
            self._category = "Uncategorized"
        elif isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise ValueError("category must be a string")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("category must be a string")

    # Method that will return all articles associated with a Magazine
    def articles(self):
        from models.article import Article
        from models.author import Author

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

    # Method that will return all Authors associated with a magazine
    def contributors(self):
        from models.author import Author

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        return [Author(row["id"], row["name"]) for row in rows]

    # Model that returns a list of the titles of all articles written for that magazine
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT articles.title
            FROM articles
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        rows = cursor.fetchall()

        if len(rows) <= 0:
            return None
        
        return [row["title"] for row in rows]

    def contributing_authors(self):
    # I'm having trouble figuring what sql query I can / write  use to return authors with 
    # a count  of mor than 2 for a magazine.
    # Its the same challenge I faced in the last code challenge (Week 2) 
    # If I had more time I would try and figure it out but I need to submit before deadline  
        pass

    def __repr__(self):
        return f'<Magazine {self.name}>'