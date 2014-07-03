# Make my life easier

clean:
	find . -name "*.pyc" | xargs rm || true
	find . -type d -name "__pycache__" | xargs rm -r || true
