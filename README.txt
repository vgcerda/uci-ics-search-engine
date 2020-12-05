Steps To Use Our Search Engine:

* Make sure that the dataset folder (DEV or ANALYST) is in same directory as the files to be ran.

I. Build the Index
	- enter 'python3 index.py' into the console/terminal
		- You will know that the Indexing process is finished when the analytics are outputted in the console/terminal
		- Analytics include:
			1. Execution Time (in seconds)
			2. Number of Tokens
			3. Number of Documents

II. Start Searching
	- enter 'python3 website.py' into the console/terminal
		- There will be a warning "WARNING: This is a development server. Do not use it in a production deployment.", which 
			can be ignored
		- You will know when you're ready to load the website when both:
			- "Debugger is active!" is outputted to the console/terminal
			- "Debugger PIN: <whatever the pin number is>" is outputted to the console/terminal
		- To load the website, locate "Running on <website url> (Press CTRL+C to quit)" which is under "Debug mode: on"
			and above "Restarting with stat"
			- "<website url>" is a placehold for the actual url of the hosted website. Copy this url and paste it into a
				web browser.
			- You should be directed to the home page of our search website with the mast header being "Zoogle" and a
				search bar right under it.
			- Input your query into the search bar and press enter. You should be directed to another page that lists
				the top 10 results of your search query.
				- You are able to input another query into the search bar in this page as well.
	- To terminate the search website, exit out of the website page and press CTRL + c in the console/terminal.