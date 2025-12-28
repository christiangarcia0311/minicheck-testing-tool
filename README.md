<p align="center">
  <img src="assets/banner.png" width="350" height="250" alt="MiniCheck Banner">
</p>

<h1 align="center">MiniCheck Testing Tool</h1>

<div align="center">
  <img alt="Static Badge" src="https://img.shields.io/badge/PyPi-%238c52ff?style=for-the-badge&logo=pypi&logoColor=white">
  <img alt="Static Badge" src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Static Badge" src="https://img.shields.io/badge/MIT-brown?style=for-the-badge">

  <br />

  <p align="justify">
    MiniCheck is a simple and easy-to-use Python testing framework that makes writing and running tests straightforward. It’s designed for developers who want to quickly check that their code works as expected without dealing with complicated setup or extra overhead. MiniCheck lets you organize your tests clearly, handle setup and teardown, and see results in a clean, readable format. Whether you’re working on small projects, learning Python or building larger applications, MiniCheck helps you catch issues early and keep your code reliable—all while staying lightweight and easy to use. Its goal is to let you focus on writing your tests, not on learning the framework.
  </p>
</div>

## Installation

Install MiniCheck in [PyPi](https://pypi.org/project/minicheck):
```bash
pip install minicheck
```
## Usage

Create Python test file and inherit from `Check`

```python
from minicheck import Check

class TestExample(Check):
  def test_addition(self):
    self.equal(5 + 5, 10)
  
  def test_subtraction(self):
    self.equal(5 - 4, 1)

if __name__ == '__main__':
  TestExample().run()
```

Run your tests:

```bash
python test_example.py
```

You can filter test by name:

```bash
python test_example.py addition
```

Or list all available tests:

```bash
python test_example.py --list
```

Or show help message:

```bash
python test_example.py --help
```

### Assertion Helpers

MiniCheck provides a unified set of assertions that can be used for general python code as well as web application testing. This allows you to write concise and readable tests across different types of projects.

#### General Assertions

```python
self.equal(actual, expected, message) # Check equality
self.true(expression, message) # Check if it is True
self.false(expression, message) # Check if it is false
self.raises(Exception, function, *args, **kwargs) # Expect an exception
```

#### Web & API Assertions

```python
self.status_code(response, expected_code, message) # Check HTTP status code
self.json_equal(response, key, expected_code, message) # Check JSON value by key
```

### Web App Testing Example

`app.py` - Actual Flask App

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

dummy_users = {
  'admin': 'password123',
  'user': 'password456'
}

@app.route('/')
def homepage():
  return jsonify({
    'message': 'Welcome to MiniCheck App'
  })

@app.route('/signin', methods=['POST'])
def signin():
  data = request.json()
  username = data.get('username')
  password = data.get('password')

  if not username or password:
    return jsonify({
      'success': False,
      'error': 'Missing credentials'
    }, 400)

  if user.get(username) == password:
    return jsonify({
      'success': True,
      'message': 'Sign-in successful'
    })

  return jsonify({
    'success': False,
    'error': 'Invalid username or password'
  }, 401)

@app.route('/profile/<username>')
def profile(username):
  if username in dummy_users:
    return jsonify({
      'username': username,
      'role': 'admin' if username == 'admin' else 'user'
    })
  
  return jsonify({
    'error': 'User credentials not found'
  }, 404)

if __name__ == '__main__':
  app.run(debug=True)
```

`test_auth_app.py` - MiniCheck Tests

```python
from minicheck import Check
from app import app

class TestAuthApp(Check):
  
  def setup(self):
    self.client = app.test_client()

  def test_home_route(self):
    response = self.client.get('/')

    self.status_code(response, 200)
    self.json_equal(response, 'Welcome to MiniCheck App')
  
  def test_login_success(self):
    response = self.client.post('/signin', json={
      'username': 'admin',
      'password': 'password123'
    })

    self.status_code(response, 200)
    self.json_equal(response, 'success', True)

  def test_login_failed(self):
    response = self.client.post('/signin', json={
      'username': 'admin',
      'password': 'wrongpass'
    })

    self.status_code(response, 401)
    self.json_equal(response, 'success', False)

  def test_profile_exist(self):
    response = self.client.get('/profile/admin')

    self.status_code(response, 200)
    self.json_equal(response, 'username', 'admin')
  
  def test_profile_nonexist(self):
    response = self.client.get('/profile/guest')

    self.status_code(response, 404)
    self.json_equal(response, 'error', 'User credentials not found')

if __name__ == '__main__':
  TestAuthApp().run()
```

Run your web-app tests:

```python
# run all tests
python test_auth_app.py 

# filter test by name
python test_auth_app.py home_route
```

Or list all available web-app tests:

```python
python test_auth_app.py --list
```


## Release & Versioning

**Current version**: [minicheck v.0.1.0](https://pypi.org/project/minicheck)


### How to Check for Updates

You can always check the latest version on [PyPI](https://pypi.org/project/minicheck). To update MiniCheck to the latest version:

```bash
pip install --upgrade minicheck
```

### Issues & Feature Requests

If you encounter any problems, have suggestions or want new features added, please follow these steps:

1. **Check existing issues first**
  - Make sure your problem or idea hasn’t already been  reported in the [issues](https://github.com/christiangarcia0311/minicheck-testing-tool/issues)

2. **Report a Bug**
  - Click **New Issue** -> **Bug Report**
  - Provide clear `title` amd `description`
  - Include **steps to reproduce**, `expected behavior` and `actual behavior`
  - Add relevant **code snippets or screenshots** if applicable

3. **Request a Feature**
  - Click **New Issue** -> **Feature Request**
  - Describe the **feature idea** clearly
  - Explain **why it would be useful**
  - Oprionally include **examples or mockups**


### LICENSE

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

### Author

| [<img src="https://github.com/christiangarcia0311.png" width="100px;">](https://github.com/christiangarcia0311) |
|:--:|
| [Christian Garcia](https://github.com/christiangarcia0311) | 
| Programmer |