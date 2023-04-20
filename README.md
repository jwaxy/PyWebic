## PyWebic: a Python library for dynamic web development.

---

PyWebic is a Python library designed for dynamic web development. The name comes from a combination of 'Python' and 'Webic', which is a made-up word representing the idea of a dynamic web. We chose this name because it aligns with our library's goal of making web development more dynamic and efficient using Python.



##### Installation:

---

```bash
pip install git+https://github.com/jwaxy/PyWebic.git
```



##### Example:

---

> example.py

```python
import asyncio
from pywebic import WebServer

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

srv = WebServer(loop=loop)

loop.run_until_complete(srv.run())
loop.close()
```

> index.html

```html
<!DOCTYPE html>
<html>
<head>
	<title>PyWebic Example</title>
	<style>
		body {
			background-color: #f0f0f0;
			font-family: Arial, sans-serif;
			font-size: 16px;
			color: #333;
			margin: 0;
			padding: 0;
		}
		h1 {
			font-size: 32px;
			color: #0077ff;
			margin: 0;
			padding: 16px;
			text-align: center;
		}
		p {
			margin: 0;
			padding: 8px;
		}
	</style>
</head>
<body>
	<h1>PyWebic Example</h1>
	<p>This is a paragraph.</p>
    <p>The current time is <?py from datetime import datetime
print(datetime.now().strftime('%H:%M:%S')) ?></p>
</body>
</html>
```
