# 🗑️ Trashbin

[![GitHub License](https://img.shields.io/github/license/nitondev/trashbin?color=purple)](https://github.com/nitondev/trashbin/blob/main/LICENSE) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**[ [Installation](#installation) ] [ [Usage](#usage) ] [ [Examples](#examples) ] [ [License](#license) ]**

#### What is Trashbin?
Trashbin is a utility designed for safer file and directory removal.


## Installation

> [!Note]
> There is no official release at this moment.

You can still install the unreleased beta version directly from the Git repository:
``` bash
pip install git+https://github.com/nitondev/trashbin
```
Please be aware that there may be bugs and other errors.


## Usage

Trash file or directory:
```
$ trash binladen.jpg
$ trash notc0rn/
```

List trashed files:
```
$ trash --list
trash: v0.1.0 

 #  Date                 File path                      
 1  2024-07-18 16:54:07  /home/niton/secret_token.txt 
 2  2024-07-18 16:54:07  /home/niton/important.pdf    
 3  2024-07-18 16:54:08  /home/niton/user_backup.zip
 ```

Restore trashed files:
```
$ trash --restore
trash: v0.1.0 

 #  Date                 File path                      
 1  2024-07-18 16:54:07  /home/niton/secret_token.txt 
 2  2024-07-18 16:54:07  /home/niton/important.pdf    
 3  2024-07-18 16:54:08  /home/niton/user_backup.zip  

Select file in list [1..3] to restore: 3
trash: 'user_backup.zip' has been restored.
```

Remove everything from the trash bin:
```
$ trash --empty
trash: This action is not reversible.
Type 'yes' to confirm: yes

trash: 3 item(s) shredded.
```


## Examples

The trash command supports file patterns as arguments.

Trash all files with the extension .webp in a folder:
```bash
$ trash images/*.webp
```

Trash all compiled Python files (*.pyc, *.pyo, *.pyd) in a folder:
```bash
$ trash project/*.py[cod]
```


## License

This project is licensed under MIT - see the [LICENSE](LICENSE) file for details.
