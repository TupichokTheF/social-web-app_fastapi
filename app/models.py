from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

Base = declarative_base()

class Language(Base):
    """Supported interface languages."""

    __tablename__ = "languages"

    language_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    language: Mapped[Optional[str]] = mapped_column(Text)

    # relationships
    user_settings: Mapped[list["UserSettings"]] = relationship(back_populates="language")

    def __repr__(self) -> str:
        return f"<Language id={self.language_id} language={self.language!r}>"


class PostType(Base):
    """Classifies posts (e.g. original, reply, repost, …)."""

    __tablename__ = "post_types"

    post_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_type: Mapped[Optional[str]] = mapped_column(String(30))

    # relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="post_type")

    def __repr__(self) -> str:
        return f"<PostType id={self.post_type_id} post_type={self.post_type!r}>"


class PostMediaType(Base):
    """MIME / media categories for post attachments."""

    __tablename__ = "post_media_types"

    media_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_type: Mapped[Optional[str]] = mapped_column(Text)

    # relationships
    post_media: Mapped[list["PostMedia"]] = relationship(back_populates="media_type")

    def __repr__(self) -> str:
        return f"<PostMediaType id={self.media_type_id} media_type={self.media_type!r}>"


class CommentMediaType(Base):
    """MIME / media categories for comment attachments."""

    __tablename__ = "comment_media_type"

    media_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_type: Mapped[Optional[str]] = mapped_column(Text)

    # relationships
    comment_media: Mapped[list["CommentMedia"]] = relationship(back_populates="media_type")

    def __repr__(self) -> str:
        return f"<CommentMediaType id={self.media_type_id} media_type={self.media_type!r}>"


# ---------------------------------------------------------------------------
# Core user tables
# ---------------------------------------------------------------------------

class User(Base):
    """Registered users."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="users_username_key"),
        UniqueConstraint("email", name="users_email_key"),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(50))
    password_hash: Mapped[Optional[str]] = mapped_column(Text)
    display_name: Mapped[Optional[str]] = mapped_column(String(50))
    bio: Mapped[Optional[str]] = mapped_column(String(250))
    avatar_path: Mapped[Optional[str]] = mapped_column(Text)
    banner_path: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships — authored content
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        foreign_keys="Post.user_id",
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    post_likes: Mapped[list["PostLike"]] = relationship(back_populates="user")
    comment_likes: Mapped[list["CommentLike"]] = relationship(back_populates="user")
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="user")
    reposts: Mapped[list["Repost"]] = relationship(back_populates="user")

    # relationships — social graph
    following: Mapped[list["Follow"]] = relationship(
        back_populates="follower",
        foreign_keys="Follow.follower_id",
    )
    followers: Mapped[list["Follow"]] = relationship(
        back_populates="following_user",
        foreign_keys="Follow.following_id",
    )

    # settings
    settings: Mapped[Optional["UserSettings"]] = relationship(
        back_populates="user", uselist=False
    )

    def __repr__(self) -> str:
        return f"<User id={self.user_id} username={self.username!r}>"


class UserSettings(Base):
    """Per-user application settings (language, etc.)."""

    __tablename__ = "user_settings"

    settings_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    language_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("languages.language_id")
    )

    # relationships
    user: Mapped[Optional["User"]] = relationship(back_populates="settings")
    language: Mapped[Optional["Language"]] = relationship(back_populates="user_settings")

    def __repr__(self) -> str:
        return f"<UserSettings id={self.settings_id} user_id={self.user_id}>"


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

class Post(Base):
    """Main post entity (supports threading and reposts)."""

    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    content: Mapped[Optional[str]] = mapped_column(Text)
    parent_post_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("posts.post_id")
    )
    repost_post_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("posts.post_id")
    )
    type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("post_types.post_type_id")
    )
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    is_pinned: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    author: Mapped[Optional["User"]] = relationship(
        back_populates="posts",
        foreign_keys=[user_id],
    )
    post_type: Mapped[Optional["PostType"]] = relationship(back_populates="posts")

    # self-referential: replies and reposts
    parent_post: Mapped[Optional["Post"]] = relationship(
        back_populates="replies",
        foreign_keys=[parent_post_id],
        remote_side="Post.post_id",
    )
    replies: Mapped[list["Post"]] = relationship(
        back_populates="parent_post",
        foreign_keys=[parent_post_id],
    )
    repost_of: Mapped[Optional["Post"]] = relationship(
        back_populates="reposted_as",
        foreign_keys=[repost_post_id],
        remote_side="Post.post_id",
    )
    reposted_as: Mapped[list["Post"]] = relationship(
        back_populates="repost_of",
        foreign_keys=[repost_post_id],
    )

    # child entities
    media: Mapped[list["PostMedia"]] = relationship(back_populates="post")
    likes: Mapped[list["PostLike"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="post")
    reposts: Mapped[list["Repost"]] = relationship(back_populates="post")

    def __repr__(self) -> str:
        return f"<Post id={self.post_id} user_id={self.user_id}>"


class PostMedia(Base):
    """Media attachments (images, videos, etc.) belonging to a post."""

    __tablename__ = "post_media"

    post_media_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.post_id"), nullable=False
    )
    media_path: Mapped[str] = mapped_column(Text, nullable=False)
    media_type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("post_media_types.media_type_id")
    )
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    duration_sec: Mapped[Optional[int]] = mapped_column(Integer)
    media_order: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    post: Mapped["Post"] = relationship(back_populates="media")
    media_type: Mapped[Optional["PostMediaType"]] = relationship(back_populates="post_media")

    def __repr__(self) -> str:
        return f"<PostMedia id={self.post_media_id} post_id={self.post_id}>"


class PostLike(Base):
    """User ♥ post — composite primary key (post_id, user_id)."""

    __tablename__ = "post_likes"
    __table_args__ = (
        # composite PK reflected from dump constraint "p_key"
    )

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.post_id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), primary_key=True
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    post: Mapped["Post"] = relationship(back_populates="likes")
    user: Mapped["User"] = relationship(back_populates="post_likes")

    def __repr__(self) -> str:
        return f"<PostLike post_id={self.post_id} user_id={self.user_id}>"


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------

class Comment(Base):
    """Comments on posts, with optional threading via parent_comment_id."""

    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.post_id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
    parent_comment_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("comments.comment_id")
    )
    content: Mapped[Optional[str]] = mapped_column(Text)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")

    parent_comment: Mapped[Optional["Comment"]] = relationship(
        back_populates="replies",
        remote_side="Comment.comment_id",
        foreign_keys=[parent_comment_id],
    )
    replies: Mapped[list["Comment"]] = relationship(
        back_populates="parent_comment",
        foreign_keys=[parent_comment_id],
    )

    media: Mapped[list["CommentMedia"]] = relationship(back_populates="comment")
    likes: Mapped[list["CommentLike"]] = relationship(back_populates="comment")

    def __repr__(self) -> str:
        return f"<Comment id={self.comment_id} post_id={self.post_id}>"


class CommentMedia(Base):
    """Media attachments belonging to a comment."""

    __tablename__ = "comment_media"

    comment_media_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("comments.comment_id")
    )
    media_path: Mapped[Optional[str]] = mapped_column(Text)
    media_type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("comment_media_type.media_type_id")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    comment: Mapped[Optional["Comment"]] = relationship(back_populates="media")
    media_type: Mapped[Optional["CommentMediaType"]] = relationship(
        back_populates="comment_media"
    )

    def __repr__(self) -> str:
        return f"<CommentMedia id={self.comment_media_id} comment_id={self.comment_id}>"


class CommentLike(Base):
    """User ♥ comment."""

    __tablename__ = "comment_likes"

    comment_like_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("comments.comment_id")
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    comment: Mapped[Optional["Comment"]] = relationship(back_populates="likes")
    user: Mapped[Optional["User"]] = relationship(back_populates="comment_likes")

    def __repr__(self) -> str:
        return f"<CommentLike id={self.comment_like_id} user_id={self.user_id}>"


# ---------------------------------------------------------------------------
# Social interactions
# ---------------------------------------------------------------------------

class Follow(Base):
    """follower_id follows following_id."""

    __tablename__ = "follows"

    follow_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    follower_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    following_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    follower: Mapped[Optional["User"]] = relationship(
        back_populates="following",
        foreign_keys=[follower_id],
    )
    following_user: Mapped[Optional["User"]] = relationship(
        back_populates="followers",
        foreign_keys=[following_id],
    )

    def __repr__(self) -> str:
        return f"<Follow follower={self.follower_id} → following={self.following_id}>"


class Bookmark(Base):
    """User saves a post for later."""

    __tablename__ = "bookmarks"

    bookmark_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("posts.post_id")
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    post: Mapped[Optional["Post"]] = relationship(back_populates="bookmarks")
    user: Mapped[Optional["User"]] = relationship(back_populates="bookmarks")

    def __repr__(self) -> str:
        return f"<Bookmark id={self.bookmark_id} user_id={self.user_id} post_id={self.post_id}>"


class Repost(Base):
    """User re-shares a post (explicit repost record, separate from post.repost_post_id)."""

    __tablename__ = "reposts"

    repost_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("posts.post_id")
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.user_id")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now())

    # relationships
    post: Mapped[Optional["Post"]] = relationship(back_populates="reposts")
    user: Mapped[Optional["User"]] = relationship(back_populates="reposts")

    def __repr__(self) -> str:
        return f"<Repost id={self.repost_id} user_id={self.user_id} post_id={self.post_id}>"