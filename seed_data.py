#!/usr/bin/env python
"""
Seed script to populate the database with sample data.
Run with: python seed_data.py
"""
import asyncio
import os
from datetime import datetime

import bcrypt
from slugify import slugify  # from python-slugify package
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from conduit.core.config import get_app_settings
from conduit.infrastructure.models import Article, Base, Comment, Follower, Tag, ArticleTag, User


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt directly to avoid passlib compatibility issues."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


SAMPLE_USERS = [
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "password123",
        "bio": "I'm a software developer who loves writing about technology and programming.",
    },
    {
        "username": "janedoe",
        "email": "jane@example.com",
        "password": "password123",
        "bio": "Tech enthusiast and avid reader. I write about my experiences in the industry.",
    },
    {
        "username": "bobsmith",
        "email": "bob@example.com",
        "password": "password123",
        "bio": "Full-stack developer with a passion for clean code and best practices.",
    },
]

SAMPLE_TAGS = [
    "python",
    "fastapi",
    "programming",
    "webdev",
    "tutorial",
    "javascript",
    "react",
    "database",
]

SAMPLE_ARTICLES = [
    {
        "title": "Getting Started with FastAPI",
        "description": "A comprehensive guide to building APIs with FastAPI",
        "body": """FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Key Features

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase the speed to develop features by about 200% to 300%
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors
- **Intuitive**: Great editor support with completion everywhere
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Get production-ready code with automatic interactive documentation

## Getting Started

First, install FastAPI:

```bash
pip install fastapi uvicorn
```

Then create a simple API:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

Run it with:

```bash
uvicorn main:app --reload
```

That's it! You now have a working API.""",
        "tags": ["python", "fastapi", "tutorial", "webdev"],
        "author_index": 0,
    },
    {
        "title": "Understanding Python Async/Await",
        "description": "Deep dive into asynchronous programming in Python",
        "body": """Asynchronous programming in Python has become increasingly important for building high-performance applications.

## What is Async/Await?

The `async` and `await` keywords in Python allow you to write asynchronous code that looks and behaves like synchronous code.

## Why Use Async?

- Handle many concurrent connections
- Improve I/O-bound application performance
- Better resource utilization

## Example

```python
import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)
    print("Data fetched!")
    return {"data": "sample"}

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

Async programming is essential for modern web applications that need to handle many simultaneous requests efficiently.""",
        "tags": ["python", "programming", "tutorial"],
        "author_index": 1,
    },
    {
        "title": "Building RESTful APIs: Best Practices",
        "description": "Learn the best practices for designing and building RESTful APIs",
        "body": """REST (Representational State Transfer) is an architectural style for designing networked applications.

## Key Principles

1. **Use HTTP Methods Correctly**
   - GET for retrieving resources
   - POST for creating resources
   - PUT/PATCH for updating resources
   - DELETE for removing resources

2. **Use Meaningful Resource Names**
   - Use nouns, not verbs
   - Use plural names for collections
   - Example: `/users`, `/articles`, `/comments`

3. **Handle Errors Gracefully**
   - Use appropriate HTTP status codes
   - Provide meaningful error messages

4. **Version Your API**
   - Include version in URL or header
   - Example: `/api/v1/users`

5. **Implement Pagination**
   - Don't return all records at once
   - Use limit and offset parameters

Following these practices will help you build APIs that are intuitive, maintainable, and scalable.""",
        "tags": ["webdev", "programming", "tutorial"],
        "author_index": 2,
    },
    {
        "title": "Introduction to React Hooks",
        "description": "A beginner's guide to using React Hooks",
        "body": """React Hooks were introduced in React 16.8 and have revolutionized how we write React components.

## What are Hooks?

Hooks are functions that let you "hook into" React state and lifecycle features from function components.

## Common Hooks

### useState

```javascript
const [count, setCount] = useState(0);
```

### useEffect

```javascript
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);
```

### useContext

```javascript
const theme = useContext(ThemeContext);
```

## Benefits

- Simpler code
- Reusable logic
- No more class components needed
- Better code organization

Hooks make React development more intuitive and enjoyable!""",
        "tags": ["javascript", "react", "tutorial", "webdev"],
        "author_index": 0,
    },
    {
        "title": "Database Design Fundamentals",
        "description": "Essential concepts for designing efficient databases",
        "body": """Good database design is crucial for building scalable and maintainable applications.

## Normalization

Normalization is the process of organizing data to reduce redundancy:

- **1NF**: Eliminate repeating groups
- **2NF**: Remove partial dependencies
- **3NF**: Remove transitive dependencies

## Indexing

Indexes improve query performance but have trade-offs:

- Faster reads
- Slower writes
- Additional storage

## Relationships

- **One-to-One**: User -> Profile
- **One-to-Many**: Author -> Articles
- **Many-to-Many**: Articles <-> Tags

## Tips

1. Start with a clear data model
2. Use appropriate data types
3. Plan for growth
4. Consider query patterns
5. Don't over-normalize

A well-designed database is the foundation of a successful application.""",
        "tags": ["database", "programming", "tutorial"],
        "author_index": 1,
    },
]


async def seed_database() -> None:
    """Seed the database with sample data."""
    os.environ.setdefault("APP_ENV", "dev")
    settings = get_app_settings()
    
    engine = create_async_engine(settings.sql_db_uri)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        # Create users
        users = []
        for user_data in SAMPLE_USERS:
            now = datetime.utcnow()
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"]),
                bio=user_data["bio"],
                image_url=None,
                created_at=now,
                updated_at=now,
            )
            session.add(user)
            users.append(user)
        
        await session.flush()
        print(f"Created {len(users)} users")
        
        # Create tags
        tags = {}
        for tag_name in SAMPLE_TAGS:
            tag = Tag(
                tag=tag_name,
                created_at=datetime.utcnow(),
            )
            session.add(tag)
            tags[tag_name] = tag
        
        await session.flush()
        print(f"Created {len(tags)} tags")
        
        # Create articles
        articles = []
        for article_data in SAMPLE_ARTICLES:
            author = users[article_data["author_index"]]
            now = datetime.utcnow()
            article = Article(
                author_id=author.id,
                slug=slugify(article_data["title"]),
                title=article_data["title"],
                description=article_data["description"],
                body=article_data["body"],
                created_at=now,
                updated_at=now,
            )
            session.add(article)
            articles.append((article, article_data["tags"]))
        
        await session.flush()
        print(f"Created {len(articles)} articles")
        
        # Create article-tag associations
        for article, tag_names in articles:
            for tag_name in tag_names:
                article_tag = ArticleTag(
                    article_id=article.id,
                    tag_id=tags[tag_name].id,
                    created_at=datetime.utcnow(),
                )
                session.add(article_tag)
        
        await session.flush()
        print("Created article-tag associations")
        
        # Create some comments
        comments_data = [
            {"article_index": 0, "author_index": 1, "body": "Great introduction to FastAPI! Very helpful."},
            {"article_index": 0, "author_index": 2, "body": "I've been using FastAPI for a while now, it's amazing!"},
            {"article_index": 1, "author_index": 0, "body": "Async programming can be tricky, thanks for the clear explanation."},
            {"article_index": 2, "author_index": 1, "body": "These best practices are spot on. I wish I had read this earlier."},
            {"article_index": 3, "author_index": 2, "body": "Hooks changed how I write React code. Great article!"},
        ]
        
        for comment_data in comments_data:
            article, _ = articles[comment_data["article_index"]]
            author = users[comment_data["author_index"]]
            now = datetime.utcnow()
            comment = Comment(
                article_id=article.id,
                author_id=author.id,
                body=comment_data["body"],
                created_at=now,
                updated_at=now,
            )
            session.add(comment)
        
        await session.flush()
        print(f"Created {len(comments_data)} comments")
        
        # Create follower relationships so "Your Feed" shows articles
        # johndoe follows janedoe and bobsmith
        # janedoe follows johndoe
        # bobsmith follows johndoe and janedoe
        follower_relationships = [
            {"follower_index": 0, "following_index": 1},  # johndoe follows janedoe
            {"follower_index": 0, "following_index": 2},  # johndoe follows bobsmith
            {"follower_index": 1, "following_index": 0},  # janedoe follows johndoe
            {"follower_index": 2, "following_index": 0},  # bobsmith follows johndoe
            {"follower_index": 2, "following_index": 1},  # bobsmith follows janedoe
        ]
        
        for rel in follower_relationships:
            follower = Follower(
                follower_id=users[rel["follower_index"]].id,
                following_id=users[rel["following_index"]].id,
                created_at=datetime.utcnow(),
            )
            session.add(follower)
        
        await session.flush()
        print(f"Created {len(follower_relationships)} follower relationships")
        
        await session.commit()
    
    await engine.dispose()
    print("\nDatabase seeded successfully!")
    print("\nSample login credentials:")
    for user in SAMPLE_USERS:
        print(f"  - Email: {user['email']}, Password: {user['password']}")


if __name__ == "__main__":
    asyncio.run(seed_database())
