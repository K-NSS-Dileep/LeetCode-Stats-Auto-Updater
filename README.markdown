# LeetCode Stats Card

![LeetCode Stats](https://raw.githubusercontent.com/K-NSS-Dileep/LeetCode-Stats-Auto-Updater/main/Display.svg)

A dynamic, automated solution to display your LeetCode statistics in a visually appealing SVG card, seamlessly integrated into your GitHub profile README. This project fetches your LeetCode stats, generates a custom SVG card, and updates your README with the latest stats using GitHub Actions.

---

## 📖 Project Overview

The **LeetCode Stats Card** project is designed to showcase your LeetCode progress, including problems solved, global ranking, and preferred programming languages, in a sleek SVG card. The card is automatically updated every 3 hours via a GitHub Actions workflow, ensuring your stats are always current without manual intervention.

### Key Features
- **Dynamic Stats Fetching**: Retrieves real-time data from LeetCode's GraphQL API, including total problems solved, difficulty-wise breakdown (Easy, Medium, Hard), global ranking, and languages used.
- **Custom SVG Design**: Generates a visually appealing SVG card using Jinja2 templating, styled to match modern design standards.
- **Automated Updates**: Uses GitHub Actions to periodically fetch stats, update the SVG, and commit changes to your repositories.
- **Cache Busting**: Ensures the latest SVG is displayed by appending a timestamp to the image URL.
- **Cross-Repository Integration**: Updates the SVG in the `LeetCode-Stats` repository and embeds it in the `Krishnarevanthkarra` repository's README.

---

## 🛠️ How It Works

The project consists of a Python script, a GitHub Actions workflow, and an SVG template. Here's a detailed breakdown:

1. **Data Fetching**:
   - The `app.py` script uses the `requests` library to query LeetCode's GraphQL API.
   - It retrieves stats like total problems solved, difficulty-wise counts, global ranking, and programming languages used.
   - The data is structured using a `Pydantic` model (`LeetCodeStats`) for type safety and easy access.

2. **SVG Generation**:
   - The `Design.svg` template defines the layout of the stats card, including placeholders for stats.
   - Jinja2 renders the template with fetched stats, producing `Display.svg`.
   - The card displays:
     - Total problems solved vs. total questions.
     - Global ranking.
     - Difficulty-wise stats (Easy, Medium, Hard).
     - Top 3 programming languages used, sorted by problems solved.

3. **README Integration**:
   - The script updates the `README.md` in the `Krishnarevanthkarra` repository by replacing content between `<!-- LEETCODE_STATS_START -->` and `<!-- LEETCODE_STATS_END -->` with a markdown image tag linking to `Display.svg`.
   - A cache-busting timestamp is added to the SVG URL to ensure browsers load the latest version.

4. **Automation**:
   - A GitHub Actions workflow (`workflow.yml`) runs every 24 hours or on manual trigger.
   - It checks out two repositories: `LeetCode-Stats-Auto-Updater` (for `Display.svg`) and `Krishnarevanthkarra` (for `README.md`).
   - The workflow installs Python dependencies, runs `app.py`, and commits changes to both repositories.

---

## 📂 Project Structure

```
LeetCode-Stats-Auto-Updater/
├── app.py              # Main script to fetch stats and generate SVG
├── Design.svg          # SVG template for the stats card
├── Display.svg         # Generated SVG with updated stats
├── requirements.txt    # Python dependencies
└── workflow.yml        # GitHub Actions workflow for automation
```

---

## 🚀 Getting Started

Follow these steps to set up the project for your own LeetCode profile.

### Prerequisites
- Python 3.8 or higher
- A GitHub account with two repositories:
  - One for the project code (e.g., `LeetCode-Stats-Auto-Updater`).
  - One for your profile README (e.g., `username/username`).
- A LeetCode account with public stats.
- A GitHub Personal Access Token with `repo` scope for authentication.

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Krishnarevanthkarra/LeetCode-Stats.git
   cd LeetCode-Stats
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Script**:
   - Open `app.py` and update the `leetcode_username` variable with your LeetCode username:
     ```python
     leetcode_username = "YourLeetCodeUsername"
     ```
   - Ensure the `readme_path` in `app.py` points to your profile repository's README:
     ```python
     readme_path = os.path.join("YourUsername", "README.md")
     ```

4. **Set Up GitHub Actions**:
   - Add your GitHub Personal Access Token as a secret named `LCToken` in both repositories:
     - Go to `Settings > Secrets and variables > Actions > New repository secret`.
   - Update `workflow.yml` to reference your repositories:
     ```yaml
     repository: YourUsername/LeetCode-Stats
     repository: YourUsername/YourUsername
     ```

5. **Run the Script Locally** (Optional):
   ```bash
   python app.py
   ```
   This generates `Display.svg` and updates `README.md` locally.

6. **Push Changes**:
   Commit and push the code to your `LeetCode-Stats` repository. The GitHub Actions workflow will handle updates automatically.

---

## 🎨 Customizing the SVG

The `Design.svg` template is fully customizable. To modify the design:
- Edit the SVG elements (e.g., colors, fonts, positions) in `Design.svg`.
- Adjust the `generate_lang_count` function in `app.py` to change how languages are displayed (e.g., show more than 3 languages).
- Update the Jinja2 placeholders (`{{stats.<field>}}`) to match any new fields in the `LeetCodeStats` model.

Example customization:
- Change the background color by modifying the `fill` attribute of the `<rect>` element.
- Adjust text sizes or fonts by updating the `font-size` or `font-family` attributes.

---

## ⚙️ GitHub Actions Workflow

The workflow (`workflow.yml`) automates the stats update process:
- **Trigger**: Runs every 3 hours (`cron: "0 */3 * * *"`) or manually via the GitHub Actions tab.
- **Steps**:
  1. Checks out both repositories using the `LCToken` secret.
  2. Sets up Python 3.8.
  3. Installs dependencies from `requirements.txt`.
  4. Runs `app.py` to update `Display.svg` and `README.md`.
  5. Commits and pushes changes to both repositories if updates are detected.

To modify the schedule, update the `cron` expression in `workflow.yml`. For example, to run daily at midnight:
```yaml
schedule:
  - cron: "0 0 * * *"
```

---

## 🐛 Troubleshooting

- **Empty SVG Generated**:
  - Check if `Design.svg` exists and contains valid Jinja2 placeholders.
  - Verify your LeetCode username is correct and the account is public.
- **GraphQL Errors**:
  - Ensure the GraphQL query in `app.py` matches LeetCode's API schema.
  - Check for rate limits or network issues.
- **Workflow Failures**:
  - Confirm the `LCToken` secret is set correctly in both repositories.
  - Verify repository paths in `workflow.yml` are correct.
- **README Not Updating**:
  - Ensure the `readme_path` in `app.py` points to the correct file.
  - Check for the `<!-- LEETCODE_STATS_START -->` and `<!-- LEETCODE_STATS_END -->` tags in `README.md`.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- [LeetCode](https://leetcode.com) for providing the GraphQL API.
- [Jinja2](https://jinja.palletsprojects.com) for templating.
- [Pydantic](https://pydantic.dev) for data validation.
- [GitHub Actions](https://github.com/features/actions) for automation.

---

Feel free to contribute, open issues, or suggest improvements! Let's make this stats card even better. 🚀
