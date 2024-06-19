from app import db
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Swap(db.Model):
    __tablename__ = 'swaps'
    
    id_swap: int = db.Column('id_swap', db.Integer, primary_key=True, autoincrement=True)
    operation_date: datetime = db.Column('operation_date', db.DateTime, nullable=False, default=datetime.utcnow()) # fecha actual por default
    amount_send: int = db.Column('amount_send', db.Integer, nullable=False)
    amount_recv: int = db.Column('amount_recv', db.Integer, nullable=False)
    id_wallet_send: int = db.Column('id_wallet_send', db.Integer, nullable=False)
    id_wallet_recv: int = db.Column('id_wallet_recv', db.Integer, nullable=False)

    # wallet_send = db.relationship('Wallet', back_populates='swap_send')
    # wallet_recv = db.relationship('Wallet', back_populates='swap_recv')

