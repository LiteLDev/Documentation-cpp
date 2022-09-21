"""!@package extract_texts
@author Futrime (futrime@outlook.com)
@brief The text extractor for LiteLoaderSDK documentation
@version 1.0.0
@date 2022-09-13

@details This program extract texts from the comments for i18n.

@copyright Copyright (c) 2022 Futrime
"""

"""
    LiteLoaderBDS C++ Documentation Text Extractor, a text extractor for
    the C++ documentation of LiteLoaderBDS.
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
import re
regex_list = [
    '@brief +(.*)',
    '@note +(.*)',
    '@par +(.*)',
    '@param +\S+ +(.*)',
    '@return +(.*)',
    '@tparam +\S+ +(.*)',
    '@warning +(.*)'
]

if __name__ == '__main__':
    file_list = []

    for root, dirs, files in os.walk('./SDK/Header/'):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))

    text_list = []

    for file_path in file_list:
        print('Extracting texts from ' + file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for regex in regex_list:
            text_list += re.findall(regex, content)

    with open('./i18n/en.txt', 'w', encoding='utf-8') as f:
        for text in set(text_list):
            f.write(text + '\n')
