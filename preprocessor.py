"""!@package preprocessor
@author Futrime (futrime@outlook.com)
@brief The preprocessor for LiteLoaderSDK documentation
@version 1.0.0
@date 2022-08-28

@details This program preprocess the LiteLoaderSDK for Doxygen documentation
         generation, removing all Doxygen comment blocks with \c \@symbol but
         without \c \@brief in header files in the SDK.

@copyright Copyright (c) 2022 Futrime
"""

"""
    LiteLoaderSDK Documentation Preprocessor. Preprocess the LiteLoaderSDK for
    Doxygen documentation generation.
    Copyright (C) 2022  Futrime

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
"""


import os
import re
regex_list = [
    ' *\/\*{2}\n( +\* @hash.*\n| +\* @symbol.*\n| +\* @vftbl.*\n)* +\*\/\n', # comments before methods
    ' *\/\*\*\n * \* @brief MC class \w+\.\n * \*\n * \*\/\n' # comments before classes
]

if __name__ == '__main__':
    file_list = []

    for root, dirs, files in os.walk('./SDK/Header/MC/'):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))

    for file_path in file_list:
        print('Preprocessing ' + file_path)

        with open(file_path, 'r') as f:
            content = f.read()

        for regex in regex_list:
            content = re.sub(regex, '', content)

        with open(file_path, 'w') as f:
            f.write(content)
