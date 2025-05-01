# PaperEngineerTools-Python

A set of Python add-ins for Autodesk Revit using [`pyRevit`](https://github.com/eirannejad/pyRevit). This extension provides various custom tools and automations to streamline your Revit workflows.

---

## 📋 Prerequisites

- **Autodesk Revit** (2020, 2021, 2022, _etc._) installed on Windows.
- **pyRevit** installed and attached to your Revit version(s).
  - Download the latest installer from the [pyRevit Releases page](https://github.com/eirannejad/pyRevit/releases).
  - Run the installer and select the Revit versions you want to attach.

---

## 🗂️ Extension Structure

```
PaperEngineerTools-Python.extension/
├── extension.json           # Metadata for pyRevit
└── PaperEngineerTools.tab/  # Ribbon tab name
    └── Panel1.panel/        # First panel of tools
        └── tool1.pushbutton  # Python script or stack file
    └── Panel2.panel/        # Second panel
        └── tool2.pushbutton
```

- **extension.json** defines the extension metadata:
  ```json
  {
    "name": "PaperEngineerTools-Python",
    "author": "YourName",
    "version": "1.0.0",
    "unloadable": false,
    "engine": "2.x"
  }
  ```
- **.tab** folder name becomes your custom Ribbon tab in Revit.
- **.panel** folders become panels under that tab.
- **.pushbutton** scripts (.py or .stack) appear as buttons inside panels.

---

## 🚀 Installation

### 1. Copy extension folder

1. Close Revit if it’s running.
2. Copy the entire `PaperEngineerTools-Python.extension` folder into the pyRevit Extensions directory:
   ```
   %APPDATA%\pyRevit\Extensions\
   ```

### 2. (Optional) Register via CLI

If you prefer the pyRevit CLI, run in a Command Prompt:
```bash
pyrevit extensions add "C:\Path\To\PaperEngineerTools-Python.extension"
```

### 3. Attach or reload in Revit

1. Launch (or restart) Revit.
2. Go to the **pyRevit** tab on the Ribbon.
3. Click **Reload**. You should now see a new tab called **PaperEngineerTools** with your custom tools.

---

## 📖 Usage

- Click on your **PaperEngineerTools** tab in Revit.
- Select any tool button to run the corresponding Python script.
- Check the **pyRevit Output** window for logs and errors.

---

## 🛠️ Development

1. Make changes to the scripts inside `PaperEngineerTools-Python.extension`.
2. Save your scripts.
3. Click **Reload** in the pyRevit tab to apply updates immediately.

---

## 🤝 Contributing

1. Fork this repository.
2. Create a new branch: `git checkout -b feature/YourTool`.
3. Commit your changes: `git commit -m "Add new tool: YourTool"`.
4. Push to the branch: `git push origin feature/YourTool`.
5. Open a pull request against `main`.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

