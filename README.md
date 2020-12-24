# python scraper examples

This repository contains examples of web scrapers used in `Internet Source` node to demonstrate their use cases and capabilities.

## Installation

1. Install the newest version of python from https://python.org/downloads. Python 3.6+ is required.
2. Download this repository (here we're placed it to D drive, so full path is `D:\python-scraper-examples`. You can use any path.)
3. Open `Command Prompt` and navigate to the repository root folder
4. Create and activate virtual environment
```commandline
python -m venv env
env\Script\activate.bat
```
5. Install scraper dependencies
```commandline
pip install -r requirements.txt
```
6. Register web scrapers in `PolyAnalyst`:
   - Open `PolyAnalyst Administrative Tool`
   - Go to `Server setting`
   - Open `Web scrapers` context menu and click on `Add item`
   - Enter the scraper name in the `Name` field. This name will be displayed in the drop-down `Scraper` menu in the `Internet Source` node wizard
   - Enter a command in the `Command` field. For example, 
   ```commandline
   D:\python-scraper-examples\env\Scripts\python.exe D:\python-scraper-examples\megaputer_blog.py
   ```
   - Click `Save changes` to apply new settings

## Usage

- Add `Internet Source` node to workspace
- Choose one of scrapers registered earlier in the drop-down `Scraper` menu
- Set parameters if selected scraper supports them
- Execute node

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
