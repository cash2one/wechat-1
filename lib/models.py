# -*- coding: utf-8 -*-
from skylark import Model, Field, PrimaryKey

class OfficialAccount(Model):
    """
    model for OfficialAccount
    """

    id = PrimaryKey()
    wechat_id = Field()
    wechat_code = Field()
    name = Field()
    desc = Field()
    classify = Field()
    last_list_update = Field()
    wechat_status = Field()
    worker = Field()
    last_update_time = Field()
    last_article_time = Field()
    create_time = Field()
    update_time = Field()