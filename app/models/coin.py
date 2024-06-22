from dataclasses import dataclass
from app import db
# Esta sería la clase padre de wallet
@dataclass
class Coin(db.Model):
    __tablename__ = 'coins'
    id_coin = db.Column('id_coin', db.Integer, primary_key=True, autoincrement= True)
    coin_name = db.Column('coin_name', db.String(50))
    coin_symbol = db.Column('coin_symbol', db.String(5))
    is_active = db.Column('is_active', db.Boolean, nullable=False, default = True)
    # Relación one-to-many: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # One coin - many wallets
    wallet = db.relationship('Wallet', back_populates='coin', cascade="all, delete-orphan")