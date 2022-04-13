# -*- coding: utf-8 -*-

from pathlib import Path

import nonebot
from nonebot import get_driver, on_command
from nonebot.permission import Permission
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
    resolve()))

code_runner = on_command('python', permission = Permission(), priority = 3)

@code_runner.handle()
async def python_run(bot : Bot, event : Event, state : T_State):
    args = str(event.get_message()).split()[1:]

    if args:
        s = ' '.join(args)
    else:
        await code_runner.finish('请输入表达式')

    try:
        s = str(eval(s))
    except:
        await code_runner.finish('运行时出错')
    else:
        await code_runner.finish('运行结果: ' + s)
