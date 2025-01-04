
# Contributing to HORCRUX

Thank you for your interest in contributing to our project! We're excited to have you on board.

## Getting Started

1. **Fork the Repository**

Go ahead and click the "Fork" button to create your own copy of the repository.

2. **Clone the Repository**

Clone your forked repository to your local machine:

```bash
git clone https://github.com/<your-username>/HORCRUX
```

3. **Install Dependencies**

Navigate to the project directory, create a Python virtual environment, and install the  necessary dependencies using `requirements.txt`. Ensure you're using **Python 3.12.5** or higher. You can check your Python version by running:
```bash
python --version
```
      
Then install the dependencies:
```bash
cd your-forked-repo
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Set Up Environment Variables**

- Create a `.env` file in directory "horcrux/url".
- Copy the contents from `.env.example` and update it with your configurations.

5. **Run the Application**

Start the application to ensure everything is working correctly:

```bash
cd horcrux
python manage.py runserver
```

6. Send POST Requests in Index page

Go to 127.0.0.1:8000 (localhost:8000) and send post request with the following body format
```bash
{
"url": "YOUR_GITHUB_REPO_LINK"
}
```

7. Process Repository Files

If repository have .py files, you will get them in XML format for further processing 

## Replicating Behavior or Bugs

To replicate specific behaviors or bugs:

1. **Match the Required Configurations**

To replicate specific behaviors or bugs, ensure your environment matches the required configurations mentioned above.

## Making Changes

- **Create a New Branch**

Before making changes, create a new branch:

```bash
git checkout -b feature/your-feature-name
```

- **Implement Your Changes**

Make your desired changes to the codebase.

- **Commit Your Changes**

Commit your changes with a clear and descriptive message:

```bash
git commit -m "Add feature XYZ"
```

- **Push to Your Fork**

Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

- **Open a Pull Request**

Go to the original repository and open a pull request from your branch.

## Guidelines

- **Code Style**

Follow the code style guidelines outlined in `STYLEGUIDE.md`.

- **Commit Messages**

Write clear and concise commit messages.

- **Focused Commits**

Keep your commits small and focused on a single feature or fix.

## Need Help?

If you have any questions or need assistance, feel free to open an issue or reach out to one of the maintainers.

---

We appreciate your contributions and efforts to improve the project!
