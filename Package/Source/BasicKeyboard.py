Keyboard = []
Subgroup = ['FileSystem', 'AdditionalOptions']

Text = {
    'FileSystem': ['PDF', 'DOCX', 'SVG', 'XLSX'],
    'AdditionalOptions': ['Статус', 'История']
}

for key in Subgroup:
    for text in Text[key]: Keyboard.append((text, key))