# -*- coding: utf-8 -*-
import sys
from peewee import *
sys.path.append("..")
import config

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = config.MYSQL_DB

class OfficialAccount(BaseModel):
    """
    model for OfficialAccount
    """

    id = PrimaryKeyField()
    wechat_id = CharField()
    wechat_code = CharField()
    name = CharField()
    desc = CharField()
    classify = IntegerField()
    last_list_update = BigIntegerField()
    wechat_status = IntegerField()
    worker = CharField()
    last_update_time = DateTimeField()
    last_article_time = DateTimeField()
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        db_table = 'official_account'













