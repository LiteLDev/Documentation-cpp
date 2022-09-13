"""!@package apply_translations
@author Futrime (futrime@outlook.com)
@brief The preprocessor for LiteLoaderSDK documentation
@version 1.0.0
@date 2022-09-13

@details This program applis the translations back to the SDK.

@copyright Copyright (c) 2022 Futrime
"""

"""
    LiteLoaderBDS C++ Documentation Translation Applier, a translation
    applier for the C++ documentation of LiteLoaderBDS.
    Copyright (C) 2022  Futrime

    This program is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this program.  If not, see
    <https://www.gnu.org/licenses/>.
"""


import os
lang_list = ['en', 'zh-Hans']

if __name__ == '__main__':
    translation_dict = {}

    original_text_list = open('./i18n/en.txt', encoding='utf-8').readlines()
    for lang in lang_list:
        translated_text_list = open(
            f'./i18n/{lang}.txt', encoding='utf-8').readlines()
        translation_dict[lang] = {}
        for i in range(min(len(original_text_list), len(translated_text_list))):
            translation_dict[lang][original_text_list[i]
                                   ] = translated_text_list[i]

    file_list = []

    for root, dirs, files in os.walk('./SDK/Header/'):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))

    for file_path in file_list:
        print('Solving ' + file_path)

        with open(file_path, encoding='utf-8') as f:
            original_content = f.read()

        for lang in lang_list:
            content = original_content

            for key in translation_dict[lang]:
                content = content.replace(key, translation_dict[lang][key])

            filename = f'./build/{lang}{file_path[1:]}'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
