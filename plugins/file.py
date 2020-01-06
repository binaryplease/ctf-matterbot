from mmpy_bot.bot import respond_to


@respond_to('files')
def message_with_file(message):
    # upload_file() can upload only one file at a time
    # If you have several files to upload, you need call this function several times.
    file = open('test.txt')
    result = message.upload_file(file)
    file.close()
    if 'file_infos' not in result:
        message.reply('upload file error')
    file_id = result['file_infos'][0]['id']
    # file_id need convert to array
    message.reply('hello', [file_id])
