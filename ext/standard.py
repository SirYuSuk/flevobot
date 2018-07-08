def test(bot, update):
    """Some stupid test function"""
    bot.send_message(chat_id=update.message.chat_id, text="test")


cmds = [test]