from dataclasses import dataclass
from datetime import date


@dataclass
class PostDto:
    """represents a post"""
    id_: int
    author: str
    title: str
    content: str
    date: str = date.today().strftime('%Y-%m-%d')
    like: int = 0
