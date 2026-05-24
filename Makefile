.PHONY: css css-watch

css:
	./tailwindcss -i src/adapters/web/static/input.css -o src/adapters/web/static/style.css --minify

css-watch:
	./tailwindcss -i src/adapters/web/static/input.css -o src/adapters/web/static/style.css --watch
