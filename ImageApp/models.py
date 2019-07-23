from settings import db, images, ma
import os
from flask_sqlalchemy import event


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    filename = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '' if self.name is None else self.name

    @property
    def url(self):
        i = images.url(self.filename)
        return i

    @property
    def filepath(self):
        if self.filename is None:
            return
        return images.path(self.filename)


@event.listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.filepath is not None:
        try:
            os.remove(target.filepath)
        except OSError:
            pass


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image
