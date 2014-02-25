# Calvin PaperCut
A python command line interface for printing to PaperCut enabled printers. **Warning:** this script has not been extensively tested and will cost you money.

## Installation
Clone the repo.

Install the requirements with `pip install -r requirements.txt`

For global usage add an alias to your bash config: 	`alias papercut='python /path/to/repo/Calvin-Papercut/cli.py'`

To save your username, add a file `~/.papercut` with the contents:

	[papercut]
	username: your_user_name
	
## Usage
List all arguments with `-h`

Print files with `--print FILENAME` or `-p FILENAME`. You will be prompted for a printer. You can specify the printer name with the optional argument `--printer`.

List all printers with `--list` or `-l`.

View your print balance with `--balance` or `-b`

Mess with your password options with `--password-options` or `-o`:

* `-o save` will save your password to your system keyring
* `-o prompt` will force the script to prompt for your password. This could be useful if you have to change your PaperCut password and the old one is still saved in the keyring.