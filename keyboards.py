from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_builder(lst):
    builder = InlineKeyboardBuilder()
    for l in lst:
        builder.button(text=l, callback_data=l)
    return builder.adjust(1).as_markup()

def vars_key(dct):
    builder = InlineKeyboardBuilder()
    for l in dct['var']:
        if l == dct['var'][dct['correct']]:
            builder.button(text=l, callback_data='correct')
        else:
            builder.button(text=l, callback_data='incorrect')
    builder.button(text='Меню',
                   callback_data='menu')
    return builder.adjust(1).as_markup()