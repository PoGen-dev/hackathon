Keyboard = []
Subgroup = ['FileSystem']

Text = {
    'FileSystem': ['PDF', 'DOCX', 'SVG']
}

for key in Subgroup:
    for text in Text[key]: Keyboard.append((text, key))