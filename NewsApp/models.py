from settings import db, ma

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vk_json = db.Column(db.JSON, nullable=False)

    def __init__(self, vk_json):
        self.vk_json = vk_json
