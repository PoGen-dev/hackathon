Keyboard = []
Subgroup = ['FileSystem']

Text = {
    'FileSystem': ['PDF', 'DOCX', 'CVG']
}

for key in Subgroup:
    for text in Text[key]: Keyboard.append((text, key))