import dataclasses
import json

from backend.DB.post_dto import PostDto


class BlogPostsDB:
    """represent a database
    :param blog_posts_db: path to json file"""
    def __init__(self, blog_posts_db):
        self.blog_posts_db = blog_posts_db
        self._posts = []

    def setup(self):
        """loads data from json file"""
        self._posts = []
        with open(self.blog_posts_db, "r", encoding="utf-8") as file:
            for post in json.load(file):
                self._posts.append(PostDto(*post.values()))

    def _flush_data(self):
        """saves data to json file"""
        with open(self.blog_posts_db, "w", encoding="utf-8") as file:
            data = [dataclasses.asdict(post) for post in self._posts]
            json.dump(data, file, indent=4)

    def get_blog_posts(self):
        """:returns: a list of posts: List[PostDto]"""
        return self._posts

    def get_post(self, post_id: int):
        """searches for a post by id
        :returns: an instance of post: PostDto"""
        for post in self._posts:
            if post.id_ == post_id:
                return post
        return None

    def add_post(self, post: PostDto):
        """
        adds a new post to database
        :param post: instance of post
        """
        self._posts.append(post)
        self._flush_data()

    def delete_post(self, post_id: int):
        """deletes a post from database"""
        post = self.get_post(post_id)
        self._posts.remove(post)
        self._flush_data()

    def update_post(self, post_id: int, title: str, content: str):
        """updates an existing post"""
        post = self.get_post(post_id)
        post.title = title
        post.content = content
        self._flush_data()

    def like_post(self, post_id):
        """add like to a post"""
        post = self.get_post(post_id)
        post.like += 1
        self._flush_data()
