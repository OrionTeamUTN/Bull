from app import db
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Swap(db.Model):
    __tablename__ = 'swaps'
    
    id_swap: int = db.Column('id_swap', db.Integer, primary_key=True, autoincrement=True)
    operation_date: datetime = db.Columnn('operation_date', db.DateTime, nullable=False)
    amount_in: int = db.Column('amount_in', db.Integer, nullable=False)
    amount_out: int = db.Column('amount_out', db.Integer, nullable=False)
    id_wallet_in: int = db.Column('id_wallet_in', db.Integer, nullable=False)
    id_wallet_out: int = db.Column('id_wallet_out', db.Intener, nullable=False)

    #wallet_in = db.relationship('Wallet', back_populates='')
    #wallet_out = db.relationship('Wallet', back_populates='')

