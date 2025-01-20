import os
import sys
from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy.orm import mapped_column

Base = declarative_base()


# tablausuario
class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    firstname = mapped_column(String(50), nullable=False)
    lastname = mapped_column(String(50), nullable=False)
    email = mapped_column(String(120), unique=True, nullable=False)

    # relaciones de usuario 
    # usuario con post es uno a muchos porque un usuario puede tener (MUCHOS) post pero un post solo puede tener un usuario (UNO)
    # usuario con coments mas de lo mismo, un usuario puede tener (MUCHOS) comments pero los comments solo pueden tener (UNO) usuario
    # usuario con followers es muchos a muchos: un unsuario puede tener (MUCHOS) followers y (MUHCOS) followers pueden seguir a ese usuario
    posts = relationship('Post', back_populates='user') 
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='followed')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower')

# tabla post
class Post(Base):
    __tablename__ = 'post'

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    # relaciones de post
    # usuario con post es uno a muchos porque un usuario puede tener (MUCHOS) post pero un post solo puede tener un usuario (UNO)
    # post con comments es uno a muchos porque un (UNO) post puede tener (MUCHOS) comentarios, pero esos comentarios pertenecen a (UNO) solo post
    # post con media es uno a muchos porque (UNO) post puede tener varios archiuvos multimedia (MUCHOS), pero siempre pertenecen a (UNO) post
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

# tabla comment
class Comment(Base):
    __tablename__ = 'comment'

    id = mapped_column(Integer, primary_key=True)
    comment_text = mapped_column(String(255), nullable=False)
    author_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    # relaciones de coment
    # la relacion de author con comment es de uno a muchos pq (UNO) autor puede tener (MUHCOS) comentarios
    # post con comments es igual, (UNO) post puede tener (MUCHOS) comments, pero todos pertenecen al mismo post
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

# tabla media
class Media(Base):
    __tablename__ = 'media'

    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url = mapped_column(String(255), nullable=False)
    post_id = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    # relaciones de media
    #post con media esta explicado antes en el apartado post
    post = relationship('Post', back_populates='media')

# tabla seguidores
class Follower(Base):
    __tablename__ = 'follower'

    user_from_id = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)

    # relaciones seguidores
    # es de MUCHOS a MUCHOS porque muchos seguidores pueden tener muchos seguidos
    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

# Código para generar el diagrama (diagram.png)
from eralchemy2 import render_er

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
