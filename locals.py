langs = ['Eng', 'Ru']

lines = {
    'Eng_cmd_help': 
        """
Arguments:
    NoW - Number Of Winners [Number]
    gId - Giveaway Id [text]
    gName - Giveaway Name [text]
    gDescr - Giveaway Description [text]
    
    Giveaway Id is sent to you when new giveaway is created

My commands:
    /start - Displays start message
    /help - Displays commands
    /g_create {NoW}''{gName}''{gDescr} - 
        Creates new giveaway. Photo can be attached.
    /g_edit {gId}''{NoW}''{gName}''{gDescr} - 
        Overrides values of a given giveaway. Photo can be attached.
    /g_post {gId} - Creates post of about a given giveaway 
    /g_subs {gId} - Displays subscribers of a given giveaway 
    /g_finish {gId} - Finishes a given giveaway and displays winners 
        """,
    'Eng_cmd_start': 
        'I am your giveaway bot-manager!\nWith my help you can create and manage giveaways.\nType "/help" to see my commands.',
    'Eng_cmd_restart': 'Bot will be back in 5 seconds!',
    'Eng_cmd_giveaway_subs': "Number of subs: <strong>{0}</strong>",
    'Eng_btn_sub_txt': 'subscribe',
    'Eng_btn_unsub_txt': 'unsubscribe',
    'Eng_msg_g_created': 'New giveaway created!\ngiveawayId:{0}\nFirst posted in chatId:{1}\nNumberOfWinners:{2}\nname:{3}\ndescription:{4}',
    'Eng_msg_g_post_created': 'New giveaway post created!\ngiveawayId:{0}\nPosted in chatId:{1}',
    'Eng_post_g_finished': '<strong>{0} has finished!</strong>\nCongratulations to our winners:\n{1}',
    'Eng_err_no_g_exists': 'Giveaway with id "%s" does not exist',
    'Eng_err_no_g_id': 'Please specify giveawayId',
    'Eng_err_no_g_name': 'Giveaway is missing the name',
    'Eng_err_no_g_descr': 'Giveaway is missing the description',
    'Eng_err_no_g_NoW': 'Giveaway is missing the NumberOfWinners',
    'Eng_err_wr_g_NoW': 'NumberOfWinners should be greater than zero',
    'Eng_err_wr_create_params': "Expected three parameters in format \"/g_create Now''name''description\", but got %s parameters",
    'Eng_err_wr_edit_params': "Expected four parameters in format \"/g_edit GiveawayId''Now''name''description\", but got %s parameters",
    'Eng_err_no_access': "You do not have permission for this command!\nPlease contact the creator %s.",

    'Ru_cmd_help': 
        """
Аргументы:
    NoW - Количество победителей конкурса [Число]
    gId - Id конкурса [текст]
    gName - имя конкурса [текст]
    gDescr - описание конкурса [текст]
    
    Id Конкурса Содержится в оповещении о создании конкурса

Команды:
    /start - Отображает вводное сообщение
    /help - Отображает информацию о командах
    /g_create {NoW}''{gName}''{gDescr} - 
        Создает новый конкурс. Можно прикрепить фото.
    /g_edit {gId}''{NoW}''{gName}''{gDescr} - 
        Изменяет параметры конкурса. Можно прикрепить фото.
    /g_post {gId} - Создает пост о конкурсе 
    /g_subs {gId} - Отображает подписчиков конкурса 
    /g_finish {gId} - Выбирает победителей и делает пост об этом 
        """,
    'Ru_cmd_start': 
        'Привет! я бот-менеджер конкурсов!\nС моей помощью ты можешь создавать и управлять конкурсами в своих группах.\nНапиши "/help" чтобы увидеть список команд.',
    'Ru_cmd_restart': 'Бот перезапустится через 5 секунд!',
    'Ru_cmd_giveaway_subs': "Количество подписчиков: <strong>{0}</strong>",
    'Ru_btn_sub_txt': 'Участвовать',
    'Ru_btn_unsub_txt': 'отписаться',
    'Ru_msg_g_created': 'Новый конкурс создан!\nId Конкурса:{0}\nВпервые опубликован в чате:{1}\nКоличество победителей:{2}\nИмя конкурса:{3}\nОписание конкурса:{4}',
    'Ru_msg_g_post_created': 'Новый пост о конкурсе создан!\nId Конкурса:{0}\nОпубликован в чате:{1}',
    'Ru_post_g_finished': '<strong>{0} окончен!</strong>\n\nПоздравляем победителей:\n\n{1}\n\nЖдите сообщение в ЛС.\n\nВсем спасибо за участие. Впереди будут ещё розыгрыши, не пропустите ✨',
    'Ru_err_no_g_exists': 'Конкурса с Id "%s" не существует',
    'Ru_err_no_g_id': 'Пожалуйста укажите Id конкурса',
    'Ru_err_no_g_name': 'Не хватает имени конкурса',
    'Ru_err_no_g_descr': 'Не хватает описания конкурса',
    'Ru_err_no_g_NoW': 'Не хватает количества победителей конкурса',
    'Ru_err_wr_g_NoW': 'количество победителей должно быть больше нуля',
    'Ru_err_wr_create_params': "Ожидалось три параметра в виде \"/g_create Now''name''description\", но было получено %s",
    'Ru_err_wr_edit_params': "Ожидалось четыре параметра в виде \"/g_edit GiveawayId''Now''name''description\", но было получено %s",
    'Ru_err_no_access': "У вас нет доступа к этой команде!\nПожалуйста свяжитесь с создателем %s.",
}


def get_line(langId: int, line_name: str):
    key = '%s_%s' % (langs[langId], line_name)
    return lines[key]
