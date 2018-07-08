def std_test(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="test std")


cmds = [std_test]