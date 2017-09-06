# -*- coding: utf-8 -*-


class Customdb_Functions():

    def __init__(self, custom_cursor):
        self.custom_cursor = custom_cursor

    def get_movie_id(self, cid):
        query = ' '.join((
            "SELECT kodi_id, kodi_fileid, kodi_pathid, parent_id, media_type, source_type",
            "FROM source",
            "WHERE source_id = ?"
        ))
        try:
            self.custom_cursor.execute(query, (cid,))
            item = self.custom_cursor.fetchone()[0]
            return item
        except Exception:
            return None

    def get_movie_item(self, movie_id):
        query = "SELECT * From movie WHERE idMovie = ?"
        try:
            self.custom_cursor.execute(query, (movie_id,))
            item = self.custom_cursor.fetchone()
            return item
        except Exception:
            return None

    def get_movie_poster(self, movie_id):
        query = "SELECT url FROM art WHERE media_id = ? AND type = ?"
        try:
            self.custom_cursor.execute(query, (movie_id, "poster"))
            item = self.custom_cursor.fetchone()[0]
            return item
        except Exception:
            return None

    def get_movie_actors(self, movie_id):
        query = "SELECT strActor From actors NATURAL JOIN actorlinkmovie WHERE idMovie = ?"
        try:
            self.custom_cursor.execute(query, (movie_id,))
            item = self.custom_cursor.fetchall()
            return item
        except Exception:
            return None
