# python scraper examples

This repository contains examples of web scrapers that demonstrate use cases and
capabilities of external web scrapers.

## Installation

1. Install the newest version of python from https://python.org/downloads. Python 3.6+ is required.
2. Download this repository
3. Open `Command Prompt` and navigate to the repository root folder
4. Create and activate virtual environment
```commandline
python -m venv env
env/Script/activate
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
   D:\python-scraper-template\env\Scripts\python.exe D:\python-scraper-template\megaputer_blog.py
   ```
   - Click `Save changes` apply the new settings

## Usage

- Add `Internet Source` node to workspace from node palette
- Choose registered earlier scraper from `Scrapers` drop down menu
- Set parameters if selected scraper supports them
- Execute node

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
