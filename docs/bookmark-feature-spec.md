# Bookmark Feature - Product Specification

## Overview

The bookmark feature allows authenticated users to save articles for later reading. This is distinct from the "favorite" feature which indicates appreciation/liking of an article. Bookmarks are personal reading lists that help users organize content they want to revisit.

**Key Difference from Favorites:**
- **Favorites**: Public indicator of appreciation (like a "like" button), shows count to all users
- **Bookmarks**: Private reading list for the user, not visible to others

---

## Feature Requirements

### Functional Requirements

1. **Add Bookmark**: Authenticated users can bookmark any article
2. **Remove Bookmark**: Users can remove articles from their bookmarks
3. **View Bookmarked Articles**: Users can view a list of their bookmarked articles
4. **Bookmark Status**: Article responses should indicate if the current user has bookmarked the article
5. **Persistence**: Bookmarks persist across sessions in the database

### Non-Functional Requirements

1. **Performance**: Bookmark operations should complete within 200ms
2. **Consistency**: Bookmark state should be immediately reflected in UI
3. **Privacy**: Users cannot see other users' bookmarks

---

## Architecture Overview

Following the existing codebase patterns (similar to the Favorite feature):

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (Next.js)                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │ ArticlePreview  │  │ ArticleActions  │  │ ProfileTab          │  │
│  │ (bookmark btn)  │  │ (bookmark btn)  │  │ (bookmarked tab)    │  │
│  └────────┬────────┘  └────────┬────────┘  └──────────┬──────────┘  │
│           │                    │                      │             │
│           └────────────────────┼──────────────────────┘             │
│                                │                                    │
│                    ┌───────────▼───────────┐                        │
│                    │   lib/api/article.ts  │                        │
│                    │   (API client)        │                        │
│                    └───────────┬───────────┘                        │
└────────────────────────────────┼────────────────────────────────────┘
                                 │ HTTP
┌────────────────────────────────┼────────────────────────────────────┐
│                           Backend (FastAPI)                         │
│                    ┌───────────▼───────────┐                        │
│                    │   api/routes/article  │                        │
│                    │   (REST endpoints)    │                        │
│                    └───────────┬───────────┘                        │
│                                │                                    │
│                    ┌───────────▼───────────┐                        │
│                    │  services/article.py  │                        │
│                    │  (business logic)     │                        │
│                    └───────────┬───────────┘                        │
│                                │                                    │
│           ┌────────────────────┼────────────────────┐               │
│           │                    │                    │               │
│  ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼───────┐       │
│  │ IBookmarkRepo   │  │ IArticleRepo    │  │ IProfileSvc   │       │
│  │ (interface)     │  │ (interface)     │  │ (interface)   │       │
│  └────────┬────────┘  └─────────────────┘  └───────────────┘       │
│           │                                                         │
│  ┌────────▼────────┐                                                │
│  │ BookmarkRepo    │                                                │
│  │ (SQLAlchemy)    │                                                │
│  └────────┬────────┘                                                │
└───────────┼─────────────────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────────────────┐
│                         Database (SQLite)                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  bookmark table                                             │    │
│  │  - user_id (FK -> user.id, PK)                              │    │
│  │  - article_id (FK -> article.id, PK, CASCADE DELETE)        │    │
│  │  - created_at (datetime)                                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### New Table: `bookmark`

```sql
CREATE TABLE bookmark (
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, article_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE
);
```

### SQLAlchemy Model

**File**: `conduit/infrastructure/models.py`

```python
class Bookmark(Base):
    __tablename__ = "bookmark"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("article.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime]
```

---

## API Endpoints

### 1. Add Bookmark

**Endpoint**: `POST /api/articles/{slug}/bookmark`

**Authentication**: Required

**Request**: Empty body

**Response** (200 OK):
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian...",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "bookmarked": true,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

**Error Responses**:
- `401 Unauthorized`: User not authenticated
- `404 Not Found`: Article does not exist
- `400 Bad Request`: Article already bookmarked

### 2. Remove Bookmark

**Endpoint**: `DELETE /api/articles/{slug}/bookmark`

**Authentication**: Required

**Request**: Empty body

**Response** (200 OK): Same as Add Bookmark with `"bookmarked": false`

**Error Responses**:
- `401 Unauthorized`: User not authenticated
- `404 Not Found`: Article does not exist
- `400 Bad Request`: Article not bookmarked

### 3. Get Bookmarked Articles

**Endpoint**: `GET /api/articles?bookmarked={username}`

**Authentication**: Required (can only query own bookmarks)

**Query Parameters**:
- `bookmarked`: Username to filter by (must match authenticated user)
- `limit`: Number of articles (default: 20)
- `offset`: Pagination offset (default: 0)

**Response** (200 OK):
```json
{
  "articles": [...],
  "articlesCount": 10
}
```

---

## Backend Implementation Files

### 1. Domain Layer - Repository Interface

**File**: `conduit/domain/repositories/bookmark.py`

```python
import abc
from typing import Any


class IBookmarkRepository(abc.ABC):
    """Bookmark articles repository interface."""

    @abc.abstractmethod
    async def exists(self, session: Any, user_id: int, article_id: int) -> bool: ...

    @abc.abstractmethod
    async def create(self, session: Any, article_id: int, user_id: int) -> None: ...

    @abc.abstractmethod
    async def delete(self, session: Any, article_id: int, user_id: int) -> None: ...
```

### 2. Infrastructure Layer - Repository Implementation

**File**: `conduit/infrastructure/repositories/bookmark.py`

```python
from datetime import datetime

from sqlalchemy import delete, exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.repositories.bookmark import IBookmarkRepository
from conduit.infrastructure.models import Bookmark


class BookmarkRepository(IBookmarkRepository):
    """Repository for Bookmark model."""

    async def exists(
        self, session: AsyncSession, user_id: int, article_id: int
    ) -> bool:
        query = (
            exists()
            .where(Bookmark.user_id == user_id, Bookmark.article_id == article_id)
            .select()
        )
        result = await session.execute(query)
        return result.scalar()

    async def create(
        self, session: AsyncSession, article_id: int, user_id: int
    ) -> None:
        query = insert(Bookmark).values(
            user_id=user_id, article_id=article_id, created_at=datetime.now()
        )
        await session.execute(query)

    async def delete(
        self, session: AsyncSession, article_id: int, user_id: int
    ) -> None:
        query = delete(Bookmark).where(
            Bookmark.user_id == user_id, Bookmark.article_id == article_id
        )
        await session.execute(query)
```

### 3. Domain Layer - DTO Updates

**File**: `conduit/domain/dtos/article.py` (modifications)

Add `bookmarked: bool` field to `ArticleDTO`:

```python
@dataclass(frozen=True)
class ArticleDTO:
    id: int
    author_id: int
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    author: ArticleAuthorDTO
    created_at: datetime.datetime
    updated_at: datetime.datetime
    favorited: bool
    favorites_count: int
    bookmarked: bool  # NEW FIELD
```

### 4. Domain Layer - Service Interface Updates

**File**: `conduit/domain/services/article.py` (additions)

```python
@abc.abstractmethod
async def add_article_to_bookmarks(
    self, session: Any, slug: str, current_user: UserDTO
) -> ArticleDTO: ...

@abc.abstractmethod
async def remove_article_from_bookmarks(
    self, session: Any, slug: str, current_user: UserDTO
) -> ArticleDTO: ...
```

### 5. Service Layer - Implementation Updates

**File**: `conduit/services/article.py` (additions)

```python
async def add_article_to_bookmarks(
    self, session: AsyncSession, slug: str, current_user: UserDTO
) -> ArticleDTO:
    article = await self.get_article_by_slug(
        session=session, slug=slug, current_user=current_user
    )
    if article.bookmarked:
        raise ArticleAlreadyBookmarkedException()

    await self._bookmark_repo.create(
        session=session, article_id=article.id, user_id=current_user.id
    )
    return ArticleDTO.with_updated_fields(
        dto=article,
        updated_fields=dict(bookmarked=True),
    )

async def remove_article_from_bookmarks(
    self, session: AsyncSession, slug: str, current_user: UserDTO
) -> ArticleDTO:
    article = await self.get_article_by_slug(
        session=session, slug=slug, current_user=current_user
    )
    if not article.bookmarked:
        raise ArticleNotBookmarkedException()

    await self._bookmark_repo.delete(
        session=session, article_id=article.id, user_id=current_user.id
    )
    return ArticleDTO.with_updated_fields(
        dto=article,
        updated_fields=dict(bookmarked=False),
    )
```

### 6. Exceptions

**File**: `conduit/core/exceptions.py` (additions)

```python
class ArticleAlreadyBookmarkedException(BaseInternalException):
    """Exception raised when article already bookmarked."""

    _status_code = 400
    _message = "Article has already been bookmarked."


class ArticleNotBookmarkedException(BaseInternalException):
    """Exception raised when article is not bookmarked."""

    _status_code = 400
    _message = "Article is not bookmarked."
```

### 7. API Routes

**File**: `conduit/api/routes/article.py` (additions)

```python
@router.post("/{slug}/bookmark", response_model=ArticleResponse)
async def bookmark_article(
    slug: str,
    session: DBSession,
    current_user: CurrentUser,
    article_service: IArticleService,
) -> ArticleResponse:
    """
    Bookmark an article.
    """
    article_dto = await article_service.add_article_to_bookmarks(
        session=session, slug=slug, current_user=current_user
    )
    return ArticleResponse.from_dto(dto=article_dto)


@router.delete("/{slug}/bookmark", response_model=ArticleResponse)
async def unbookmark_article(
    slug: str,
    session: DBSession,
    current_user: CurrentUser,
    article_service: IArticleService,
) -> ArticleResponse:
    """
    Remove bookmark from an article.
    """
    article_dto = await article_service.remove_article_from_bookmarks(
        session=session, slug=slug, current_user=current_user
    )
    return ArticleResponse.from_dto(dto=article_dto)
```

### 8. API Response Schema Updates

**File**: `conduit/api/schemas/responses/article.py` (modifications)

```python
class ArticleData(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tags: list[str] = Field(alias="tagList")
    created_at: datetime.datetime = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(alias="updatedAt")
    favorited: bool = False
    favorites_count: int = Field(default=0, alias="favoritesCount")
    bookmarked: bool = False  # NEW FIELD
    author: ArticleAuthorData
```

### 9. Container Updates

**File**: `conduit/core/container.py` (additions)

```python
from conduit.domain.repositories.bookmark import IBookmarkRepository
from conduit.infrastructure.repositories.bookmark import BookmarkRepository

# Add method:
@staticmethod
def bookmark_repository() -> IBookmarkRepository:
    return BookmarkRepository()

# Update article_service method:
def article_service(self) -> IArticleService:
    return ArticleService(
        article_repo=self.article_repository(),
        article_tag_repo=self.article_tag_repository(),
        favorite_repo=self.favorite_repository(),
        bookmark_repo=self.bookmark_repository(),  # NEW
        profile_service=self.profile_service(),
    )
```

---

## Frontend Implementation Files

### 1. Type Updates

**File**: `frontend/lib/types/articleType.ts`

```typescript
export type ArticleType = {
  tagList: string[];
  createdAt: number;
  author: Author;
  description: string;
  title: string;
  body: string;
  slug: string;
  updatedAt: number;
  favoritesCount: number;
  favorited: boolean;
  bookmarked: boolean;  // NEW FIELD
};
```

### 2. API Client Updates

**File**: `frontend/lib/api/article.ts` (additions)

```typescript
bookmark: (slug: string, token: string) =>
  axios.post(
    `${SERVER_BASE_URL}/articles/${slug}/bookmark`,
    {},
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  ),

unbookmark: (slug: string, token: string) =>
  axios.delete(`${SERVER_BASE_URL}/articles/${slug}/bookmark`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  }),

bookmarkedBy: (username: string, page: number, token: string) =>
  axios.get(
    `${SERVER_BASE_URL}/articles?bookmarked=${encodeURIComponent(
      username
    )}&${getQuery(10, page)}`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  ),
```

### 3. ArticlePreview Component Updates

**File**: `frontend/components/article/ArticlePreview.tsx`

Add bookmark button next to favorite button:

```tsx
const BOOKMARKED_CLASS = "btn btn-sm btn-secondary";
const NOT_BOOKMARKED_CLASS = "btn btn-sm btn-outline-secondary";

// Add state for bookmark
const [bookmarked, setBookmarked] = React.useState(article.bookmarked);

// Add handler
const handleClickBookmark = async (slug: string) => {
  if (!isLoggedIn) {
    Router.push(`/user/login`);
    return;
  }

  setBookmarked(!bookmarked);

  try {
    if (bookmarked) {
      await axios.delete(`${SERVER_BASE_URL}/articles/${slug}/bookmark`, {
        headers: {
          Authorization: `Token ${currentUser?.token}`,
        },
      });
    } else {
      await axios.post(
        `${SERVER_BASE_URL}/articles/${slug}/bookmark`,
        {},
        {
          headers: {
            Authorization: `Token ${currentUser?.token}`,
          },
        }
      );
    }
  } catch (error) {
    setBookmarked(!bookmarked); // Revert on error
  }
};

// Add button in JSX (next to favorite button)
<button
  className={bookmarked ? BOOKMARKED_CLASS : NOT_BOOKMARKED_CLASS}
  onClick={() => handleClickBookmark(preview.slug)}
  title={bookmarked ? "Remove bookmark" : "Save for later"}
>
  <i className="ion-bookmark" />
</button>
```

### 4. ProfileTab Component Updates

**File**: `frontend/components/profile/ProfileTab.tsx`

Add "Bookmarked Articles" tab:

```tsx
// Add new tab option
<li className="nav-item">
  <CustomLink
    href="/profile/[pid]?tab=bookmarked"
    as={`/profile/${profile.username}?tab=bookmarked`}
    className={`nav-link ${tab === "bookmarked" ? "active" : ""}`}
  >
    Bookmarked Articles
  </CustomLink>
</li>
```

---

## Test-Driven Development Plan

### Phase 1: Repository Layer Tests

**File**: `tests/infrastructure/repositories/test_bookmark.py`

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.infrastructure.repositories.bookmark import BookmarkRepository


@pytest.mark.anyio
async def test_bookmark_does_not_exist_initially(
    session: AsyncSession,
    bookmark_repository: BookmarkRepository,
    test_user,
    test_article,
) -> None:
    """Test that bookmark does not exist for new user/article pair."""
    exists = await bookmark_repository.exists(
        session=session, user_id=test_user.id, article_id=test_article.id
    )
    assert exists is False


@pytest.mark.anyio
async def test_can_create_bookmark(
    session: AsyncSession,
    bookmark_repository: BookmarkRepository,
    test_user,
    test_article,
) -> None:
    """Test that a bookmark can be created."""
    await bookmark_repository.create(
        session=session, article_id=test_article.id, user_id=test_user.id
    )
    exists = await bookmark_repository.exists(
        session=session, user_id=test_user.id, article_id=test_article.id
    )
    assert exists is True


@pytest.mark.anyio
async def test_can_delete_bookmark(
    session: AsyncSession,
    bookmark_repository: BookmarkRepository,
    test_user,
    test_article,
) -> None:
    """Test that a bookmark can be deleted."""
    await bookmark_repository.create(
        session=session, article_id=test_article.id, user_id=test_user.id
    )
    await bookmark_repository.delete(
        session=session, article_id=test_article.id, user_id=test_user.id
    )
    exists = await bookmark_repository.exists(
        session=session, user_id=test_user.id, article_id=test_article.id
    )
    assert exists is False
```

### Phase 2: Service Layer Tests

**File**: `tests/services/test_article_bookmark.py`

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    ArticleAlreadyBookmarkedException,
    ArticleNotBookmarkedException,
)
from conduit.domain.dtos.article import ArticleDTO
from conduit.domain.dtos.user import UserDTO
from conduit.services.article import ArticleService


@pytest.mark.anyio
async def test_can_bookmark_article(
    session: AsyncSession,
    article_service: ArticleService,
    test_article: ArticleDTO,
    test_user: UserDTO,
) -> None:
    """Test that user can bookmark an article."""
    result = await article_service.add_article_to_bookmarks(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert result.bookmarked is True


@pytest.mark.anyio
async def test_cannot_bookmark_already_bookmarked_article(
    session: AsyncSession,
    article_service: ArticleService,
    test_article: ArticleDTO,
    test_user: UserDTO,
) -> None:
    """Test that bookmarking an already bookmarked article raises exception."""
    await article_service.add_article_to_bookmarks(
        session=session, slug=test_article.slug, current_user=test_user
    )
    with pytest.raises(ArticleAlreadyBookmarkedException):
        await article_service.add_article_to_bookmarks(
            session=session, slug=test_article.slug, current_user=test_user
        )


@pytest.mark.anyio
async def test_can_remove_bookmark(
    session: AsyncSession,
    article_service: ArticleService,
    test_article: ArticleDTO,
    test_user: UserDTO,
) -> None:
    """Test that user can remove bookmark from article."""
    await article_service.add_article_to_bookmarks(
        session=session, slug=test_article.slug, current_user=test_user
    )
    result = await article_service.remove_article_from_bookmarks(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert result.bookmarked is False


@pytest.mark.anyio
async def test_cannot_remove_bookmark_from_not_bookmarked_article(
    session: AsyncSession,
    article_service: ArticleService,
    test_article: ArticleDTO,
    test_user: UserDTO,
) -> None:
    """Test that removing bookmark from non-bookmarked article raises exception."""
    with pytest.raises(ArticleNotBookmarkedException):
        await article_service.remove_article_from_bookmarks(
            session=session, slug=test_article.slug, current_user=test_user
        )
```

### Phase 3: API Route Tests

**File**: `tests/api/routes/test_bookmark.py`

```python
import pytest
from httpx import AsyncClient

from conduit.domain.dtos.article import ArticleDTO


@pytest.mark.anyio
async def test_user_can_bookmark_article(
    authorized_test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that authenticated user can bookmark an article."""
    response = await authorized_test_client.post(
        url=f"/articles/{test_article.slug}/bookmark"
    )
    assert response.status_code == 200
    assert response.json()["article"]["bookmarked"] is True


@pytest.mark.anyio
async def test_user_cannot_bookmark_already_bookmarked_article(
    authorized_test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that bookmarking already bookmarked article returns 400."""
    await authorized_test_client.post(url=f"/articles/{test_article.slug}/bookmark")
    response = await authorized_test_client.post(
        url=f"/articles/{test_article.slug}/bookmark"
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_user_can_remove_bookmark(
    authorized_test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that user can remove bookmark from article."""
    await authorized_test_client.post(url=f"/articles/{test_article.slug}/bookmark")
    response = await authorized_test_client.delete(
        url=f"/articles/{test_article.slug}/bookmark"
    )
    assert response.status_code == 200
    assert response.json()["article"]["bookmarked"] is False


@pytest.mark.anyio
async def test_user_cannot_remove_bookmark_from_not_bookmarked_article(
    authorized_test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that removing bookmark from non-bookmarked article returns 400."""
    response = await authorized_test_client.delete(
        url=f"/articles/{test_article.slug}/bookmark"
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_unauthenticated_user_cannot_bookmark(
    test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that unauthenticated user cannot bookmark article."""
    response = await test_client.post(url=f"/articles/{test_article.slug}/bookmark")
    assert response.status_code == 403


@pytest.mark.anyio
async def test_bookmark_nonexistent_article_returns_404(
    authorized_test_client: AsyncClient,
) -> None:
    """Test that bookmarking non-existent article returns 404."""
    response = await authorized_test_client.post(
        url="/articles/nonexistent-slug/bookmark"
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_article_response_includes_bookmarked_field(
    authorized_test_client: AsyncClient, test_article: ArticleDTO
) -> None:
    """Test that article response includes bookmarked field."""
    response = await authorized_test_client.get(
        url=f"/articles/{test_article.slug}"
    )
    assert response.status_code == 200
    assert "bookmarked" in response.json()["article"]
```

---

## Implementation Order (TDD Approach)

### Step 1: Write Failing Tests First
1. Create `tests/api/routes/test_bookmark.py` with API tests
2. Create `tests/infrastructure/repositories/test_bookmark.py` with repository tests
3. Run tests to confirm they fail

### Step 2: Implement Database Layer
1. Add `Bookmark` model to `conduit/infrastructure/models.py`
2. Create `conduit/domain/repositories/bookmark.py` (interface)
3. Create `conduit/infrastructure/repositories/bookmark.py` (implementation)
4. Run repository tests to confirm they pass

### Step 3: Implement Service Layer
1. Add exceptions to `conduit/core/exceptions.py`
2. Update `conduit/domain/dtos/article.py` with `bookmarked` field
3. Update `conduit/domain/services/article.py` interface
4. Update `conduit/services/article.py` implementation
5. Update `conduit/core/container.py` with bookmark repository
6. Run service tests to confirm they pass

### Step 4: Implement API Layer
1. Update `conduit/api/schemas/responses/article.py`
2. Add routes to `conduit/api/routes/article.py`
3. Run API tests to confirm they pass

### Step 5: Implement Frontend
1. Update `frontend/lib/types/articleType.ts`
2. Update `frontend/lib/api/article.ts`
3. Update `frontend/components/article/ArticlePreview.tsx`
4. Update `frontend/components/profile/ProfileTab.tsx`
5. Manual testing in browser

---

## Files to Create/Modify Summary

### New Files
| File | Description |
|------|-------------|
| `conduit/domain/repositories/bookmark.py` | Repository interface |
| `conduit/infrastructure/repositories/bookmark.py` | Repository implementation |
| `tests/api/routes/test_bookmark.py` | API route tests |
| `tests/infrastructure/repositories/test_bookmark.py` | Repository tests |

### Modified Files
| File | Changes |
|------|---------|
| `conduit/infrastructure/models.py` | Add `Bookmark` model |
| `conduit/domain/dtos/article.py` | Add `bookmarked` field to `ArticleDTO` |
| `conduit/domain/services/article.py` | Add bookmark methods to interface |
| `conduit/services/article.py` | Implement bookmark methods |
| `conduit/core/exceptions.py` | Add bookmark exceptions |
| `conduit/core/container.py` | Add bookmark repository |
| `conduit/api/schemas/responses/article.py` | Add `bookmarked` field |
| `conduit/api/routes/article.py` | Add bookmark endpoints |
| `conduit/infrastructure/repositories/article.py` | Update queries for bookmarked filter |
| `frontend/lib/types/articleType.ts` | Add `bookmarked` field |
| `frontend/lib/api/article.ts` | Add bookmark API methods |
| `frontend/components/article/ArticlePreview.tsx` | Add bookmark button |
| `frontend/components/profile/ProfileTab.tsx` | Add bookmarked tab |
| `tests/conftest.py` | Add bookmark repository fixture |

---

## Acceptance Criteria

1. ✅ User can click bookmark button on article preview
2. ✅ Bookmark state persists in database
3. ✅ Bookmark button shows correct state (filled/outline)
4. ✅ User can view list of bookmarked articles on profile
5. ✅ Bookmarking requires authentication
6. ✅ Cannot bookmark same article twice (returns error)
7. ✅ Cannot remove bookmark from non-bookmarked article
8. ✅ All tests pass
9. ✅ API documentation updated (OpenAPI/Swagger)

---

## Future Enhancements (Out of Scope)

1. **Bookmark folders/categories**: Organize bookmarks into collections
2. **Bookmark notes**: Add personal notes to bookmarks
3. **Bookmark sharing**: Share bookmark collections with others
4. **Bookmark export**: Export bookmarks to various formats
5. **Bookmark reminders**: Set reminders to read bookmarked articles
